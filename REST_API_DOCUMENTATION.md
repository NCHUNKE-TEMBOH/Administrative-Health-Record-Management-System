# 🏥 REST API Documentation - Administrative Health Record Management System

## 📋 Base Information

- **Base URL**: `http://127.0.0.1:5001`
- **Content-Type**: `application/json`
- **Authentication**: JWT Bearer Token (except login/register)

## 🔐 Authentication APIs

### 1. User Login

**Endpoint**: `POST /auth/login`
**Description**: Authenticate user and get JWT token
**Authentication**: None required

**Request:**

```http
POST http://127.0.0.1:5001/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "user_id": 1,
    "username": "admin",
    "role": "admin",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Error Response (401 Unauthorized):**

```json
{
  "error": "Invalid username or password"
}
```

### 2. User Registration

**Endpoint**: `POST /auth/register`
**Description**: Register a new user account
**Authentication**: None required

**Request:**

```http
POST http://127.0.0.1:5001/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@hospital.com",
  "password": "secure123",
  "role": "patient",
  "firstName": "Jane",
  "lastName": "Smith",
  "phoneNumber": "+1234567890"
}
```

**Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user_id": 15
}
```

### 3. Get User Profile

**Endpoint**: `GET /auth/profile`
**Description**: Get current user's profile
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/auth/profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

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

### 4. Change Password

**Endpoint**: `POST /auth/change-password`
**Description**: Change user's password
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/auth/change-password
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "current_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

**Response (200 OK):**

```json
{
  "message": "Password changed successfully"
}
```

## 👤 User Management APIs

### 5. Get All Users

**Endpoint**: `GET /users`
**Description**: Get list of all users (Admin only)
**Authentication**: Required (Admin role)

**Request:**

```http
GET http://127.0.0.1:5001/users
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
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
  },
  {
    "user_id": 2,
    "username": "doctor1",
    "email": "doctor@hospital.com",
    "role": "doctor",
    "first_name": "Dr. Jane",
    "last_name": "Smith",
    "phone_number": "+1234567891",
    "is_active": true,
    "created_at": "2024-01-02T00:00:00Z"
  }
]
```

### 6. Create User

**Endpoint**: `POST /users`
**Description**: Create a new user (Admin only)
**Authentication**: Required (Admin role)

**Request:**

```http
POST http://127.0.0.1:5001/users
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "username": "newdoctor",
  "email": "newdoctor@hospital.com",
  "password": "secure123",
  "role": "doctor",
  "first_name": "Dr. Michael",
  "last_name": "Johnson",
  "phone_number": "+1234567892",
  "entity_id": 5
}
```

**Response (201 Created):**

```json
{
  "message": "User created successfully",
  "user_id": 16
}
```

### 7. Get User by ID

**Endpoint**: `GET /users/{user_id}`
**Description**: Get specific user details (Admin only)
**Authentication**: Required (Admin role)

**Request:**

```http
GET http://127.0.0.1:5001/users/2
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "user_id": 2,
  "username": "doctor1",
  "email": "doctor@hospital.com",
  "role": "doctor",
  "first_name": "Dr. Jane",
  "last_name": "Smith",
  "phone_number": "+1234567891",
  "is_active": true,
  "entity_id": 1,
  "created_at": "2024-01-02T00:00:00Z"
}
```

### 8. Update User

**Endpoint**: `PUT /users/{user_id}`
**Description**: Update user information (Admin only)
**Authentication**: Required (Admin role)

**Request:**

```http
PUT http://127.0.0.1:5001/users/2
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "email": "updated.doctor@hospital.com",
  "phone_number": "+1234567899",
  "is_active": true
}
```

**Response (200 OK):**

```json
{
  "message": "User updated successfully"
}
```

### 9. Delete User

**Endpoint**: `DELETE /users/{user_id}`
**Description**: Delete user account (Admin only)
**Authentication**: Required (Admin role)

**Request:**

```http
DELETE http://127.0.0.1:5001/users/2
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "message": "User deleted successfully"
}
```

## 👥 Patient Management APIs

### 10. Get All Patients

**Endpoint**: `GET /patients`
**Description**: Retrieve all patients
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/patients
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

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
  },
  {
    "pat_id": 2,
    "pat_first_name": "John",
    "pat_last_name": "Smith",
    "pat_insurance_no": "INS789012",
    "pat_ph_no": "+1234567891",
    "pat_address": "456 Oak Ave, City, State",
    "pat_date": "2024-01-02T00:00:00Z"
  }
]
```

### 11. Create Patient

**Endpoint**: `POST /patients`
**Description**: Add a new patient
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/patients
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "pat_first_name": "Robert",
  "pat_last_name": "Johnson",
  "pat_insurance_no": "INS345678",
  "pat_ph_no": "+1234567892",
  "pat_address": "789 Pine St, City, State"
}
```

**Response (201 Created):**

```json
{
  "pat_id": 3,
  "pat_first_name": "Robert",
  "pat_last_name": "Johnson",
  "pat_insurance_no": "INS345678",
  "pat_ph_no": "+1234567892",
  "pat_address": "789 Pine St, City, State"
}
```

### 12. Get Patient by ID

**Endpoint**: `GET /patients/{patient_id}`
**Description**: Get specific patient details
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/patients/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

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

### 13. Update Patient

**Endpoint**: `PUT /patients/{patient_id}`
**Description**: Update patient information
**Authentication**: Required

**Request:**

```http
PUT http://127.0.0.1:5001/patients/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "pat_first_name": "Jane",
  "pat_last_name": "Doe-Smith",
  "pat_insurance_no": "INS123456",
  "pat_ph_no": "+1234567890",
  "pat_address": "123 Main St, Apt 2B, City, State"
}
```

**Response (200 OK):**

```json
{
  "message": "Patient updated successfully"
}
```

### 14. Delete Patient

**Endpoint**: `DELETE /patients/{patient_id}`
**Description**: Delete patient record
**Authentication**: Required

**Request:**

```http
DELETE http://127.0.0.1:5001/patients/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "msg": "sucessfully deleted"
}
```

## 👨‍⚕️ Doctor Management APIs

### 15. Get All Doctors

**Endpoint**: `GET /doctor`
**Description**: Retrieve all doctors
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/doctor
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "doc_id": 1,
    "doc_first_name": "Dr. John",
    "doc_last_name": "Smith",
    "doc_specialization": "Cardiology",
    "doc_ph_no": "+1234567890",
    "doc_address": "Hospital Address"
  },
  {
    "doc_id": 2,
    "doc_first_name": "Dr. Sarah",
    "doc_last_name": "Johnson",
    "doc_specialization": "Neurology",
    "doc_ph_no": "+1234567891",
    "doc_address": "Hospital Address"
  }
]
```

### 16. Create Doctor

**Endpoint**: `POST /doctor`
**Description**: Add a new doctor
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/doctor
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "doc_first_name": "Dr. Michael",
  "doc_last_name": "Brown",
  "doc_specialization": "Emergency Medicine",
  "doc_ph_no": "+1234567892",
  "doc_address": "Emergency Department, Main Hospital"
}
```

**Response (201 Created):**

```json
{
  "doc_id": 3,
  "doc_first_name": "Dr. Michael",
  "doc_last_name": "Brown",
  "doc_specialization": "Emergency Medicine",
  "doc_ph_no": "+1234567892",
  "doc_address": "Emergency Department, Main Hospital"
}
```

### 17. Get Doctor by ID

**Endpoint**: `GET /doctor/{doctor_id}`
**Description**: Get specific doctor details
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/doctor/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

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

### 18. Update Doctor

**Endpoint**: `PUT /doctor/{doctor_id}`
**Description**: Update doctor information
**Authentication**: Required

**Request:**

```http
PUT http://127.0.0.1:5001/doctor/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "doc_first_name": "Dr. John",
  "doc_last_name": "Smith",
  "doc_specialization": "Interventional Cardiology",
  "doc_ph_no": "+1234567890",
  "doc_address": "Cardiology Department, Main Hospital"
}
```

**Response (200 OK):**

```json
{
  "message": "Doctor updated successfully"
}
```

### 19. Delete Doctor

**Endpoint**: `DELETE /doctor/{doctor_id}`
**Description**: Delete doctor record
**Authentication**: Required

**Request:**

```http
DELETE http://127.0.0.1:5001/doctor/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "message": "Doctor deleted successfully"
}
```

## 📋 Health Records Management APIs

### 20. Get All Health Records

**Endpoint**: `GET /health-records`
**Description**: Retrieve all health records
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/health-records
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "record_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "record_type": "consultation",
    "diagnosis": "Hypertension",
    "treatment": "Medication prescribed",
    "notes": "Patient responding well to treatment",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### 21. Create Health Record

**Endpoint**: `POST /health-records`
**Description**: Create a new health record
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/health-records
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "patient_id": 1,
  "record_type": "consultation",
  "diagnosis": "Type 2 Diabetes",
  "treatment": "Metformin 500mg twice daily",
  "notes": "Patient needs dietary counseling"
}
```

**Response (201 Created):**

```json
{
  "message": "Health record created successfully",
  "record_id": 2
}
```

### 22. Get Vital Signs

**Endpoint**: `GET /vital-signs`
**Description**: Retrieve vital signs records
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/vital-signs
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

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
    "recorded_at": "2024-01-01T08:00:00Z"
  }
]
```

### 23. Record Vital Signs

**Endpoint**: `POST /vital-signs`
**Description**: Record new vital signs
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/vital-signs
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "patient_id": 1,
  "temperature": 99.2,
  "blood_pressure_systolic": 125,
  "blood_pressure_diastolic": 82,
  "heart_rate": 75,
  "respiratory_rate": 18,
  "oxygen_saturation": 97
}
```

**Response (201 Created):**

```json
{
  "message": "Vital signs recorded successfully",
  "vital_id": 2
}
```

## 🧪 Lab Tests Management APIs

### 24. Get All Lab Tests

**Endpoint**: `GET /lab-tests`
**Description**: Retrieve all lab tests
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/lab-tests
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "test_id": 1,
    "patient_id": 1,
    "test_type": "Blood Test",
    "test_name": "Complete Blood Count",
    "status": "completed",
    "priority": "normal",
    "ordered_by": 1,
    "ordered_date": "2024-01-01T09:00:00Z",
    "completed_date": "2024-01-01T14:00:00Z",
    "results": "All values within normal range",
    "notes": "No abnormalities detected"
  }
]
```

### 25. Create Lab Test

**Endpoint**: `POST /lab-tests`
**Description**: Order a new lab test
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/lab-tests
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "patient_id": 1,
  "test_type": "Blood Test",
  "test_name": "Lipid Panel",
  "priority": "normal",
  "instructions": "Patient should fast for 12 hours"
}
```

**Response (201 Created):**

```json
{
  "message": "Lab test ordered successfully",
  "test_id": 2
}
```

### 26. Get Lab Tests by Patient

**Endpoint**: `GET /lab-tests/patient/{patient_id}`
**Description**: Get all lab tests for a specific patient
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/lab-tests/patient/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "test_id": 1,
    "patient_id": 1,
    "test_type": "Blood Test",
    "test_name": "Complete Blood Count",
    "status": "completed",
    "results": "All values within normal range"
  }
]
```

### 27. Get Pending Lab Tests

**Endpoint**: `GET /lab-tests/pending`
**Description**: Get all pending lab tests
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/lab-tests/pending
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "test_id": 2,
    "patient_id": 1,
    "test_type": "Blood Test",
    "test_name": "Lipid Panel",
    "status": "pending",
    "priority": "normal",
    "ordered_date": "2024-01-01T15:00:00Z"
  }
]
```

## 💊 Prescriptions Management APIs

### 28. Get All Prescriptions

**Endpoint**: `GET /prescriptions`
**Description**: Retrieve all prescriptions
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/prescriptions
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

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
    "prescribed_date": "2024-01-01T10:00:00Z",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
]
```

### 29. Create Prescription

**Endpoint**: `POST /prescriptions`
**Description**: Create a new prescription
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/prescriptions
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "patient_id": 1,
  "medication_name": "Metformin",
  "dosage": "500mg",
  "frequency": "Twice daily",
  "duration": "90 days",
  "instructions": "Take with meals",
  "start_date": "2024-01-01",
  "end_date": "2024-03-31"
}
```

**Response (201 Created):**

```json
{
  "message": "Prescription created successfully",
  "prescription_id": 2
}
```

### 30. Get Prescription by ID

**Endpoint**: `GET /prescriptions/{prescription_id}`
**Description**: Get specific prescription details
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/prescriptions/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
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
  "prescribed_date": "2024-01-01T10:00:00Z"
}
```

### 31. Record Medication Dispensing

**Endpoint**: `POST /medication-dispensing`
**Description**: Record medication dispensing
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/medication-dispensing
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "prescription_id": 1,
  "quantity_dispensed": 30,
  "dispensed_by": 1,
  "notes": "Patient counseled on proper usage"
}
```

**Response (201 Created):**

```json
{
  "message": "Medication dispensing recorded successfully",
  "dispensing_id": 1
}
```

## 📅 Appointments Management APIs

### 32. Get All Appointments

**Endpoint**: `GET /appointments`
**Description**: Retrieve all appointments
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/appointments
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "appointment_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_date": "2024-01-15",
    "appointment_time": "10:00:00",
    "status": "scheduled",
    "reason": "Regular checkup",
    "notes": "Annual physical examination",
    "created_at": "2024-01-01T09:00:00Z"
  }
]
```

### 33. Create Appointment

**Endpoint**: `POST /appointments`
**Description**: Schedule a new appointment
**Authentication**: Required

**Request:**

```http
POST http://127.0.0.1:5001/appointments
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-01-20",
  "appointment_time": "14:30:00",
  "reason": "Follow-up visit",
  "notes": "Check blood pressure medication effectiveness"
}
```

**Response (201 Created):**

```json
{
  "message": "Appointment scheduled successfully",
  "appointment_id": 2
}
```

### 34. Get Appointment by ID

**Endpoint**: `GET /appointments/{appointment_id}`
**Description**: Get specific appointment details
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/appointments/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "appointment_id": 1,
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-01-15",
  "appointment_time": "10:00:00",
  "status": "scheduled",
  "reason": "Regular checkup",
  "notes": "Annual physical examination"
}
```

### 35. Update Appointment

**Endpoint**: `PUT /appointments/{appointment_id}`
**Description**: Update appointment information
**Authentication**: Required

**Request:**

```http
PUT http://127.0.0.1:5001/appointments/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "appointment_date": "2024-01-16",
  "appointment_time": "11:00:00",
  "status": "rescheduled",
  "notes": "Patient requested time change"
}
```

**Response (200 OK):**

```json
{
  "message": "Appointment updated successfully"
}
```

## 🏢 Department Management APIs

### 36. Get All Departments

**Endpoint**: `GET /department`
**Description**: Retrieve all departments
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/department
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "department_id": 1,
    "name": "Cardiology",
    "head_id": 1,
    "doc_first_name": "Dr. John",
    "doc_last_name": "Smith"
  },
  {
    "department_id": 2,
    "name": "Neurology",
    "head_id": 2,
    "doc_first_name": "Dr. Sarah",
    "doc_last_name": "Johnson"
  }
]
```

## 💊 Medication Management APIs

### 37. Get All Medications

**Endpoint**: `GET /medication`
**Description**: Retrieve medication catalog
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/medication
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
[
  {
    "code": 1,
    "name": "Aspirin",
    "description": "Pain reliever and anti-inflammatory",
    "dosage_form": "tablet",
    "strength": "325mg",
    "manufacturer": "Generic Pharma"
  },
  {
    "code": 2,
    "name": "Ibuprofen",
    "description": "Nonsteroidal anti-inflammatory drug",
    "dosage_form": "tablet",
    "strength": "200mg",
    "manufacturer": "Generic Pharma"
  }
]
```

### 38. Get Medication by Code

**Endpoint**: `GET /medication/{code}`
**Description**: Get specific medication details
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/medication/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "code": 1,
  "name": "Aspirin",
  "description": "Pain reliever and anti-inflammatory",
  "dosage_form": "tablet",
  "strength": "325mg",
  "manufacturer": "Generic Pharma"
}
```

## 🛠️ Common Utilities APIs

### 39. Get Common Data

**Endpoint**: `GET /common`
**Description**: Retrieve common system data
**Authentication**: Required

**Request:**

```http
GET http://127.0.0.1:5001/common
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**

```json
{
  "message": "Common API endpoint working",
  "timestamp": "2024-01-01T12:00:00Z",
  "system_status": "operational"
}
```

## ❌ Error Responses

### 400 Bad Request

```json
{
  "error": "Missing required field: patient_id",
  "code": "VALIDATION_ERROR"
}
```

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
  "error": "Insufficient permissions for this operation",
  "code": "FORBIDDEN"
}
```

### 404 Not Found

```json
{
  "error": "Patient not found",
  "code": "NOT_FOUND"
}
```

### 409 Conflict

```json
{
  "error": "Username already exists",
  "code": "CONFLICT"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "code": "INTERNAL_ERROR"
}
```

## 🔧 Testing Examples

### Using cURL

#### 1. Login and Get Token

```bash
curl -X POST http://127.0.0.1:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 2. Create Patient

```bash
curl -X POST http://127.0.0.1:5001/patients \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pat_first_name": "John",
    "pat_last_name": "Doe",
    "pat_insurance_no": "INS123456",
    "pat_ph_no": "+1234567890",
    "pat_address": "123 Main St"
  }'
```

#### 3. Get All Patients

```bash
curl -X GET http://127.0.0.1:5001/patients \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using Python requests

```python
import requests

# Base URL
BASE_URL = "http://127.0.0.1:5001"

# 1. Login
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
token = login_response.json()["token"]

# 2. Set headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 3. Create patient
patient_data = {
    "pat_first_name": "Jane",
    "pat_last_name": "Smith",
    "pat_insurance_no": "INS789012",
    "pat_ph_no": "+1234567891",
    "pat_address": "456 Oak Ave"
}
create_response = requests.post(f"{BASE_URL}/patients",
                               json=patient_data, headers=headers)

# 4. Get all patients
patients_response = requests.get(f"{BASE_URL}/patients", headers=headers)
patients = patients_response.json()
```

## 📋 Quick Reference

### Authentication Flow

1. `POST /auth/login` → Get JWT token
2. Include token in all subsequent requests: `Authorization: Bearer <token>`
3. Token expires after 24 hours

### Common HTTP Methods

- **GET**: Retrieve data
- **POST**: Create new resource
- **PUT**: Update existing resource
- **DELETE**: Remove resource

### Required Headers

- **Content-Type**: `application/json` (for POST/PUT requests)
- **Authorization**: `Bearer <jwt_token>` (for protected endpoints)

---

**Documentation Version**: 1.0
**Last Updated**: 2024-06-25
**Total Endpoints Documented**: 39
**Base URL**: <http://127.0.0.1:5001>
