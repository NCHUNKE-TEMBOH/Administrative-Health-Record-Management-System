from flask_restful import Resource, request
from flask import jsonify
from package.model import conn
from package.auth import login_required, role_required, patient_access_required, get_current_user, log_access
from datetime import datetime, timedelta

# Global blockchain instance - will be set by app.py
blockchain = None

def set_blockchain_instance(blockchain_instance):
    """Set the blockchain instance for this module"""
    global blockchain
    blockchain = blockchain_instance

class Prescriptions(Resource):
    """Handle prescription operations"""
    
    @login_required
    def get(self):
        """Get prescriptions based on user role"""
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        status = request.args.get('status')
        
        # Base query
        query = """
            SELECT p.*, 
                   doc.first_name as doctor_first_name, doc.last_name as doctor_last_name,
                   pat.pat_first_name, pat.pat_last_name,
                   m.name as medication_name, m.brand as medication_brand
            FROM prescriptions p
            JOIN users doc ON p.doc_id = doc.user_id
            JOIN patient pat ON p.pat_id = pat.pat_id
            JOIN medication m ON p.med_code = m.code
        """
        params = []
        conditions = []
        
        # Role-based filtering
        if current_user['role'] == 'pharmacist':
            # Pharmacists see active prescriptions
            if status:
                conditions.append("p.status = ?")
                params.append(status)
            else:
                conditions.append("p.status = 'active'")
        
        elif current_user['role'] == 'doctor':
            # Doctors see prescriptions they wrote
            conditions.append("p.doc_id = ?")
            params.append(current_user['user_id'])
            
            if patient_id:
                conditions.append("p.pat_id = ?")
                params.append(patient_id)
            if status:
                conditions.append("p.status = ?")
                params.append(status)
        
        elif current_user['role'] == 'nurse':
            # Nurses see prescriptions for assigned patients
            if patient_id:
                # Check if nurse is assigned to this patient
                assignment = conn.execute(
                    "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                    (current_user['user_id'], patient_id)
                ).fetchone()
                
                if not assignment:
                    return {'error': 'Access denied to patient data'}, 403
                
                conditions.append("p.pat_id = ?")
                params.append(patient_id)
            else:
                # Get all assigned patients
                query += """
                    JOIN patient_assignments pa ON p.pat_id = pa.pat_id 
                """
                conditions.append("pa.nurse_id = ? AND pa.is_active = 1")
                params.append(current_user['user_id'])
        
        elif current_user['role'] == 'patient':
            # Patients see only their own prescriptions
            if current_user['entity_id']:
                conditions.append("p.pat_id = ?")
                params.append(current_user['entity_id'])
            else:
                return {'error': 'Patient entity not linked'}, 400
        
        elif current_user['role'] == 'admin':
            # Admin sees all prescriptions
            if patient_id:
                conditions.append("p.pat_id = ?")
                params.append(patient_id)
            if status:
                conditions.append("p.status = ?")
                params.append(status)
        
        else:
            return {'error': 'Access denied'}, 403
        
        # Add conditions to query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY p.prescribed_date DESC"
        
        prescriptions = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_PRESCRIPTIONS', 'PRESCRIPTION', patient_id=patient_id)
        
        return prescriptions, 200
    
    @role_required('admin', 'doctor')
    def post(self):
        """Create new prescription (Doctor/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['pat_id', 'med_code', 'dosage', 'frequency', 'duration']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Check if medication exists
        medication = conn.execute("SELECT code FROM medication WHERE code = ?", (data['med_code'],)).fetchone()
        if not medication:
            return {'error': 'Medication not found'}, 404
        
        # Calculate start and end dates
        start_date = data.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Parse duration to calculate end date
        duration = data['duration'].lower()
        try:
            if 'day' in duration:
                days = int(duration.split()[0])
                end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=days)).strftime('%Y-%m-%d')
            elif 'week' in duration:
                weeks = int(duration.split()[0])
                end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(weeks=weeks)).strftime('%Y-%m-%d')
            elif 'month' in duration:
                months = int(duration.split()[0])
                end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=months*30)).strftime('%Y-%m-%d')
            else:
                end_date = None
        except:
            end_date = None
        
        try:
            prescription_id = conn.execute("""
                INSERT INTO prescriptions (
                    pat_id, doc_id, med_code, dosage, frequency, duration, 
                    instructions, start_date, end_date, refills_remaining
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['pat_id'],
                current_user['user_id'],
                data['med_code'],
                data['dosage'],
                data['frequency'],
                data['duration'],
                data.get('instructions', ''),
                start_date,
                end_date,
                data.get('refills_remaining', 0)
            )).lastrowid
            
            conn.commit()

            # Add to blockchain if available
            if blockchain:
                try:
                    blockchain_data = {
                        'prescription_id': prescription_id,
                        'pat_id': data['pat_id'],
                        'doc_id': current_user['user_id'],
                        'med_code': data['med_code'],
                        'dosage': data['dosage'],
                        'frequency': data['frequency']
                    }
                    blockchain.add_prescription(blockchain_data)
                except Exception as e:
                    print(f"Warning: Failed to add prescription to blockchain: {e}")

            log_access(current_user['user_id'], 'CREATE_PRESCRIPTION', 'PRESCRIPTION', prescription_id, data['pat_id'])

            return {
                'message': 'Prescription created successfully',
                'prescription_id': prescription_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to create prescription'}, 500

class Prescription(Resource):
    """Handle individual prescription operations"""
    
    @login_required
    def get(self, prescription_id):
        """Get specific prescription"""
        current_user = get_current_user()
        
        query = """
            SELECT p.*, 
                   doc.first_name as doctor_first_name, doc.last_name as doctor_last_name,
                   pat.pat_first_name, pat.pat_last_name,
                   m.name as medication_name, m.brand as medication_brand, m.description as medication_description
            FROM prescriptions p
            JOIN users doc ON p.doc_id = doc.user_id
            JOIN patient pat ON p.pat_id = pat.pat_id
            JOIN medication m ON p.med_code = m.code
            WHERE p.prescription_id = ?
        """
        
        prescription = conn.execute(query, (prescription_id,)).fetchone()
        
        if not prescription:
            return {'error': 'Prescription not found'}, 404
        
        # Check access permissions
        if current_user['role'] == 'patient':
            if current_user['entity_id'] != prescription['pat_id']:
                return {'error': 'Access denied'}, 403
        elif current_user['role'] == 'nurse':
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], prescription['pat_id'])
            ).fetchone()
            if not assignment:
                return {'error': 'Access denied'}, 403
        elif current_user['role'] == 'doctor':
            if prescription['doc_id'] != current_user['user_id']:
                return {'error': 'Access denied'}, 403
        
        # Get dispensing history
        dispensing_history = conn.execute("""
            SELECT md.*, u.first_name as pharmacist_first_name, u.last_name as pharmacist_last_name
            FROM medication_dispensing md
            JOIN users u ON md.pharmacist_id = u.user_id
            WHERE md.prescription_id = ?
            ORDER BY md.dispensed_date DESC
        """, (prescription_id,)).fetchall()
        
        result = dict(prescription)
        result['dispensing_history'] = dispensing_history
        
        log_access(current_user['user_id'], 'VIEW_PRESCRIPTION', 'PRESCRIPTION', prescription_id, prescription['pat_id'])
        
        return result, 200
    
    @role_required('admin', 'doctor')
    def put(self, prescription_id):
        """Update prescription (Doctor/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Check if prescription exists
        prescription = conn.execute("SELECT * FROM prescriptions WHERE prescription_id = ?", (prescription_id,)).fetchone()
        if not prescription:
            return {'error': 'Prescription not found'}, 404
        
        # Only prescribing doctor or admin can update
        if current_user['role'] == 'doctor' and prescription['doc_id'] != current_user['user_id']:
            return {'error': 'Only the prescribing doctor can update this prescription'}, 403
        
        # Fields that can be updated
        updatable_fields = ['dosage', 'frequency', 'duration', 'instructions', 'status', 'refills_remaining']
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return {'error': 'No valid fields to update'}, 400
        
        # Validate status
        if 'status' in update_data:
            valid_statuses = ['active', 'completed', 'cancelled', 'on_hold']
            if update_data['status'] not in valid_statuses:
                return {'error': 'Invalid status'}, 400
        
        try:
            # Build dynamic update query
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values()) + [prescription_id]
            
            conn.execute(f"UPDATE prescriptions SET {set_clause} WHERE prescription_id = ?", values)
            conn.commit()
            
            log_access(current_user['user_id'], 'UPDATE_PRESCRIPTION', 'PRESCRIPTION', prescription_id, prescription['pat_id'])
            
            return {'message': 'Prescription updated successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to update prescription'}, 500

class MedicationDispensing(Resource):
    """Handle medication dispensing operations"""
    
    @role_required('pharmacist', 'admin')
    def post(self):
        """Dispense medication (Pharmacist/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['prescription_id', 'quantity_dispensed']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Check if prescription exists and is active
        prescription = conn.execute(
            "SELECT * FROM prescriptions WHERE prescription_id = ? AND status = 'active'",
            (data['prescription_id'],)
        ).fetchone()
        
        if not prescription:
            return {'error': 'Active prescription not found'}, 404
        
        try:
            dispensing_id = conn.execute("""
                INSERT INTO medication_dispensing (
                    prescription_id, pharmacist_id, quantity_dispensed, 
                    batch_number, expiry_date, notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['prescription_id'],
                current_user['user_id'],
                data['quantity_dispensed'],
                data.get('batch_number'),
                data.get('expiry_date'),
                data.get('notes')
            )).lastrowid
            
            # Update refills if applicable
            if prescription['refills_remaining'] > 0:
                conn.execute(
                    "UPDATE prescriptions SET refills_remaining = refills_remaining - 1 WHERE prescription_id = ?",
                    (data['prescription_id'],)
                )
            
            # Mark as completed if no refills remaining
            if prescription['refills_remaining'] <= 1:
                conn.execute(
                    "UPDATE prescriptions SET status = 'completed' WHERE prescription_id = ?",
                    (data['prescription_id'],)
                )
            
            conn.commit()
            
            log_access(current_user['user_id'], 'DISPENSE_MEDICATION', 'MEDICATION_DISPENSING', dispensing_id, prescription['pat_id'])
            
            return {
                'message': 'Medication dispensed successfully',
                'dispensing_id': dispensing_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to dispense medication'}, 500
    
    @role_required('pharmacist', 'admin')
    def get(self):
        """Get dispensing records"""
        current_user = get_current_user()
        
        query = """
            SELECT md.*, 
                   p.pat_first_name, p.pat_last_name,
                   m.name as medication_name, m.brand as medication_brand,
                   pr.dosage, pr.frequency
            FROM medication_dispensing md
            JOIN prescriptions pr ON md.prescription_id = pr.prescription_id
            JOIN patient p ON pr.pat_id = p.pat_id
            JOIN medication m ON pr.med_code = m.code
        """
        
        if current_user['role'] == 'pharmacist':
            query += " WHERE md.pharmacist_id = ?"
            params = [current_user['user_id']]
        else:
            params = []
        
        query += " ORDER BY md.dispensed_date DESC"
        
        dispensing_records = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_DISPENSING_RECORDS', 'MEDICATION_DISPENSING')
        
        return dispensing_records, 200
