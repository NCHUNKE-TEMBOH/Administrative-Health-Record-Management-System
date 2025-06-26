"""
Integration tests for database operations
"""

import pytest
import sqlite3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from package.model import get_db_connection
from tests.conftest import insert_test_user, insert_test_patient, insert_test_doctor


class TestDatabaseConnections:
    """Test database connection and basic operations"""
    
    def test_database_connection(self, db_connection):
        """Test that database connection works"""
        assert db_connection is not None
        
        # Test basic query
        cursor = db_connection.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
    
    def test_database_schema_exists(self, db_connection):
        """Test that all required tables exist"""
        required_tables = [
            'users', 'patient', 'doctor', 'nurse', 'appointment',
            'prescriptions', 'lab_tests', 'health_records', 'vital_signs',
            'department', 'medication', 'room', 'procedure'
        ]
        
        # Get all table names
        cursor = db_connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        for table in required_tables:
            assert table in existing_tables, f"Table {table} does not exist"
    
    def test_table_structures(self, db_connection):
        """Test that tables have expected columns"""
        # Test users table structure
        cursor = db_connection.execute("PRAGMA table_info(users)")
        users_columns = [row[1] for row in cursor.fetchall()]
        
        expected_users_columns = [
            'user_id', 'username', 'email', 'password_hash', 'role',
            'first_name', 'last_name', 'phone_number', 'is_active',
            'entity_id', 'created_at'
        ]
        
        for column in expected_users_columns:
            assert column in users_columns, f"Column {column} missing from users table"
        
        # Test patient table structure
        cursor = db_connection.execute("PRAGMA table_info(patient)")
        patient_columns = [row[1] for row in cursor.fetchall()]
        
        expected_patient_columns = [
            'pat_id', 'pat_first_name', 'pat_last_name', 'pat_insurance_no',
            'pat_ph_no', 'pat_address', 'pat_date'
        ]
        
        for column in expected_patient_columns:
            assert column in patient_columns, f"Column {column} missing from patient table"


class TestUserDatabaseOperations:
    """Test user-related database operations"""
    
    def test_insert_user(self, db_connection, sample_users):
        """Test inserting a user into the database"""
        user_data = sample_users[0]
        user_id = insert_test_user(db_connection, user_data)
        
        assert user_id is not None
        assert user_id > 0
        
        # Verify user was inserted
        cursor = db_connection.execute(
            "SELECT username, email, role FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == user_data['username']
        assert result[1] == user_data['email']
        assert result[2] == user_data['role']
    
    def test_user_unique_constraints(self, db_connection, sample_users):
        """Test that username and email are unique"""
        user_data = sample_users[0]
        
        # Insert first user
        user_id1 = insert_test_user(db_connection, user_data)
        assert user_id1 is not None
        
        # Try to insert user with same username
        with pytest.raises(sqlite3.IntegrityError):
            insert_test_user(db_connection, user_data)
    
    def test_user_password_hashing(self, db_connection, sample_users):
        """Test that passwords are properly hashed"""
        user_data = sample_users[0]
        user_id = insert_test_user(db_connection, user_data)
        
        # Retrieve password hash
        cursor = db_connection.execute(
            "SELECT password_hash FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        
        password_hash = result[0]
        
        # Password hash should not be the plain password
        assert password_hash != user_data['password']
        # Password hash should be a reasonable length
        assert len(password_hash) > 20


class TestPatientDatabaseOperations:
    """Test patient-related database operations"""
    
    def test_insert_patient(self, db_connection, sample_patients):
        """Test inserting a patient into the database"""
        patient_data = sample_patients[0]
        patient_id = insert_test_patient(db_connection, patient_data)
        
        assert patient_id is not None
        assert patient_id > 0
        
        # Verify patient was inserted
        cursor = db_connection.execute(
            "SELECT pat_first_name, pat_last_name, pat_insurance_no FROM patient WHERE pat_id = ?",
            (patient_id,)
        )
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == patient_data['pat_first_name']
        assert result[1] == patient_data['pat_last_name']
        assert result[2] == patient_data['pat_insurance_no']
    
    def test_patient_update(self, db_connection, sample_patients):
        """Test updating patient information"""
        patient_data = sample_patients[0]
        patient_id = insert_test_patient(db_connection, patient_data)
        
        # Update patient
        new_address = "456 Updated Street"
        db_connection.execute(
            "UPDATE patient SET pat_address = ? WHERE pat_id = ?",
            (new_address, patient_id)
        )
        db_connection.commit()
        
        # Verify update
        cursor = db_connection.execute(
            "SELECT pat_address FROM patient WHERE pat_id = ?",
            (patient_id,)
        )
        result = cursor.fetchone()
        
        assert result[0] == new_address
    
    def test_patient_deletion(self, db_connection, sample_patients):
        """Test deleting a patient"""
        patient_data = sample_patients[0]
        patient_id = insert_test_patient(db_connection, patient_data)
        
        # Delete patient
        db_connection.execute("DELETE FROM patient WHERE pat_id = ?", (patient_id,))
        db_connection.commit()
        
        # Verify deletion
        cursor = db_connection.execute(
            "SELECT COUNT(*) FROM patient WHERE pat_id = ?",
            (patient_id,)
        )
        count = cursor.fetchone()[0]
        
        assert count == 0


class TestDoctorDatabaseOperations:
    """Test doctor-related database operations"""
    
    def test_insert_doctor(self, db_connection, sample_doctors):
        """Test inserting a doctor into the database"""
        doctor_data = sample_doctors[0]
        doctor_id = insert_test_doctor(db_connection, doctor_data)
        
        assert doctor_id is not None
        assert doctor_id > 0
        
        # Verify doctor was inserted
        cursor = db_connection.execute(
            "SELECT doc_first_name, doc_last_name, doc_specialization FROM doctor WHERE doc_id = ?",
            (doctor_id,)
        )
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == doctor_data['doc_first_name']
        assert result[1] == doctor_data['doc_last_name']
        assert result[2] == doctor_data['doc_specialization']


class TestRelationalIntegrity:
    """Test foreign key relationships and data integrity"""
    
    def test_appointment_foreign_keys(self, db_connection, sample_patients, sample_doctors):
        """Test appointment foreign key relationships"""
        # Insert patient and doctor
        patient_id = insert_test_patient(db_connection, sample_patients[0])
        doctor_id = insert_test_doctor(db_connection, sample_doctors[0])
        
        # Insert appointment
        cursor = db_connection.execute("""
            INSERT INTO appointment (patient_id, doctor_id, appointment_date, appointment_time, reason)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, doctor_id, "2024-12-31", "10:00:00", "Regular checkup"))
        
        appointment_id = cursor.lastrowid
        db_connection.commit()
        
        # Verify appointment was created with correct relationships
        cursor = db_connection.execute("""
            SELECT a.appointment_id, a.patient_id, a.doctor_id, p.pat_first_name, d.doc_first_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.pat_id
            JOIN doctor d ON a.doctor_id = d.doc_id
            WHERE a.appointment_id = ?
        """, (appointment_id,))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[1] == patient_id
        assert result[2] == doctor_id
        assert result[3] == sample_patients[0]['pat_first_name']
        assert result[4] == sample_doctors[0]['doc_first_name']
    
    def test_prescription_relationships(self, db_connection, sample_patients, sample_doctors):
        """Test prescription relationships with patients and doctors"""
        # Insert patient and doctor
        patient_id = insert_test_patient(db_connection, sample_patients[0])
        doctor_id = insert_test_doctor(db_connection, sample_doctors[0])
        
        # Insert prescription
        cursor = db_connection.execute("""
            INSERT INTO prescriptions (patient_id, doctor_id, medication_name, dosage, frequency)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, doctor_id, "Aspirin", "325mg", "Once daily"))
        
        prescription_id = cursor.lastrowid
        db_connection.commit()
        
        # Verify prescription relationships
        cursor = db_connection.execute("""
            SELECT pr.prescription_id, pr.patient_id, pr.doctor_id, pr.medication_name,
                   p.pat_first_name, d.doc_first_name
            FROM prescriptions pr
            JOIN patient p ON pr.patient_id = p.pat_id
            JOIN doctor d ON pr.doctor_id = d.doc_id
            WHERE pr.prescription_id = ?
        """, (prescription_id,))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[1] == patient_id
        assert result[2] == doctor_id
        assert result[3] == "Aspirin"
    
    def test_health_records_relationships(self, db_connection, sample_patients, sample_doctors):
        """Test health records relationships"""
        # Insert patient and doctor
        patient_id = insert_test_patient(db_connection, sample_patients[0])
        doctor_id = insert_test_doctor(db_connection, sample_doctors[0])
        
        # Insert health record
        cursor = db_connection.execute("""
            INSERT INTO health_records (patient_id, doctor_id, record_type, diagnosis, treatment)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, doctor_id, "consultation", "Hypertension", "Medication"))
        
        record_id = cursor.lastrowid
        db_connection.commit()
        
        # Verify health record relationships
        cursor = db_connection.execute("""
            SELECT hr.record_id, hr.patient_id, hr.doctor_id, hr.diagnosis,
                   p.pat_first_name, d.doc_first_name
            FROM health_records hr
            JOIN patient p ON hr.patient_id = p.pat_id
            JOIN doctor d ON hr.doctor_id = d.doc_id
            WHERE hr.record_id = ?
        """, (record_id,))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[1] == patient_id
        assert result[2] == doctor_id
        assert result[3] == "Hypertension"


class TestDatabaseTransactions:
    """Test database transaction handling"""
    
    def test_transaction_rollback(self, db_connection, sample_patients):
        """Test transaction rollback on error"""
        patient_data = sample_patients[0]
        
        try:
            # Start transaction
            db_connection.execute("BEGIN")
            
            # Insert patient
            cursor = db_connection.execute("""
                INSERT INTO patient (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address)
                VALUES (?, ?, ?, ?, ?)
            """, (
                patient_data['pat_first_name'],
                patient_data['pat_last_name'],
                patient_data['pat_insurance_no'],
                patient_data['pat_ph_no'],
                patient_data['pat_address']
            ))
            
            patient_id = cursor.lastrowid
            
            # Intentionally cause an error
            db_connection.execute("INSERT INTO non_existent_table VALUES (1)")
            
            # This should not be reached
            db_connection.commit()
            
        except sqlite3.OperationalError:
            # Rollback transaction
            db_connection.rollback()
        
        # Verify patient was not inserted due to rollback
        cursor = db_connection.execute(
            "SELECT COUNT(*) FROM patient WHERE pat_first_name = ? AND pat_last_name = ?",
            (patient_data['pat_first_name'], patient_data['pat_last_name'])
        )
        count = cursor.fetchone()[0]
        
        assert count == 0
    
    def test_transaction_commit(self, db_connection, sample_patients):
        """Test successful transaction commit"""
        patient_data = sample_patients[0]
        
        # Start transaction
        db_connection.execute("BEGIN")
        
        # Insert patient
        cursor = db_connection.execute("""
            INSERT INTO patient (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address)
            VALUES (?, ?, ?, ?, ?)
        """, (
            patient_data['pat_first_name'],
            patient_data['pat_last_name'],
            patient_data['pat_insurance_no'],
            patient_data['pat_ph_no'],
            patient_data['pat_address']
        ))
        
        patient_id = cursor.lastrowid
        
        # Commit transaction
        db_connection.commit()
        
        # Verify patient was inserted
        cursor = db_connection.execute(
            "SELECT COUNT(*) FROM patient WHERE pat_id = ?",
            (patient_id,)
        )
        count = cursor.fetchone()[0]
        
        assert count == 1


if __name__ == "__main__":
    pytest.main([__file__])
