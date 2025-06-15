from flask_restful import Resource, request
from flask import jsonify
from package.model import conn
from package.auth import login_required, role_required, patient_access_required, get_current_user, log_access
from datetime import datetime

# Global blockchain instance - will be set by app.py
blockchain = None

def set_blockchain_instance(blockchain_instance):
    """Set the blockchain instance for this module"""
    global blockchain
    blockchain = blockchain_instance

class LabTests(Resource):
    """Handle lab test operations"""
    
    @login_required
    def get(self):
        """Get lab tests based on user role"""
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        status = request.args.get('status')
        
        # Base query
        query = """
            SELECT lt.*, 
                   req.first_name as requested_by_first_name, req.last_name as requested_by_last_name,
                   proc.first_name as processed_by_first_name, proc.last_name as processed_by_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM lab_tests lt
            JOIN users req ON lt.requested_by = req.user_id
            LEFT JOIN users proc ON lt.processed_by = proc.user_id
            JOIN patient p ON lt.pat_id = p.pat_id
        """
        params = []
        conditions = []
        
        # Role-based filtering
        if current_user['role'] == 'lab_technician':
            # Lab technicians see all tests they can process
            if status:
                conditions.append("lt.status = ?")
                params.append(status)
            else:
                conditions.append("lt.status IN ('pending', 'in_progress')")
        
        elif current_user['role'] == 'doctor':
            # Doctors see tests they requested or all if admin
            if patient_id:
                conditions.append("lt.pat_id = ?")
                params.append(patient_id)
            else:
                conditions.append("lt.requested_by = ?")
                params.append(current_user['user_id'])
        
        elif current_user['role'] == 'nurse':
            # Nurses see tests for assigned patients
            if patient_id:
                # Check if nurse is assigned to this patient
                assignment = conn.execute(
                    "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                    (current_user['user_id'], patient_id)
                ).fetchone()
                
                if not assignment:
                    return {'error': 'Access denied to patient data'}, 403
                
                conditions.append("lt.pat_id = ?")
                params.append(patient_id)
            else:
                # Get all assigned patients
                query += """
                    JOIN patient_assignments pa ON lt.pat_id = pa.pat_id 
                    WHERE pa.nurse_id = ? AND pa.is_active = 1
                """
                params.append(current_user['user_id'])
        
        elif current_user['role'] == 'patient':
            # Patients see only their own tests
            if current_user['entity_id']:
                conditions.append("lt.pat_id = ?")
                params.append(current_user['entity_id'])
            else:
                return {'error': 'Patient entity not linked'}, 400
        
        elif current_user['role'] == 'admin':
            # Admin sees all tests
            if patient_id:
                conditions.append("lt.pat_id = ?")
                params.append(patient_id)
            if status:
                conditions.append("lt.status = ?")
                params.append(status)
        
        else:
            return {'error': 'Access denied'}, 403
        
        # Add conditions to query
        if conditions:
            if 'WHERE' not in query:
                query += " WHERE " + " AND ".join(conditions)
            else:
                query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY lt.requested_date DESC"
        
        tests = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_LAB_TESTS', 'LAB_TEST', patient_id=patient_id)
        
        return tests, 200
    
    @role_required('admin', 'doctor')
    def post(self):
        """Request new lab test (Doctor/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['pat_id', 'test_type', 'test_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Validate priority
        valid_priorities = ['normal', 'urgent', 'stat']
        priority = data.get('priority', 'normal')
        if priority not in valid_priorities:
            return {'error': 'Invalid priority level'}, 400
        
        try:
            test_id = conn.execute("""
                INSERT INTO lab_tests (pat_id, requested_by, test_type, test_name, priority)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['pat_id'],
                current_user['user_id'],
                data['test_type'],
                data['test_name'],
                priority
            )).lastrowid
            
            conn.commit()
            
            log_access(current_user['user_id'], 'REQUEST_LAB_TEST', 'LAB_TEST', test_id, data['pat_id'])
            
            return {
                'message': 'Lab test requested successfully',
                'test_id': test_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to request lab test'}, 500

class LabTest(Resource):
    """Handle individual lab test operations"""
    
    @login_required
    def get(self, test_id):
        """Get specific lab test"""
        current_user = get_current_user()
        
        query = """
            SELECT lt.*, 
                   req.first_name as requested_by_first_name, req.last_name as requested_by_last_name,
                   proc.first_name as processed_by_first_name, proc.last_name as processed_by_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM lab_tests lt
            JOIN users req ON lt.requested_by = req.user_id
            LEFT JOIN users proc ON lt.processed_by = proc.user_id
            JOIN patient p ON lt.pat_id = p.pat_id
            WHERE lt.test_id = ?
        """
        
        test = conn.execute(query, (test_id,)).fetchone()
        
        if not test:
            return {'error': 'Lab test not found'}, 404
        
        # Check access permissions
        if current_user['role'] == 'patient':
            if current_user['entity_id'] != test['pat_id']:
                return {'error': 'Access denied'}, 403
        elif current_user['role'] == 'nurse':
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], test['pat_id'])
            ).fetchone()
            if not assignment:
                return {'error': 'Access denied'}, 403
        elif current_user['role'] == 'doctor':
            # Doctors can see tests they requested or for their patients
            if test['requested_by'] != current_user['user_id']:
                # Check if doctor has access to this patient (through appointments)
                appointment = conn.execute(
                    "SELECT 1 FROM appointment WHERE doc_id = ? AND pat_id = ?",
                    (current_user['entity_id'], test['pat_id'])
                ).fetchone()
                if not appointment:
                    return {'error': 'Access denied'}, 403
        
        log_access(current_user['user_id'], 'VIEW_LAB_TEST', 'LAB_TEST', test_id, test['pat_id'])
        
        return test, 200
    
    @role_required('admin', 'lab_technician', 'doctor')
    def put(self, test_id):
        """Update lab test (Lab Technician can update results, Doctor can update request)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Check if test exists
        test = conn.execute("SELECT * FROM lab_tests WHERE test_id = ?", (test_id,)).fetchone()
        if not test:
            return {'error': 'Lab test not found'}, 404
        
        update_data = {}
        
        # Role-based update permissions
        if current_user['role'] == 'lab_technician':
            # Lab technicians can update status, results, and processing info
            allowed_fields = ['status', 'results', 'normal_range', 'is_abnormal', 'technician_notes']
            
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            # Set processed_by and completed_date when completing test
            if 'status' in data and data['status'] == 'completed':
                update_data['processed_by'] = current_user['user_id']
                update_data['completed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Validate status
            if 'status' in update_data:
                valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
                if update_data['status'] not in valid_statuses:
                    return {'error': 'Invalid status'}, 400
        
        elif current_user['role'] == 'doctor':
            # Doctors can update test details if they requested it
            if test['requested_by'] != current_user['user_id']:
                return {'error': 'Only the requesting doctor can update test details'}, 403
            
            allowed_fields = ['test_type', 'test_name', 'priority']
            
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            # Validate priority
            if 'priority' in update_data:
                valid_priorities = ['normal', 'urgent', 'stat']
                if update_data['priority'] not in valid_priorities:
                    return {'error': 'Invalid priority level'}, 400
        
        elif current_user['role'] == 'admin':
            # Admin can update any field
            allowed_fields = ['test_type', 'test_name', 'priority', 'status', 'results', 'normal_range', 'is_abnormal', 'technician_notes']
            
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
        
        if not update_data:
            return {'error': 'No valid fields to update'}, 400
        
        try:
            # Build dynamic update query
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values()) + [test_id]
            
            conn.execute(f"UPDATE lab_tests SET {set_clause} WHERE test_id = ?", values)
            conn.commit()

            # Add to blockchain if test is completed
            if blockchain and 'status' in update_data and update_data['status'] == 'completed':
                try:
                    blockchain_data = {
                        'test_id': test_id,
                        'pat_id': test['pat_id'],
                        'test_type': test['test_type'],
                        'result_value': update_data.get('results', ''),
                        'status': 'completed',
                        'technician_id': current_user['user_id']
                    }
                    blockchain.add_lab_result(blockchain_data)
                except Exception as e:
                    print(f"Warning: Failed to add lab result to blockchain: {e}")

            log_access(current_user['user_id'], 'UPDATE_LAB_TEST', 'LAB_TEST', test_id, test['pat_id'])

            return {'message': 'Lab test updated successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to update lab test'}, 500
    
    @role_required('admin', 'doctor')
    def delete(self, test_id):
        """Cancel lab test (Admin/Doctor only)"""
        current_user = get_current_user()
        
        # Check if test exists
        test = conn.execute("SELECT * FROM lab_tests WHERE test_id = ?", (test_id,)).fetchone()
        if not test:
            return {'error': 'Lab test not found'}, 404
        
        # Only requesting doctor or admin can cancel
        if current_user['role'] == 'doctor' and test['requested_by'] != current_user['user_id']:
            return {'error': 'Only the requesting doctor can cancel this test'}, 403
        
        # Can't cancel completed tests
        if test['status'] == 'completed':
            return {'error': 'Cannot cancel completed test'}, 400
        
        try:
            conn.execute("UPDATE lab_tests SET status = 'cancelled' WHERE test_id = ?", (test_id,))
            conn.commit()
            
            log_access(current_user['user_id'], 'CANCEL_LAB_TEST', 'LAB_TEST', test_id, test['pat_id'])
            
            return {'message': 'Lab test cancelled successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to cancel lab test'}, 500

class LabTestsByPatient(Resource):
    """Get lab tests for a specific patient"""
    
    @patient_access_required
    def get(self, patient_id):
        """Get all lab tests for a patient"""
        current_user = get_current_user()
        
        query = """
            SELECT lt.*, 
                   req.first_name as requested_by_first_name, req.last_name as requested_by_last_name,
                   proc.first_name as processed_by_first_name, proc.last_name as processed_by_last_name
            FROM lab_tests lt
            JOIN users req ON lt.requested_by = req.user_id
            LEFT JOIN users proc ON lt.processed_by = proc.user_id
            WHERE lt.pat_id = ?
            ORDER BY lt.requested_date DESC
        """
        
        tests = conn.execute(query, (patient_id,)).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_PATIENT_LAB_TESTS', 'LAB_TEST', patient_id=patient_id)
        
        return tests, 200

class PendingLabTests(Resource):
    """Get pending lab tests for lab technicians"""
    
    @role_required('lab_technician', 'admin')
    def get(self):
        """Get all pending lab tests"""
        current_user = get_current_user()
        
        query = """
            SELECT lt.*, 
                   req.first_name as requested_by_first_name, req.last_name as requested_by_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM lab_tests lt
            JOIN users req ON lt.requested_by = req.user_id
            JOIN patient p ON lt.pat_id = p.pat_id
            WHERE lt.status IN ('pending', 'in_progress')
            ORDER BY 
                CASE lt.priority 
                    WHEN 'stat' THEN 1 
                    WHEN 'urgent' THEN 2 
                    WHEN 'normal' THEN 3 
                END,
                lt.requested_date ASC
        """
        
        tests = conn.execute(query).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_PENDING_LAB_TESTS', 'LAB_TEST')
        
        return tests, 200
