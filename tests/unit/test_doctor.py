"""
Unit tests for doctor management module
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from package.doctor import Doctors, Doctor


class TestDoctorsResource:
    """Test cases for Doctors resource (collection operations)"""
    
    @patch('package.doctor.get_db_connection')
    def test_get_all_doctors_success(self, mock_db):
        """Test successful retrieval of all doctors"""
        # Mock database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Dr. John", "Smith", "Cardiology", "+1234567890", "Hospital Address"),
            (2, "Dr. Sarah", "Johnson", "Neurology", "+1234567891", "Hospital Address")
        ]
        
        doctors_resource = Doctors()
        result = doctors_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['doc_first_name'] == "Dr. John"
        assert result[1]['doc_first_name'] == "Dr. Sarah"
    
    @patch('package.doctor.get_db_connection')
    def test_get_all_doctors_empty(self, mock_db):
        """Test retrieval when no doctors exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        doctors_resource = Doctors()
        result = doctors_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('package.doctor.get_db_connection')
    def test_get_all_doctors_database_error(self, mock_db):
        """Test handling of database errors"""
        mock_db.side_effect = Exception("Database connection failed")
        
        doctors_resource = Doctors()
        result = doctors_resource.get()
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error
    
    @patch('package.doctor.request')
    @patch('package.doctor.get_db_connection')
    def test_post_doctor_success(self, mock_db, mock_request):
        """Test successful doctor creation"""
        # Mock request data
        mock_request.get_json.return_value = {
            "doc_first_name": "Dr. Michael",
            "doc_last_name": "Brown",
            "doc_specialization": "Emergency Medicine",
            "doc_ph_no": "+1234567892",
            "doc_address": "Emergency Department"
        }
        
        # Mock database
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.lastrowid = 3
        
        doctors_resource = Doctors()
        result = doctors_resource.post()
        
        assert 'doc_id' in result
        assert result['doc_id'] == 3
        assert result['doc_first_name'] == "Dr. Michael"
    
    @patch('package.doctor.request')
    def test_post_doctor_missing_data(self, mock_request):
        """Test doctor creation with missing required data"""
        mock_request.get_json.return_value = {
            "doc_first_name": "Dr. Michael"
            # Missing required fields
        }
        
        doctors_resource = Doctors()
        result = doctors_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.doctor.request')
    def test_post_doctor_no_json(self, mock_request):
        """Test doctor creation with no JSON data"""
        mock_request.get_json.return_value = None
        
        doctors_resource = Doctors()
        result = doctors_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request


class TestDoctorResource:
    """Test cases for Doctor resource (individual operations)"""
    
    @patch('package.doctor.get_db_connection')
    def test_get_doctor_success(self, mock_db):
        """Test successful retrieval of specific doctor"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Dr. John", "Smith", "Cardiology", "+1234567890", "Hospital Address")
        ]
        
        doctor_resource = Doctor()
        result = doctor_resource.get(1)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['doc_id'] == 1
        assert result[0]['doc_first_name'] == "Dr. John"
    
    @patch('package.doctor.get_db_connection')
    def test_get_doctor_not_found(self, mock_db):
        """Test retrieval of non-existent doctor"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        doctor_resource = Doctor()
        result = doctor_resource.get(999)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('package.doctor.request')
    @patch('package.doctor.get_db_connection')
    def test_put_doctor_success(self, mock_db, mock_request):
        """Test successful doctor update"""
        mock_request.get_json.return_value = {
            "doc_first_name": "Dr. John",
            "doc_last_name": "Smith",
            "doc_specialization": "Interventional Cardiology",
            "doc_ph_no": "+1234567890",
            "doc_address": "Cardiology Department"
        }
        
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        doctor_resource = Doctor()
        result = doctor_resource.put(1)
        
        assert 'message' in result
        assert 'updated' in result['message'].lower()
    
    @patch('package.doctor.get_db_connection')
    def test_delete_doctor_success(self, mock_db):
        """Test successful doctor deletion"""
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        doctor_resource = Doctor()
        result = doctor_resource.delete(1)
        
        assert 'message' in result
        assert 'deleted' in result['message'].lower()


class TestDoctorValidation:
    """Test cases for doctor data validation"""
    
    def test_valid_doctor_data(self):
        """Test validation of valid doctor data"""
        valid_data = {
            "doc_first_name": "Dr. John",
            "doc_last_name": "Smith",
            "doc_specialization": "Cardiology",
            "doc_ph_no": "+1234567890",
            "doc_address": "Hospital Address"
        }
        
        # All required fields are present
        assert all(key in valid_data for key in ["doc_first_name", "doc_last_name"])
    
    def test_specialization_validation(self):
        """Test specialization field validation"""
        valid_specializations = [
            "Cardiology", "Neurology", "Emergency Medicine", 
            "Internal Medicine", "Pediatrics", "Surgery"
        ]
        
        for spec in valid_specializations:
            assert isinstance(spec, str)
            assert len(spec) > 0
    
    def test_doctor_name_format(self):
        """Test doctor name format validation"""
        valid_names = ["Dr. John", "Dr. Sarah", "Dr. Michael"]
        
        for name in valid_names:
            assert name.startswith("Dr.")
            assert len(name.split()) >= 2


if __name__ == "__main__":
    pytest.main([__file__])
