#!/usr/bin/env python3
"""
Full Workflow Testing for medicare Health Record Management System
Tests complete patient care workflows with actual data creation
"""

import requests
import json
import time
from datetime import datetime

class FullWorkflowTest:
    def __init__(self, base_url="http://127.0.0.1:5001"):
        self.base_url = base_url
        self.tokens = {}
        self.created_entities = {
            'patients': [],
            'appointments': [],
            'prescriptions': [],
            'lab_tests': [],
            'vital_signs': [],
            'health_records': []
        }
        
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
        
        print("🔐 Logging in all users...")
        for user in users:
            response = requests.post(f"{self.base_url}/auth/login", json={
                "username": user["username"],
                "password": user["password"]
            })
            
            if response.status_code == 200:
                self.tokens[user["role"]] = response.json()["token"]
                print(f"✓ {user['role']} logged in successfully")
            else:
                print(f"✗ {user['role']} login failed: {response.status_code}")
                return False
        return True
    
    def test_patient_creation_workflow(self):
        """Test creating a new patient and associated records"""
        print("\n👤 Testing Patient Creation Workflow...")
        
        if "admin" not in self.tokens:
            print("✗ Admin token not available")
            return False
        
        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        
        # Create a new patient
        patient_data = {
            "pat_first_name": "Test",
            "pat_last_name": "Patient",
            "pat_insurance_no": f"INS{int(time.time())}",
            "pat_ph_no": "+1-555-TEST",
            "pat_address": "123 Test Street"
        }
        
        response = requests.post(f"{self.base_url}/patients", json=patient_data, headers=headers)
        if response.status_code in [200, 201]:  # Accept both 200 and 201
            patient_id = response.json()["pat_id"]
            self.created_entities['patients'].append(patient_id)
            print(f"✓ Created patient with ID: {patient_id}")
            return patient_id
        else:
            print(f"✗ Failed to create patient: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def test_appointment_workflow(self, patient_id):
        """Test appointment creation and management"""
        print("\n📅 Testing Appointment Workflow...")
        
        if "doctor" not in self.tokens:
            print("✗ Doctor token not available")
            return False
        
        headers = {"Authorization": f"Bearer {self.tokens['doctor']}"}
        
        # Create appointment
        appointment_data = {
            "pat_id": patient_id,
            "doc_id": 1,  # Dr. Smith
            "appointment_date": "2025-12-10",
            "appointment_time": "10:00:00",
            "reason": "Regular checkup"
        }
        
        response = requests.post(f"{self.base_url}/appointments", json=appointment_data, headers=headers)
        if response.status_code in [200, 201]:  # Accept both 200 and 201
            appointment_id = response.json()["app_id"]
            self.created_entities['appointments'].append(appointment_id)
            print(f"✓ Created appointment with ID: {appointment_id}")
            return appointment_id
        else:
            print(f"✗ Failed to create appointment: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def assign_nurse_to_patient(self, patient_id):
        """Assign nurse to patient so they can record vital signs"""
        if "admin" not in self.tokens:
            return False

        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}

        # Get nurse user ID (nurse.williams)
        users_response = requests.get(f"{self.base_url}/users", headers=headers)
        if users_response.status_code == 200:
            users = users_response.json()
            nurse_user = next((u for u in users if u['username'] == 'nurse.williams'), None)
            if nurse_user:
                assignment_data = {
                    "nurse_id": nurse_user['user_id'],
                    "pat_id": patient_id,
                    "shift": "day",
                    "notes": "Test assignment"
                }

                response = requests.post(f"{self.base_url}/patient-assignments", json=assignment_data, headers=headers)
                if response.status_code in [200, 201]:
                    print(f"✓ Assigned nurse to patient {patient_id}")
                    return True
                else:
                    print(f"✗ Failed to assign nurse: {response.status_code}")
                    return False
        return False

    def test_vital_signs_workflow(self, patient_id):
        """Test vital signs recording by nurse"""
        print("\n🩺 Testing Vital Signs Workflow...")

        # First assign nurse to patient
        if not self.assign_nurse_to_patient(patient_id):
            print("✗ Failed to assign nurse to patient")
            return None

        if "nurse" not in self.tokens:
            print("✗ Nurse token not available")
            return False

        headers = {"Authorization": f"Bearer {self.tokens['nurse']}"}

        # Record vital signs
        vital_data = {
            "pat_id": patient_id,
            "temperature": 98.6,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "heart_rate": 72,
            "respiratory_rate": 16,
            "oxygen_saturation": 98.5,
            "weight": 70.5,
            "height": 175.0,
            "notes": "Normal vital signs"
        }

        response = requests.post(f"{self.base_url}/vital-signs", json=vital_data, headers=headers)
        if response.status_code in [200, 201]:
            vital_id = response.json()["vital_id"]
            self.created_entities['vital_signs'].append(vital_id)
            print(f"✓ Recorded vital signs with ID: {vital_id}")
            return vital_id
        else:
            print(f"✗ Failed to record vital signs: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def test_prescription_workflow(self, patient_id):
        """Test prescription creation and dispensing"""
        print("\n💊 Testing Prescription Workflow...")
        
        if "doctor" not in self.tokens:
            print("✗ Doctor token not available")
            return False
        
        headers = {"Authorization": f"Bearer {self.tokens['doctor']}"}
        
        # Create prescription
        prescription_data = {
            "pat_id": patient_id,
            "doc_id": 1,
            "med_code": 1002,  # Amoxicillin from sample data
            "medication_name": "Amoxicillin",
            "dosage": "500mg",
            "frequency": "3 times daily",
            "duration": "7 days",
            "instructions": "Take with food"
        }
        
        response = requests.post(f"{self.base_url}/prescriptions", json=prescription_data, headers=headers)
        if response.status_code == 201:
            prescription_id = response.json()["prescription_id"]
            self.created_entities['prescriptions'].append(prescription_id)
            print(f"✓ Created prescription with ID: {prescription_id}")
            return prescription_id
        else:
            print(f"✗ Failed to create prescription: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def test_lab_test_workflow(self, patient_id):
        """Test lab test ordering and processing"""
        print("\n🔬 Testing Lab Test Workflow...")
        
        if "doctor" not in self.tokens:
            print("✗ Doctor token not available")
            return False
        
        headers = {"Authorization": f"Bearer {self.tokens['doctor']}"}
        
        # Order lab test
        lab_test_data = {
            "pat_id": patient_id,
            "test_name": "Complete Blood Count",
            "test_type": "blood",
            "ordered_by": 1,  # Dr. Smith
            "priority": "normal",  # Changed from "routine" to "normal"
            "instructions": "Fasting required"
        }
        
        response = requests.post(f"{self.base_url}/lab-tests", json=lab_test_data, headers=headers)
        if response.status_code == 201:
            test_id = response.json()["test_id"]
            self.created_entities['lab_tests'].append(test_id)
            print(f"✓ Ordered lab test with ID: {test_id}")
            return test_id
        else:
            print(f"✗ Failed to order lab test: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def run_full_workflow_test(self):
        """Run complete workflow test"""
        print("🏥 medicare Full Workflow Test")
        print("="*50)
        
        if not self.login_all_users():
            print("✗ Failed to login users")
            return
        
        # Test patient creation
        patient_id = self.test_patient_creation_workflow()
        if not patient_id:
            print("✗ Patient creation failed, stopping workflow test")
            return
        
        # Test various workflows
        appointment_id = self.test_appointment_workflow(patient_id)
        vital_id = self.test_vital_signs_workflow(patient_id)
        prescription_id = self.test_prescription_workflow(patient_id)
        lab_test_id = self.test_lab_test_workflow(patient_id)
        
        # Summary
        print("\n📊 Workflow Test Summary")
        print("="*50)
        print(f"Patient Created: {'✓' if patient_id else '✗'}")
        print(f"Appointment Created: {'✓' if appointment_id else '✗'}")
        print(f"Vital Signs Recorded: {'✓' if vital_id else '✗'}")
        print(f"Prescription Created: {'✓' if prescription_id else '✗'}")
        print(f"Lab Test Ordered: {'✓' if lab_test_id else '✗'}")
        
        success_count = sum([bool(x) for x in [patient_id, appointment_id, vital_id, prescription_id, lab_test_id]])
        print(f"\nWorkflow Success Rate: {success_count}/5 ({success_count/5*100:.1f}%)")

if __name__ == "__main__":
    test = FullWorkflowTest()
    test.run_full_workflow_test()
