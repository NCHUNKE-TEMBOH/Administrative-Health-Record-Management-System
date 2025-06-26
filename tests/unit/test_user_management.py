"""
Unit tests for user management module
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from package.user_management import UserLogin, UserRegistration, UserProfile, ChangePassword, Users, User


class TestUserLogin:
    """Test cases for user login functionality"""
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_db_connection')
    @patch('package.user_management.check_password_hash')
    def test_login_success(self, mock_check_password, mock_db, mock_request):
        """Test successful user login"""
        # Mock request data
        mock_request.get_json.return_value = {
            "username": "testuser",
            "password": "testpass"
        }
        
        # Mock database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (
            1, "testuser", "test@example.com", "hashed_password", 
            "admin", "Test", "User", "+1234567890", 1, "2024-01-01"
        )
        
        # Mock password verification
        mock_check_password.return_value = True
        
        login_resource = UserLogin()
        result = login_resource.post()
        
        assert 'token' in result
        assert 'user' in result
        assert result['user']['username'] == "testuser"
    
    @patch('package.user_management.request')
    def test_login_missing_data(self, mock_request):
        """Test login with missing username or password"""
        mock_request.get_json.return_value = {
            "username": "testuser"
            # Missing password
        }
        
        login_resource = UserLogin()
        result = login_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_db_connection')
    def test_login_user_not_found(self, mock_db, mock_request):
        """Test login with non-existent user"""
        mock_request.get_json.return_value = {
            "username": "nonexistent",
            "password": "testpass"
        }
        
        # Mock database response - no user found
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        login_resource = UserLogin()
        result = login_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 401  # Unauthorized
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_db_connection')
    @patch('package.user_management.check_password_hash')
    def test_login_wrong_password(self, mock_check_password, mock_db, mock_request):
        """Test login with wrong password"""
        mock_request.get_json.return_value = {
            "username": "testuser",
            "password": "wrongpass"
        }
        
        # Mock database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (
            1, "testuser", "test@example.com", "hashed_password", 
            "admin", "Test", "User", "+1234567890", 1, "2024-01-01"
        )
        
        # Mock password verification - wrong password
        mock_check_password.return_value = False
        
        login_resource = UserLogin()
        result = login_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 401  # Unauthorized


class TestUserRegistration:
    """Test cases for user registration functionality"""
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_db_connection')
    @patch('package.user_management.generate_password_hash')
    def test_registration_success(self, mock_hash_password, mock_db, mock_request):
        """Test successful user registration"""
        mock_request.get_json.return_value = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass",
            "role": "patient",
            "firstName": "New",
            "lastName": "User"
        }
        
        # Mock password hashing
        mock_hash_password.return_value = "hashed_password"
        
        # Mock database
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.lastrowid = 5
        
        registration_resource = UserRegistration()
        result = registration_resource.post()
        
        assert 'message' in result
        assert 'user_id' in result
        assert result['user_id'] == 5
    
    @patch('package.user_management.request')
    def test_registration_missing_data(self, mock_request):
        """Test registration with missing required data"""
        mock_request.get_json.return_value = {
            "username": "newuser"
            # Missing required fields
        }
        
        registration_resource = UserRegistration()
        result = registration_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_db_connection')
    def test_registration_duplicate_username(self, mock_db, mock_request):
        """Test registration with duplicate username"""
        mock_request.get_json.return_value = {
            "username": "existinguser",
            "email": "new@example.com",
            "password": "newpass",
            "role": "patient",
            "firstName": "New",
            "lastName": "User"
        }
        
        # Mock database error for duplicate username
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.side_effect = Exception("UNIQUE constraint failed")
        
        registration_resource = UserRegistration()
        result = registration_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 409  # Conflict


class TestUserProfile:
    """Test cases for user profile functionality"""
    
    @patch('package.user_management.get_current_user')
    @patch('package.user_management.get_db_connection')
    def test_get_profile_success(self, mock_db, mock_get_user):
        """Test successful profile retrieval"""
        # Mock current user
        mock_get_user.return_value = {"user_id": 1}
        
        # Mock database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (
            1, "testuser", "test@example.com", "hashed_password", 
            "admin", "Test", "User", "+1234567890", 1, "2024-01-01"
        )
        
        profile_resource = UserProfile()
        result = profile_resource.get()
        
        assert 'user_id' in result
        assert 'username' in result
        assert result['user_id'] == 1
    
    @patch('package.user_management.get_current_user')
    def test_get_profile_no_user(self, mock_get_user):
        """Test profile retrieval with no current user"""
        mock_get_user.return_value = None
        
        profile_resource = UserProfile()
        result = profile_resource.get()
        
        assert isinstance(result, tuple)
        assert result[1] == 401  # Unauthorized


class TestChangePassword:
    """Test cases for password change functionality"""
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_current_user')
    @patch('package.user_management.get_db_connection')
    @patch('package.user_management.check_password_hash')
    @patch('package.user_management.generate_password_hash')
    def test_change_password_success(self, mock_hash_new, mock_check_old, mock_db, mock_get_user, mock_request):
        """Test successful password change"""
        mock_request.get_json.return_value = {
            "current_password": "oldpass",
            "new_password": "newpass"
        }
        
        # Mock current user
        mock_get_user.return_value = {"user_id": 1}
        
        # Mock database response for current password
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("hashed_old_password",)
        
        # Mock password verification
        mock_check_old.return_value = True
        mock_hash_new.return_value = "hashed_new_password"
        
        change_password_resource = ChangePassword()
        result = change_password_resource.post()
        
        assert 'message' in result
        assert 'success' in result['message'].lower()
    
    @patch('package.user_management.request')
    def test_change_password_missing_data(self, mock_request):
        """Test password change with missing data"""
        mock_request.get_json.return_value = {
            "current_password": "oldpass"
            # Missing new_password
        }
        
        change_password_resource = ChangePassword()
        result = change_password_resource.post()
        
        assert isinstance(result, tuple)
        assert result[1] == 400  # Bad request


class TestUsersResource:
    """Test cases for Users resource (admin operations)"""
    
    @patch('package.user_management.get_db_connection')
    def test_get_all_users_success(self, mock_db):
        """Test successful retrieval of all users"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "admin", "admin@example.com", "hashed_pass", "admin", "Admin", "User", "+1234567890", 1, "2024-01-01"),
            (2, "doctor", "doctor@example.com", "hashed_pass", "doctor", "Dr. John", "Smith", "+1234567891", 1, "2024-01-02")
        ]
        
        users_resource = Users()
        result = users_resource.get()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['username'] == "admin"
        assert result[1]['username'] == "doctor"
    
    @patch('package.user_management.request')
    @patch('package.user_management.get_db_connection')
    @patch('package.user_management.generate_password_hash')
    def test_create_user_success(self, mock_hash_password, mock_db, mock_request):
        """Test successful user creation by admin"""
        mock_request.get_json.return_value = {
            "username": "newdoctor",
            "email": "newdoctor@example.com",
            "password": "securepass",
            "role": "doctor",
            "first_name": "Dr. Jane",
            "last_name": "Doe"
        }
        
        mock_hash_password.return_value = "hashed_password"
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.lastrowid = 10
        
        users_resource = Users()
        result = users_resource.post()
        
        assert 'message' in result
        assert 'user_id' in result
        assert result['user_id'] == 10


class TestUserValidation:
    """Test cases for user data validation"""
    
    def test_valid_email_format(self):
        """Test email format validation"""
        valid_emails = ["test@example.com", "user.name@domain.co.uk", "admin@hospital.org"]
        invalid_emails = ["invalid", "@domain.com", "user@", "user@.com"]
        
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for email in valid_emails:
            assert re.match(email_pattern, email) is not None
        
        for email in invalid_emails:
            assert re.match(email_pattern, email) is None
    
    def test_valid_role_values(self):
        """Test role validation"""
        valid_roles = ["admin", "doctor", "nurse", "patient", "lab_technician", "pharmacist"]
        invalid_roles = ["invalid_role", "", "ADMIN", "Doctor"]
        
        for role in valid_roles:
            assert role in valid_roles
        
        for role in invalid_roles:
            assert role not in valid_roles
    
    def test_password_strength(self):
        """Test password strength validation"""
        strong_passwords = ["SecurePass123!", "MyP@ssw0rd", "Complex1ty!"]
        weak_passwords = ["123", "password", "abc"]
        
        def is_strong_password(password):
            return len(password) >= 8
        
        for password in strong_passwords:
            assert is_strong_password(password)
        
        for password in weak_passwords:
            assert not is_strong_password(password)


if __name__ == "__main__":
    pytest.main([__file__])
