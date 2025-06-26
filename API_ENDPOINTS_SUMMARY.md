# 🏥 API Endpoints Summary - Administrative Health Record Management System

## 📋 Complete API Endpoints List

### 🔐 Authentication & User Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | User login | No |
| POST | `/auth/register` | User registration | No |
| GET | `/auth/profile` | Get user profile | Yes |
| POST | `/auth/change-password` | Change password | Yes |
| GET | `/users` | Get all users | Yes (Admin) |
| POST | `/users` | Create user | Yes (Admin) |
| GET | `/users/<user_id>` | Get user by ID | Yes (Admin) |
| PUT | `/users/<user_id>` | Update user | Yes (Admin) |
| DELETE | `/users/<user_id>` | Delete user | Yes (Admin) |

### 👥 Patient Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/patient` or `/patients` | Get all patients | Yes |
| POST | `/patient` or `/patients` | Create patient | Yes |
| GET | `/patient/<id>` or `/patients/<id>` | Get patient by ID | Yes |
| PUT | `/patient/<id>` or `/patients/<id>` | Update patient | Yes |
| DELETE | `/patient/<id>` or `/patients/<id>` | Delete patient | Yes |

### 👨‍⚕️ Doctor Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/doctor` | Get all doctors | Yes |
| POST | `/doctor` | Create doctor | Yes |
| GET | `/doctor/<id>` | Get doctor by ID | Yes |
| PUT | `/doctor/<id>` | Update doctor | Yes |
| DELETE | `/doctor/<id>` | Delete doctor | Yes |

### 👩‍⚕️ Nurse Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/nurse` | Get all nurses | Yes |
| POST | `/nurse` | Create nurse | Yes |
| GET | `/nurse/<id>` | Get nurse by ID | Yes |
| PUT | `/nurse/<id>` | Update nurse | Yes |
| DELETE | `/nurse/<id>` | Delete nurse | Yes |

### 📋 Health Records Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health-records` | Get all health records | Yes |
| POST | `/health-records` | Create health record | Yes |
| GET | `/health-records/<record_id>` | Get health record by ID | Yes |
| PUT | `/health-records/<record_id>` | Update health record | Yes |
| DELETE | `/health-records/<record_id>` | Delete health record | Yes |
| GET | `/vital-signs` | Get vital signs | Yes |
| POST | `/vital-signs` | Record vital signs | Yes |

### 🧪 Lab Tests Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/lab-tests` | Get all lab tests | Yes |
| POST | `/lab-tests` | Create lab test | Yes |
| GET | `/lab-tests/<test_id>` | Get lab test by ID | Yes |
| PUT | `/lab-tests/<test_id>` | Update lab test | Yes |
| DELETE | `/lab-tests/<test_id>` | Delete lab test | Yes |
| GET | `/lab-tests/patient/<patient_id>` | Get lab tests by patient | Yes |
| GET | `/lab-tests/pending` | Get pending lab tests | Yes |

### 💊 Prescriptions Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/prescriptions` | Get all prescriptions | Yes |
| POST | `/prescriptions` | Create prescription | Yes |
| GET | `/prescriptions/<prescription_id>` | Get prescription by ID | Yes |
| PUT | `/prescriptions/<prescription_id>` | Update prescription | Yes |
| DELETE | `/prescriptions/<prescription_id>` | Delete prescription | Yes |
| GET | `/medication-dispensing` | Get dispensing records | Yes |
| POST | `/medication-dispensing` | Record dispensing | Yes |

### 📝 Medical Notes Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/medical-notes` | Get all medical notes | Yes |
| POST | `/medical-notes` | Create medical note | Yes |
| GET | `/medical-notes/<note_id>` | Get medical note by ID | Yes |
| PUT | `/medical-notes/<note_id>` | Update medical note | Yes |
| DELETE | `/medical-notes/<note_id>` | Delete medical note | Yes |
| GET | `/nursing-notes` | Get all nursing notes | Yes |
| POST | `/nursing-notes` | Create nursing note | Yes |
| GET | `/patient-assignments` | Get patient assignments | Yes |
| POST | `/patient-assignments` | Create assignment | Yes |

### 📅 Appointments Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/appointment` or `/appointments` | Get all appointments | Yes |
| POST | `/appointment` or `/appointments` | Create appointment | Yes |
| GET | `/appointment/<id>` or `/appointments/<id>` | Get appointment by ID | Yes |
| PUT | `/appointment/<id>` or `/appointments/<id>` | Update appointment | Yes |
| DELETE | `/appointment/<id>` or `/appointments/<id>` | Delete appointment | Yes |

### 🏢 Department Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/department` | Get all departments | Yes |
| POST | `/department` | Create department | Yes |
| GET | `/department/<department_id>` | Get department by ID | Yes |
| PUT | `/department/<department_id>` | Update department | Yes |
| DELETE | `/department/<department_id>` | Delete department | Yes |

### 💊 Medication Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/medication` | Get all medications | Yes |
| POST | `/medication` | Create medication | Yes |
| GET | `/medication/<code>` | Get medication by code | Yes |
| PUT | `/medication/<code>` | Update medication | Yes |
| DELETE | `/medication/<code>` | Delete medication | Yes |

### 🏠 Room Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/room` | Get all rooms | Yes |
| POST | `/room` | Create room | Yes |
| GET | `/room/<room_no>` | Get room by number | Yes |
| PUT | `/room/<room_no>` | Update room | Yes |
| DELETE | `/room/<room_no>` | Delete room | Yes |

### 🔬 Procedures Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/procedure` | Get all procedures | Yes |
| POST | `/procedure` | Create procedure | Yes |
| GET | `/procedure/<code>` | Get procedure by code | Yes |
| PUT | `/procedure/<code>` | Update procedure | Yes |
| DELETE | `/procedure/<code>` | Delete procedure | Yes |

### 🔗 Relationship Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/prescribes` | Get prescription relationships | Yes |
| POST | `/prescribes` | Create prescription relationship | Yes |
| GET | `/undergoes` | Get procedure relationships | Yes |
| POST | `/undergoes` | Create procedure relationship | Yes |

### 🛠️ Common Utilities
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/common` | Get common system data | Yes |

## 📁 API Files and Their Endpoints

### Core Application Files
- **`app.py`** - Main Flask application with route mappings
- **`package/auth.py`** - Authentication utilities and JWT handling

### API Resource Files
1. **`package/user_management.py`**
   - `/auth/login`, `/auth/register`, `/auth/profile`, `/auth/change-password`
   - `/users`, `/users/<user_id>`

2. **`package/patient.py`**
   - `/patient`, `/patients`, `/patient/<id>`, `/patients/<id>`

3. **`package/doctor.py`**
   - `/doctor`, `/doctor/<id>`

4. **`package/nurse.py`**
   - `/nurse`, `/nurse/<id>`

5. **`package/health_records.py`**
   - `/health-records`, `/health-records/<record_id>`, `/vital-signs`

6. **`package/lab_results.py`**
   - `/lab-tests`, `/lab-tests/<test_id>`, `/lab-tests/patient/<patient_id>`, `/lab-tests/pending`

7. **`package/prescriptions_enhanced.py`**
   - `/prescriptions`, `/prescriptions/<prescription_id>`, `/medication-dispensing`

8. **`package/medical_notes.py`**
   - `/medical-notes`, `/medical-notes/<note_id>`, `/nursing-notes`, `/patient-assignments`

9. **`package/appointment.py`**
   - `/appointment`, `/appointments`, `/appointment/<id>`, `/appointments/<id>`

10. **`package/department.py`**
    - `/department`, `/department/<department_id>`

11. **`package/medication.py`**
    - `/medication`, `/medication/<code>`

12. **`package/room.py`**
    - `/room`, `/room/<room_no>`

13. **`package/procedure.py`**
    - `/procedure`, `/procedure/<code>`

14. **`package/prescribes.py`**
    - `/prescribes`

15. **`package/undergoes.py`**
    - `/undergoes`

16. **`package/common.py`**
    - `/common`

## 🔐 Authentication Requirements

### Public Endpoints (No Authentication Required)
- `POST /auth/login`
- `POST /auth/register`

### Protected Endpoints (JWT Token Required)
- All other endpoints require valid JWT token in Authorization header
- Format: `Authorization: Bearer <jwt_token>`

### Role-Based Access Control
- **Admin**: Full access to all endpoints
- **Doctor**: Patient care, health records, prescriptions, lab tests
- **Nurse**: Patient care, vital signs, nursing notes
- **Lab Technician**: Lab test management
- **Pharmacist**: Prescription and medication management
- **Patient**: Personal health records access only

## 📊 Total API Count
- **Total Endpoints**: 85+
- **Authentication Endpoints**: 5
- **Patient Management**: 5
- **Doctor Management**: 5
- **Nurse Management**: 5
- **Health Records**: 7
- **Lab Tests**: 7
- **Prescriptions**: 7
- **Medical Notes**: 8
- **Appointments**: 5
- **Departments**: 5
- **Medications**: 5
- **Rooms**: 5
- **Procedures**: 5
- **Relationships**: 4
- **Utilities**: 1

---
**Generated**: 2024-06-25  
**System**: Administrative Health Record Management System  
**API Version**: 1.0
