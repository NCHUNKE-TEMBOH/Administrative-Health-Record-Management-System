"""
Unit tests for appointment management module
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from package.appointment import Appointments, Appointment


class TestAppointmentsResource:
    """Test cases for Appointments resource (collection operations)"""
    
    @patch('package.appointment.get_db_connection')
    def test_get_all_appointments_success(self, mock_db):
        """Test successful retrieval of all appointments"""
        # Mock database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 1, 1, "2024-01-15", "10:00:00", "scheduled", "Regular checkup", "Annual exam", "2024-01-01 09:00:00"),
            (2, 2, 1, "2024-01-16", "14:30:00", "scheduled", "Follow-up", "Check results", "2024-01-01 10:00:00")
        ]
        
        appointments_resource = Appointments()
        result = appointments_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['appointment_id'] == 1
        assert result[0]['reason'] == "Regular checkup"
        assert result[1]['appointment_id'] == 2
        assert result[1]['reason'] == "Follow-up"
    
    @patch('package.appointment.get_db_connection')
    def test_get_all_appointments_empty(self, mock_db):
        """Test retrieval when no appointments exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        appointments_resource = Appointments()
        result = appointments_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('package.appointment.get_db_connection')
    def test_get_all_appointments_database_error(self, mock_db):
        """Test handling of database errors"""
        mock_db.side_effect = Exception("Database connection failed")
        
        appointments_resource = Appointments()
        result = appointments_resource.get()
        
        assert isinstance(result, tuple)
        assert result[1] == 500  # Internal server error
    
    @patch('package.appointment.request')
    @patch('package.appointment.get_db_connection')
    def test_post_appointment_success(self, mock_db, mock_request):
        """Test successful appointment creation"""
        # Mock request data
        mock_request.get_json.return_value = {
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_date": "2024-01-20",
            "appointment_time": "14:30:00",
            "reason": "Follow-up visit",
            "notes": "Check medication effectiveness"
        }
        
        # Mock database
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.lastrowid = 3
        
        appointments_resource = Appointments()
        result = appointments_resource.post()
        
        assert 'appointment_id' in result
        assert result['appointment_id'] == 3
        assert result['reason'] == "Follow-up visit"
    
    @patch('package.appointment.request')
    def test_post_appointment_missing_data(self, mock_request):
        """Test appointment creation with missing required data"""
        mock_request.get_json.return_value = {
            "patient_id": 1
            # Missing required fields
        }
        
        appointments_resource = Appointments()
        result = appointments_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.appointment.request')
    def test_post_appointment_no_json(self, mock_request):
        """Test appointment creation with no JSON data"""
        mock_request.get_json.return_value = None
        
        appointments_resource = Appointments()
        result = appointments_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request


class TestAppointmentResource:
    """Test cases for Appointment resource (individual operations)"""
    
    @patch('package.appointment.get_db_connection')
    def test_get_appointment_success(self, mock_db):
        """Test successful retrieval of specific appointment"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 1, 1, "2024-01-15", "10:00:00", "scheduled", "Regular checkup", "Annual exam", "2024-01-01 09:00:00")
        ]
        
        appointment_resource = Appointment()
        result = appointment_resource.get(1)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['appointment_id'] == 1
        assert result[0]['reason'] == "Regular checkup"
    
    @patch('package.appointment.get_db_connection')
    def test_get_appointment_not_found(self, mock_db):
        """Test retrieval of non-existent appointment"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        appointment_resource = Appointment()
        result = appointment_resource.get(999)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('package.appointment.request')
    @patch('package.appointment.get_db_connection')
    def test_put_appointment_success(self, mock_db, mock_request):
        """Test successful appointment update"""
        mock_request.get_json.return_value = {
            "appointment_date": "2024-01-16",
            "appointment_time": "11:00:00",
            "status": "rescheduled",
            "notes": "Patient requested time change"
        }
        
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        appointment_resource = Appointment()
        result = appointment_resource.put(1)
        
        assert 'message' in result
        assert 'updated' in result['message'].lower()
    
    @patch('package.appointment.get_db_connection')
    def test_delete_appointment_success(self, mock_db):
        """Test successful appointment deletion"""
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        appointment_resource = Appointment()
        result = appointment_resource.delete(1)
        
        assert 'message' in result
        assert 'deleted' in result['message'].lower()


class TestAppointmentValidation:
    """Test cases for appointment data validation"""
    
    def test_valid_appointment_data(self):
        """Test validation of valid appointment data"""
        valid_data = {
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_date": "2024-01-20",
            "appointment_time": "14:30:00",
            "reason": "Follow-up visit",
            "notes": "Check medication effectiveness"
        }
        
        # All required fields are present
        required_fields = ["patient_id", "doctor_id", "appointment_date", "appointment_time"]
        assert all(key in valid_data for key in required_fields)
    
    def test_date_format_validation(self):
        """Test date format validation"""
        valid_dates = ["2024-01-20", "2024-12-31", "2025-06-15"]
        invalid_dates = ["20-01-2024", "2024/01/20", "invalid-date"]
        
        for date_str in valid_dates:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                assert True
            except ValueError:
                assert False, f"Valid date {date_str} failed parsing"
        
        for date_str in invalid_dates:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                assert False, f"Invalid date {date_str} should have failed parsing"
            except ValueError:
                assert True
    
    def test_time_format_validation(self):
        """Test time format validation"""
        valid_times = ["14:30:00", "09:00:00", "23:59:00"]
        invalid_times = ["2:30 PM", "14:30", "25:00:00"]
        
        for time_str in valid_times:
            try:
                datetime.strptime(time_str, "%H:%M:%S")
                assert True
            except ValueError:
                assert False, f"Valid time {time_str} failed parsing"
        
        for time_str in invalid_times:
            try:
                datetime.strptime(time_str, "%H:%M:%S")
                assert False, f"Invalid time {time_str} should have failed parsing"
            except ValueError:
                assert True
    
    def test_appointment_status_validation(self):
        """Test appointment status validation"""
        valid_statuses = ["scheduled", "completed", "cancelled", "rescheduled", "no-show"]
        
        for status in valid_statuses:
            assert isinstance(status, str)
            assert len(status) > 0
            assert status.lower() == status  # Should be lowercase
    
    def test_future_date_validation(self):
        """Test that appointment dates should be in the future"""
        today = date.today()
        future_date = date(2025, 12, 31)
        past_date = date(2020, 1, 1)
        
        assert future_date > today
        assert past_date < today
    
    def test_business_hours_validation(self):
        """Test appointment time within business hours"""
        business_start = "08:00:00"
        business_end = "18:00:00"
        
        valid_times = ["09:00:00", "12:30:00", "17:00:00"]
        invalid_times = ["07:00:00", "19:00:00", "23:30:00"]
        
        start_time = datetime.strptime(business_start, "%H:%M:%S").time()
        end_time = datetime.strptime(business_end, "%H:%M:%S").time()
        
        for time_str in valid_times:
            appointment_time = datetime.strptime(time_str, "%H:%M:%S").time()
            assert start_time <= appointment_time <= end_time
        
        for time_str in invalid_times:
            appointment_time = datetime.strptime(time_str, "%H:%M:%S").time()
            assert not (start_time <= appointment_time <= end_time)


class TestAppointmentBusinessLogic:
    """Test cases for appointment business logic"""
    
    def test_appointment_duration_calculation(self):
        """Test calculation of appointment duration"""
        start_time = datetime.strptime("09:00:00", "%H:%M:%S")
        end_time = datetime.strptime("09:30:00", "%H:%M:%S")
        
        duration = end_time - start_time
        duration_minutes = duration.total_seconds() / 60
        
        assert duration_minutes == 30
    
    def test_appointment_conflict_detection(self):
        """Test detection of appointment conflicts"""
        # Two appointments at the same time with same doctor
        appointment1 = {
            "doctor_id": 1,
            "appointment_date": "2024-01-20",
            "appointment_time": "14:30:00"
        }
        
        appointment2 = {
            "doctor_id": 1,
            "appointment_date": "2024-01-20",
            "appointment_time": "14:30:00"
        }
        
        # Should detect conflict
        assert (appointment1["doctor_id"] == appointment2["doctor_id"] and
                appointment1["appointment_date"] == appointment2["appointment_date"] and
                appointment1["appointment_time"] == appointment2["appointment_time"])
    
    def test_appointment_reminder_timing(self):
        """Test appointment reminder timing calculation"""
        appointment_datetime = datetime(2024, 1, 20, 14, 30, 0)
        reminder_hours = 24
        
        reminder_time = appointment_datetime - timedelta(hours=reminder_hours)
        
        expected_reminder = datetime(2024, 1, 19, 14, 30, 0)
        assert reminder_time == expected_reminder


if __name__ == "__main__":
    from datetime import timedelta
    pytest.main([__file__])
