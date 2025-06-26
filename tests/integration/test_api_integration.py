"""
Integration tests for API endpoints
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import insert_test_user, insert_test_patient, insert_test_doctor


class TestAuthenticationIntegration:
    """Integration tests for authentication flow"""
    
    def test_complete_auth_flow(self, app_client, db_connection, sample_users):
        """Test complete authentication flow: register -> login -> access protected endpoint"""
        # Step 1: Register a new user
        user_data = sample_users[0]
        register_response = app_client.post('/auth/register', 
                                          json=user_data,
                                          content_type='application/json')
        
        assert register_response.status_code == 201
        register_data = json.loads(register_response.data)
        assert 'user_id' in register_data
        
        # Step 2: Login with the registered user
        login_response = app_client.post('/auth/login',
                                       json={
                                           "username": user_data["username"],
                                           "password": user_data["password"]
                                       },
                                       content_type='application/json')
        
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        assert 'token' in login_data
        assert 'user' in login_data
        
        token = login_data['token']
        
        # Step 3: Access protected endpoint with token
        headers = {'Authorization': f'Bearer {token}'}
        profile_response = app_client.get('/auth/profile', headers=headers)
        
        assert profile_response.status_code == 200
        profile_data = json.loads(profile_response.data)
        assert profile_data['username'] == user_data["username"]
    
    def test_invalid_token_access(self, app_client):
        """Test access to protected endpoint with invalid token"""
        headers = {'Authorization': 'Bearer invalid_token'}
        response = app_client.get('/auth/profile', headers=headers)
        
        assert response.status_code == 401
    
    def test_missing_token_access(self, app_client):
        """Test access to protected endpoint without token"""
        response = app_client.get('/auth/profile')
        
        assert response.status_code == 401


class TestPatientManagementIntegration:
    """Integration tests for patient management"""
    
    def test_patient_crud_operations(self, app_client, db_connection, auth_headers, sample_patients):
        """Test complete CRUD operations for patients"""
        headers = auth_headers()
        patient_data = sample_patients[0]
        
        # Create patient
        create_response = app_client.post('/patients',
                                        json=patient_data,
                                        headers=headers)
        
        assert create_response.status_code == 201
        created_patient = json.loads(create_response.data)
        patient_id = created_patient['pat_id']
        
        # Read patient
        read_response = app_client.get(f'/patients/{patient_id}', headers=headers)
        assert read_response.status_code == 200
        read_patient = json.loads(read_response.data)
        assert len(read_patient) == 1
        assert read_patient[0]['pat_first_name'] == patient_data['pat_first_name']
        
        # Update patient
        updated_data = patient_data.copy()
        updated_data['pat_last_name'] = 'Updated-Name'
        
        update_response = app_client.put(f'/patients/{patient_id}',
                                       json=updated_data,
                                       headers=headers)
        assert update_response.status_code == 200
        
        # Verify update
        verify_response = app_client.get(f'/patients/{patient_id}', headers=headers)
        verify_patient = json.loads(verify_response.data)
        assert verify_patient[0]['pat_last_name'] == 'Updated-Name'
        
        # Delete patient
        delete_response = app_client.delete(f'/patients/{patient_id}', headers=headers)
        assert delete_response.status_code == 200
        
        # Verify deletion
        verify_delete_response = app_client.get(f'/patients/{patient_id}', headers=headers)
        verify_delete_data = json.loads(verify_delete_response.data)
        assert len(verify_delete_data) == 0
    
    def test_patient_list_operations(self, app_client, db_connection, auth_headers, sample_patients):
        """Test patient list operations"""
        headers = auth_headers()
        
        # Get initial count
        initial_response = app_client.get('/patients', headers=headers)
        initial_patients = json.loads(initial_response.data)
        initial_count = len(initial_patients)
        
        # Add multiple patients
        for patient_data in sample_patients:
            create_response = app_client.post('/patients',
                                            json=patient_data,
                                            headers=headers)
            assert create_response.status_code == 201
        
        # Verify count increased
        final_response = app_client.get('/patients', headers=headers)
        final_patients = json.loads(final_response.data)
        assert len(final_patients) == initial_count + len(sample_patients)


class TestDoctorPatientIntegration:
    """Integration tests for doctor-patient relationships"""
    
    def test_doctor_patient_workflow(self, app_client, db_connection, auth_headers, sample_doctors, sample_patients):
        """Test workflow involving doctors and patients"""
        headers = auth_headers()
        
        # Create doctor
        doctor_data = sample_doctors[0]
        doctor_response = app_client.post('/doctor',
                                        json=doctor_data,
                                        headers=headers)
        assert doctor_response.status_code == 201
        created_doctor = json.loads(doctor_response.data)
        doctor_id = created_doctor['doc_id']
        
        # Create patient
        patient_data = sample_patients[0]
        patient_response = app_client.post('/patients',
                                         json=patient_data,
                                         headers=headers)
        assert patient_response.status_code == 201
        created_patient = json.loads(patient_response.data)
        patient_id = created_patient['pat_id']
        
        # Create appointment
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": "2024-12-31",
            "appointment_time": "10:00:00",
            "reason": "Regular checkup"
        }
        
        appointment_response = app_client.post('/appointments',
                                             json=appointment_data,
                                             headers=headers)
        assert appointment_response.status_code == 201
        
        # Verify appointment was created
        appointments_response = app_client.get('/appointments', headers=headers)
        appointments = json.loads(appointments_response.data)
        
        # Find our appointment
        our_appointment = None
        for apt in appointments:
            if apt['patient_id'] == patient_id and apt['doctor_id'] == doctor_id:
                our_appointment = apt
                break
        
        assert our_appointment is not None
        assert our_appointment['reason'] == "Regular checkup"


class TestHealthRecordsIntegration:
    """Integration tests for health records management"""
    
    def test_health_records_workflow(self, app_client, db_connection, auth_headers, sample_patients, sample_doctors):
        """Test complete health records workflow"""
        headers = auth_headers()
        
        # Create patient and doctor first
        patient_data = sample_patients[0]
        patient_response = app_client.post('/patients', json=patient_data, headers=headers)
        patient_id = json.loads(patient_response.data)['pat_id']
        
        doctor_data = sample_doctors[0]
        doctor_response = app_client.post('/doctor', json=doctor_data, headers=headers)
        doctor_id = json.loads(doctor_response.data)['doc_id']
        
        # Create health record
        health_record_data = {
            "patient_id": patient_id,
            "record_type": "consultation",
            "diagnosis": "Hypertension",
            "treatment": "Medication prescribed",
            "notes": "Patient responding well"
        }
        
        record_response = app_client.post('/health-records',
                                        json=health_record_data,
                                        headers=headers)
        assert record_response.status_code == 201
        
        # Record vital signs
        vital_signs_data = {
            "patient_id": patient_id,
            "temperature": 98.6,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "heart_rate": 72,
            "respiratory_rate": 16,
            "oxygen_saturation": 98
        }
        
        vitals_response = app_client.post('/vital-signs',
                                        json=vital_signs_data,
                                        headers=headers)
        assert vitals_response.status_code == 201
        
        # Verify records exist
        records_response = app_client.get('/health-records', headers=headers)
        records = json.loads(records_response.data)
        
        patient_records = [r for r in records if r['patient_id'] == patient_id]
        assert len(patient_records) > 0
        assert patient_records[0]['diagnosis'] == "Hypertension"


class TestPrescriptionWorkflow:
    """Integration tests for prescription workflow"""
    
    def test_prescription_dispensing_workflow(self, app_client, db_connection, auth_headers, sample_patients, sample_doctors):
        """Test complete prescription workflow from creation to dispensing"""
        headers = auth_headers()
        
        # Create patient and doctor
        patient_data = sample_patients[0]
        patient_response = app_client.post('/patients', json=patient_data, headers=headers)
        patient_id = json.loads(patient_response.data)['pat_id']
        
        doctor_data = sample_doctors[0]
        doctor_response = app_client.post('/doctor', json=doctor_data, headers=headers)
        doctor_id = json.loads(doctor_response.data)['doc_id']
        
        # Create prescription
        prescription_data = {
            "patient_id": patient_id,
            "medication_name": "Lisinopril",
            "dosage": "10mg",
            "frequency": "Once daily",
            "duration": "30 days",
            "instructions": "Take with food"
        }
        
        prescription_response = app_client.post('/prescriptions',
                                              json=prescription_data,
                                              headers=headers)
        assert prescription_response.status_code == 201
        prescription_result = json.loads(prescription_response.data)
        prescription_id = prescription_result['prescription_id']
        
        # Record medication dispensing
        dispensing_data = {
            "prescription_id": prescription_id,
            "quantity_dispensed": 30,
            "dispensed_by": 1,
            "notes": "Patient counseled on usage"
        }
        
        dispensing_response = app_client.post('/medication-dispensing',
                                            json=dispensing_data,
                                            headers=headers)
        assert dispensing_response.status_code == 201
        
        # Verify prescription exists
        prescriptions_response = app_client.get('/prescriptions', headers=headers)
        prescriptions = json.loads(prescriptions_response.data)
        
        our_prescription = None
        for p in prescriptions:
            if p['prescription_id'] == prescription_id:
                our_prescription = p
                break
        
        assert our_prescription is not None
        assert our_prescription['medication_name'] == "Lisinopril"


class TestLabTestWorkflow:
    """Integration tests for lab test workflow"""
    
    def test_lab_test_complete_workflow(self, app_client, db_connection, auth_headers, sample_patients, sample_doctors):
        """Test complete lab test workflow from ordering to results"""
        headers = auth_headers()
        
        # Create patient and doctor
        patient_data = sample_patients[0]
        patient_response = app_client.post('/patients', json=patient_data, headers=headers)
        patient_id = json.loads(patient_response.data)['pat_id']
        
        doctor_data = sample_doctors[0]
        doctor_response = app_client.post('/doctor', json=doctor_data, headers=headers)
        doctor_id = json.loads(doctor_response.data)['doc_id']
        
        # Order lab test
        lab_test_data = {
            "patient_id": patient_id,
            "test_type": "Blood Test",
            "test_name": "Complete Blood Count",
            "priority": "normal",
            "instructions": "Fasting required"
        }
        
        test_response = app_client.post('/lab-tests',
                                      json=lab_test_data,
                                      headers=headers)
        assert test_response.status_code == 201
        test_result = json.loads(test_response.data)
        test_id = test_result['test_id']
        
        # Check pending tests
        pending_response = app_client.get('/lab-tests/pending', headers=headers)
        pending_tests = json.loads(pending_response.data)
        
        our_test = None
        for test in pending_tests:
            if test['test_id'] == test_id:
                our_test = test
                break
        
        assert our_test is not None
        assert our_test['status'] == 'pending'
        
        # Update test with results
        update_data = {
            "status": "completed",
            "results": "All values within normal range",
            "notes": "No abnormalities detected"
        }
        
        update_response = app_client.put(f'/lab-tests/{test_id}',
                                       json=update_data,
                                       headers=headers)
        assert update_response.status_code == 200
        
        # Verify test is completed
        completed_response = app_client.get(f'/lab-tests/{test_id}', headers=headers)
        assert completed_response.status_code == 200


class TestErrorHandlingIntegration:
    """Integration tests for error handling across the system"""
    
    def test_cascade_error_handling(self, app_client, auth_headers):
        """Test error handling when operations depend on non-existent resources"""
        headers = auth_headers()
        
        # Try to create appointment with non-existent patient and doctor
        appointment_data = {
            "patient_id": 99999,  # Non-existent
            "doctor_id": 99999,   # Non-existent
            "appointment_date": "2024-12-31",
            "appointment_time": "10:00:00",
            "reason": "Test appointment"
        }
        
        response = app_client.post('/appointments',
                                 json=appointment_data,
                                 headers=headers)
        
        # Should handle gracefully (either 400 or 404)
        assert response.status_code in [400, 404, 500]
    
    def test_data_integrity_constraints(self, app_client, auth_headers):
        """Test data integrity constraints"""
        headers = auth_headers()
        
        # Try to create patient with invalid data
        invalid_patient_data = {
            "pat_first_name": "",  # Empty name
            "pat_last_name": "",   # Empty name
            "pat_insurance_no": "INS123",
            "pat_ph_no": "invalid_phone",
            "pat_address": ""
        }
        
        response = app_client.post('/patients',
                                 json=invalid_patient_data,
                                 headers=headers)
        
        # Should reject invalid data
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__])
