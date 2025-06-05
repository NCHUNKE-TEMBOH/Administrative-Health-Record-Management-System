from flask_restful import Resource, request
from flask import jsonify
from package.model import conn
from package.auth import login_required, role_required, patient_access_required, get_current_user, log_access

class MedicalNotes(Resource):
    """Handle medical notes operations"""
    
    @patient_access_required
    def get(self):
        """Get medical notes for a patient"""
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        note_type = request.args.get('note_type')
        
        if not patient_id:
            return {'error': 'Patient ID is required'}, 400
        
        # Base query
        query = """
            SELECT mn.*, 
                   u.first_name as doctor_first_name, u.last_name as doctor_last_name,
                   p.pat_first_name, p.pat_last_name,
                   a.appointment_date
            FROM medical_notes mn
            JOIN users u ON mn.doc_id = u.user_id
            JOIN patient p ON mn.pat_id = p.pat_id
            LEFT JOIN appointment a ON mn.appointment_id = a.app_id
            WHERE mn.pat_id = ?
        """
        params = [patient_id]
        
        # Filter by note type if provided
        if note_type:
            query += " AND mn.note_type = ?"
            params.append(note_type)
        
        # Filter private notes based on role
        if current_user['role'] not in ['admin', 'doctor']:
            query += " AND mn.is_private = 0"
        elif current_user['role'] == 'doctor':
            # Doctors can see their own private notes and all non-private notes
            query += " AND (mn.is_private = 0 OR mn.doc_id = ?)"
            params.append(current_user['user_id'])
        
        query += " ORDER BY mn.created_date DESC"
        
        notes = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_MEDICAL_NOTES', 'MEDICAL_NOTE', patient_id=patient_id)
        
        return notes, 200
    
    @role_required('admin', 'doctor')
    def post(self):
        """Create new medical note (Doctor/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['pat_id', 'subject', 'content']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Validate note type
        valid_types = ['general', 'diagnosis', 'treatment', 'follow_up']
        note_type = data.get('note_type', 'general')
        if note_type not in valid_types:
            return {'error': 'Invalid note type'}, 400
        
        # Validate appointment if provided
        appointment_id = data.get('appointment_id')
        if appointment_id:
            appointment = conn.execute(
                "SELECT app_id FROM appointment WHERE app_id = ? AND pat_id = ? AND doc_id = ?",
                (appointment_id, data['pat_id'], current_user['entity_id'])
            ).fetchone()
            if not appointment:
                return {'error': 'Invalid appointment or access denied'}, 400
        
        try:
            note_id = conn.execute("""
                INSERT INTO medical_notes (
                    pat_id, doc_id, appointment_id, note_type, subject, content, is_private
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data['pat_id'],
                current_user['user_id'],
                appointment_id,
                note_type,
                data['subject'],
                data['content'],
                data.get('is_private', 0)
            )).lastrowid
            
            conn.commit()
            
            log_access(current_user['user_id'], 'CREATE_MEDICAL_NOTE', 'MEDICAL_NOTE', note_id, data['pat_id'])
            
            return {
                'message': 'Medical note created successfully',
                'note_id': note_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to create medical note'}, 500

class MedicalNote(Resource):
    """Handle individual medical note operations"""
    
    @login_required
    def get(self, note_id):
        """Get specific medical note"""
        current_user = get_current_user()
        
        query = """
            SELECT mn.*, 
                   u.first_name as doctor_first_name, u.last_name as doctor_last_name,
                   p.pat_first_name, p.pat_last_name,
                   a.appointment_date
            FROM medical_notes mn
            JOIN users u ON mn.doc_id = u.user_id
            JOIN patient p ON mn.pat_id = p.pat_id
            LEFT JOIN appointment a ON mn.appointment_id = a.app_id
            WHERE mn.note_id = ?
        """
        
        note = conn.execute(query, (note_id,)).fetchone()
        
        if not note:
            return {'error': 'Medical note not found'}, 404
        
        # Check access permissions
        if note['is_private'] and current_user['role'] != 'admin':
            if current_user['role'] != 'doctor' or note['doc_id'] != current_user['user_id']:
                return {'error': 'Access denied to private note'}, 403
        
        # Check patient access for non-admin/doctor roles
        if current_user['role'] not in ['admin', 'doctor']:
            if current_user['role'] == 'patient' and current_user['entity_id'] != note['pat_id']:
                return {'error': 'Access denied'}, 403
            elif current_user['role'] == 'nurse':
                assignment = conn.execute(
                    "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                    (current_user['user_id'], note['pat_id'])
                ).fetchone()
                if not assignment:
                    return {'error': 'Access denied'}, 403
        
        log_access(current_user['user_id'], 'VIEW_MEDICAL_NOTE', 'MEDICAL_NOTE', note_id, note['pat_id'])
        
        return note, 200
    
    @role_required('admin', 'doctor')
    def put(self, note_id):
        """Update medical note (Doctor/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Check if note exists
        note = conn.execute("SELECT * FROM medical_notes WHERE note_id = ?", (note_id,)).fetchone()
        if not note:
            return {'error': 'Medical note not found'}, 404
        
        # Only note creator or admin can update
        if current_user['role'] != 'admin' and note['doc_id'] != current_user['user_id']:
            return {'error': 'Only the note creator or admin can update this note'}, 403
        
        # Fields that can be updated
        updatable_fields = ['note_type', 'subject', 'content', 'is_private']
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return {'error': 'No valid fields to update'}, 400
        
        # Validate note type if provided
        if 'note_type' in update_data:
            valid_types = ['general', 'diagnosis', 'treatment', 'follow_up']
            if update_data['note_type'] not in valid_types:
                return {'error': 'Invalid note type'}, 400
        
        try:
            # Build dynamic update query
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values()) + [note_id]
            
            conn.execute(f"UPDATE medical_notes SET {set_clause} WHERE note_id = ?", values)
            conn.commit()
            
            log_access(current_user['user_id'], 'UPDATE_MEDICAL_NOTE', 'MEDICAL_NOTE', note_id, note['pat_id'])
            
            return {'message': 'Medical note updated successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to update medical note'}, 500
    
    @role_required('admin')
    def delete(self, note_id):
        """Delete medical note (Admin only)"""
        current_user = get_current_user()
        
        # Check if note exists
        note = conn.execute("SELECT pat_id FROM medical_notes WHERE note_id = ?", (note_id,)).fetchone()
        if not note:
            return {'error': 'Medical note not found'}, 404
        
        try:
            conn.execute("DELETE FROM medical_notes WHERE note_id = ?", (note_id,))
            conn.commit()
            
            log_access(current_user['user_id'], 'DELETE_MEDICAL_NOTE', 'MEDICAL_NOTE', note_id, note['pat_id'])
            
            return {'message': 'Medical note deleted successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to delete medical note'}, 500

class NursingNotes(Resource):
    """Handle nursing notes operations"""
    
    @login_required
    def get(self):
        """Get nursing notes for a patient"""
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        shift = request.args.get('shift')
        note_type = request.args.get('note_type')
        
        if not patient_id:
            return {'error': 'Patient ID is required'}, 400
        
        # Check patient access
        if current_user['role'] == 'patient':
            if current_user['entity_id'] != int(patient_id):
                return {'error': 'Access denied'}, 403
        elif current_user['role'] == 'nurse':
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], patient_id)
            ).fetchone()
            if not assignment:
                return {'error': 'Access denied to patient data'}, 403
        elif current_user['role'] not in ['admin', 'doctor']:
            return {'error': 'Access denied'}, 403
        
        # Base query
        query = """
            SELECT nn.*, 
                   u.first_name as nurse_first_name, u.last_name as nurse_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM nursing_notes nn
            JOIN users u ON nn.nurse_id = u.user_id
            JOIN patient p ON nn.pat_id = p.pat_id
            WHERE nn.pat_id = ?
        """
        params = [patient_id]
        
        # Filter by shift if provided
        if shift:
            query += " AND nn.shift = ?"
            params.append(shift)
        
        # Filter by note type if provided
        if note_type:
            query += " AND nn.note_type = ?"
            params.append(note_type)
        
        query += " ORDER BY nn.created_date DESC"
        
        notes = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_NURSING_NOTES', 'NURSING_NOTE', patient_id=patient_id)
        
        return notes, 200
    
    @role_required('admin', 'nurse')
    def post(self):
        """Create new nursing note (Nurse/Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['pat_id', 'content']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Check if nurse is assigned to patient (unless admin)
        if current_user['role'] == 'nurse':
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], data['pat_id'])
            ).fetchone()
            
            if not assignment:
                return {'error': 'Access denied to patient data'}, 403
        
        # Validate shift
        valid_shifts = ['day', 'evening', 'night']
        shift = data.get('shift')
        if shift and shift not in valid_shifts:
            return {'error': 'Invalid shift'}, 400
        
        # Validate note type
        valid_types = ['observation', 'care_plan', 'medication_admin', 'incident']
        note_type = data.get('note_type', 'observation')
        if note_type not in valid_types:
            return {'error': 'Invalid note type'}, 400
        
        try:
            note_id = conn.execute("""
                INSERT INTO nursing_notes (pat_id, nurse_id, shift, note_type, content)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['pat_id'],
                current_user['user_id'],
                shift,
                note_type,
                data['content']
            )).lastrowid
            
            conn.commit()
            
            log_access(current_user['user_id'], 'CREATE_NURSING_NOTE', 'NURSING_NOTE', note_id, data['pat_id'])
            
            return {
                'message': 'Nursing note created successfully',
                'note_id': note_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to create nursing note'}, 500

class PatientAssignments(Resource):
    """Handle patient assignments for nurses"""
    
    @role_required('admin', 'nurse')
    def get(self):
        """Get patient assignments"""
        current_user = get_current_user()
        
        if current_user['role'] == 'nurse':
            # Nurses see only their assignments
            query = """
                SELECT pa.*, p.pat_first_name, p.pat_last_name, p.pat_insurance_no
                FROM patient_assignments pa
                JOIN patient p ON pa.pat_id = p.pat_id
                WHERE pa.nurse_id = ? AND pa.is_active = 1
                ORDER BY pa.assigned_date DESC
            """
            params = [current_user['user_id']]
        else:
            # Admin sees all assignments
            query = """
                SELECT pa.*, 
                       p.pat_first_name, p.pat_last_name, p.pat_insurance_no,
                       u.first_name as nurse_first_name, u.last_name as nurse_last_name
                FROM patient_assignments pa
                JOIN patient p ON pa.pat_id = p.pat_id
                JOIN users u ON pa.nurse_id = u.user_id
                WHERE pa.is_active = 1
                ORDER BY pa.assigned_date DESC
            """
            params = []
        
        assignments = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_PATIENT_ASSIGNMENTS', 'PATIENT_ASSIGNMENT')
        
        return assignments, 200
    
    @role_required('admin')
    def post(self):
        """Create patient assignment (Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['nurse_id', 'pat_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Check if nurse exists and has nurse role
        nurse = conn.execute(
            "SELECT user_id FROM users WHERE user_id = ? AND role = 'nurse' AND is_active = 1",
            (data['nurse_id'],)
        ).fetchone()
        if not nurse:
            return {'error': 'Nurse not found or inactive'}, 404
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Validate shift
        valid_shifts = ['day', 'evening', 'night']
        shift = data.get('shift')
        if shift and shift not in valid_shifts:
            return {'error': 'Invalid shift'}, 400
        
        try:
            assignment_id = conn.execute("""
                INSERT INTO patient_assignments (nurse_id, pat_id, shift, notes)
                VALUES (?, ?, ?, ?)
            """, (
                data['nurse_id'],
                data['pat_id'],
                shift,
                data.get('notes')
            )).lastrowid
            
            conn.commit()
            
            log_access(current_user['user_id'], 'CREATE_PATIENT_ASSIGNMENT', 'PATIENT_ASSIGNMENT', assignment_id, data['pat_id'])
            
            return {
                'message': 'Patient assignment created successfully',
                'assignment_id': assignment_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to create patient assignment'}, 500
