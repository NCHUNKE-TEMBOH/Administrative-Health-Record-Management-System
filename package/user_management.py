from flask_restful import Resource, request
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from package.model import conn
from package.auth import login_required, role_required, get_current_user, log_access, authenticate_user, generate_token, AuthenticationError
import re

class UserLogin(Resource):
    """Handle user authentication"""

    def post(self):
        """Authenticate user and return JWT token"""
        try:
            data = request.get_json(force=True)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'error': 'Username and password required'}, 400

            user = authenticate_user(username, password)

            # Generate JWT token
            token = generate_token(user['user_id'], user['username'], user['role'])

            log_access(user['user_id'], 'LOGIN', 'AUTH', success=True)

            return {
                'token': token,
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'role': user['role'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            }, 200

        except AuthenticationError as e:
            return {'error': str(e)}, 401
        except Exception as e:
            return {'error': 'Login failed'}, 500

class UserProfile(Resource):
    """Handle user profile operations"""

    @login_required
    def get(self):
        """Get current user profile"""
        current_user = get_current_user()

        user_data = {
            'user_id': current_user['user_id'],
            'username': current_user['username'],
            'email': current_user['email'],
            'role': current_user['role'],
            'first_name': current_user['first_name'],
            'last_name': current_user['last_name'],
            'phone_number': current_user['phone_number'],
            'created_date': current_user['created_date'],
            'last_login': current_user['last_login']
        }

        return user_data, 200

    @login_required
    def put(self):
        """Update current user profile"""
        current_user = get_current_user()
        data = request.get_json(force=True)

        # Fields that can be updated by user
        updatable_fields = ['first_name', 'last_name', 'phone_number', 'email']
        update_data = {}

        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]

        if not update_data:
            return {'error': 'No valid fields to update'}, 400

        # Validate email format if provided
        if 'email' in update_data:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', update_data['email']):
                return {'error': 'Invalid email format'}, 400

        try:
            # Build dynamic update query
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values()) + [current_user['user_id']]

            conn.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
            conn.commit()

            log_access(current_user['user_id'], 'UPDATE_PROFILE', 'USER', current_user['user_id'])

            return {'message': 'Profile updated successfully'}, 200

        except Exception as e:
            return {'error': 'Failed to update profile'}, 500

class Users(Resource):
    """Handle user management operations (Admin only)"""

    @role_required('admin')
    def get(self):
        """Get all users (Admin only)"""
        current_user = get_current_user()

        users_rows = conn.execute("""
            SELECT user_id, username, email, role, first_name, last_name,
                   phone_number, is_active, created_date, last_login, entity_id
            FROM users
            ORDER BY created_date DESC
        """).fetchall()

        # Convert Row objects to dictionaries
        users = []
        for row in users_rows:
            users.append({
                'user_id': row['user_id'],
                'username': row['username'],
                'email': row['email'],
                'role': row['role'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'is_active': row['is_active'],
                'created_date': row['created_date'],
                'last_login': row['last_login'],
                'entity_id': row['entity_id']
            })

        log_access(current_user['user_id'], 'LIST_USERS', 'USER')

        return users, 200

    @role_required('admin')
    def post(self):
        """Create new user (Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)

        # Required fields
        required_fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'{field} is required'}, 400

        # Validate role
        valid_roles = ['admin', 'doctor', 'nurse', 'lab_technician', 'pharmacist', 'patient']
        if data['role'] not in valid_roles:
            return {'error': 'Invalid role'}, 400

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return {'error': 'Invalid email format'}, 400

        # Check if username or email already exists
        existing_user = conn.execute(
            "SELECT user_id FROM users WHERE username = ? OR email = ?",
            (data['username'], data['email'])
        ).fetchone()

        if existing_user:
            return {'error': 'Username or email already exists'}, 400

        try:
            # Hash password
            password_hash = generate_password_hash(data['password'])

            # Insert new user
            user_id = conn.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number, entity_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['username'],
                data['email'],
                password_hash,
                data['role'],
                data['first_name'],
                data['last_name'],
                data.get('phone_number'),
                data.get('entity_id')
            )).lastrowid

            conn.commit()

            log_access(current_user['user_id'], 'CREATE_USER', 'USER', user_id)

            return {
                'message': 'User created successfully',
                'user_id': user_id
            }, 201

        except Exception as e:
            return {'error': 'Failed to create user'}, 500

class User(Resource):
    """Handle individual user operations"""

    @role_required('admin')
    def get(self, user_id):
        """Get user by ID (Admin only)"""
        current_user = get_current_user()

        user_row = conn.execute("""
            SELECT user_id, username, email, role, first_name, last_name,
                   phone_number, is_active, created_date, last_login, entity_id
            FROM users
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        if not user_row:
            return {'error': 'User not found'}, 404

        # Convert Row object to dictionary
        user = {
            'user_id': user_row['user_id'],
            'username': user_row['username'],
            'email': user_row['email'],
            'role': user_row['role'],
            'first_name': user_row['first_name'],
            'last_name': user_row['last_name'],
            'phone_number': user_row['phone_number'],
            'is_active': user_row['is_active'],
            'created_date': user_row['created_date'],
            'last_login': user_row['last_login'],
            'entity_id': user_row['entity_id']
        }

        log_access(current_user['user_id'], 'VIEW_USER', 'USER', user_id)

        return user, 200

    @role_required('admin')
    def put(self, user_id):
        """Update user (Admin only)"""
        current_user = get_current_user()
        data = request.get_json(force=True)

        # Check if user exists
        user = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not user:
            return {'error': 'User not found'}, 404

        # Fields that can be updated
        updatable_fields = ['username', 'email', 'role', 'first_name', 'last_name', 'phone_number', 'is_active', 'entity_id']
        update_data = {}

        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]

        # Handle password update separately
        if 'password' in data and data['password']:
            update_data['password_hash'] = generate_password_hash(data['password'])

        if not update_data:
            return {'error': 'No valid fields to update'}, 400

        # Validate email format if provided
        if 'email' in update_data:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', update_data['email']):
                return {'error': 'Invalid email format'}, 400

        # Validate role if provided
        if 'role' in update_data:
            valid_roles = ['admin', 'doctor', 'nurse', 'lab_technician', 'pharmacist', 'patient']
            if update_data['role'] not in valid_roles:
                return {'error': 'Invalid role'}, 400

        try:
            # Build dynamic update query
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values()) + [user_id]

            conn.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
            conn.commit()

            log_access(current_user['user_id'], 'UPDATE_USER', 'USER', user_id)

            return {'message': 'User updated successfully'}, 200

        except Exception as e:
            return {'error': 'Failed to update user'}, 500

    @role_required('admin')
    def delete(self, user_id):
        """Deactivate user (Admin only) - We don't actually delete for audit purposes"""
        current_user = get_current_user()

        # Check if user exists
        user = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not user:
            return {'error': 'User not found'}, 404

        # Prevent admin from deactivating themselves
        if user_id == current_user['user_id']:
            return {'error': 'Cannot deactivate your own account'}, 400

        try:
            conn.execute("UPDATE users SET is_active = 0 WHERE user_id = ?", (user_id,))
            conn.commit()

            log_access(current_user['user_id'], 'DEACTIVATE_USER', 'USER', user_id)

            return {'message': 'User deactivated successfully'}, 200

        except Exception as e:
            return {'error': 'Failed to deactivate user'}, 500

class ChangePassword(Resource):
    """Handle password change"""

    @login_required
    def post(self):
        """Change user password"""
        current_user = get_current_user()
        data = request.get_json(force=True)

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return {'error': 'Current password and new password required'}, 400

        # Verify current password
        user = conn.execute(
            "SELECT password_hash FROM users WHERE user_id = ?",
            (current_user['user_id'],)
        ).fetchone()

        if not check_password_hash(user['password_hash'], current_password):
            return {'error': 'Current password is incorrect'}, 400

        # Validate new password strength (basic validation)
        if len(new_password) < 6:
            return {'error': 'New password must be at least 6 characters long'}, 400

        try:
            # Update password
            new_password_hash = generate_password_hash(new_password)
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE user_id = ?",
                (new_password_hash, current_user['user_id'])
            )
            conn.commit()

            log_access(current_user['user_id'], 'CHANGE_PASSWORD', 'USER', current_user['user_id'])

            return {'message': 'Password changed successfully'}, 200

        except Exception as e:
            return {'error': 'Failed to change password'}, 500
