/**
 * Doctor Appointments Management JavaScript
 */

// Global variables
let appointmentsTable;
let editingAppointmentId = null;

// Initialize when document is ready
$(document).ready(function() {
    // Check authentication
    checkAuthentication();
    
    // Initialize components
    initializeAppointmentsTable();
    loadAppointments();
    loadPatients();
    
    // Set minimum date to today
    document.getElementById('appointmentDate').min = new Date().toISOString().split('T')[0];
    
    // Bind events
    bindEvents();
});

/**
 * Check if user is authenticated and has doctor role
 */
function checkAuthentication() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token || user.role !== 'doctor') {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

/**
 * Initialize DataTable for appointments
 */
function initializeAppointmentsTable() {
    appointmentsTable = $('#appointmentsTable').DataTable({
        responsive: true,
        pageLength: 25,
        order: [[0, 'asc']], // Sort by date/time
        columnDefs: [
            { targets: [7], orderable: false } // Actions column
        ],
        language: {
            emptyTable: "No appointments found",
            loadingRecords: "Loading appointments...",
            processing: "Processing..."
        }
    });
}

/**
 * Load all appointments for the doctor
 */
async function loadAppointments() {
    try {
        showLoadingIndicator(true);
        const response = await apiCall('/appointments');
        
        if (response && Array.isArray(response)) {
            displayAppointments(response);
            updateQuickStats(response);
            showAlert(`Loaded ${response.length} appointments`, 'success');
        } else {
            showAlert('No appointments found', 'info');
        }
    } catch (error) {
        console.error('Error loading appointments:', error);
        showAlert('Error loading appointments: ' + error.message, 'danger');
    } finally {
        showLoadingIndicator(false);
    }
}

/**
 * Display appointments in the DataTable
 */
function displayAppointments(appointments) {
    appointmentsTable.clear();
    
    appointments.forEach(appointment => {
        const dateTime = formatAppointmentDateTime(appointment.appointment_date, appointment.appointment_time);
        const patientName = `${appointment.patient_first_name || ''} ${appointment.patient_last_name || ''}`.trim();
        const status = createStatusBadge(appointment.status);
        const priority = createPriorityBadge(appointment.priority);
        const actions = createActionButtons(appointment);
        
        appointmentsTable.row.add([
            dateTime,
            patientName,
            formatAppointmentType(appointment.appointment_type),
            status,
            priority,
            `${appointment.duration || 30} min`,
            appointment.notes || 'N/A',
            actions
        ]);
    });
    
    appointmentsTable.draw();
}

/**
 * Update quick statistics
 */
function updateQuickStats(appointments) {
    const today = new Date().toISOString().split('T')[0];
    const weekFromNow = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    
    const todayAppointments = appointments.filter(apt => apt.appointment_date === today).length;
    const upcomingAppointments = appointments.filter(apt => 
        apt.appointment_date > today && apt.appointment_date <= weekFromNow && apt.status === 'scheduled'
    ).length;
    const completedToday = appointments.filter(apt => 
        apt.appointment_date === today && apt.status === 'completed'
    ).length;
    const pendingAppointments = appointments.filter(apt => apt.status === 'scheduled').length;
    
    document.getElementById('todayAppointments').textContent = todayAppointments;
    document.getElementById('upcomingAppointments').textContent = upcomingAppointments;
    document.getElementById('completedToday').textContent = completedToday;
    document.getElementById('pendingAppointments').textContent = pendingAppointments;
}

/**
 * Load patients for the dropdown
 */
async function loadPatients() {
    try {
        const response = await apiCall('/patients');
        const patientSelect = document.getElementById('patientSelect');
        
        patientSelect.innerHTML = '<option value="">Select Patient</option>';
        
        if (response && Array.isArray(response)) {
            response.forEach(patient => {
                const option = document.createElement('option');
                option.value = patient.patient_id;
                option.textContent = `${patient.first_name} ${patient.last_name} (ID: ${patient.patient_id})`;
                patientSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading patients:', error);
        showAlert('Error loading patients: ' + error.message, 'warning');
    }
}

/**
 * Create status badge
 */
function createStatusBadge(status) {
    const statusClasses = {
        'scheduled': 'status-scheduled',
        'completed': 'status-completed',
        'cancelled': 'status-cancelled',
        'no-show': 'status-no-show'
    };
    
    const className = statusClasses[status] || 'status-scheduled';
    return `<span class="appointment-status ${className}">${formatStatus(status)}</span>`;
}

/**
 * Create priority badge
 */
function createPriorityBadge(priority) {
    const priorityClasses = {
        'high': 'priority-high',
        'medium': 'priority-medium',
        'low': 'priority-low'
    };
    
    const className = priorityClasses[priority] || 'priority-medium';
    return `<span class="${className}">${priority ? priority.toUpperCase() : 'MEDIUM'}</span>`;
}

/**
 * Create action buttons
 */
function createActionButtons(appointment) {
    const canEdit = appointment.status === 'scheduled';
    const canComplete = appointment.status === 'scheduled';
    const canCancel = appointment.status === 'scheduled';
    
    return `
        <div class="btn-group" role="group">
            <button class="btn btn-sm btn-outline-info" onclick="viewAppointment(${appointment.appointment_id})" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            ${canEdit ? `
            <button class="btn btn-sm btn-outline-primary" onclick="editAppointment(${appointment.appointment_id})" title="Edit">
                <i class="fas fa-edit"></i>
            </button>
            ` : ''}
            ${canComplete ? `
            <button class="btn btn-sm btn-outline-success" onclick="completeAppointment(${appointment.appointment_id})" title="Mark Complete">
                <i class="fas fa-check"></i>
            </button>
            ` : ''}
            ${canCancel ? `
            <button class="btn btn-sm btn-outline-danger" onclick="cancelAppointment(${appointment.appointment_id})" title="Cancel">
                <i class="fas fa-times"></i>
            </button>
            ` : ''}
        </div>
    `;
}

/**
 * Show create appointment modal
 */
function showCreateAppointmentModal() {
    editingAppointmentId = null;
    document.getElementById('appointmentModalTitle').innerHTML = '<i class="fas fa-calendar-plus me-2"></i>Schedule New Appointment';
    document.getElementById('appointmentForm').reset();
    document.getElementById('appointmentId').value = '';
    
    // Set default date to today
    document.getElementById('appointmentDate').value = new Date().toISOString().split('T')[0];
    
    new bootstrap.Modal(document.getElementById('appointmentModal')).show();
}

/**
 * Edit appointment
 */
async function editAppointment(appointmentId) {
    try {
        const response = await apiCall(`/appointments/${appointmentId}`);
        if (response) {
            editingAppointmentId = appointmentId;
            document.getElementById('appointmentModalTitle').innerHTML = '<i class="fas fa-calendar-edit me-2"></i>Edit Appointment';
            
            // Populate form
            populateAppointmentForm(response);
            
            new bootstrap.Modal(document.getElementById('appointmentModal')).show();
        }
    } catch (error) {
        showAlert('Error loading appointment details: ' + error.message, 'danger');
    }
}

/**
 * View appointment details
 */
async function viewAppointment(appointmentId) {
    try {
        const response = await apiCall(`/appointments/${appointmentId}`);
        if (response) {
            // Show appointment details in a read-only modal or alert
            const details = `
                Patient: ${response.patient_first_name} ${response.patient_last_name}
                Date: ${formatDate(response.appointment_date)}
                Time: ${response.appointment_time}
                Type: ${formatAppointmentType(response.appointment_type)}
                Status: ${formatStatus(response.status)}
                Duration: ${response.duration || 30} minutes
                Priority: ${response.priority || 'medium'}
                Notes: ${response.notes || 'No notes'}
            `;
            
            alert('Appointment Details:\n\n' + details);
        }
    } catch (error) {
        showAlert('Error loading appointment details: ' + error.message, 'danger');
    }
}

/**
 * Complete appointment
 */
async function completeAppointment(appointmentId) {
    if (!confirm('Mark this appointment as completed?')) {
        return;
    }
    
    try {
        const response = await apiCall(`/appointments/${appointmentId}`, 'PUT', { status: 'completed' });
        if (response) {
            showAlert('Appointment marked as completed!', 'success');
            loadAppointments();
        }
    } catch (error) {
        showAlert('Error completing appointment: ' + error.message, 'danger');
    }
}

/**
 * Cancel appointment
 */
async function cancelAppointment(appointmentId) {
    if (!confirm('Are you sure you want to cancel this appointment?')) {
        return;
    }
    
    try {
        const response = await apiCall(`/appointments/${appointmentId}`, 'PUT', { status: 'cancelled' });
        if (response) {
            showAlert('Appointment cancelled successfully!', 'success');
            loadAppointments();
        }
    } catch (error) {
        showAlert('Error cancelling appointment: ' + error.message, 'danger');
    }
}

/**
 * Save appointment
 */
async function saveAppointment() {
    const form = document.getElementById('appointmentForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const appointmentData = collectFormData('appointmentForm');
    
    // Combine date and time
    appointmentData.appointment_datetime = `${appointmentData.appointment_date} ${appointmentData.appointment_time}`;
    
    try {
        let response;
        if (editingAppointmentId) {
            response = await apiCall(`/appointments/${editingAppointmentId}`, 'PUT', appointmentData);
        } else {
            response = await apiCall('/appointments', 'POST', appointmentData);
        }

        if (response) {
            showAlert(editingAppointmentId ? 'Appointment updated successfully!' : 'Appointment scheduled successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('appointmentModal')).hide();
            loadAppointments();
        }
    } catch (error) {
        showAlert('Error saving appointment: ' + error.message, 'danger');
    }
}

/**
 * Populate appointment form
 */
function populateAppointmentForm(appointmentData) {
    document.getElementById('appointmentId').value = appointmentData.appointment_id || '';
    document.getElementById('patientSelect').value = appointmentData.patient_id || '';
    document.getElementById('appointmentType').value = appointmentData.appointment_type || '';
    document.getElementById('appointmentDate').value = appointmentData.appointment_date || '';
    document.getElementById('appointmentTime').value = appointmentData.appointment_time || '';
    document.getElementById('duration').value = appointmentData.duration || '30';
    document.getElementById('priority').value = appointmentData.priority || 'medium';
    document.getElementById('appointmentNotes').value = appointmentData.notes || '';
    document.getElementById('sendReminder').checked = appointmentData.send_reminder || false;
}

/**
 * Bind events
 */
function bindEvents() {
    // Status filter
    document.getElementById('statusFilter').addEventListener('change', function() {
        const filterValue = this.value;
        appointmentsTable.column(3).search(filterValue).draw();
    });
    
    // Reset form when modal is hidden
    $('#appointmentModal').on('hidden.bs.modal', function () {
        document.getElementById('appointmentForm').reset();
    });
}

/**
 * Utility functions
 */
function formatAppointmentDateTime(date, time) {
    if (!date) return 'N/A';
    const formattedDate = formatDate(date);
    return time ? `${formattedDate} ${time}` : formattedDate;
}

function formatAppointmentType(type) {
    if (!type) return 'N/A';
    return type.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatStatus(status) {
    if (!status) return 'Scheduled';
    return status.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function showLoadingIndicator(show) {
    const indicator = document.getElementById('loadingIndicator');
    const tableContainer = document.getElementById('appointmentsTableContainer');
    
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
window.showCreateAppointmentModal = showCreateAppointmentModal;
window.editAppointment = editAppointment;
window.viewAppointment = viewAppointment;
window.completeAppointment = completeAppointment;
window.cancelAppointment = cancelAppointment;
window.saveAppointment = saveAppointment;
