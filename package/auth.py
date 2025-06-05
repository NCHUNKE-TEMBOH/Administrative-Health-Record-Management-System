from flask import request, jsonify, session, g
from functools import wraps
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from package.model import conn
import json

# Load config for JWT secret
with open('config.json') as data_file:
    config = json.load(data_file)

JWT_SECRET = config.get('jwt_secret', 'your-secret-key-change-this')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):
    pass

def generate_token(user_id, username, role):
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    user = conn.execute(
        "SELECT user_id, username, password_hash, role, first_name, last_name, is_active FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    
    if not user:
        raise AuthenticationError("Invalid username or password")
    
    if not user['is_active']:
        raise AuthenticationError("Account is deactivated")
    
    if not check_password_hash(user['password_hash'], password):
        raise AuthenticationError("Invalid username or password")
    
    # Update last login
    conn.execute(
        "UPDATE users SET last_login = datetime('now','localtime') WHERE user_id = ?",
        (user['user_id'],)
    )
    conn.commit()
    
    return user

def get_current_user():
    """Get current authenticated user from request context"""
    return getattr(g, 'current_user', None)

def log_access(user_id, action, resource_type, resource_id=None, patient_id=None, success=True):
    """Log user access for audit trail"""
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
    user_agent = request.environ.get('HTTP_USER_AGENT', '')
    
    conn.execute('''
        INSERT INTO access_logs (user_id, action, resource_type, resource_id, patient_id, ip_address, user_agent, success)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, action, resource_type, resource_id, patient_id, ip_address, user_agent, int(success)))
    conn.commit()

# Authentication decorator
def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        # Check for token in session (for web interface)
        elif 'token' in session:
            token = session['token']
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            payload = verify_token(token)
            
            # Get user details
            user = conn.execute(
                "SELECT * FROM users WHERE user_id = ? AND is_active = 1",
                (payload['user_id'],)
            ).fetchone()
            
            if not user:
                return jsonify({'error': 'User not found or inactive'}), 401
            
            # Store user in request context
            g.current_user = user
            
        except AuthenticationError as e:
            return jsonify({'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# Role-based authorization decorator
def role_required(*allowed_roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            
            if current_user['role'] not in allowed_roles:
                log_access(
                    current_user['user_id'], 
                    f"UNAUTHORIZED_ACCESS_{f.__name__}", 
                    "FUNCTION", 
                    success=False
                )
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

# Patient access control decorator
def patient_access_required(f):
    """Decorator to ensure user can only access their own patient data or has appropriate role"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()

        # Admin and doctors can access all patient data
        if current_user['role'] in ['admin', 'doctor']:
            return f(*args, **kwargs)

        # Get patient ID from URL parameters or query parameters
        patient_id = (kwargs.get('id') or
                     kwargs.get('pat_id') or
                     request.view_args.get('id') if request.view_args else None or
                     request.args.get('patient_id'))

        if not patient_id:
            return {'error': 'Patient ID required'}, 400

        # Patients can only access their own data
        if current_user['role'] == 'patient':
            if current_user['entity_id'] != int(patient_id):
                log_access(
                    current_user['user_id'],
                    "UNAUTHORIZED_PATIENT_ACCESS",
                    "PATIENT",
                    patient_id=patient_id,
                    success=False
                )
                return {'error': 'Access denied to patient data'}, 403

        # Nurses can only access assigned patients
        elif current_user['role'] == 'nurse':
            assignment = conn.execute(
                "SELECT 1 FROM patient_assignments WHERE nurse_id = ? AND pat_id = ? AND is_active = 1",
                (current_user['user_id'], patient_id)
            ).fetchone()

            if not assignment:
                log_access(
                    current_user['user_id'],
                    "UNAUTHORIZED_PATIENT_ACCESS",
                    "PATIENT",
                    patient_id=patient_id,
                    success=False
                )
                return {'error': 'Access denied to patient data'}, 403

        return f(*args, **kwargs)

    return decorated_function

# Permission definitions
ROLE_PERMISSIONS = {
    'admin': {
        'users': ['create', 'read', 'update', 'delete'],
        'patients': ['create', 'read', 'update', 'delete'],
        'doctors': ['create', 'read', 'update', 'delete'],
        'nurses': ['create', 'read', 'update', 'delete'],
        'health_records': ['create', 'read', 'update', 'delete'],
        'vital_signs': ['create', 'read', 'update', 'delete'],
        'lab_tests': ['create', 'read', 'update', 'delete'],
        'prescriptions': ['create', 'read', 'update', 'delete'],
        'audit_logs': ['read'],
        'system': ['manage']
    },
    'doctor': {
        'patients': ['read', 'update'],
        'health_records': ['create', 'read', 'update'],
        'vital_signs': ['read'],
        'lab_tests': ['create', 'read', 'update'],
        'prescriptions': ['create', 'read', 'update'],
        'medical_notes': ['create', 'read', 'update'],
        'appointments': ['create', 'read', 'update']
    },
    'nurse': {
        'patients': ['read'],  # Only assigned patients
        'health_records': ['read'],
        'vital_signs': ['create', 'read', 'update'],
        'nursing_notes': ['create', 'read', 'update'],
        'prescriptions': ['read'],
        'patient_assignments': ['read']
    },
    'lab_technician': {
        'patients': ['read'],  # Limited patient info
        'lab_tests': ['read', 'update'],  # Can update results
        'health_records': ['read']  # Limited access
    },
    'pharmacist': {
        'patients': ['read'],  # Limited patient info
        'prescriptions': ['read', 'update'],
        'medication_dispensing': ['create', 'read', 'update'],
        'medications': ['read']
    },
    'patient': {
        'health_records': ['read'],  # Own records only
        'vital_signs': ['read'],  # Own data only
        'lab_tests': ['read'],  # Own results only
        'prescriptions': ['read'],  # Own prescriptions only
        'appointments': ['read']  # Own appointments only
    }
}

def has_permission(role, resource, action):
    """Check if role has permission for action on resource"""
    role_perms = ROLE_PERMISSIONS.get(role, {})
    resource_perms = role_perms.get(resource, [])
    return action in resource_perms
