"""
Unit tests for authentication module
"""

import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from package.auth import generate_token, verify_token, auth_required, role_required
from werkzeug.security import generate_password_hash, check_password_hash


class TestAuthModule:
    """Test cases for authentication module"""
    
    def test_generate_token_valid_user(self):
        """Test token generation for valid user"""
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "role": "admin"
        }
        
        token = generate_token(user_data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_generate_token_missing_data(self):
        """Test token generation with missing user data"""
        with pytest.raises((KeyError, TypeError)):
            generate_token({})
    
    def test_verify_token_valid(self):
        """Test token verification with valid token"""
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "role": "admin"
        }
        
        token = generate_token(user_data)
        decoded_data = verify_token(token)
        
        assert decoded_data is not None
        assert decoded_data["user_id"] == user_data["user_id"]
        assert decoded_data["username"] == user_data["username"]
        assert decoded_data["role"] == user_data["role"]
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token"""
        invalid_token = "invalid.token.here"
        
        decoded_data = verify_token(invalid_token)
        
        assert decoded_data is None
    
    def test_verify_token_expired(self):
        """Test token verification with expired token"""
        # Create an expired token
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "role": "admin",
            "exp": datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
        }
        
        # Mock the JWT secret
        with patch('package.auth.JWT_SECRET', 'test_secret'):
            expired_token = jwt.encode(user_data, 'test_secret', algorithm='HS256')
            decoded_data = verify_token(expired_token)
            
            assert decoded_data is None
    
    def test_verify_token_none(self):
        """Test token verification with None token"""
        decoded_data = verify_token(None)
        assert decoded_data is None
    
    def test_verify_token_empty_string(self):
        """Test token verification with empty string"""
        decoded_data = verify_token("")
        assert decoded_data is None
    
    @patch('package.auth.request')
    def test_auth_required_decorator_valid_token(self, mock_request):
        """Test auth_required decorator with valid token"""
        # Mock request headers
        user_data = {"user_id": 1, "username": "testuser", "role": "admin"}
        token = generate_token(user_data)
        
        mock_request.headers = {"Authorization": f"Bearer {token}"}
        
        @auth_required
        def test_function():
            return "success"
        
        result = test_function()
        assert result == "success"
    
    @patch('package.auth.request')
    def test_auth_required_decorator_missing_token(self, mock_request):
        """Test auth_required decorator with missing token"""
        mock_request.headers = {}
        
        @auth_required
        def test_function():
            return "success"
        
        result = test_function()
        
        # Should return error response
        assert isinstance(result, tuple)
        assert result[1] == 401  # Unauthorized
    
    @patch('package.auth.request')
    def test_auth_required_decorator_invalid_token(self, mock_request):
        """Test auth_required decorator with invalid token"""
        mock_request.headers = {"Authorization": "Bearer invalid_token"}
        
        @auth_required
        def test_function():
            return "success"
        
        result = test_function()
        
        # Should return error response
        assert isinstance(result, tuple)
        assert result[1] == 401  # Unauthorized
    
    @patch('package.auth.request')
    def test_role_required_decorator_valid_role(self, mock_request):
        """Test role_required decorator with valid role"""
        user_data = {"user_id": 1, "username": "testuser", "role": "admin"}
        token = generate_token(user_data)
        
        mock_request.headers = {"Authorization": f"Bearer {token}"}
        
        @role_required('admin')
        def test_function():
            return "success"
        
        result = test_function()
        assert result == "success"
    
    @patch('package.auth.request')
    def test_role_required_decorator_invalid_role(self, mock_request):
        """Test role_required decorator with invalid role"""
        user_data = {"user_id": 1, "username": "testuser", "role": "patient"}
        token = generate_token(user_data)
        
        mock_request.headers = {"Authorization": f"Bearer {token}"}
        
        @role_required('admin')
        def test_function():
            return "success"
        
        result = test_function()
        
        # Should return error response
        assert isinstance(result, tuple)
        assert result[1] == 403  # Forbidden
    
    @patch('package.auth.request')
    def test_role_required_decorator_multiple_roles(self, mock_request):
        """Test role_required decorator with multiple allowed roles"""
        user_data = {"user_id": 1, "username": "testuser", "role": "doctor"}
        token = generate_token(user_data)
        
        mock_request.headers = {"Authorization": f"Bearer {token}"}
        
        @role_required(['admin', 'doctor'])
        def test_function():
            return "success"
        
        result = test_function()
        assert result == "success"
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        password = "test_password_123"
        
        # Hash the password
        hashed = generate_password_hash(password)
        
        assert hashed is not None
        assert hashed != password  # Should be different from original
        assert len(hashed) > 0
        
        # Verify the password
        assert check_password_hash(hashed, password) is True
        assert check_password_hash(hashed, "wrong_password") is False
    
    def test_password_hashing_empty_password(self):
        """Test password hashing with empty password"""
        with pytest.raises(ValueError):
            generate_password_hash("")
    
    def test_password_hashing_none_password(self):
        """Test password hashing with None password"""
        with pytest.raises((ValueError, TypeError)):
            generate_password_hash(None)


class TestTokenSecurity:
    """Test cases for token security"""
    
    def test_token_contains_required_fields(self):
        """Test that generated tokens contain required fields"""
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "role": "admin"
        }
        
        token = generate_token(user_data)
        decoded = verify_token(token)
        
        assert "user_id" in decoded
        assert "username" in decoded
        assert "role" in decoded
        assert "exp" in decoded  # Expiration time
    
    def test_token_expiration_time(self):
        """Test that tokens have proper expiration time"""
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "role": "admin"
        }
        
        token = generate_token(user_data)
        decoded = verify_token(token)
        
        # Check that expiration is in the future
        exp_time = datetime.fromtimestamp(decoded["exp"])
        current_time = datetime.utcnow()
        
        assert exp_time > current_time
        
        # Check that expiration is within 24 hours (default)
        time_diff = exp_time - current_time
        assert time_diff.total_seconds() <= 24 * 60 * 60  # 24 hours
    
    def test_different_users_different_tokens(self):
        """Test that different users get different tokens"""
        user1_data = {
            "user_id": 1,
            "username": "user1",
            "role": "admin"
        }
        
        user2_data = {
            "user_id": 2,
            "username": "user2",
            "role": "doctor"
        }
        
        token1 = generate_token(user1_data)
        token2 = generate_token(user2_data)
        
        assert token1 != token2
    
    def test_same_user_different_tokens_over_time(self):
        """Test that same user gets different tokens when generated at different times"""
        import time
        
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "role": "admin"
        }
        
        token1 = generate_token(user_data)
        time.sleep(1)  # Wait 1 second
        token2 = generate_token(user_data)
        
        # Tokens should be different due to different timestamps
        assert token1 != token2


if __name__ == "__main__":
    pytest.main([__file__])
