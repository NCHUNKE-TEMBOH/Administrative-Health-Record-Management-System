# 📁 API Files Inventory - Administrative Health Record Management System

## 🏗️ Core Application Files

### 1. **`app.py`** - Main Flask Application
- **Purpose**: Main application entry point with route definitions
- **Key Components**:
  - Flask app initialization
  - API resource registration
  - Route mappings
  - Static file serving
- **API Routes Defined**: All endpoint mappings
- **Dependencies**: All package modules

### 2. **`config.json`** - Configuration File
- **Purpose**: Application configuration settings
- **Contains**: Database settings, JWT secrets, server configuration

## 🔐 Authentication & Security

### 3. **`package/auth.py`** - Authentication Utilities
- **Purpose**: JWT token handling and authentication decorators
- **Key Functions**:
  - `generate_token()` - Create JWT tokens
  - `verify_token()` - Validate JWT tokens
  - `@auth_required` - Authentication decorator
  - `@role_required()` - Role-based access decorator
- **Security Features**: Password hashing, token validation, role permissions

## 👤 User Management APIs

### 4. **`package/user_management.py`** - User Management
- **API Classes**:
  - `UserLogin` - `/auth/login`
  - `UserRegistration` - `/auth/register`
  - `UserProfile` - `/auth/profile`
  - `ChangePassword` - `/auth/change-password`
  - `Users` - `/users`
  - `User` - `/users/<user_id>`
- **Features**: User CRUD, authentication, profile management

## 🏥 Healthcare Entity APIs

### 5. **`package/patient.py`** - Patient Management
- **API Classes**:
  - `Patients` - `/patient`, `/patients`
  - `Patient` - `/patient/<id>`, `/patients/<id>`
- **Operations**: Create, read, update, delete patients
- **Database Table**: `patient`

### 6. **`package/doctor.py`** - Doctor Management
- **API Classes**:
  - `Doctors` - `/doctor`
  - `Doctor` - `/doctor/<id>`
- **Operations**: Doctor CRUD operations
- **Database Table**: `doctor`

### 7. **`package/nurse.py`** - Nurse Management
- **API Classes**:
  - `Nurses` - `/nurse`
  - `Nurse` - `/nurse/<id>`
- **Operations**: Nurse CRUD operations
- **Database Table**: `nurse`

## 📋 Health Records APIs

### 8. **`package/health_records.py`** - Health Records Management
- **API Classes**:
  - `HealthRecords` - `/health-records`
  - `HealthRecord` - `/health-records/<record_id>`
  - `VitalSigns` - `/vital-signs`
- **Features**: Medical records, vital signs tracking
- **Database Tables**: `health_records`, `vital_signs`

### 9. **`package/lab_results.py`** - Lab Tests Management
- **API Classes**:
  - `LabTests` - `/lab-tests`
  - `LabTest` - `/lab-tests/<test_id>`
  - `LabTestsByPatient` - `/lab-tests/patient/<patient_id>`
  - `PendingLabTests` - `/lab-tests/pending`
- **Features**: Lab test ordering, results management
- **Database Table**: `lab_tests`

### 10. **`package/prescriptions_enhanced.py`** - Prescription Management
- **API Classes**:
  - `PrescriptionsEnhanced` - `/prescriptions`
  - `PrescriptionEnhanced` - `/prescriptions/<prescription_id>`
  - `MedicationDispensing` - `/medication-dispensing`
- **Features**: Prescription management, medication dispensing
- **Database Tables**: `prescriptions`, `medication_dispensing`

### 11. **`package/medical_notes.py`** - Medical & Nursing Notes
- **API Classes**:
  - `MedicalNotes` - `/medical-notes`
  - `MedicalNote` - `/medical-notes/<note_id>`
  - `NursingNotes` - `/nursing-notes`
  - `PatientAssignments` - `/patient-assignments`
- **Features**: Medical documentation, nursing notes, patient assignments
- **Database Tables**: `medical_notes`, `nursing_notes`, `patient_assignments`

## 📅 Scheduling & Operations APIs

### 12. **`package/appointment.py`** - Appointment Management
- **API Classes**:
  - `Appointments` - `/appointment`, `/appointments`
  - `Appointment` - `/appointment/<id>`, `/appointments/<id>`
- **Features**: Appointment scheduling, management
- **Database Table**: `appointment`

### 13. **`package/department.py`** - Department Management
- **API Classes**:
  - `Departments` - `/department`
  - `Department` - `/department/<department_id>`
- **Features**: Hospital department management
- **Database Table**: `department`

## 💊 Medication & Procedures APIs

### 14. **`package/medication.py`** - Medication Catalog
- **API Classes**:
  - `Medications` - `/medication`
  - `Medication` - `/medication/<code>`
- **Features**: Medication catalog management
- **Database Table**: `medication`

### 15. **`package/procedure.py`** - Medical Procedures
- **API Classes**:
  - `Procedures` - `/procedure`
  - `Procedure` - `/procedure/<code>`
- **Features**: Medical procedure catalog
- **Database Table**: `procedure`

## 🏠 Facility Management APIs

### 16. **`package/room.py`** - Room Management
- **API Classes**:
  - `Rooms` - `/room`
  - `Room` - `/room/<room_no>`
- **Features**: Hospital room management
- **Database Table**: `room`

## 🔗 Relationship APIs

### 17. **`package/prescribes.py`** - Prescription Relationships
- **API Classes**:
  - `Prescribes` - `/prescribes`
  - `Prescribe` - Individual prescription relationship
- **Features**: Doctor-patient prescription relationships
- **Database Table**: `prescribes`

### 18. **`package/undergoes.py`** - Procedure Relationships
- **API Classes**:
  - `Undergoess` - `/undergoes`
  - `Undergoes` - Individual procedure relationship
- **Features**: Patient-procedure relationships
- **Database Table**: `undergoes`

## 🛠️ Utility APIs

### 19. **`package/common.py`** - Common Utilities
- **API Classes**:
  - `Common` - `/common`
- **Features**: Common system utilities and data
- **Purpose**: Shared functionality across the system

### 20. **`package/model.py`** - Database Model
- **Purpose**: Database connection and model definitions
- **Features**: SQLite connection, database utilities
- **Not an API**: Backend utility module

## 📊 API Statistics

### Total Files with APIs: **16 files**
### Total API Classes: **30+ classes**
### Total Endpoints: **85+ endpoints**

### Breakdown by Category:
- **Authentication**: 5 endpoints
- **User Management**: 4 endpoints
- **Patient Management**: 5 endpoints
- **Doctor Management**: 5 endpoints
- **Nurse Management**: 5 endpoints
- **Health Records**: 7 endpoints
- **Lab Tests**: 7 endpoints
- **Prescriptions**: 7 endpoints
- **Medical Notes**: 8 endpoints
- **Appointments**: 5 endpoints
- **Departments**: 5 endpoints
- **Medications**: 5 endpoints
- **Rooms**: 5 endpoints
- **Procedures**: 5 endpoints
- **Relationships**: 4 endpoints
- **Utilities**: 1 endpoint

## 🔍 File Dependencies

### Import Structure:
```
app.py
├── package/auth.py
├── package/user_management.py
├── package/patient.py
├── package/doctor.py
├── package/nurse.py
├── package/health_records.py
├── package/lab_results.py
├── package/prescriptions_enhanced.py
├── package/medical_notes.py
├── package/appointment.py
├── package/department.py
├── package/medication.py
├── package/room.py
├── package/procedure.py
├── package/prescribes.py
├── package/undergoes.py
├── package/common.py
└── package/model.py (database connection)
```

## 📚 Documentation Files Created

1. **`API_DOCUMENTATION.md`** - Complete API documentation
2. **`API_ENDPOINTS_SUMMARY.md`** - Endpoints summary table
3. **`API_QUICK_REFERENCE.md`** - Quick reference guide
4. **`API_FILES_INVENTORY.md`** - This file (files inventory)

## 🚀 Getting Started

1. **Start Server**: `python app.py`
2. **Base URL**: `http://127.0.0.1:5001`
3. **Authentication**: Login at `/auth/login` to get JWT token
4. **Authorization**: Include `Authorization: Bearer <token>` in headers
5. **Content-Type**: Use `application/json` for requests

---
**Inventory Version**: 1.0  
**Last Updated**: 2024-06-25  
**Total API Files**: 16  
**Total Endpoints**: 85+
