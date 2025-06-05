# Health Record Management System

## Overview

This is an enhanced Hospital Management System with comprehensive Health Record Management capabilities and role-based access control. The system supports six user roles, each with specific permissions and access rights tailored to their responsibilities in a healthcare environment.

## User Roles and Access Rights

### 1. Administrator (Admin)
- **Full system access** - Can manage all aspects of the system
- **User Management** - Create, update, and deactivate user accounts
- **System Monitoring** - Access audit logs and system analytics
- **Data Management** - Full CRUD access to all patient and medical data
- **Permissions**: All operations on all resources

### 2. Doctor
- **Patient Records** - View and update comprehensive patient medical records
- **Medical Notes** - Create and manage patient medical notes and diagnoses
- **Prescriptions** - Create, update, and manage patient prescriptions
- **Lab Tests** - Request laboratory tests and review results
- **Appointments** - Manage patient appointments
- **Permissions**: Create/Read/Update access to patient data, health records, prescriptions, lab tests

### 3. Nurse
- **Assigned Patients** - Access only to patients assigned to their care
- **Vital Signs** - Record and monitor patient vital signs
- **Nursing Notes** - Document patient care, observations, and nursing interventions
- **Medication Administration** - View prescriptions and document medication administration
- **Patient Assignments** - View their current patient assignments
- **Permissions**: Limited patient access, vital signs management, nursing documentation

### 4. Lab Technician
- **Lab Tests** - Process pending laboratory test requests
- **Test Results** - Enter and update laboratory test results
- **Patient Information** - Limited access to patient information relevant to lab work
- **Quality Control** - Flag abnormal results for immediate attention
- **Permissions**: Lab test management, limited patient data access

### 5. Pharmacist
- **Prescriptions** - View and process active prescriptions
- **Medication Dispensing** - Dispense medications and update dispensing records
- **Drug Interactions** - Monitor for potential drug conflicts and interactions
- **Inventory Management** - Manage medication inventory and availability
- **Permissions**: Prescription access, medication dispensing, inventory management

### 6. Patient
- **Personal Health Records** - View their own health records and medical history
- **Prescriptions** - View current and past prescriptions
- **Appointments** - View appointment history and upcoming appointments
- **Lab Results** - Access their own laboratory test results
- **Vital Signs** - View their recorded vital signs and health metrics
- **Permissions**: Read-only access to own medical data

## Key Features

### Authentication & Security
- **JWT-based Authentication** - Secure token-based authentication system
- **Role-based Access Control (RBAC)** - Granular permissions based on user roles
- **Audit Logging** - Comprehensive logging of all user actions and data access
- **Session Management** - Secure session handling with automatic logout

### Health Records Management
- **Digital Health Records** - Comprehensive electronic health record system
- **Medical Notes** - Doctor notes with categorization (diagnosis, treatment, follow-up)
- **Nursing Notes** - Nursing observations and care documentation
- **Vital Signs Tracking** - Complete vital signs monitoring and trending
- **Lab Test Management** - Full laboratory workflow from request to results

### Enhanced Prescription System
- **Digital Prescriptions** - Electronic prescription creation and management
- **Medication Dispensing** - Pharmacy workflow with dispensing tracking
- **Drug Interaction Checking** - Safety features for medication management
- **Refill Management** - Automated refill tracking and management

### Patient Assignment System
- **Nurse-Patient Assignments** - Dynamic patient assignment system for nurses
- **Shift Management** - Support for different nursing shifts (day, evening, night)
- **Care Coordination** - Improved communication between healthcare providers

## API Endpoints

### Authentication
- `POST /auth/login` - User authentication
- `GET /auth/profile` - Get current user profile
- `PUT /auth/profile` - Update user profile
- `POST /auth/change-password` - Change user password

### User Management (Admin only)
- `GET /users` - List all users
- `POST /users` - Create new user
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Deactivate user

### Health Records
- `GET /health-records` - Get health records (filtered by patient access)
- `POST /health-records` - Create health record
- `GET /health-records/{id}` - Get specific health record
- `PUT /health-records/{id}` - Update health record
- `DELETE /health-records/{id}` - Delete health record (Admin only)

### Vital Signs
- `GET /vital-signs` - Get vital signs (filtered by patient access)
- `POST /vital-signs` - Record vital signs

### Lab Tests
- `GET /lab-tests` - Get lab tests (role-based filtering)
- `POST /lab-tests` - Request lab test (Doctor/Admin)
- `GET /lab-tests/{id}` - Get specific lab test
- `PUT /lab-tests/{id}` - Update lab test (Lab Tech/Doctor/Admin)
- `GET /lab-tests/patient/{patient_id}` - Get lab tests for patient
- `GET /lab-tests/pending` - Get pending lab tests (Lab Tech/Admin)

### Enhanced Prescriptions
- `GET /prescriptions` - Get prescriptions (role-based filtering)
- `POST /prescriptions` - Create prescription (Doctor/Admin)
- `GET /prescriptions/{id}` - Get specific prescription
- `PUT /prescriptions/{id}` - Update prescription (Doctor/Admin)

### Medication Dispensing
- `POST /medication-dispensing` - Dispense medication (Pharmacist/Admin)
- `GET /medication-dispensing` - Get dispensing records

### Medical Notes
- `GET /medical-notes` - Get medical notes (filtered by patient access)
- `POST /medical-notes` - Create medical note (Doctor/Admin)
- `GET /medical-notes/{id}` - Get specific medical note
- `PUT /medical-notes/{id}` - Update medical note (Doctor/Admin)

### Nursing Notes
- `GET /nursing-notes` - Get nursing notes (filtered by patient access)
- `POST /nursing-notes` - Create nursing note (Nurse/Admin)

### Patient Assignments
- `GET /patient-assignments` - Get patient assignments
- `POST /patient-assignments` - Create patient assignment (Admin)

## Installation and Setup

### Prerequisites
- Python 3.7+
- Flask
- Flask-RESTful
- SQLite3
- PyJWT
- Werkzeug

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install flask flask-restful pyjwt werkzeug
   ```

2. **Initialize Database**
   ```bash
   python init_users.py
   ```

3. **Start the Application**
   ```bash
   python app.py
   ```

4. **Access the System**
   - Main Application: http://127.0.0.1:5001/
   - Login Page: http://127.0.0.1:5001/login.html
   - Dashboard: http://127.0.0.1:5001/dashboard.html

## Sample Login Credentials

The `init_users.py` script creates sample users for testing:

### Admin
- Username: `admin` | Password: `admin123`

### Doctors
- Username: `dr.smith` | Password: `doctor123`
- Username: `dr.johnson` | Password: `doctor123`

### Nurses
- Username: `nurse.williams` | Password: `nurse123`
- Username: `nurse.brown` | Password: `nurse123`

### Lab Technician
- Username: `lab.tech1` | Password: `lab123`

### Pharmacist
- Username: `pharmacist1` | Password: `pharm123`

### Patients
- Username: `patient.doe` | Password: `patient123`
- Username: `patient.jones` | Password: `patient123`

## Database Schema

The system extends the original database with new tables:

- `users` - User accounts with role-based access
- `health_records` - Comprehensive patient health records
- `vital_signs` - Patient vital signs tracking
- `lab_tests` - Laboratory test management
- `medical_notes` - Doctor medical notes
- `nursing_notes` - Nursing observations and care notes
- `prescriptions` - Enhanced prescription management
- `medication_dispensing` - Pharmacy dispensing records
- `access_logs` - Audit trail for all user actions
- `patient_assignments` - Nurse-patient assignments

## Security Features

- **Password Hashing** - All passwords are securely hashed using Werkzeug
- **JWT Tokens** - Secure authentication tokens with expiration
- **Role-based Permissions** - Granular access control based on user roles
- **Audit Logging** - Complete audit trail of all system access and modifications
- **Data Isolation** - Users can only access data appropriate to their role
- **Session Security** - Automatic logout on token expiration

## Future Enhancements

- **Real-time Notifications** - Push notifications for critical alerts
- **Mobile Application** - Mobile app for healthcare providers
- **Integration APIs** - Integration with external healthcare systems
- **Advanced Analytics** - Healthcare analytics and reporting dashboard
- **Telemedicine Support** - Video consultation capabilities
- **Document Management** - Medical document upload and management

## Support

For technical support or questions about the Health Record Management System, please refer to the system documentation or contact the development team.
