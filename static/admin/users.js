/**
 * User Management JavaScript
 * Handles all user management functionality for admin portal
 */

// Global variables
let usersTable;
let editingUserId = null;

// Initialize when document is ready
$(document).ready(function() {
    // Check authentication
    checkAuthentication();
    
    // Initialize components
    initializeUsersTable();
    loadUsers();
    
    // Bind form events
    bindFormEvents();
});

/**
 * Check if user is authenticated and has admin role
 */
function checkAuthentication() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token || user.role !== 'admin') {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

/**
 * Initialize DataTable for users
 */
function initializeUsersTable() {
    usersTable = $('#usersTable').DataTable({
        responsive: true,
        pageLength: 25,
        order: [[0, 'desc']],
        columnDefs: [
            { targets: [7], orderable: false } // Actions column
        ],
        language: {
            emptyTable: "No users found",
            loadingRecords: "Loading users...",
            processing: "Processing..."
        }
    });
}

/**
 * Load all users from API
 */
async function loadUsers() {
    try {
        showLoadingIndicator(true);
        const response = await apiCall('/users');
        
        if (response && Array.isArray(response)) {
            displayUsers(response);
            showAlert(`Loaded ${response.length} users successfully`, 'success');
        } else {
            showAlert('No users found', 'warning');
        }
    } catch (error) {
        console.error('Error loading users:', error);
        showAlert('Error loading users: ' + error.message, 'danger');
    } finally {
        showLoadingIndicator(false);
    }
}

/**
 * Display users in the DataTable
 */
function displayUsers(users) {
    usersTable.clear();
    
    users.forEach(user => {
        const roleColors = {
            'admin': 'danger',
            'doctor': 'primary',
            'nurse': 'success',
            'lab_technician': 'info',
            'pharmacist': 'warning',
            'patient': 'secondary'
        };

        const roleBadge = `<span class="badge bg-${roleColors[user.role] || 'secondary'} role-badge">${formatRole(user.role)}</span>`;
        const statusIcon = user.is_active ? 
            '<i class="fas fa-check-circle text-success"></i> Active' : 
            '<i class="fas fa-times-circle text-danger"></i> Inactive';
        
        const actions = createActionButtons(user);

        usersTable.row.add([
            user.user_id,
            user.username,
            `${user.first_name || ''} ${user.last_name || ''}`.trim(),
            user.email,
            roleBadge,
            statusIcon,
            formatDate(user.created_date),
            actions
        ]);
    });
    
    usersTable.draw();
}

/**
 * Create action buttons for each user row
 */
function createActionButtons(user) {
    return `
        <div class="btn-group" role="group">
            <button class="btn btn-sm btn-outline-primary" onclick="editUser(${user.user_id})" title="Edit User">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-sm btn-outline-info" onclick="viewUser(${user.user_id})" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button class="btn btn-sm btn-outline-${user.is_active ? 'warning' : 'success'}" 
                    onclick="toggleUserStatus(${user.user_id}, ${user.is_active})" 
                    title="${user.is_active ? 'Deactivate' : 'Activate'} User">
                <i class="fas fa-${user.is_active ? 'ban' : 'check'}"></i>
            </button>
            ${user.role !== 'admin' ? `
            <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${user.user_id})" title="Delete User">
                <i class="fas fa-trash"></i>
            </button>
            ` : ''}
        </div>
    `;
}

/**
 * Open modal for creating new user
 */
function showCreateUserModal() {
    editingUserId = null;
    document.getElementById('userModalTitle').innerHTML = '<i class="fas fa-user-plus me-2"></i>Add New User';
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    document.getElementById('password').required = true;
    document.getElementById('passwordSection').style.display = 'block';
    
    // Show modal
    new bootstrap.Modal(document.getElementById('userModal')).show();
}

/**
 * Edit existing user
 */
async function editUser(userId) {
    try {
        const response = await apiCall(`/users/${userId}`);
        if (response) {
            editingUserId = userId;
            document.getElementById('userModalTitle').innerHTML = '<i class="fas fa-user-edit me-2"></i>Edit User';
            
            // Populate form
            populateUserForm(response);
            
            // Password not required for editing
            document.getElementById('password').required = false;
            document.getElementById('passwordSection').style.display = 'block';
            
            // Show modal
            new bootstrap.Modal(document.getElementById('userModal')).show();
        }
    } catch (error) {
        showAlert('Error loading user details: ' + error.message, 'danger');
    }
}

/**
 * View user details (read-only)
 */
async function viewUser(userId) {
    try {
        const response = await apiCall(`/users/${userId}`);
        if (response) {
            // Create a read-only view modal or populate existing modal in read-only mode
            populateUserForm(response);
            
            // Make form read-only
            const formElements = document.querySelectorAll('#userForm input, #userForm select');
            formElements.forEach(element => {
                element.disabled = true;
            });
            
            document.getElementById('userModalTitle').innerHTML = '<i class="fas fa-user me-2"></i>User Details';
            document.getElementById('passwordSection').style.display = 'none';
            
            // Hide save button, show close button only
            document.querySelector('#userModal .modal-footer').innerHTML = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            `;
            
            new bootstrap.Modal(document.getElementById('userModal')).show();
        }
    } catch (error) {
        showAlert('Error loading user details: ' + error.message, 'danger');
    }
}

/**
 * Populate user form with data
 */
function populateUserForm(userData) {
    document.getElementById('userId').value = userData.user_id || '';
    document.getElementById('username').value = userData.username || '';
    document.getElementById('email').value = userData.email || '';
    document.getElementById('firstName').value = userData.first_name || '';
    document.getElementById('lastName').value = userData.last_name || '';
    document.getElementById('role').value = userData.role || '';
    document.getElementById('phoneNumber').value = userData.phone_number || '';
    document.getElementById('isActive').checked = userData.is_active || false;
    document.getElementById('password').value = '';
}

/**
 * Save user (create or update)
 */
async function saveUser() {
    const form = document.getElementById('userForm');
    
    // Validate form
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Collect form data
    const userData = collectFormData();
    
    // Validate passwords match if provided
    if (userData.password && userData.password !== document.getElementById('confirmPassword').value) {
        showAlert('Passwords do not match', 'danger');
        return;
    }
    
    try {
        let response;
        if (editingUserId) {
            // Update existing user
            response = await apiCall(`/users/${editingUserId}`, 'PUT', userData);
        } else {
            // Create new user
            response = await apiCall('/users', 'POST', userData);
        }

        if (response) {
            showAlert(editingUserId ? 'User updated successfully!' : 'User created successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
            loadUsers(); // Reload the users table
        }
    } catch (error) {
        showAlert('Error saving user: ' + error.message, 'danger');
    }
}

/**
 * Collect form data into object
 */
function collectFormData() {
    const formData = new FormData(document.getElementById('userForm'));
    const userData = {};
    
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            userData[key] = value.trim();
        }
    }
    
    // Handle checkbox
    userData.is_active = document.getElementById('isActive').checked ? 1 : 0;
    
    // Remove empty password for updates
    if (editingUserId && !userData.password) {
        delete userData.password;
    }
    
    return userData;
}

/**
 * Toggle user active status
 */
async function toggleUserStatus(userId, currentStatus) {
    const action = currentStatus ? 'deactivate' : 'activate';
    
    if (!confirm(`Are you sure you want to ${action} this user?`)) {
        return;
    }

    try {
        const response = await apiCall(`/users/${userId}`, 'PUT', { 
            is_active: currentStatus ? 0 : 1 
        });
        
        if (response) {
            showAlert(`User ${action}d successfully!`, 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert(`Error ${action}ing user: ` + error.message, 'danger');
    }
}

/**
 * Delete user
 */
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await apiCall(`/users/${userId}`, 'DELETE');
        if (response) {
            showAlert('User deleted successfully!', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Error deleting user: ' + error.message, 'danger');
    }
}

/**
 * Bind form events
 */
function bindFormEvents() {
    // Reset form when modal is hidden
    $('#userModal').on('hidden.bs.modal', function () {
        const form = document.getElementById('userForm');
        form.reset();
        
        // Re-enable form elements
        const formElements = document.querySelectorAll('#userForm input, #userForm select');
        formElements.forEach(element => {
            element.disabled = false;
        });
        
        // Restore modal footer
        document.querySelector('#userModal .modal-footer').innerHTML = `
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" onclick="saveUser()">
                <i class="fas fa-save me-1"></i>Save User
            </button>
        `;
    });
}

/**
 * Utility Functions
 */

function formatRole(role) {
    return role.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
}

function showLoadingIndicator(show) {
    const indicator = document.getElementById('loadingIndicator');
    const tableContainer = document.getElementById('usersTableContainer');
    
    if (indicator && tableContainer) {
        if (show) {
            indicator.style.display = 'block';
            tableContainer.style.display = 'none';
        } else {
            indicator.style.display = 'none';
            tableContainer.style.display = 'block';
        }
    }
}

// Export functions for global access
window.showCreateUserModal = showCreateUserModal;
window.editUser = editUser;
window.viewUser = viewUser;
window.saveUser = saveUser;
window.toggleUserStatus = toggleUserStatus;
window.deleteUser = deleteUser;
