import sqlite3
import json
with open('config.json') as data_file:
    config = json.load(data_file)

conn=sqlite3.connect(config['database'], check_same_thread=False)
conn.execute('pragma foreign_keys=ON')



def dict_factory(cursor, row):
    """This is a function use to format the json when retirve from the  mysql database"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn.row_factory = dict_factory

conn.execute('''CREATE TABLE if not exists patient
(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_first_name TEXT NOT NULL,
pat_last_name TEXT NOT NULL,
pat_insurance_no TEXT NOT NULL,
pat_ph_no TEXT NOT NULL,
pat_date DATE DEFAULT (datetime('now','localtime')),
pat_address TEXT NOT NULL);''')

conn.execute('''CREATE TABLE if not exists doctor
(doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
doc_first_name TEXT NOT NULL,
doc_last_name TEXT NOT NULL,
doc_ph_no TEXT NOT NULL,
doc_date DATE DEFAULT (datetime('now','localtime')),
doc_address TEXT NOT NULL);''')

conn.execute('''CREATE TABLE if not exists nurse
(nur_id INTEGER PRIMARY KEY AUTOINCREMENT,
nur_first_name TEXT NOT NULL,
nur_last_name TEXT NOT NULL,
nur_ph_no TEXT NOT NULL,
nur_date DATE DEFAULT (datetime('now','localtime')),
nur_address TEXT NOT NULL);''')

conn.execute('''CREATE TABLE if not exists appointment
(app_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
doc_id INTEGER NOT NULL,
appointment_date DATE NOT NULL,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(doc_id) REFERENCES doctor(doc_id));''')

conn.execute('''CREATE TABLE if not exists room
(room_no INTEGER PRIMARY KEY,
room_type TEXT NOT NULL,
available INTEGER NOT NULL);''')

conn.execute('''CREATE TABLE if not exists medication
(code INTEGER PRIMARY KEY,
name TEXT NOT NULL,
brand TEXT NOT NULL,
description TEXT);''')

conn.execute('''CREATE TABLE if not exists department
(department_id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
head_id INTEGER NOT NULL,
FOREIGN KEY(head_id) REFERENCES doctor(doc_id));''')

conn.execute('''CREATE TABLE if not exists procedure
(code integer PRIMARY KEY,
name TEXT NOT NULL,
cost INTEGER NOT NULL);''')

conn.execute('''CREATE TABLE if not exists undergoes
(pat_id INTEGER NOT NULL,
proc_code INTEGER NOT NULL,
u_date DATE NOT NULL,
doc_id INTEGER,
nur_id INTEGER,
room_no INTEGER,
PRIMARY KEY(pat_id, proc_code, u_date),
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(proc_code) REFERENCES procedure(code),
FOREIGN KEY(doc_id) REFERENCES doctor(doc_id),
FOREIGN KEY(nur_id) REFERENCES nurse(nur_id),
FOREIGN KEY(room_no) REFERENCES room(room_no));''')

conn.execute('''CREATE TABLE if not exists prescribes
(doc_id INTEGER,
pat_id INTEGER,
med_code INTEGER,
p_date DATE NOT NULL,
app_id INTEGER NOT NULL,
dose INTEGER NOT NULL,
PRIMARY KEY(doc_id, pat_id, med_code, p_date),
FOREIGN KEY(doc_id) REFERENCES doctor(doc_id),
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(med_code) REFERENCES medication(code),
FOREIGN KEY(app_id) REFERENCES appointment(app_id));''')

# Enhanced User Management with Roles
conn.execute('''CREATE TABLE if not exists users
(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
email TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
role TEXT NOT NULL CHECK(role IN ('admin', 'doctor', 'nurse', 'lab_technician', 'pharmacist', 'patient')),
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
phone_number TEXT,
is_active INTEGER DEFAULT 1,
created_date DATE DEFAULT (datetime('now','localtime')),
last_login DATE,
entity_id INTEGER);''') # Links to doctor, nurse, patient table IDs

# Health Records Management
conn.execute('''CREATE TABLE if not exists health_records
(record_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
record_type TEXT NOT NULL CHECK(record_type IN ('medical_history', 'diagnosis', 'treatment_plan', 'discharge_summary')),
title TEXT NOT NULL,
content TEXT NOT NULL,
created_by INTEGER NOT NULL,
created_date DATE DEFAULT (datetime('now','localtime')),
updated_date DATE DEFAULT (datetime('now','localtime')),
is_confidential INTEGER DEFAULT 0,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(created_by) REFERENCES users(user_id));''')

# Vital Signs Tracking
conn.execute('''CREATE TABLE if not exists vital_signs
(vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
recorded_by INTEGER NOT NULL,
temperature REAL,
blood_pressure_systolic INTEGER,
blood_pressure_diastolic INTEGER,
heart_rate INTEGER,
respiratory_rate INTEGER,
oxygen_saturation REAL,
weight REAL,
height REAL,
notes TEXT,
recorded_date DATE DEFAULT (datetime('now','localtime')),
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(recorded_by) REFERENCES users(user_id));''')

# Lab Tests and Results
conn.execute('''CREATE TABLE if not exists lab_tests
(test_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
requested_by INTEGER NOT NULL,
test_type TEXT NOT NULL,
test_name TEXT NOT NULL,
status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'cancelled')),
priority TEXT DEFAULT 'normal' CHECK(priority IN ('normal', 'urgent', 'stat')),
requested_date DATE DEFAULT (datetime('now','localtime')),
completed_date DATE,
processed_by INTEGER,
results TEXT,
normal_range TEXT,
is_abnormal INTEGER DEFAULT 0,
technician_notes TEXT,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(requested_by) REFERENCES users(user_id),
FOREIGN KEY(processed_by) REFERENCES users(user_id));''')

# Medical Notes by Doctors
conn.execute('''CREATE TABLE if not exists medical_notes
(note_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
doc_id INTEGER NOT NULL,
appointment_id INTEGER,
note_type TEXT DEFAULT 'general' CHECK(note_type IN ('general', 'diagnosis', 'treatment', 'follow_up')),
subject TEXT NOT NULL,
content TEXT NOT NULL,
created_date DATE DEFAULT (datetime('now','localtime')),
is_private INTEGER DEFAULT 0,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(doc_id) REFERENCES users(user_id),
FOREIGN KEY(appointment_id) REFERENCES appointment(app_id));''')

# Nursing Notes and Observations
conn.execute('''CREATE TABLE if not exists nursing_notes
(note_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
nurse_id INTEGER NOT NULL,
shift TEXT CHECK(shift IN ('day', 'evening', 'night')),
note_type TEXT DEFAULT 'observation' CHECK(note_type IN ('observation', 'care_plan', 'medication_admin', 'incident')),
content TEXT NOT NULL,
created_date DATE DEFAULT (datetime('now','localtime')),
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(nurse_id) REFERENCES users(user_id));''')

# Enhanced Prescription Management
conn.execute('''CREATE TABLE if not exists prescriptions
(prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
doc_id INTEGER NOT NULL,
med_code INTEGER NOT NULL,
dosage TEXT NOT NULL,
frequency TEXT NOT NULL,
duration TEXT NOT NULL,
instructions TEXT,
status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'cancelled', 'on_hold')),
prescribed_date DATE DEFAULT (datetime('now','localtime')),
start_date DATE,
end_date DATE,
refills_remaining INTEGER DEFAULT 0,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(doc_id) REFERENCES users(user_id),
FOREIGN KEY(med_code) REFERENCES medication(code));''')

# Medication Dispensing by Pharmacists
conn.execute('''CREATE TABLE if not exists medication_dispensing
(dispensing_id INTEGER PRIMARY KEY AUTOINCREMENT,
prescription_id INTEGER NOT NULL,
pharmacist_id INTEGER NOT NULL,
quantity_dispensed INTEGER NOT NULL,
dispensed_date DATE DEFAULT (datetime('now','localtime')),
batch_number TEXT,
expiry_date DATE,
notes TEXT,
FOREIGN KEY(prescription_id) REFERENCES prescriptions(prescription_id),
FOREIGN KEY(pharmacist_id) REFERENCES users(user_id));''')

# Access Control and Audit Logs
conn.execute('''CREATE TABLE if not exists access_logs
(log_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
action TEXT NOT NULL,
resource_type TEXT NOT NULL,
resource_id INTEGER,
patient_id INTEGER,
ip_address TEXT,
user_agent TEXT,
timestamp DATE DEFAULT (datetime('now','localtime')),
success INTEGER DEFAULT 1,
FOREIGN KEY(user_id) REFERENCES users(user_id),
FOREIGN KEY(patient_id) REFERENCES patient(pat_id));''')

# Patient Assignments for Nurses
conn.execute('''CREATE TABLE if not exists patient_assignments
(assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
nurse_id INTEGER NOT NULL,
pat_id INTEGER NOT NULL,
assigned_date DATE DEFAULT (datetime('now','localtime')),
shift TEXT CHECK(shift IN ('day', 'evening', 'night')),
is_active INTEGER DEFAULT 1,
notes TEXT,
FOREIGN KEY(nurse_id) REFERENCES users(user_id),
FOREIGN KEY(pat_id) REFERENCES patient(pat_id));''')