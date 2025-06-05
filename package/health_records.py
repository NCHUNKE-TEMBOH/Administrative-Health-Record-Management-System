from flask_restful import Resource, request
from flask import jsonify
from package.model import conn
from package.auth import login_required, role_required, patient_access_required, get_current_user, log_access, has_permission
from datetime import datetime

class HealthRecords(Resource):
    """Handle health records operations"""
    
    @patient_access_required
    def get(self):
        """Get health records for a patient"""
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        record_type = request.args.get('record_type')
        
        if not patient_id:
            return {'error': 'Patient ID is required'}, 400
        
        # Build query based on filters
        query = """
            SELECT hr.*, u.first_name as created_by_first_name, u.last_name as created_by_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM health_records hr
            JOIN users u ON hr.created_by = u.user_id
            JOIN patient p ON hr.pat_id = p.pat_id
            WHERE hr.pat_id = ?
        """
        params = [patient_id]
        
        if record_type:
            query += " AND hr.record_type = ?"
            params.append(record_type)
        
        # Filter confidential records based on role
        if current_user['role'] not in ['admin', 'doctor']:
            query += " AND hr.is_confidential = 0"
        
        query += " ORDER BY hr.created_date DESC"
        
        records = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_HEALTH_RECORDS', 'HEALTH_RECORD', patient_id=patient_id)
        
        return records, 200
    
    @role_required('admin', 'doctor', 'nurse')
    def post(self):
        """Create new health record"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        required_fields = ['pat_id', 'record_type', 'title', 'content']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400
        
        # Validate record type
        valid_types = ['medical_history', 'diagnosis', 'treatment_plan', 'discharge_summary']
        if data['record_type'] not in valid_types:
            return {'error': 'Invalid record type'}, 400
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Check permissions for patient access
        if current_user['role'] == 'nurse':
            # Nurses can only create records for assigned patients
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], data['pat_id'])
            ).fetchone()
            
            if not assignment:
                return {'error': 'Access denied to patient data'}, 403
        
        try:
            record_id = conn.execute("""
                INSERT INTO health_records (pat_id, record_type, title, content, created_by, is_confidential)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['pat_id'],
                data['record_type'],
                data['title'],
                data['content'],
                current_user['user_id'],
                data.get('is_confidential', 0)
            )).lastrowid
            
            conn.commit()
            
            log_access(current_user['user_id'], 'CREATE_HEALTH_RECORD', 'HEALTH_RECORD', record_id, data['pat_id'])
            
            return {
                'message': 'Health record created successfully',
                'record_id': record_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to create health record'}, 500

class HealthRecord(Resource):
    """Handle individual health record operations"""
    
    @patient_access_required
    def get(self, record_id):
        """Get specific health record"""
        current_user = get_current_user()
        
        query = """
            SELECT hr.*, u.first_name as created_by_first_name, u.last_name as created_by_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM health_records hr
            JOIN users u ON hr.created_by = u.user_id
            JOIN patient p ON hr.pat_id = p.pat_id
            WHERE hr.record_id = ?
        """
        
        record = conn.execute(query, (record_id,)).fetchone()
        
        if not record:
            return {'error': 'Health record not found'}, 404
        
        # Check confidential access
        if record['is_confidential'] and current_user['role'] not in ['admin', 'doctor']:
            return {'error': 'Access denied to confidential record'}, 403
        
        # Check patient access for non-admin/doctor roles
        if current_user['role'] not in ['admin', 'doctor']:
            if current_user['role'] == 'patient' and current_user['entity_id'] != record['pat_id']:
                return {'error': 'Access denied'}, 403
            elif current_user['role'] == 'nurse':
                assignment = conn.execute(
                    "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                    (current_user['user_id'], record['pat_id'])
                ).fetchone()
                if not assignment:
                    return {'error': 'Access denied'}, 403
        
        log_access(current_user['user_id'], 'VIEW_HEALTH_RECORD', 'HEALTH_RECORD', record_id, record['pat_id'])
        
        return record, 200
    
    @role_required('admin', 'doctor')
    def put(self, record_id):
        """Update health record (Admin/Doctor only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Check if record exists
        record = conn.execute("SELECT * FROM health_records WHERE record_id = ?", (record_id,)).fetchone()
        if not record:
            return {'error': 'Health record not found'}, 404
        
        # Only allow creator or admin to update
        if current_user['role'] != 'admin' and record['created_by'] != current_user['user_id']:
            return {'error': 'Only the creator or admin can update this record'}, 403
        
        # Fields that can be updated
        updatable_fields = ['record_type', 'title', 'content', 'is_confidential']
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return {'error': 'No valid fields to update'}, 400
        
        # Validate record type if provided
        if 'record_type' in update_data:
            valid_types = ['medical_history', 'diagnosis', 'treatment_plan', 'discharge_summary']
            if update_data['record_type'] not in valid_types:
                return {'error': 'Invalid record type'}, 400
        
        try:
            # Add updated_date
            update_data['updated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Build dynamic update query
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values()) + [record_id]
            
            conn.execute(f"UPDATE health_records SET {set_clause} WHERE record_id = ?", values)
            conn.commit()
            
            log_access(current_user['user_id'], 'UPDATE_HEALTH_RECORD', 'HEALTH_RECORD', record_id, record['pat_id'])
            
            return {'message': 'Health record updated successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to update health record'}, 500
    
    @role_required('admin')
    def delete(self, record_id):
        """Delete health record (Admin only)"""
        current_user = get_current_user()
        
        # Check if record exists
        record = conn.execute("SELECT pat_id FROM health_records WHERE record_id = ?", (record_id,)).fetchone()
        if not record:
            return {'error': 'Health record not found'}, 404
        
        try:
            conn.execute("DELETE FROM health_records WHERE record_id = ?", (record_id,))
            conn.commit()
            
            log_access(current_user['user_id'], 'DELETE_HEALTH_RECORD', 'HEALTH_RECORD', record_id, record['pat_id'])
            
            return {'message': 'Health record deleted successfully'}, 200
            
        except Exception as e:
            return {'error': 'Failed to delete health record'}, 500

class VitalSigns(Resource):
    """Handle vital signs operations"""
    
    @patient_access_required
    def get(self):
        """Get vital signs for a patient"""
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        
        if not patient_id:
            return {'error': 'Patient ID is required'}, 400
        
        # Get date range if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = """
            SELECT vs.*, u.first_name as recorded_by_first_name, u.last_name as recorded_by_last_name,
                   p.pat_first_name, p.pat_last_name
            FROM vital_signs vs
            JOIN users u ON vs.recorded_by = u.user_id
            JOIN patient p ON vs.pat_id = p.pat_id
            WHERE vs.pat_id = ?
        """
        params = [patient_id]
        
        if start_date:
            query += " AND vs.recorded_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND vs.recorded_date <= ?"
            params.append(end_date)
        
        query += " ORDER BY vs.recorded_date DESC"
        
        vital_signs = conn.execute(query, params).fetchall()
        
        log_access(current_user['user_id'], 'VIEW_VITAL_SIGNS', 'VITAL_SIGNS', patient_id=patient_id)
        
        return vital_signs, 200
    
    @role_required('admin', 'doctor', 'nurse')
    def post(self):
        """Record new vital signs"""
        current_user = get_current_user()
        data = request.get_json(force=True)
        
        # Required fields
        if 'pat_id' not in data:
            return {'error': 'Patient ID is required'}, 400
        
        # Check if patient exists
        patient = conn.execute("SELECT pat_id FROM patient WHERE pat_id = ?", (data['pat_id'],)).fetchone()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Check permissions for patient access
        if current_user['role'] == 'nurse':
            # Nurses can only record vitals for assigned patients
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], data['pat_id'])
            ).fetchone()
            
            if not assignment:
                return {'error': 'Access denied to patient data'}, 403
        
        # Validate vital signs data
        vital_fields = [
            'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'weight', 'height'
        ]
        
        # At least one vital sign must be provided
        if not any(field in data and data[field] is not None for field in vital_fields):
            return {'error': 'At least one vital sign measurement is required'}, 400
        
        try:
            vital_id = conn.execute("""
                INSERT INTO vital_signs (
                    pat_id, recorded_by, temperature, blood_pressure_systolic, 
                    blood_pressure_diastolic, heart_rate, respiratory_rate, 
                    oxygen_saturation, weight, height, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['pat_id'],
                current_user['user_id'],
                data.get('temperature'),
                data.get('blood_pressure_systolic'),
                data.get('blood_pressure_diastolic'),
                data.get('heart_rate'),
                data.get('respiratory_rate'),
                data.get('oxygen_saturation'),
                data.get('weight'),
                data.get('height'),
                data.get('notes')
            )).lastrowid
            
            conn.commit()
            
            log_access(current_user['user_id'], 'CREATE_VITAL_SIGNS', 'VITAL_SIGNS', vital_id, data['pat_id'])
            
            return {
                'message': 'Vital signs recorded successfully',
                'vital_id': vital_id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to record vital signs'}, 500
