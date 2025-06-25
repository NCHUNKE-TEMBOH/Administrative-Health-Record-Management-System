# UML Diagrams for Health Record Management System
## Architectural Views and Design Documentation

**Document Version:** 1.0  
**Date:** December 2024  
**System:** Administrative Health Record Management System  

---

## Table of Contents

1. [Use Case Diagrams](#use-case-diagrams)
2. [Class Diagrams](#class-diagrams)
3. [Sequence Diagrams](#sequence-diagrams)
4. [Component Diagrams](#component-diagrams)
5. [Deployment Diagrams](#deployment-diagrams)
6. [Activity Diagrams](#activity-diagrams)

---

## Use Case Diagrams

### System Overview Use Cases

```mermaid
graph TB
    subgraph "Health Record Management System"
        subgraph "Patient Management"
            UC1[Register Patient]
            UC2[Update Patient Info]
            UC3[View Patient Records]
            UC4[Search Patients]
        end
        
        subgraph "Health Records"
            UC5[Create Health Record]
            UC6[Update Health Record]
            UC7[View Health Records]
            UC8[Generate Reports]
        end
        
        subgraph "Lab Management"
            UC9[Order Lab Tests]
            UC10[Record Test Results]
            UC11[View Lab Results]
            UC12[Manage Lab Queue]
        end
        
        subgraph "Prescription Management"
            UC13[Prescribe Medication]
            UC14[Dispense Medication]
            UC15[Track Prescriptions]
            UC16[Manage Inventory]
        end
        
        subgraph "System Administration"
            UC17[Manage Users]
            UC18[Configure System]
            UC19[Monitor Blockchain]
            UC20[Generate Analytics]
        end
    end
    
    subgraph "Actors"
        ADMIN[Administrator]
        DOCTOR[Doctor]
        NURSE[Nurse]
        LAB_TECH[Lab Technician]
        PHARMACIST[Pharmacist]
        PATIENT[Patient]
    end
    
    ADMIN --> UC17
    ADMIN --> UC18
    ADMIN --> UC19
    ADMIN --> UC20
    
    DOCTOR --> UC1
    DOCTOR --> UC3
    DOCTOR --> UC5
    DOCTOR --> UC6
    DOCTOR --> UC7
    DOCTOR --> UC9
    DOCTOR --> UC13
    
    NURSE --> UC2
    NURSE --> UC3
    NURSE --> UC7
    NURSE --> UC11
    
    LAB_TECH --> UC10
    LAB_TECH --> UC11
    LAB_TECH --> UC12
    
    PHARMACIST --> UC14
    PHARMACIST --> UC15
    PHARMACIST --> UC16
    
    PATIENT --> UC3
    PATIENT --> UC7
    PATIENT --> UC11
    PATIENT --> UC15
```

### Detailed Use Case: Health Record Management

```mermaid
graph TB
    subgraph "Health Record Management Use Cases"
        UC_CREATE[Create Health Record]
        UC_UPDATE[Update Health Record]
        UC_VIEW[View Health Record]
        UC_DELETE[Archive Health Record]
        UC_SEARCH[Search Health Records]
        UC_EXPORT[Export Health Records]
        UC_AUDIT[Audit Health Records]
        UC_BLOCKCHAIN[Log to Blockchain]
    end
    
    subgraph "Actors"
        DOCTOR[Doctor]
        NURSE[Nurse]
        ADMIN[Administrator]
        PATIENT[Patient]
        SYSTEM[System]
    end
    
    DOCTOR --> UC_CREATE
    DOCTOR --> UC_UPDATE
    DOCTOR --> UC_VIEW
    DOCTOR --> UC_SEARCH
    
    NURSE --> UC_VIEW
    NURSE --> UC_SEARCH
    
    ADMIN --> UC_DELETE
    ADMIN --> UC_AUDIT
    ADMIN --> UC_EXPORT
    
    PATIENT --> UC_VIEW
    
    UC_CREATE --> UC_BLOCKCHAIN
    UC_UPDATE --> UC_BLOCKCHAIN
    UC_DELETE --> UC_BLOCKCHAIN
    
    SYSTEM --> UC_BLOCKCHAIN
```

---

## Class Diagrams

### Core Domain Model

```mermaid
classDiagram
    class User {
        +int user_id
        +string username
        +string password_hash
        +string email
        +string first_name
        +string last_name
        +string role
        +boolean is_active
        +datetime created_at
        +authenticate(password) boolean
        +hasPermission(resource) boolean
        +getRole() string
    }
    
    class Patient {
        +int pat_id
        +string first_name
        +string last_name
        +date date_of_birth
        +string gender
        +string phone
        +string email
        +string address
        +string emergency_contact
        +datetime created_at
        +getAge() int
        +getFullName() string
        +updateContactInfo(info) void
    }
    
    class HealthRecord {
        +int record_id
        +int pat_id
        +int doctor_id
        +string diagnosis
        +string treatment
        +text notes
        +date record_date
        +datetime created_at
        +validate() boolean
        +generateSummary() string
        +logToBlockchain() boolean
    }
    
    class VitalSigns {
        +int vital_id
        +int pat_id
        +int nurse_id
        +float temperature
        +int blood_pressure_systolic
        +int blood_pressure_diastolic
        +int heart_rate
        +int respiratory_rate
        +float oxygen_saturation
        +datetime recorded_at
        +isNormal() boolean
        +getBloodPressure() string
        +flagAbnormal() boolean
    }
    
    class LabTest {
        +int test_id
        +int pat_id
        +int doctor_id
        +string test_type
        +string test_name
        +string status
        +string priority
        +date ordered_date
        +date sample_collected_date
        +date result_date
        +text results
        +text notes
        +datetime created_at
        +updateStatus(status) void
        +addResults(results) void
        +isOverdue() boolean
    }
    
    class Prescription {
        +int prescription_id
        +int pat_id
        +int doctor_id
        +string medication_name
        +string dosage
        +string frequency
        +string duration
        +text instructions
        +string status
        +date prescribed_date
        +datetime created_at
        +isActive() boolean
        +calculateEndDate() date
        +dispense() boolean
    }
    
    class AuditLog {
        +int log_id
        +int user_id
        +string action
        +string record_type
        +int record_id
        +int patient_id
        +string details
        +datetime created_at
        +validateAccess() boolean
        +generateReport() string
    }
    
    User ||--o{ HealthRecord : creates
    User ||--o{ LabTest : orders
    User ||--o{ Prescription : prescribes
    User ||--o{ VitalSigns : records
    
    Patient ||--o{ HealthRecord : has
    Patient ||--o{ VitalSigns : has
    Patient ||--o{ LabTest : undergoes
    Patient ||--o{ Prescription : receives
    
    HealthRecord ||--o{ AuditLog : logged_in
    LabTest ||--o{ AuditLog : logged_in
    Prescription ||--o{ AuditLog : logged_in
    VitalSigns ||--o{ AuditLog : logged_in
```

### Service Layer Architecture

```mermaid
classDiagram
    class HealthRecordsService {
        -repository: HealthRecordRepository
        -blockchainLogger: BlockchainLogger
        -validator: DataValidator
        +getHealthRecords() List~HealthRecord~
        +createHealthRecord(data) HealthRecord
        +updateHealthRecord(id, data) HealthRecord
        +deleteHealthRecord(id) boolean
        +searchHealthRecords(criteria) List~HealthRecord~
        -validateData(data) boolean
        -logToBlockchain(record) boolean
    }
    
    class PatientService {
        -repository: PatientRepository
        -validator: DataValidator
        +getPatients() List~Patient~
        +createPatient(data) Patient
        +updatePatient(id, data) Patient
        +getPatientById(id) Patient
        +searchPatients(criteria) List~Patient~
        -validatePatientData(data) boolean
    }
    
    class LabService {
        -repository: LabTestRepository
        -blockchainLogger: BlockchainLogger
        -notificationService: NotificationService
        +getLabTests() List~LabTest~
        +orderLabTest(data) LabTest
        +updateTestResults(id, results) LabTest
        +getTestsByStatus(status) List~LabTest~
        +getTestsByPatient(patientId) List~LabTest~
        -notifyDoctor(test) void
        -logToBlockchain(test) boolean
    }
    
    class PrescriptionService {
        -repository: PrescriptionRepository
        -auditLogger: AuditLogger
        -inventoryService: InventoryService
        +getPrescriptions() List~Prescription~
        +createPrescription(data) Prescription
        +dispensePrescription(id) boolean
        +getPrescriptionsByPatient(patientId) List~Prescription~
        +checkDrugInteractions(medications) List~Interaction~
        -updateInventory(medication, quantity) boolean
        -logToAudit(prescription) boolean
    }

    class AuditService {
        -auditRepository: AuditRepository
        -logger: AuditLogger
        +getAuditStats() AuditStats
        +validateAccess() boolean
        +getAuditTrail() List~AuditLog~
        +getPatientAudit(patientId) List~AuditLog~
        +addAuditEntry(data) AuditLog
        -generateHash(data) string
        -validateEntry(entry) boolean
    }
    
    class AuthenticationService {
        -userRepository: UserRepository
        -tokenManager: JWTTokenManager
        -passwordEncoder: PasswordEncoder
        +authenticate(username, password) AuthToken
        +validateToken(token) boolean
        +refreshToken(token) AuthToken
        +logout(token) boolean
        +changePassword(userId, oldPassword, newPassword) boolean
        -encodePassword(password) string
        -generateToken(user) string
    }
    
    HealthRecordsService --> PatientService : uses
    HealthRecordsService --> BlockchainService : uses
    LabService --> PatientService : uses
    LabService --> BlockchainService : uses
    PrescriptionService --> PatientService : uses
    PrescriptionService --> BlockchainService : uses
```

---

## Sequence Diagrams

### Create Health Record Sequence

```mermaid
sequenceDiagram
    participant Doctor
    participant WebUI
    participant APIGateway
    participant AuthService
    participant HealthRecordService
    participant Database
    participant BlockchainService
    participant Blockchain
    
    Doctor->>WebUI: Fill health record form
    WebUI->>APIGateway: POST /api/health_records
    APIGateway->>AuthService: Validate JWT token
    AuthService-->>APIGateway: Token valid, user info
    APIGateway->>HealthRecordService: Create health record
    
    HealthRecordService->>HealthRecordService: Validate data
    HealthRecordService->>Database: Insert health record
    Database-->>HealthRecordService: Record ID
    
    HealthRecordService->>BlockchainService: Log operation
    BlockchainService->>Blockchain: Create block
    Blockchain-->>BlockchainService: Block hash
    BlockchainService-->>HealthRecordService: Success
    
    HealthRecordService-->>APIGateway: Health record created
    APIGateway-->>WebUI: HTTP 201 Created
    WebUI-->>Doctor: Success message
```

### Blockchain Validation Sequence

```mermaid
sequenceDiagram
    participant Admin
    participant WebUI
    participant APIGateway
    participant AuditService
    participant AuditLog
    participant Database

    Admin->>WebUI: Request audit validation
    WebUI->>APIGateway: GET /api/audit/validate
    APIGateway->>AuditService: Validate audit trail

    AuditService->>AuditLog: Get all audit entries
    AuditLog-->>AuditService: Audit entry list

    loop For each entry
        AuditService->>AuditService: Verify integrity
        AuditService->>AuditService: Check access permissions
    end

    AuditService->>Database: Get audit statistics
    Database-->>AuditService: Statistics data

    AuditService-->>APIGateway: Validation result
    APIGateway-->>WebUI: Validation response
    WebUI-->>Admin: Display audit status
```

### Patient Record Access Sequence

```mermaid
sequenceDiagram
    participant Patient
    participant WebUI
    participant APIGateway
    participant AuthService
    participant PatientService
    participant HealthRecordService
    participant Database
    participant BlockchainService
    
    Patient->>WebUI: Login to patient portal
    WebUI->>APIGateway: POST /api/auth/login
    APIGateway->>AuthService: Authenticate
    AuthService-->>APIGateway: JWT token
    APIGateway-->>WebUI: Authentication success
    
    Patient->>WebUI: Request health records
    WebUI->>APIGateway: GET /api/patient/records
    APIGateway->>AuthService: Validate token
    AuthService-->>APIGateway: Token valid
    
    APIGateway->>PatientService: Get patient info
    PatientService->>Database: Query patient
    Database-->>PatientService: Patient data
    
    APIGateway->>HealthRecordService: Get records for patient
    HealthRecordService->>Database: Query health records
    Database-->>HealthRecordService: Health records
    
    APIGateway->>BlockchainService: Get audit trail
    BlockchainService->>Database: Query blockchain records
    Database-->>BlockchainService: Blockchain audit data
    
    APIGateway-->>WebUI: Combined patient data
    WebUI-->>Patient: Display health records
```

---

## Component Diagrams

### System Component Overview

```mermaid
graph TB
    subgraph "Presentation Layer"
        WEB[Web Dashboard]
        MOBILE[Mobile App]
        API_GW[API Gateway]
    end
    
    subgraph "Application Layer"
        AUTH_SVC[Authentication Service]
        PATIENT_SVC[Patient Service]
        HEALTH_SVC[Health Records Service]
        LAB_SVC[Lab Service]
        PHARMACY_SVC[Pharmacy Service]
        BLOCKCHAIN_SVC[Blockchain Service]
        NOTIFICATION_SVC[Notification Service]
    end
    
    subgraph "Business Layer"
        VALIDATION[Data Validation]
        WORKFLOW[Workflow Engine]
        RULES[Business Rules]
        SECURITY[Security Policies]
    end
    
    subgraph "Data Access Layer"
        PATIENT_REPO[Patient Repository]
        HEALTH_REPO[Health Records Repository]
        LAB_REPO[Lab Repository]
        PHARMACY_REPO[Pharmacy Repository]
        BLOCKCHAIN_REPO[Blockchain Repository]
        USER_REPO[User Repository]
    end
    
    subgraph "Infrastructure Layer"
        DATABASE[(Database)]
        BLOCKCHAIN_DB[(Blockchain Storage)]
        CACHE[(Redis Cache)]
        FILE_STORAGE[(File Storage)]
        MESSAGE_QUEUE[(Message Queue)]
    end
    
    WEB --> API_GW
    MOBILE --> API_GW
    
    API_GW --> AUTH_SVC
    API_GW --> PATIENT_SVC
    API_GW --> HEALTH_SVC
    API_GW --> LAB_SVC
    API_GW --> PHARMACY_SVC
    API_GW --> BLOCKCHAIN_SVC
    
    HEALTH_SVC --> VALIDATION
    HEALTH_SVC --> WORKFLOW
    HEALTH_SVC --> RULES
    HEALTH_SVC --> SECURITY
    
    PATIENT_SVC --> PATIENT_REPO
    HEALTH_SVC --> HEALTH_REPO
    LAB_SVC --> LAB_REPO
    PHARMACY_SVC --> PHARMACY_REPO
    BLOCKCHAIN_SVC --> BLOCKCHAIN_REPO
    AUTH_SVC --> USER_REPO
    
    PATIENT_REPO --> DATABASE
    HEALTH_REPO --> DATABASE
    LAB_REPO --> DATABASE
    PHARMACY_REPO --> DATABASE
    USER_REPO --> DATABASE
    BLOCKCHAIN_REPO --> BLOCKCHAIN_DB
    
    AUTH_SVC --> CACHE
    PATIENT_SVC --> CACHE
    HEALTH_SVC --> MESSAGE_QUEUE
    LAB_SVC --> NOTIFICATION_SVC
```

### Blockchain Component Detail

```mermaid
graph TB
    subgraph "Audit Service Components"
        AUDIT_API[Audit API]
        AUDIT_LOGGER[Audit Logger]
        LOG_VALIDATOR[Log Validator]
        TRAIL_MANAGER[Trail Manager]
        HASH_CALCULATOR[Hash Calculator]
        INTEGRITY_ENGINE[Integrity Engine]
    end

    subgraph "Audit Core"
        LOG_ENTRY[Log Entry]
        AUDIT_TRAIL[Audit Trail]
        LOG_DATA[Log Data]
        ACCESS_LOG[Access Log]
    end

    subgraph "Storage Components"
        LOG_STORAGE[Log Storage]
        INDEX_STORAGE[Index Storage]
        METADATA_STORAGE[Metadata Storage]
    end

    subgraph "Integration Hooks"
        HEALTH_HOOK[Health Record Hook]
        LAB_HOOK[Lab Test Hook]
        PHARMACY_HOOK[Pharmacy Hook]
        VITAL_HOOK[Vital Signs Hook]
    end
    
    BLOCKCHAIN_API --> BLOCKCHAIN_LOGGER
    BLOCKCHAIN_API --> BLOCK_VALIDATOR
    BLOCKCHAIN_API --> CHAIN_MANAGER
    
    BLOCKCHAIN_LOGGER --> HASH_CALCULATOR
    BLOCKCHAIN_LOGGER --> MINING_ENGINE
    
    CHAIN_MANAGER --> BLOCK
    CHAIN_MANAGER --> BLOCKCHAIN
    
    BLOCK --> BLOCK_DATA
    BLOCK --> TRANSACTION
    
    BLOCKCHAIN --> BLOCK_STORAGE
    BLOCKCHAIN --> INDEX_STORAGE
    BLOCKCHAIN --> METADATA_STORAGE
    
    HEALTH_HOOK --> BLOCKCHAIN_LOGGER
    LAB_HOOK --> BLOCKCHAIN_LOGGER
    PHARMACY_HOOK --> BLOCKCHAIN_LOGGER
    VITAL_HOOK --> BLOCKCHAIN_LOGGER
```

---

## Deployment Diagrams

### Kubernetes Deployment Architecture

```mermaid
graph TB
    subgraph "Load Balancer Tier"
        LB[NGINX Load Balancer]
        INGRESS[Kubernetes Ingress]
    end
    
    subgraph "Kubernetes Cluster"
        subgraph "Frontend Namespace"
            UI_POD1[UI Pod 1]
            UI_POD2[UI Pod 2]
            UI_POD3[UI Pod 3]
            API_POD1[API Gateway Pod 1]
            API_POD2[API Gateway Pod 2]
        end
        
        subgraph "Application Namespace"
            AUTH_POD1[Auth Service Pod 1]
            AUTH_POD2[Auth Service Pod 2]
            PATIENT_POD1[Patient Service Pod 1]
            PATIENT_POD2[Patient Service Pod 2]
            PATIENT_POD3[Patient Service Pod 3]
            HEALTH_POD1[Health Records Pod 1]
            HEALTH_POD2[Health Records Pod 2]
            HEALTH_POD3[Health Records Pod 3]
            LAB_POD1[Lab Service Pod 1]
            LAB_POD2[Lab Service Pod 2]
            PHARMACY_POD1[Pharmacy Service Pod 1]
            PHARMACY_POD2[Pharmacy Service Pod 2]
            BLOCKCHAIN_POD1[Blockchain Service Pod 1]
            BLOCKCHAIN_POD2[Blockchain Service Pod 2]
        end
        
        subgraph "Data Namespace"
            DB_MASTER[Database Master]
            DB_SLAVE1[Database Slave 1]
            DB_SLAVE2[Database Slave 2]
            REDIS_MASTER[Redis Master]
            REDIS_SLAVE[Redis Slave]
            STORAGE_POD1[Storage Pod 1]
            STORAGE_POD2[Storage Pod 2]
        end
        
        subgraph "Monitoring Namespace"
            PROMETHEUS[Prometheus]
            GRAFANA[Grafana]
            ELASTICSEARCH[Elasticsearch]
            KIBANA[Kibana]
        end
    end
    
    subgraph "External Services"
        BACKUP_SERVICE[Backup Service]
        NOTIFICATION_SERVICE[Email/SMS Service]
        AUDIT_SERVICE[External Audit Service]
    end
    
    LB --> INGRESS
    INGRESS --> UI_POD1
    INGRESS --> UI_POD2
    INGRESS --> UI_POD3
    INGRESS --> API_POD1
    INGRESS --> API_POD2
    
    API_POD1 --> AUTH_POD1
    API_POD1 --> PATIENT_POD1
    API_POD1 --> HEALTH_POD1
    API_POD1 --> LAB_POD1
    API_POD1 --> PHARMACY_POD1
    API_POD1 --> BLOCKCHAIN_POD1
    
    API_POD2 --> AUTH_POD2
    API_POD2 --> PATIENT_POD2
    API_POD2 --> HEALTH_POD2
    API_POD2 --> LAB_POD2
    API_POD2 --> PHARMACY_POD2
    API_POD2 --> BLOCKCHAIN_POD2
    
    PATIENT_POD1 --> DB_MASTER
    PATIENT_POD2 --> DB_SLAVE1
    PATIENT_POD3 --> DB_SLAVE2
    
    HEALTH_POD1 --> DB_MASTER
    HEALTH_POD2 --> DB_SLAVE1
    HEALTH_POD3 --> DB_SLAVE2
    
    AUTH_POD1 --> REDIS_MASTER
    AUTH_POD2 --> REDIS_SLAVE
    
    BLOCKCHAIN_POD1 --> STORAGE_POD1
    BLOCKCHAIN_POD2 --> STORAGE_POD2
    
    DB_MASTER --> BACKUP_SERVICE
    HEALTH_POD1 --> NOTIFICATION_SERVICE
    BLOCKCHAIN_POD1 --> AUDIT_SERVICE
```

### Network Architecture Deployment

```mermaid
graph TB
    subgraph "Internet"
        USERS[Users]
        EXTERNAL_APIS[External APIs]
    end

    subgraph "DMZ (Demilitarized Zone)"
        WAF[Web Application Firewall]
        REVERSE_PROXY[Reverse Proxy]
        RATE_LIMITER[Rate Limiter]
    end

    subgraph "VPS Infrastructure"
        subgraph "Public Subnet"
            LOAD_BALANCER[Load Balancer]
            BASTION[Bastion Host]
        end

        subgraph "Private Subnet"
            K8S_MASTER[Kubernetes Master]
            K8S_WORKER1[Kubernetes Worker 1]
            K8S_WORKER2[Kubernetes Worker 2]
            K8S_WORKER3[Kubernetes Worker 3]
        end

        subgraph "Database Subnet"
            DB_PRIMARY[Database Primary]
            DB_REPLICA[Database Replica]
            BACKUP_STORAGE[Backup Storage]
        end
    end

    subgraph "Monitoring & Logging"
        LOG_AGGREGATOR[Log Aggregator]
        METRICS_COLLECTOR[Metrics Collector]
        ALERT_MANAGER[Alert Manager]
    end

    USERS --> WAF
    EXTERNAL_APIS --> WAF
    WAF --> REVERSE_PROXY
    REVERSE_PROXY --> RATE_LIMITER
    RATE_LIMITER --> LOAD_BALANCER

    LOAD_BALANCER --> K8S_MASTER
    K8S_MASTER --> K8S_WORKER1
    K8S_MASTER --> K8S_WORKER2
    K8S_MASTER --> K8S_WORKER3

    K8S_WORKER1 --> DB_PRIMARY
    K8S_WORKER2 --> DB_REPLICA
    K8S_WORKER3 --> BACKUP_STORAGE

    K8S_WORKER1 --> LOG_AGGREGATOR
    K8S_WORKER2 --> METRICS_COLLECTOR
    K8S_WORKER3 --> ALERT_MANAGER
```

---

## Activity Diagrams

### Patient Registration Workflow

```mermaid
graph TD
    START([Start: New Patient Registration])

    INPUT_DATA[Input Patient Information]
    VALIDATE_DATA{Validate Data}
    SHOW_ERRORS[Show Validation Errors]

    CHECK_DUPLICATE{Check for Duplicate Patient}
    CONFIRM_DUPLICATE[Confirm Duplicate Patient Action]

    SAVE_PATIENT[Save Patient to Database]
    GENERATE_ID[Generate Patient ID]

    CREATE_BLOCKCHAIN_ENTRY[Create Blockchain Entry]
    LOG_AUDIT[Log Audit Trail]

    SEND_CONFIRMATION[Send Confirmation]
    DISPLAY_SUCCESS[Display Success Message]

    END([End: Patient Registered])

    START --> INPUT_DATA
    INPUT_DATA --> VALIDATE_DATA
    VALIDATE_DATA -->|Invalid| SHOW_ERRORS
    SHOW_ERRORS --> INPUT_DATA
    VALIDATE_DATA -->|Valid| CHECK_DUPLICATE

    CHECK_DUPLICATE -->|Duplicate Found| CONFIRM_DUPLICATE
    CONFIRM_DUPLICATE --> INPUT_DATA
    CHECK_DUPLICATE -->|No Duplicate| SAVE_PATIENT

    SAVE_PATIENT --> GENERATE_ID
    GENERATE_ID --> CREATE_BLOCKCHAIN_ENTRY
    CREATE_BLOCKCHAIN_ENTRY --> LOG_AUDIT
    LOG_AUDIT --> SEND_CONFIRMATION
    SEND_CONFIRMATION --> DISPLAY_SUCCESS
    DISPLAY_SUCCESS --> END
```

### Health Record Creation Workflow

```mermaid
graph TD
    START([Start: Create Health Record])

    SELECT_PATIENT[Select Patient]
    VERIFY_PERMISSIONS{Verify Doctor Permissions}
    ACCESS_DENIED[Access Denied]

    INPUT_DIAGNOSIS[Input Diagnosis]
    INPUT_TREATMENT[Input Treatment Plan]
    INPUT_NOTES[Input Clinical Notes]

    VALIDATE_RECORD{Validate Health Record}
    SHOW_VALIDATION_ERRORS[Show Validation Errors]

    SAVE_RECORD[Save Health Record]
    CALCULATE_HASH[Calculate Record Hash]

    CREATE_BLOCKCHAIN_BLOCK[Create Blockchain Block]
    MINE_BLOCK[Mine Block with Proof of Work]
    ADD_TO_CHAIN[Add Block to Blockchain]

    UPDATE_PATIENT_HISTORY[Update Patient History]
    NOTIFY_STAKEHOLDERS[Notify Relevant Stakeholders]

    GENERATE_SUMMARY[Generate Record Summary]
    DISPLAY_SUCCESS[Display Success Message]

    END([End: Health Record Created])

    START --> SELECT_PATIENT
    SELECT_PATIENT --> VERIFY_PERMISSIONS
    VERIFY_PERMISSIONS -->|No Permission| ACCESS_DENIED
    ACCESS_DENIED --> END
    VERIFY_PERMISSIONS -->|Authorized| INPUT_DIAGNOSIS

    INPUT_DIAGNOSIS --> INPUT_TREATMENT
    INPUT_TREATMENT --> INPUT_NOTES
    INPUT_NOTES --> VALIDATE_RECORD

    VALIDATE_RECORD -->|Invalid| SHOW_VALIDATION_ERRORS
    SHOW_VALIDATION_ERRORS --> INPUT_DIAGNOSIS
    VALIDATE_RECORD -->|Valid| SAVE_RECORD

    SAVE_RECORD --> CALCULATE_HASH
    CALCULATE_HASH --> CREATE_BLOCKCHAIN_BLOCK
    CREATE_BLOCKCHAIN_BLOCK --> MINE_BLOCK
    MINE_BLOCK --> ADD_TO_CHAIN

    ADD_TO_CHAIN --> UPDATE_PATIENT_HISTORY
    UPDATE_PATIENT_HISTORY --> NOTIFY_STAKEHOLDERS
    NOTIFY_STAKEHOLDERS --> GENERATE_SUMMARY
    GENERATE_SUMMARY --> DISPLAY_SUCCESS
    DISPLAY_SUCCESS --> END
```

### Blockchain Validation Process

```mermaid
graph TD
    START([Start: Audit Validation])

    LOAD_AUDIT[Load Audit Trail from Database]
    GET_FIRST_ENTRY[Get First Audit Entry]

    VALIDATE_ENTRY{Validate Audit Entry}
    ENTRY_ERROR[Report Entry Error]

    GET_NEXT_ENTRY[Get Next Entry]
    MORE_ENTRIES{More Entries Available?}

    VALIDATE_INTEGRITY{Validate Entry Integrity}
    INTEGRITY_ERROR[Report Integrity Error]

    VALIDATE_SEQUENCE{Validate Entry Sequence}
    SEQUENCE_ERROR[Report Sequence Error]

    VALIDATE_DATA{Validate Entry Data}
    DATA_ERROR[Report Data Error]

    CHECK_TAMPERING{Check for Tampering}
    TAMPERING_DETECTED[Report Tampering]

    INCREMENT_COUNTER[Increment Valid Entry Counter]

    GENERATE_REPORT[Generate Validation Report]
    UPDATE_STATISTICS[Update Audit Statistics]

    VALIDATION_SUCCESS[Validation Successful]
    VALIDATION_FAILED[Validation Failed]

    END([End: Validation Complete])

    START --> LOAD_BLOCKCHAIN
    LOAD_BLOCKCHAIN --> GET_FIRST_BLOCK
    GET_FIRST_BLOCK --> VALIDATE_GENESIS

    VALIDATE_GENESIS -->|Invalid| GENESIS_ERROR
    GENESIS_ERROR --> VALIDATION_FAILED
    VALIDATE_GENESIS -->|Valid| GET_NEXT_BLOCK

    GET_NEXT_BLOCK --> MORE_BLOCKS
    MORE_BLOCKS -->|No More Blocks| GENERATE_REPORT
    MORE_BLOCKS -->|More Blocks| VALIDATE_HASH

    VALIDATE_HASH -->|Invalid| HASH_ERROR
    HASH_ERROR --> VALIDATION_FAILED
    VALIDATE_HASH -->|Valid| VALIDATE_PREVIOUS_HASH

    VALIDATE_PREVIOUS_HASH -->|Invalid| LINK_ERROR
    LINK_ERROR --> VALIDATION_FAILED
    VALIDATE_PREVIOUS_HASH -->|Valid| VALIDATE_DATA

    VALIDATE_DATA -->|Invalid| DATA_ERROR
    DATA_ERROR --> VALIDATION_FAILED
    VALIDATE_DATA -->|Valid| CHECK_TAMPERING

    CHECK_TAMPERING -->|Tampering Detected| TAMPERING_DETECTED
    TAMPERING_DETECTED --> VALIDATION_FAILED
    CHECK_TAMPERING -->|No Tampering| INCREMENT_COUNTER

    INCREMENT_COUNTER --> GET_NEXT_BLOCK

    GENERATE_REPORT --> UPDATE_STATISTICS
    UPDATE_STATISTICS --> VALIDATION_SUCCESS
    VALIDATION_SUCCESS --> END
    VALIDATION_FAILED --> END
```

### Lab Test Management Workflow

```mermaid
graph TD
    START([Start: Lab Test Management])

    ORDER_TEST[Doctor Orders Lab Test]
    VALIDATE_ORDER{Validate Test Order}
    ORDER_ERROR[Show Order Errors]

    SCHEDULE_TEST[Schedule Test Collection]
    NOTIFY_PATIENT[Notify Patient]
    NOTIFY_LAB[Notify Lab Technician]

    COLLECT_SAMPLE[Collect Sample]
    UPDATE_STATUS_COLLECTED[Update Status: Sample Collected]

    PROCESS_SAMPLE[Process Sample in Lab]
    UPDATE_STATUS_PROCESSING[Update Status: Processing]

    ENTER_RESULTS[Enter Test Results]
    VALIDATE_RESULTS{Validate Results}
    RESULTS_ERROR[Show Results Errors]

    REVIEW_RESULTS[Lab Technician Reviews]
    APPROVE_RESULTS{Approve Results?}

    SAVE_RESULTS[Save Results to Database]
    CREATE_BLOCKCHAIN_ENTRY[Create Blockchain Entry]

    NOTIFY_DOCTOR[Notify Ordering Doctor]
    UPDATE_PATIENT_RECORD[Update Patient Record]

    GENERATE_REPORT[Generate Lab Report]
    SEND_REPORT[Send Report to Doctor]

    END([End: Lab Test Complete])

    START --> ORDER_TEST
    ORDER_TEST --> VALIDATE_ORDER
    VALIDATE_ORDER -->|Invalid| ORDER_ERROR
    ORDER_ERROR --> ORDER_TEST
    VALIDATE_ORDER -->|Valid| SCHEDULE_TEST

    SCHEDULE_TEST --> NOTIFY_PATIENT
    NOTIFY_PATIENT --> NOTIFY_LAB
    NOTIFY_LAB --> COLLECT_SAMPLE

    COLLECT_SAMPLE --> UPDATE_STATUS_COLLECTED
    UPDATE_STATUS_COLLECTED --> PROCESS_SAMPLE
    PROCESS_SAMPLE --> UPDATE_STATUS_PROCESSING

    UPDATE_STATUS_PROCESSING --> ENTER_RESULTS
    ENTER_RESULTS --> VALIDATE_RESULTS
    VALIDATE_RESULTS -->|Invalid| RESULTS_ERROR
    RESULTS_ERROR --> ENTER_RESULTS
    VALIDATE_RESULTS -->|Valid| REVIEW_RESULTS

    REVIEW_RESULTS --> APPROVE_RESULTS
    APPROVE_RESULTS -->|Not Approved| ENTER_RESULTS
    APPROVE_RESULTS -->|Approved| SAVE_RESULTS

    SAVE_RESULTS --> CREATE_BLOCKCHAIN_ENTRY
    CREATE_BLOCKCHAIN_ENTRY --> NOTIFY_DOCTOR
    NOTIFY_DOCTOR --> UPDATE_PATIENT_RECORD
    UPDATE_PATIENT_RECORD --> GENERATE_REPORT
    GENERATE_REPORT --> SEND_REPORT
    SEND_REPORT --> END
```

---

## State Diagrams

### Health Record State Transitions

```mermaid
stateDiagram-v2
    [*] --> Draft : Create Record

    Draft --> InReview : Submit for Review
    Draft --> [*] : Delete Draft

    InReview --> Approved : Doctor Approves
    InReview --> Rejected : Doctor Rejects
    InReview --> Draft : Return to Draft

    Rejected --> Draft : Revise Record
    Rejected --> [*] : Discard Record

    Approved --> Active : Finalize Record

    Active --> Updated : Modify Record
    Active --> Archived : Archive Record

    Updated --> Active : Save Changes
    Updated --> Archived : Archive Updated Record

    Archived --> [*] : Permanent Archive

    note right of Active
        Blockchain entry created
        when record becomes active
    end note

    note right of Updated
        New blockchain entry
        created for each update
    end note
```

### Lab Test State Machine

```mermaid
stateDiagram-v2
    [*] --> Ordered : Doctor Orders Test

    Ordered --> Scheduled : Schedule Collection
    Ordered --> Cancelled : Cancel Order

    Scheduled --> SampleCollected : Collect Sample
    Scheduled --> Cancelled : Cancel Test

    SampleCollected --> Processing : Begin Processing
    SampleCollected --> Lost : Sample Lost

    Processing --> ResultsReady : Complete Processing
    Processing --> Failed : Processing Failed

    ResultsReady --> Reviewed : Lab Tech Reviews

    Reviewed --> Approved : Approve Results
    Reviewed --> Rejected : Reject Results

    Rejected --> Processing : Reprocess Sample

    Approved --> Reported : Send to Doctor

    Reported --> [*] : Complete

    Cancelled --> [*] : End
    Lost --> [*] : End
    Failed --> [*] : End

    note right of Approved
        Blockchain entry created
        when results are approved
    end note
```

---

## Summary

This comprehensive UML documentation provides multiple architectural views of the Health Record Management System:

### Key Architectural Views Covered:

1. **Use Case Diagrams**: System functionality and user interactions
2. **Class Diagrams**: Object-oriented design and relationships
3. **Sequence Diagrams**: Dynamic behavior and message flows
4. **Component Diagrams**: System structure and dependencies
5. **Deployment Diagrams**: Physical architecture and infrastructure
6. **Activity Diagrams**: Business process workflows
7. **State Diagrams**: Object lifecycle and state transitions

### Architecture Highlights:

- **Layered Architecture** with clear separation of concerns
- **Service-Oriented Design** for scalability and maintainability
- **Blockchain Integration** for audit trails and data integrity
- **Kubernetes Deployment** for high availability and scalability
- **Security-First Design** with multiple protection layers
- **HIPAA Compliance** through comprehensive audit trails

This documentation serves as a complete architectural reference for development, deployment, and maintenance of the Health Record Management System.
