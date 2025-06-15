-- Create sample users for the Health Record Management System

-- Admin user
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active)
VALUES ('admin', 'admin@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'admin', 'System', 'Administrator', '+1-555-0001', 1);

-- Doctor users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id)
VALUES ('dr.smith', 'dr.smith@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'doctor', 'John', 'Smith', '+1-555-0002', 1, 1);

INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id)
VALUES ('dr.johnson', 'dr.johnson@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'doctor', 'Sarah', 'Johnson', '+1-555-0003', 1, 2);

-- Nurse users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id)
VALUES ('nurse.williams', 'nurse.williams@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'nurse', 'Emily', 'Williams', '+1-555-0004', 1, 1);

INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id)
VALUES ('nurse.brown', 'nurse.brown@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'nurse', 'Michael', 'Brown', '+1-555-0005', 1, 2);

-- Lab technician
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active)
VALUES ('lab.chen', 'lab.chen@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'lab_technician', 'Michael', 'Chen', '+1-555-0006', 1);

-- Pharmacist
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active)
VALUES ('pharm.wilson', 'pharm.wilson@hospital.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'pharmacist', 'David', 'Wilson', '+1-555-0007', 1);

-- Patient users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id)
VALUES ('patient.doe', 'patient.doe@email.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'patient', 'Jane', 'Doe', '+1-555-0008', 1, 1);

INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id)
VALUES ('patient.jones', 'patient.jones@email.com', 'scrypt:32768:8:1$YQhQJQhQJQhQJQ$46d4c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7e7b9c9e7', 'patient', 'Robert', 'Jones', '+1-555-0009', 1, 2);

-- Note: All passwords are hashed version of 'password123'
