# 🚀 API Quick Reference Guide

## 🔗 Base URL
```
http://127.0.0.1:5001
```

## 🔑 Authentication

### 1. Login
```bash
curl -X POST http://127.0.0.1:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Use Token
```bash
curl -X GET http://127.0.0.1:5001/patients \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📋 Most Common Endpoints

### 👥 Patients
```bash
# Get all patients
GET /patients

# Create patient
POST /patients
{
  "pat_first_name": "John",
  "pat_last_name": "Doe",
  "pat_insurance_no": "INS123",
  "pat_ph_no": "+1234567890",
  "pat_address": "123 Main St"
}

# Get patient by ID
GET /patients/1
```

### 👨‍⚕️ Doctors
```bash
# Get all doctors
GET /doctor

# Create doctor
POST /doctor
{
  "doc_first_name": "Dr. Jane",
  "doc_last_name": "Smith",
  "doc_specialization": "Cardiology",
  "doc_ph_no": "+1234567890",
  "doc_address": "Hospital Address"
}
```

### 📅 Appointments
```bash
# Get all appointments
GET /appointments

# Create appointment
POST /appointments
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-01-01",
  "appointment_time": "10:00:00",
  "reason": "Regular checkup"
}
```

### 💊 Prescriptions
```bash
# Get all prescriptions
GET /prescriptions

# Create prescription
POST /prescriptions
{
  "patient_id": 1,
  "medication_name": "Aspirin",
  "dosage": "325mg",
  "frequency": "Once daily",
  "duration": "30 days",
  "instructions": "Take with food"
}
```

### 🧪 Lab Tests
```bash
# Get all lab tests
GET /lab-tests

# Create lab test
POST /lab-tests
{
  "patient_id": 1,
  "test_type": "Blood Test",
  "test_name": "Complete Blood Count",
  "priority": "normal",
  "instructions": "Fasting required"
}

# Get pending tests
GET /lab-tests/pending
```

### 📋 Health Records
```bash
# Get all health records
GET /health-records

# Create health record
POST /health-records
{
  "patient_id": 1,
  "record_type": "consultation",
  "diagnosis": "Hypertension",
  "treatment": "Medication prescribed",
  "notes": "Patient responding well"
}
```

### 🩺 Vital Signs
```bash
# Get vital signs
GET /vital-signs

# Record vital signs
POST /vital-signs
{
  "patient_id": 1,
  "temperature": 98.6,
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "heart_rate": 72,
  "respiratory_rate": 16,
  "oxygen_saturation": 98
}
```

## 🔐 Role-Based Examples

### Admin Operations
```bash
# Create user
POST /users
{
  "username": "newdoctor",
  "email": "doctor@hospital.com",
  "password": "secure123",
  "role": "doctor",
  "first_name": "John",
  "last_name": "Smith"
}

# Get all users
GET /users
```

### Doctor Operations
```bash
# Get my patients
GET /patients

# Create prescription
POST /prescriptions
{
  "patient_id": 1,
  "medication_name": "Lisinopril",
  "dosage": "10mg",
  "frequency": "Once daily"
}

# Order lab test
POST /lab-tests
{
  "patient_id": 1,
  "test_type": "Blood Test",
  "test_name": "Lipid Panel"
}
```

### Nurse Operations
```bash
# Record vital signs
POST /vital-signs
{
  "patient_id": 1,
  "temperature": 98.6,
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80
}

# Create nursing note
POST /nursing-notes
{
  "patient_id": 1,
  "note_type": "assessment",
  "content": "Patient stable, no complaints"
}
```

### Lab Technician Operations
```bash
# Get pending tests
GET /lab-tests/pending

# Update test results
PUT /lab-tests/1
{
  "status": "completed",
  "results": "All values within normal range",
  "notes": "No abnormalities detected"
}
```

### Pharmacist Operations
```bash
# Get prescriptions
GET /prescriptions

# Record dispensing
POST /medication-dispensing
{
  "prescription_id": 1,
  "quantity_dispensed": 30,
  "notes": "Patient counseled on usage"
}
```

## ⚠️ Common Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions",
  "code": "FORBIDDEN"
}
```

### 400 Bad Request
```json
{
  "error": "Missing required field: patient_id",
  "code": "VALIDATION_ERROR"
}
```

### 404 Not Found
```json
{
  "error": "Patient not found",
  "code": "NOT_FOUND"
}
```

## 🔧 Testing with Python

```python
import requests

# Base configuration
BASE_URL = "http://127.0.0.1:5001"
headers = {"Content-Type": "application/json"}

# Login
login_data = {"username": "admin", "password": "admin123"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["token"]

# Set authorization header
auth_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Get patients
patients = requests.get(f"{BASE_URL}/patients", headers=auth_headers)
print(patients.json())

# Create patient
new_patient = {
    "pat_first_name": "John",
    "pat_last_name": "Doe",
    "pat_insurance_no": "INS123",
    "pat_ph_no": "+1234567890",
    "pat_address": "123 Main St"
}
response = requests.post(f"{BASE_URL}/patients", 
                        json=new_patient, headers=auth_headers)
print(response.json())
```

## 📊 Response Formats

### Success Response
```json
{
  "data": [...],
  "message": "Operation successful"
}
```

### List Response
```json
[
  {
    "id": 1,
    "name": "Item 1"
  },
  {
    "id": 2,
    "name": "Item 2"
  }
]
```

### Created Response
```json
{
  "message": "Resource created successfully",
  "id": 123
}
```

## 🚀 Quick Start Checklist

1. ✅ Start the Flask server: `python app.py`
2. ✅ Login to get JWT token: `POST /auth/login`
3. ✅ Include token in all requests: `Authorization: Bearer <token>`
4. ✅ Use appropriate HTTP methods (GET, POST, PUT, DELETE)
5. ✅ Send JSON data with `Content-Type: application/json`
6. ✅ Handle error responses appropriately
7. ✅ Respect role-based access controls

## 📚 Additional Resources

- **Full Documentation**: `API_DOCUMENTATION.md`
- **Endpoints Summary**: `API_ENDPOINTS_SUMMARY.md`
- **Test Files**: `test_api_endpoints.py`
- **Frontend Integration**: `static/` directory

---
**Quick Reference Version**: 1.0  
**Last Updated**: 2024-06-25
