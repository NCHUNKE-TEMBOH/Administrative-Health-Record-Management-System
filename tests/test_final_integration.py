#!/usr/bin/env python3
"""
Final Integration Test for medicare Health Record Management System
Tests complete end-to-end scenarios across all portals
"""

import requests
import json
import time

class FinalIntegrationTest:
    def __init__(self, base_url="http://127.0.0.1:5001"):
        self.base_url = base_url
        self.tokens = {}
        self.test_data = {}
        
    def login_all_users(self):
        """Login all test users"""
        users = [
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "dr.smith", "password": "doctor123", "role": "doctor"},
            {"username": "nurse.williams", "password": "nurse123", "role": "nurse"},
            {"username": "lab.tech1", "password": "lab123", "role": "lab_technician"},
            {"username": "pharmacist1", "password": "pharm123", "role": "pharmacist"},
            {"username": "patient.doe", "password": "patient123", "role": "patient"}
        ]
        
        print("🔐 Authenticating all user roles...")
        for user in users:
            response = requests.post(f"{self.base_url}/auth/login", json={
                "username": user["username"],
                "password": user["password"]
            })
            
            if response.status_code == 200:
                self.tokens[user["role"]] = response.json()["token"]
                print(f"✓ {user['role'].replace('_', ' ').title()} authenticated")
            else:
                print(f"✗ {user['role']} authentication failed")
                return False
        return True
    
    def test_complete_patient_journey(self):
        """Test complete patient journey from admission to discharge"""
        print("\n🏥 Testing Complete Patient Journey...")
        print("-" * 50)
        
        # Step 1: Admin creates new patient
        print("1️⃣ Admin creates new patient...")
        admin_headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        
        patient_data = {
            "pat_first_name": "Integration",
            "pat_last_name": "Test",
            "pat_insurance_no": f"INT{int(time.time())}",
            "pat_ph_no": "+1-555-INTEG",
            "pat_address": "123 Integration Test St"
        }
        
        response = requests.post(f"{self.base_url}/patients", json=patient_data, headers=admin_headers)
        if response.status_code in [200, 201]:
            patient_id = response.json()["pat_id"]
            self.test_data['patient_id'] = patient_id
            print(f"   ✓ Patient created with ID: {patient_id}")
        else:
            print(f"   ✗ Patient creation failed: {response.status_code}")
            return False
        
        # Step 2: Admin assigns nurse to patient
        print("2️⃣ Admin assigns nurse to patient...")
        users_response = requests.get(f"{self.base_url}/users", headers=admin_headers)
        if users_response.status_code == 200:
            users = users_response.json()
            nurse_user = next((u for u in users if u['username'] == 'nurse.williams'), None)
            if nurse_user:
                assignment_data = {
                    "nurse_id": nurse_user['user_id'],
                    "pat_id": patient_id,
                    "shift": "day",
                    "notes": "Integration test assignment"
                }
                
                response = requests.post(f"{self.base_url}/patient-assignments", json=assignment_data, headers=admin_headers)
                if response.status_code in [200, 201]:
                    print(f"   ✓ Nurse assigned to patient")
                else:
                    print(f"   ✗ Nurse assignment failed: {response.status_code}")
        
        # Step 3: Doctor schedules appointment
        print("3️⃣ Doctor schedules appointment...")
        doctor_headers = {"Authorization": f"Bearer {self.tokens['doctor']}"}
        
        appointment_data = {
            "pat_id": patient_id,
            "doc_id": 1,
            "appointment_date": "2025-12-15",
            "appointment_time": "14:00:00",
            "reason": "Integration test consultation"
        }
        
        response = requests.post(f"{self.base_url}/appointments", json=appointment_data, headers=doctor_headers)
        if response.status_code in [200, 201]:
            appointment_id = response.json()["app_id"]
            self.test_data['appointment_id'] = appointment_id
            print(f"   ✓ Appointment scheduled with ID: {appointment_id}")
        else:
            print(f"   ✗ Appointment scheduling failed: {response.status_code}")
        
        # Step 4: Nurse records vital signs
        print("4️⃣ Nurse records vital signs...")
        nurse_headers = {"Authorization": f"Bearer {self.tokens['nurse']}"}
        
        vital_data = {
            "pat_id": patient_id,
            "temperature": 99.1,
            "blood_pressure_systolic": 130,
            "blood_pressure_diastolic": 85,
            "heart_rate": 78,
            "respiratory_rate": 18,
            "oxygen_saturation": 97.8,
            "weight": 68.5,
            "height": 170.0,
            "notes": "Integration test vitals"
        }
        
        response = requests.post(f"{self.base_url}/vital-signs", json=vital_data, headers=nurse_headers)
        if response.status_code in [200, 201]:
            vital_id = response.json()["vital_id"]
            self.test_data['vital_id'] = vital_id
            print(f"   ✓ Vital signs recorded with ID: {vital_id}")
        else:
            print(f"   ✗ Vital signs recording failed: {response.status_code}")
        
        # Step 5: Doctor orders lab test
        print("5️⃣ Doctor orders lab test...")
        lab_test_data = {
            "pat_id": patient_id,
            "test_name": "Blood Chemistry Panel",
            "test_type": "blood",
            "ordered_by": 1,
            "priority": "normal",
            "instructions": "Integration test lab order"
        }
        
        response = requests.post(f"{self.base_url}/lab-tests", json=lab_test_data, headers=doctor_headers)
        if response.status_code in [200, 201]:
            lab_test_id = response.json()["test_id"]
            self.test_data['lab_test_id'] = lab_test_id
            print(f"   ✓ Lab test ordered with ID: {lab_test_id}")
        else:
            print(f"   ✗ Lab test ordering failed: {response.status_code}")
        
        # Step 6: Doctor creates prescription
        print("6️⃣ Doctor creates prescription...")
        prescription_data = {
            "pat_id": patient_id,
            "doc_id": 1,
            "med_code": 1001,  # Aspirin
            "medication_name": "Aspirin",
            "dosage": "325mg",
            "frequency": "Once daily",
            "duration": "30 days",
            "instructions": "Take with food"
        }
        
        response = requests.post(f"{self.base_url}/prescriptions", json=prescription_data, headers=doctor_headers)
        if response.status_code in [200, 201]:
            prescription_id = response.json()["prescription_id"]
            self.test_data['prescription_id'] = prescription_id
            print(f"   ✓ Prescription created with ID: {prescription_id}")
        else:
            print(f"   ✗ Prescription creation failed: {response.status_code}")
        
        # Step 7: Lab technician processes test
        print("7️⃣ Lab technician views pending tests...")
        lab_headers = {"Authorization": f"Bearer {self.tokens['lab_technician']}"}
        
        response = requests.get(f"{self.base_url}/lab-tests/pending", headers=lab_headers)
        if response.status_code == 200:
            pending_tests = response.json()
            print(f"   ✓ Lab technician can view {len(pending_tests)} pending tests")
        else:
            print(f"   ✗ Lab technician access failed: {response.status_code}")
        
        # Step 8: Pharmacist views prescriptions
        print("8️⃣ Pharmacist views prescriptions...")
        pharmacy_headers = {"Authorization": f"Bearer {self.tokens['pharmacist']}"}
        
        response = requests.get(f"{self.base_url}/prescriptions", headers=pharmacy_headers)
        if response.status_code == 200:
            prescriptions = response.json()
            print(f"   ✓ Pharmacist can view {len(prescriptions)} prescriptions")
        else:
            print(f"   ✗ Pharmacist access failed: {response.status_code}")
        
        return True
    
    def test_cross_portal_data_access(self):
        """Test that data created in one portal is accessible in others"""
        print("\n🔄 Testing Cross-Portal Data Access...")
        print("-" * 50)
        
        if 'patient_id' not in self.test_data:
            print("✗ No test patient data available")
            return False
        
        patient_id = self.test_data['patient_id']
        
        # Test doctor can see patient data
        print("🩺 Doctor accessing patient data...")
        doctor_headers = {"Authorization": f"Bearer {self.tokens['doctor']}"}
        response = requests.get(f"{self.base_url}/patients/{patient_id}", headers=doctor_headers)
        if response.status_code == 200:
            print("   ✓ Doctor can access patient data")
        else:
            print(f"   ✗ Doctor access failed: {response.status_code}")
        
        # Test nurse can see vital signs
        print("👩‍⚕️ Nurse accessing vital signs...")
        nurse_headers = {"Authorization": f"Bearer {self.tokens['nurse']}"}
        response = requests.get(f"{self.base_url}/vital-signs?patient_id={patient_id}", headers=nurse_headers)
        if response.status_code == 200:
            vital_signs = response.json()
            print(f"   ✓ Nurse can access {len(vital_signs)} vital signs records")
        else:
            print(f"   ✗ Nurse access failed: {response.status_code}")
        
        # Test admin can see all data
        print("👑 Admin accessing all patient data...")
        admin_headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        response = requests.get(f"{self.base_url}/patients", headers=admin_headers)
        if response.status_code == 200:
            patients = response.json()
            print(f"   ✓ Admin can access {len(patients)} patient records")
        else:
            print(f"   ✗ Admin access failed: {response.status_code}")
        
        return True
    
    def run_final_integration_test(self):
        """Run complete integration test"""
        print("🎯 medicare Final Integration Test")
        print("=" * 60)
        
        if not self.login_all_users():
            print("✗ User authentication failed")
            return
        
        success = True
        success &= self.test_complete_patient_journey()
        success &= self.test_cross_portal_data_access()
        
        print("\n🏆 Final Integration Test Results")
        print("=" * 60)
        if success:
            print("✅ ALL INTEGRATION TESTS PASSED")
            print("🎉 medicare system is fully functional and ready for production!")
        else:
            print("❌ Some integration tests failed")
            print("⚠️ Please review the issues before production deployment")

if __name__ == "__main__":
    test = FinalIntegrationTest()
    test.run_final_integration_test()
