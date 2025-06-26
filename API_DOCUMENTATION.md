# 🏥 Administrative Health Record Management System - API Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Files Structure](#api-files-structure)
4. [Core API Endpoints](#core-api-endpoints)
5. [Authentication & User Management](#authentication--user-management)
6. [Patient Management](#patient-management)
7. [Doctor Management](#doctor-management)
8. [Nurse Management](#nurse-management)
9. [Health Records Management](#health-records-management)
10. [Lab Tests Management](#lab-tests-management)
11. [Prescriptions Management](#prescriptions-management)
12. [Medical Notes Management](#medical-notes-management)
13. [Appointments Management](#appointments-management)
14. [Department Management](#department-management)
15. [Medication Management](#medication-management)
16. [Room Management](#room-management)
17. [Procedures Management](#procedures-management)
18. [Error Handling](#error-handling)
19. [Response Formats](#response-formats)

## 🔍 Overview

The Administrative Health Record Management System provides a comprehensive RESTful API for managing healthcare operations. The API is built using Flask-RESTful and supports JWT-based authentication with role-based access control.

**Base URL:** `http://127.0.0.1:5001`

**API Version:** 1.0

**Content-Type:** `application/json`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid JWT token in the Authorization header.

### Authentication Header Format

```
Authorization: Bearer <jwt_token>
```

### Supported Roles

- `admin` - Full system access
- `doctor` - Patient care and medical records
- `nurse` - Patient care and nursing notes
- `lab_technician` - Lab test management
- `pharmacist` - Prescription and medication management
- `patient` - Personal health records access

## 📁 API Files Structure

The following files contain API endpoints:

| File | Description | Endpoints |
|------|-------------|-----------|
| `app.py` | Main application with route definitions | Route mappings |
| `package/auth.py` | Authentication utilities | JWT handling |
| `package/user_management.py` | User authentication & management | `/auth/*`, `/users/*` |
| `package/patient.py` | Patient operations | `/patient/*`, `/patients/*` |
| `package/doctor.py` | Doctor operations | `/doctor/*` |
| `package/nurse.py` | Nurse operations | `/nurse/*` |
| `package/health_records.py` | Health records management | `/health-records/*`, `/vital-signs/*` |
| `package/lab_results.py` | Lab test management | `/lab-tests/*` |
| `package/prescriptions_enhanced.py` | Prescription management | `/prescriptions/*`, `/medication-dispensing/*` |
| `package/medical_notes.py` | Medical & nursing notes | `/medical-notes/*`, `/nursing-notes/*` |
| `package/appointment.py` | Appointment management | `/appointment/*`, `/appointments/*` |
| `package/department.py` | Department management | `/department/*` |
| `package/medication.py` | Medication catalog | `/medication/*` |
| `package/room.py` | Room management | `/room/*` |
| `package/procedure.py` | Medical procedures | `/procedure/*` |
| `package/prescribes.py` | Prescription relationships | `/prescribes/*` |
| `package/undergoes.py` | Procedure relationships | `/undergoes/*` |
| `package/common.py` | Common utilities | `/common/*` |

## 🔑 Authentication & User Management

### Login

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "token": "jwt_token_string",
  "user": {
    "user_id": 1,
    "username": "admin",
    "role": "admin",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### User Registration

**POST** `/auth/register`

Register a new user account.

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "string",
  "firstName": "string",
  "lastName": "string",
  "phoneNumber": "string" // optional
}
```

### Get User Profile

**GET** `/auth/profile`

Get current user's profile information.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
{
  "user_id": 1,
  "username": "admin",
  "email": "admin@hospital.com",
  "role": "admin",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Change Password

**POST** `/auth/change-password`

Change user's password.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "current_password": "string",
  "new_password": "string"
}
```

### Get All Users

**GET** `/users`

Get list of all users (Admin only).

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "user_id": 1,
    "username": "admin",
    "email": "admin@hospital.com",
    "role": "admin",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create User

**POST** `/users`

Create a new user (Admin only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string", // optional
  "entity_id": "integer" // optional
}
```

### Get User by ID

**GET** `/users/<user_id>`

Get specific user details (Admin only).

### Update User

**PUT** `/users/<user_id>`

Update user information (Admin only).

### Delete User

**DELETE** `/users/<user_id>`

Delete user account (Admin only).

## 👥 Patient Management

### Get All Patients

**GET** `/patient` or `/patients`

Retrieve all patients.

**Response:**

```json
[
  {
    "pat_id": 1,
    "pat_first_name": "Jane",
    "pat_last_name": "Doe",
    "pat_insurance_no": "INS123456",
    "pat_ph_no": "+1234567890",
    "pat_address": "123 Main St, City, State",
    "pat_date": "2024-01-01T00:00:00Z"
  }
]
```

### Create Patient

**POST** `/patient` or `/patients`

Add a new patient.

**Request Body:**

```json
{
  "pat_first_name": "string",
  "pat_last_name": "string",
  "pat_insurance_no": "string",
  "pat_ph_no": "string",
  "pat_address": "string"
}
```

### Get Patient by ID

**GET** `/patient/<id>` or `/patients/<id>`

Get specific patient details.

### Delete Patient

**DELETE** `/patient/<id>` or `/patients/<id>`

Delete patient record.

## 👨‍⚕️ Doctor Management

### Get All Doctors

**GET** `/doctor`

Retrieve all doctors.

**Response:**

```json
[
  {
    "doc_id": 1,
    "doc_first_name": "Dr. John",
    "doc_last_name": "Smith",
    "doc_specialization": "Cardiology",
    "doc_ph_no": "+1234567890",
    "doc_address": "Hospital Address"
  }
]
```

### Create Doctor

**POST** `/doctor`

Add a new doctor.

### Get Doctor by ID

**GET** `/doctor/<id>`

Get specific doctor details.

### Update Doctor

**PUT** `/doctor/<id>`

Update doctor information.

### Delete Doctor

**DELETE** `/doctor/<id>`

Delete doctor record.

## 👩‍⚕️ Nurse Management

### Get All Nurses

**GET** `/nurse`

Retrieve all nurses.

### Create Nurse

**POST** `/nurse`

Add a new nurse.

### Get Nurse by ID

**GET** `/nurse/<id>`

Get specific nurse details.

### Update Nurse

**PUT** `/nurse/<id>`

Update nurse information.

### Delete Nurse

**DELETE** `/nurse/<id>`

Delete nurse record.

## 📋 Health Records Management

### Get All Health Records

**GET** `/health-records`

Retrieve all health records.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "record_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "record_type": "consultation",
    "diagnosis": "Hypertension",
    "treatment": "Medication prescribed",
    "notes": "Patient responding well",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create Health Record

**POST** `/health-records`

Create a new health record.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "patient_id": 1,
  "record_type": "string",
  "diagnosis": "string",
  "treatment": "string",
  "notes": "string"
}
```

### Get Health Record by ID

**GET** `/health-records/<record_id>`

Get specific health record.

### Update Health Record

**PUT** `/health-records/<record_id>`

Update health record.

### Delete Health Record

**DELETE** `/health-records/<record_id>`

Delete health record.

### Get Vital Signs

**GET** `/vital-signs`

Retrieve vital signs records.

**Response:**

```json
[
  {
    "vital_id": 1,
    "patient_id": 1,
    "temperature": 98.6,
    "blood_pressure_systolic": 120,
    "blood_pressure_diastolic": 80,
    "heart_rate": 72,
    "respiratory_rate": 16,
    "oxygen_saturation": 98,
    "recorded_by": 1,
    "recorded_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create Vital Signs

**POST** `/vital-signs`

Record new vital signs.

**Request Body:**

```json
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

## 🧪 Lab Tests Management

### Get All Lab Tests

**GET** `/lab-tests`

Retrieve all lab tests.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "test_id": 1,
    "patient_id": 1,
    "test_type": "Blood Test",
    "test_name": "Complete Blood Count",
    "status": "completed",
    "ordered_by": 1,
    "ordered_date": "2024-01-01T00:00:00Z",
    "completed_date": "2024-01-01T12:00:00Z",
    "results": "Normal values",
    "notes": "All parameters within normal range"
  }
]
```

### Create Lab Test

**POST** `/lab-tests`

Order a new lab test.

**Request Body:**

```json
{
  "patient_id": 1,
  "test_type": "string",
  "test_name": "string",
  "priority": "normal|urgent|stat",
  "instructions": "string"
}
```

### Get Lab Test by ID

**GET** `/lab-tests/<test_id>`

Get specific lab test details.

### Update Lab Test

**PUT** `/lab-tests/<test_id>`

Update lab test (typically to add results).

**Request Body:**

```json
{
  "status": "completed",
  "results": "string",
  "notes": "string"
}
```

### Get Lab Tests by Patient

**GET** `/lab-tests/patient/<patient_id>`

Get all lab tests for a specific patient.

### Get Pending Lab Tests

**GET** `/lab-tests/pending`

Get all pending lab tests.

## 💊 Prescriptions Management

### Get All Prescriptions

**GET** `/prescriptions`

Retrieve all prescriptions.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "prescription_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "medication_name": "Lisinopril",
    "dosage": "10mg",
    "frequency": "Once daily",
    "duration": "30 days",
    "instructions": "Take with food",
    "status": "active",
    "prescribed_date": "2024-01-01T00:00:00Z",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
]
```

### Create Prescription

**POST** `/prescriptions`

Create a new prescription.

**Request Body:**

```json
{
  "patient_id": 1,
  "medication_name": "string",
  "dosage": "string",
  "frequency": "string",
  "duration": "string",
  "instructions": "string",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```

### Get Prescription by ID

**GET** `/prescriptions/<prescription_id>`

Get specific prescription details.

### Update Prescription

**PUT** `/prescriptions/<prescription_id>`

Update prescription information.

### Delete Prescription

**DELETE** `/prescriptions/<prescription_id>`

Cancel/delete prescription.

### Medication Dispensing

**POST** `/medication-dispensing`

Record medication dispensing.

**Request Body:**

```json
{
  "prescription_id": 1,
  "quantity_dispensed": 30,
  "dispensed_by": 1,
  "notes": "string"
}
```

**GET** `/medication-dispensing`

Get dispensing records.

## 📝 Medical Notes Management

### Get All Medical Notes

**GET** `/medical-notes`

Retrieve all medical notes.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "note_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "note_type": "consultation",
    "title": "Follow-up Visit",
    "content": "Patient shows improvement...",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create Medical Note

**POST** `/medical-notes`

Create a new medical note.

**Request Body:**

```json
{
  "patient_id": 1,
  "note_type": "string",
  "title": "string",
  "content": "string"
}
```

### Get Medical Note by ID

**GET** `/medical-notes/<note_id>`

Get specific medical note.

### Update Medical Note

**PUT** `/medical-notes/<note_id>`

Update medical note.

### Delete Medical Note

**DELETE** `/medical-notes/<note_id>`

Delete medical note.

### Get All Nursing Notes

**GET** `/nursing-notes`

Retrieve all nursing notes.

**Response:**

```json
[
  {
    "note_id": 1,
    "patient_id": 1,
    "nurse_id": 1,
    "note_type": "assessment",
    "content": "Patient vital signs stable...",
    "shift": "day",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create Nursing Note

**POST** `/nursing-notes`

Create a new nursing note.

### Get Patient Assignments

**GET** `/patient-assignments`

Get nurse-patient assignments.

**Response:**

```json
[
  {
    "assignment_id": 1,
    "nurse_id": 1,
    "patient_id": 1,
    "assigned_date": "2024-01-01",
    "shift": "day",
    "status": "active"
  }
]
```

## 📅 Appointments Management

### Get All Appointments

**GET** `/appointment` or `/appointments`

Retrieve all appointments.

**Response:**

```json
[
  {
    "appointment_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_date": "2024-01-01",
    "appointment_time": "10:00:00",
    "status": "scheduled",
    "reason": "Regular checkup",
    "notes": "Annual physical examination"
  }
]
```

### Create Appointment

**POST** `/appointment` or `/appointments`

Schedule a new appointment.

**Request Body:**

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "YYYY-MM-DD",
  "appointment_time": "HH:MM:SS",
  "reason": "string",
  "notes": "string"
}
```

### Get Appointment by ID

**GET** `/appointment/<id>` or `/appointments/<id>`

Get specific appointment details.

### Update Appointment

**PUT** `/appointment/<id>` or `/appointments/<id>`

Update appointment information.

### Delete Appointment

**DELETE** `/appointment/<id>` or `/appointments/<id>`

Cancel appointment.

## 🏢 Department Management

### Get All Departments

**GET** `/department`

Retrieve all departments.

**Response:**

```json
[
  {
    "department_id": 1,
    "name": "Cardiology",
    "head_id": 1,
    "doc_first_name": "Dr. John",
    "doc_last_name": "Smith"
  }
]
```

### Create Department

**POST** `/department`

Create a new department.

### Get Department by ID

**GET** `/department/<department_id>`

Get specific department details.

### Update Department

**PUT** `/department/<department_id>`

Update department information.

### Delete Department

**DELETE** `/department/<department_id>`

Delete department.

## 💊 Medication Management

### Get All Medications

**GET** `/medication`

Retrieve medication catalog.

**Response:**

```json
[
  {
    "code": 1,
    "name": "Aspirin",
    "description": "Pain reliever and anti-inflammatory",
    "dosage_form": "tablet",
    "strength": "325mg",
    "manufacturer": "Generic Pharma"
  }
]
```

### Create Medication

**POST** `/medication`

Add new medication to catalog.

### Get Medication by Code

**GET** `/medication/<code>`

Get specific medication details.

### Update Medication

**PUT** `/medication/<code>`

Update medication information.

### Delete Medication

**DELETE** `/medication/<code>`

Remove medication from catalog.

## 🏠 Room Management

### Get All Rooms

**GET** `/room`

Retrieve all rooms.

**Response:**

```json
[
  {
    "room_no": 101,
    "room_type": "private",
    "capacity": 1,
    "status": "available",
    "floor": 1,
    "department_id": 1
  }
]
```

### Create Room

**POST** `/room`

Add a new room.

### Get Room by Number

**GET** `/room/<room_no>`

Get specific room details.

### Update Room

**PUT** `/room/<room_no>`

Update room information.

### Delete Room

**DELETE** `/room/<room_no>`

Remove room.

## 🔬 Procedures Management

### Get All Procedures

**GET** `/procedure`

Retrieve all medical procedures.

**Response:**

```json
[
  {
    "code": 1,
    "name": "Blood Pressure Check",
    "description": "Routine blood pressure measurement",
    "category": "diagnostic",
    "duration": 15,
    "cost": 25.00
  }
]
```

### Create Procedure

**POST** `/procedure`

Add a new procedure.

### Get Procedure by Code

**GET** `/procedure/<code>`

Get specific procedure details.

### Update Procedure

**PUT** `/procedure/<code>`

Update procedure information.

### Delete Procedure

**DELETE** `/procedure/<code>`

Remove procedure.

## 🔗 Relationship Management

### Prescribes Relationship

**GET** `/prescribes`

Get doctor-patient prescription relationships.

**POST** `/prescribes`

Create prescription relationship.

### Undergoes Relationship

**GET** `/undergoes`

Get patient-procedure relationships.

**POST** `/undergoes`

Create procedure relationship.

## 🛠️ Common Utilities

### Get Common Data

**GET** `/common`

Retrieve common system data and utilities.

## ❌ Error Handling

The API uses standard HTTP status codes and returns error responses in JSON format.

### Error Response Format

```json
{
  "error": "Error message description",
  "code": "ERROR_CODE",
  "details": "Additional error details"
}
```

### Common HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

### Authentication Errors

- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - Valid token but insufficient permissions

### Validation Errors

- `400 Bad Request` - Missing required fields
- `422 Unprocessable Entity` - Invalid data format

## 📋 Response Formats

### Success Response

```json
{
  "data": [...],
  "message": "Success message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Error Response

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Pagination (where applicable)

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

## 🔐 Security Considerations

1. **JWT Tokens**: All tokens expire after 24 hours
2. **Role-Based Access**: Endpoints enforce role-based permissions
3. **Input Validation**: All inputs are validated and sanitized
4. **SQL Injection Protection**: Parameterized queries used throughout
5. **Password Security**: Passwords are hashed using secure algorithms

## 📝 API Testing

### Using cURL

```bash
# Login
curl -X POST http://127.0.0.1:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Get patients (with token)
curl -X GET http://127.0.0.1:5001/patients \
  -H "Authorization: Bearer <your_jwt_token>"
```

### Using Python requests

```python
import requests

# Login
response = requests.post('http://127.0.0.1:5001/auth/login',
                        json={'username': 'admin', 'password': 'admin123'})
token = response.json()['token']

# Get patients
headers = {'Authorization': f'Bearer {token}'}
patients = requests.get('http://127.0.0.1:5001/patients', headers=headers)
```

## 📚 Additional Resources

- **Database Schema**: See `database/schema.sql`
- **Configuration**: See `config.json`
- **Testing**: See `tests/` directory
- **Frontend Integration**: See `static/` directory

---

**Last Updated**: 2024-06-25
**API Version**: 1.0
**Documentation Version**: 1.0
