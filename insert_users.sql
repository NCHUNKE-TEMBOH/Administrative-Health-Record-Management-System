-- Insert sample users into the database
-- Password hash is SHA256 of the password for demo purposes

-- Admin users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active) VALUES
('admin', 'admin@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'admin', 'System', 'Administrator', '+1-555-0001', 1);

-- Doctor users  
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id) VALUES
('dr.smith', 'dr.smith@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'doctor', 'John', 'Smith', '+1-555-0002', 1, 1),
('dr.johnson', 'dr.johnson@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'doctor', 'Sarah', 'Johnson', '+1-555-0003', 1, 2),
('dr.williams', 'dr.williams@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'doctor', 'Michael', 'Williams', '+1-555-0004', 1, 1);

-- Nurse users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id) VALUES
('nurse.emily', 'nurse.emily@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'nurse', 'Emily', 'Davis', '+1-555-0005', 1, 1),
('nurse.brown', 'nurse.brown@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'nurse', 'Robert', 'Brown', '+1-555-0006', 1, 2),
('nurse.wilson', 'nurse.wilson@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'nurse', 'Lisa', 'Wilson', '+1-555-0007', 1, 1);

-- Lab technician users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active) VALUES
('lab.chen', 'lab.chen@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'lab_technician', 'Michael', 'Chen', '+1-555-0008', 1),
('lab.garcia', 'lab.garcia@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'lab_technician', 'Maria', 'Garcia', '+1-555-0009', 1);

-- Pharmacist users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active) VALUES
('pharm.wilson', 'pharm.wilson@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'pharmacist', 'David', 'Wilson', '+1-555-0010', 1),
('pharm.taylor', 'pharm.taylor@hospital.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'pharmacist', 'Jennifer', 'Taylor', '+1-555-0011', 1);

-- Patient users
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active, entity_id) VALUES
('patient.doe', 'patient.doe@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'patient', 'Jane', 'Doe', '+1-555-0012', 1, 1),
('patient.jones', 'patient.jones@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'patient', 'Robert', 'Jones', '+1-555-0013', 1, 2),
('patient.smith', 'patient.smith@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'patient', 'Mary', 'Smith', '+1-555-0014', 1, 1),
('patient.davis', 'patient.davis@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'patient', 'James', 'Davis', '+1-555-0015', 1, 2),
('patient.miller', 'patient.miller@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'patient', 'Patricia', 'Miller', '+1-555-0016', 1, 1);

-- Create blockchain tables
CREATE TABLE IF NOT EXISTS blockchain_blocks (
    block_index INTEGER PRIMARY KEY,
    timestamp REAL NOT NULL,
    data TEXT NOT NULL,
    previous_hash TEXT NOT NULL,
    hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blockchain_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Initialize blockchain metadata
INSERT OR REPLACE INTO blockchain_metadata (key, value) VALUES
('initialized', 'true'),
('version', '1.0'),
('created_at', datetime('now'));

-- Note: All passwords are 'admin123' hashed with SHA256
