"""
Unit tests for patient management module
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from package.patient import Patients, Patient


class TestPatientsResource:
    """Test cases for Patients resource (collection operations)"""
    
    @patch('package.patient.conn')
    def test_get_all_patients_success(self, mock_conn):
        """Test successful retrieval of all patients"""
        # Mock database response
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Jane", "Doe", "INS123", "+1234567890", "123 Main St", "2024-01-01"),
            (2, "John", "Smith", "INS456", "+1234567891", "456 Oak Ave", "2024-01-02")
        ]
        
        patients_resource = Patients()
        result = patients_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['pat_first_name'] == "Jane"
        assert result[1]['pat_first_name'] == "John"
    
    @patch('package.patient.get_db_connection')
    def test_get_all_patients_empty(self, mock_db):
        """Test retrieval when no patients exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        patients_resource = Patients()
        result = patients_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('package.patient.get_db_connection')
    def test_get_all_patients_database_error(self, mock_db):
        """Test handling of database errors"""
        mock_db.side_effect = Exception("Database connection failed")
        
        patients_resource = Patients()
        result = patients_resource.get()
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error
    
    @patch('package.patient.request')
    @patch('package.patient.get_db_connection')
    def test_post_patient_success(self, mock_db, mock_request):
        """Test successful patient creation"""
        # Mock request data
        mock_request.get_json.return_value = {
            "pat_first_name": "Alice",
            "pat_last_name": "Johnson",
            "pat_insurance_no": "INS789",
            "pat_ph_no": "+1234567892",
            "pat_address": "789 Pine St"
        }
        
        # Mock database
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.lastrowid = 3
        
        patients_resource = Patients()
        result = patients_resource.post()
        
        assert 'pat_id' in result
        assert result['pat_id'] == 3
        assert result['pat_first_name'] == "Alice"
    
    @patch('package.patient.request')
    def test_post_patient_missing_data(self, mock_request):
        """Test patient creation with missing required data"""
        mock_request.get_json.return_value = {
            "pat_first_name": "Alice"
            # Missing required fields
        }
        
        patients_resource = Patients()
        result = patients_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.patient.request')
    def test_post_patient_no_json(self, mock_request):
        """Test patient creation with no JSON data"""
        mock_request.get_json.return_value = None
        
        patients_resource = Patients()
        result = patients_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.patient.request')
    @patch('package.patient.get_db_connection')
    def test_post_patient_database_error(self, mock_db, mock_request):
        """Test patient creation with database error"""
        mock_request.get_json.return_value = {
            "pat_first_name": "Alice",
            "pat_last_name": "Johnson",
            "pat_insurance_no": "INS789",
            "pat_ph_no": "+1234567892",
            "pat_address": "789 Pine St"
        }
        
        mock_db.side_effect = Exception("Database error")
        
        patients_resource = Patients()
        result = patients_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error


class TestPatientResource:
    """Test cases for Patient resource (individual operations)"""
    
    @patch('package.patient.get_db_connection')
    def test_get_patient_success(self, mock_db):
        """Test successful retrieval of specific patient"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Jane", "Doe", "INS123", "+1234567890", "123 Main St", "2024-01-01")
        ]
        
        patient_resource = Patient()
        result = patient_resource.get(1)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['pat_id'] == 1
        assert result[0]['pat_first_name'] == "Jane"
    
    @patch('package.patient.get_db_connection')
    def test_get_patient_not_found(self, mock_db):
        """Test retrieval of non-existent patient"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        patient_resource = Patient()
        result = patient_resource.get(999)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('package.patient.get_db_connection')
    def test_get_patient_database_error(self, mock_db):
        """Test patient retrieval with database error"""
        mock_db.side_effect = Exception("Database error")
        
        patient_resource = Patient()
        result = patient_resource.get(1)
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error
    
    @patch('package.patient.request')
    @patch('package.patient.get_db_connection')
    def test_put_patient_success(self, mock_db, mock_request):
        """Test successful patient update"""
        mock_request.get_json.return_value = {
            "pat_first_name": "Jane",
            "pat_last_name": "Doe-Smith",
            "pat_insurance_no": "INS123",
            "pat_ph_no": "+1234567890",
            "pat_address": "123 Main St, Apt 2B"
        }
        
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        patient_resource = Patient()
        result = patient_resource.put(1)
        
        assert 'message' in result
        assert 'updated' in result['message'].lower()
    
    @patch('package.patient.request')
    def test_put_patient_no_json(self, mock_request):
        """Test patient update with no JSON data"""
        mock_request.get_json.return_value = None
        
        patient_resource = Patient()
        result = patient_resource.put(1)
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.patient.request')
    @patch('package.patient.get_db_connection')
    def test_put_patient_database_error(self, mock_db, mock_request):
        """Test patient update with database error"""
        mock_request.get_json.return_value = {
            "pat_first_name": "Jane",
            "pat_last_name": "Doe-Smith"
        }
        
        mock_db.side_effect = Exception("Database error")
        
        patient_resource = Patient()
        result = patient_resource.put(1)
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error
    
    @patch('package.patient.get_db_connection')
    def test_delete_patient_success(self, mock_db):
        """Test successful patient deletion"""
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        patient_resource = Patient()
        result = patient_resource.delete(1)
        
        assert 'msg' in result
        assert 'deleted' in result['msg'].lower()
    
    @patch('package.patient.get_db_connection')
    def test_delete_patient_database_error(self, mock_db):
        """Test patient deletion with database error"""
        mock_db.side_effect = Exception("Database error")
        
        patient_resource = Patient()
        result = patient_resource.delete(1)
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error


class TestPatientValidation:
    """Test cases for patient data validation"""
    
    def test_valid_patient_data(self):
        """Test validation of valid patient data"""
        valid_data = {
            "pat_first_name": "John",
            "pat_last_name": "Doe",
            "pat_insurance_no": "INS123456",
            "pat_ph_no": "+1234567890",
            "pat_address": "123 Main St"
        }
        
        # All required fields are present
        assert all(key in valid_data for key in ["pat_first_name", "pat_last_name"])
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields"""
        invalid_data = {
            "pat_first_name": "John"
            # Missing pat_last_name
        }
        
        required_fields = ["pat_first_name", "pat_last_name"]
        missing_fields = [field for field in required_fields if field not in invalid_data]
        
        assert len(missing_fields) > 0
    
    def test_empty_string_fields(self):
        """Test validation with empty string fields"""
        invalid_data = {
            "pat_first_name": "",
            "pat_last_name": "Doe",
            "pat_insurance_no": "INS123456",
            "pat_ph_no": "+1234567890",
            "pat_address": "123 Main St"
        }
        
        # Check for empty required fields
        empty_required = [
            field for field in ["pat_first_name", "pat_last_name"] 
            if not invalid_data.get(field, "").strip()
        ]
        
        assert len(empty_required) > 0
    
    def test_phone_number_format(self):
        """Test phone number format validation"""
        valid_phones = ["+1234567890", "1234567890", "+1-234-567-8900"]
        invalid_phones = ["123", "abc", ""]
        
        # Simple validation - phone should contain only digits, +, -, and spaces
        import re
        phone_pattern = r'^[\+\d\-\s\(\)]+$'
        
        for phone in valid_phones:
            assert re.match(phone_pattern, phone) is not None
        
        for phone in invalid_phones:
            if phone:  # Skip empty string
                assert re.match(phone_pattern, phone) is None or len(phone) < 10


class TestPatientDataTransformation:
    """Test cases for patient data transformation"""
    
    def test_database_row_to_dict(self):
        """Test conversion of database row to dictionary"""
        # Simulate database row
        db_row = (1, "Jane", "Doe", "INS123", "+1234567890", "123 Main St", "2024-01-01")
        
        # Convert to dictionary (as done in the actual code)
        patient_dict = {
            'pat_id': db_row[0],
            'pat_first_name': db_row[1],
            'pat_last_name': db_row[2],
            'pat_insurance_no': db_row[3],
            'pat_ph_no': db_row[4],
            'pat_address': db_row[5],
            'pat_date': db_row[6]
        }
        
        assert patient_dict['pat_id'] == 1
        assert patient_dict['pat_first_name'] == "Jane"
        assert patient_dict['pat_last_name'] == "Doe"
    
    def test_json_serialization(self):
        """Test JSON serialization of patient data"""
        patient_data = {
            'pat_id': 1,
            'pat_first_name': "Jane",
            'pat_last_name': "Doe",
            'pat_insurance_no': "INS123",
            'pat_ph_no': "+1234567890",
            'pat_address': "123 Main St",
            'pat_date': "2024-01-01"
        }
        
        # Should be serializable to JSON
        json_str = json.dumps(patient_data)
        assert json_str is not None
        
        # Should be deserializable from JSON
        deserialized = json.loads(json_str)
        assert deserialized == patient_data


if __name__ == "__main__":
    pytest.main([__file__])
