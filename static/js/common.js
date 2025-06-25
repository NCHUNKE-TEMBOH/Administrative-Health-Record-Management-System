/**
 * Common JavaScript utilities for HRMS
 */

// Authentication utilities
function checkAuth(requiredRole = null) {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token || !user.user_id) {
        window.location.href = '/login.html';
        return false;
    }

    if (requiredRole && user.role !== requiredRole) {
        showAlert('Access denied', 'danger');
        return false;
    }

    return { token, user };
}

// API call utility
async function apiCall(endpoint, method = 'GET', data = null) {
    const auth = checkAuth();
    if (!auth) return null;

    const options = {
        method,
        headers: {
            'Authorization': `Bearer ${auth.token}`,
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        
        if (response.status === 401) {
            logout();
            return null;
        }

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }

        return result;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Alert utility
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, duration);
}

// Logout utility
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

// Form utilities
function getFormData(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            data[key] = value;
        }
    }
    
    return data;
}

function populateForm(formId, data) {
    const form = document.getElementById(formId);
    if (!form) return;

    Object.keys(data).forEach(key => {
        const element = form.querySelector(`[name="${key}"]`);
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = data[key];
            } else {
                element.value = data[key] || '';
            }
        }
    });
}

// Date utilities
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
}

// Loading utilities
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Modal utilities
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        new bootstrap.Modal(modal).show();
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    }
}

// Table utilities
function initializeDataTable(tableId, options = {}) {
    const defaultOptions = {
        responsive: true,
        pageLength: 25,
        order: [[0, 'desc']],
        language: {
            emptyTable: "No data available",
            loadingRecords: "Loading...",
            processing: "Processing...",
            search: "Search:",
            zeroRecords: "No matching records found"
        }
    };

    return $('#' + tableId).DataTable({...defaultOptions, ...options});
}

// Validation utilities
function validateEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[1-9][\d]{0,15}$/;
    return re.test(phone.replace(/[\s\-\(\)]/g, ''));
}

function validateRequired(value) {
    return value && value.trim().length > 0;
}

// Navigation utilities
function navigateTo(url) {
    window.location.href = url;
}

function openInNewTab(url) {
    window.open(url, '_blank');
}

// Role-based navigation
function getRoleBasedUrl(role, module) {
    const roleUrls = {
        'admin': {
            'users': '/admin/users.html',
            'patients': '/admin/patients.html',
            'health-records': '/admin/health-records.html',
            'doctors': '/admin/doctors.html',
            'nurses': '/admin/nurses.html',
            'audit-logs': '/admin/audit-logs.html'
        },
        'doctor': {
            'patients': '/doctor/patients.html',
            'appointments': '/doctor/appointments.html',
            'prescriptions': '/doctor/prescriptions.html',
            'lab-tests': '/doctor/lab-tests.html',
            'medical-notes': '/doctor/medical-notes.html'
        },
        'nurse': {
            'patients': '/nurse/patients.html',
            'vital-signs': '/nurse/vital-signs.html',
            'nursing-notes': '/nurse/nursing-notes.html',
            'assignments': '/nurse/assignments.html'
        },
        'lab_technician': {
            'lab-tests': '/lab/tests.html',
            'results': '/lab/results.html'
        },
        'pharmacist': {
            'prescriptions': '/pharmacy/prescriptions.html',
            'dispensing': '/pharmacy/dispensing.html',
            'inventory': '/pharmacy/inventory.html'
        },
        'patient': {
            'health-records': '/patient/health-records.html',
            'prescriptions': '/patient/prescriptions.html',
            'appointments': '/patient/appointments.html',
            'lab-results': '/patient/lab-results.html'
        }
    };

    return roleUrls[role] && roleUrls[role][module] ? roleUrls[role][module] : null;
}

// Module availability checker
function isModuleAvailable(role, module) {
    return getRoleBasedUrl(role, module) !== null;
}

// Safe navigation with module availability check
function safeNavigate(role, module, fallbackMessage = 'Module coming soon!') {
    const url = getRoleBasedUrl(role, module);
    if (url) {
        navigateTo(url);
    } else {
        showAlert(fallbackMessage, 'info');
    }
}

// Blockchain functionality removed

// Export for use in other modules
window.HRMS = {
    checkAuth,
    apiCall,
    showAlert,
    logout,
    getFormData,
    populateForm,
    formatDate,
    formatDateTime,
    showLoading,
    hideLoading,
    showModal,
    hideModal,
    initializeDataTable,
    validateEmail,
    validatePhone,
    validateRequired,
    navigateTo,
    openInNewTab,
    getRoleBasedUrl,
    isModuleAvailable,
    safeNavigate
};
