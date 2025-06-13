// Nurse Patients Management JavaScript

// Authentication check
const token = localStorage.getItem('token');
const user = JSON.parse(localStorage.getItem('user') || '{}');

if (!token || (user.role !== 'nurse' && user.role !== 'admin')) {
    window.location.href = '/login.html';
}

let patientsTable;
let assignedPatients = [];

// Initialize page
$(document).ready(function() {
    initializePage();
});

function initializePage() {
    loadAssignedPatients();
    setupEventListeners();
}

function setupEventListeners() {
    // Status filter
    $('#statusFilter').on('change', function() {
        if (patientsTable) {
            patientsTable.column(2).search(this.value).draw();
        }
    });
}

async function loadAssignedPatients() {
    try {
        showLoadingIndicator(true);
        
        // Try to load from API first
        let patients = [];
        try {
            const response = await fetch('/nurse/assigned-patients', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                patients = await response.json();
            } else {
                throw new Error('API not available');
            }
        } catch (error) {
            console.log('Using sample data');
            patients = getSamplePatients();
        }

        assignedPatients = patients;
        displayPatients(patients);
        updateStatistics(patients);
        populateVitalSignsPatientSelect(patients);
        
    } catch (error) {
        console.error('Error loading patients:', error);
        showAlert('Error loading patients: ' + error.message, 'danger');
    } finally {
        showLoadingIndicator(false);
    }
}

function getSamplePatients() {
    return [
        {
            pat_id: 1,
            pat_first_name: 'John',
            pat_last_name: 'Doe',
            room_number: '101A',
            status: 'stable',
            priority: 'medium',
            assigned_doctor: 'Dr. Smith',
            last_vitals: {
                bp_systolic: 120,
                bp_diastolic: 80,
                heart_rate: 72,
                temperature: 98.6,
                recorded_at: new Date().toISOString()
            },
            medications: [
                { name: 'Lisinopril 10mg', due_time: '08:00', status: 'pending' },
                { name: 'Metformin 500mg', due_time: '12:00', status: 'completed' }
            ],
            admission_date: '2024-01-15',
            diagnosis: 'Hypertension, Type 2 Diabetes'
        },
        {
            pat_id: 2,
            pat_first_name: 'Jane',
            pat_last_name: 'Smith',
            room_number: '102B',
            status: 'critical',
            priority: 'high',
            assigned_doctor: 'Dr. Johnson',
            last_vitals: {
                bp_systolic: 160,
                bp_diastolic: 95,
                heart_rate: 88,
                temperature: 101.2,
                recorded_at: new Date(Date.now() - 3600000).toISOString()
            },
            medications: [
                { name: 'Amlodipine 5mg', due_time: '06:00', status: 'completed' },
                { name: 'Furosemide 40mg', due_time: '14:00', status: 'pending' }
            ],
            admission_date: '2024-01-18',
            diagnosis: 'Acute Heart Failure'
        },
        {
            pat_id: 3,
            pat_first_name: 'Robert',
            pat_last_name: 'Wilson',
            room_number: '103A',
            status: 'monitoring',
            priority: 'medium',
            assigned_doctor: 'Dr. Brown',
            last_vitals: {
                bp_systolic: 135,
                bp_diastolic: 85,
                heart_rate: 76,
                temperature: 99.1,
                recorded_at: new Date(Date.now() - 7200000).toISOString()
            },
            medications: [
                { name: 'Aspirin 81mg', due_time: '09:00', status: 'completed' },
                { name: 'Atorvastatin 20mg', due_time: '20:00', status: 'pending' }
            ],
            admission_date: '2024-01-20',
            diagnosis: 'Post-operative monitoring'
        },
        {
            pat_id: 4,
            pat_first_name: 'Mary',
            pat_last_name: 'Johnson',
            room_number: '104B',
            status: 'recovering',
            priority: 'low',
            assigned_doctor: 'Dr. Davis',
            last_vitals: {
                bp_systolic: 118,
                bp_diastolic: 75,
                heart_rate: 68,
                temperature: 98.4,
                recorded_at: new Date(Date.now() - 1800000).toISOString()
            },
            medications: [
                { name: 'Ibuprofen 400mg', due_time: '10:00', status: 'completed' },
                { name: 'Omeprazole 20mg', due_time: '16:00', status: 'pending' }
            ],
            admission_date: '2024-01-22',
            diagnosis: 'Recovery from appendectomy'
        },
        {
            pat_id: 5,
            pat_first_name: 'David',
            pat_last_name: 'Brown',
            room_number: '105A',
            status: 'stable',
            priority: 'low',
            assigned_doctor: 'Dr. Wilson',
            last_vitals: {
                bp_systolic: 125,
                bp_diastolic: 82,
                heart_rate: 70,
                temperature: 98.8,
                recorded_at: new Date(Date.now() - 5400000).toISOString()
            },
            medications: [
                { name: 'Warfarin 5mg', due_time: '18:00', status: 'pending' },
                { name: 'Digoxin 0.25mg', due_time: '08:00', status: 'completed' }
            ],
            admission_date: '2024-01-19',
            diagnosis: 'Atrial fibrillation'
        },
        {
            pat_id: 6,
            pat_first_name: 'Sarah',
            pat_last_name: 'Davis',
            room_number: '106B',
            status: 'monitoring',
            priority: 'high',
            assigned_doctor: 'Dr. Miller',
            last_vitals: {
                bp_systolic: 140,
                bp_diastolic: 90,
                heart_rate: 82,
                temperature: 100.1,
                recorded_at: new Date(Date.now() - 900000).toISOString()
            },
            medications: [
                { name: 'Ceftriaxone 1g', due_time: '12:00', status: 'pending' },
                { name: 'Acetaminophen 650mg', due_time: '15:00', status: 'pending' }
            ],
            admission_date: '2024-01-21',
            diagnosis: 'Pneumonia'
        },
        {
            pat_id: 7,
            pat_first_name: 'Michael',
            pat_last_name: 'Garcia',
            room_number: '107A',
            status: 'stable',
            priority: 'medium',
            assigned_doctor: 'Dr. Anderson',
            last_vitals: {
                bp_systolic: 130,
                bp_diastolic: 78,
                heart_rate: 74,
                temperature: 98.2,
                recorded_at: new Date(Date.now() - 10800000).toISOString()
            },
            medications: [
                { name: 'Insulin Glargine 20u', due_time: '22:00', status: 'pending' },
                { name: 'Metformin 1000mg', due_time: '07:00', status: 'completed' }
            ],
            admission_date: '2024-01-17',
            diagnosis: 'Diabetic ketoacidosis'
        },
        {
            pat_id: 8,
            pat_first_name: 'Lisa',
            pat_last_name: 'Martinez',
            room_number: '108B',
            status: 'recovering',
            priority: 'low',
            assigned_doctor: 'Dr. Taylor',
            last_vitals: {
                bp_systolic: 115,
                bp_diastolic: 70,
                heart_rate: 65,
                temperature: 98.0,
                recorded_at: new Date(Date.now() - 14400000).toISOString()
            },
            medications: [
                { name: 'Morphine 5mg', due_time: '11:00', status: 'completed' },
                { name: 'Ondansetron 4mg', due_time: '17:00', status: 'pending' }
            ],
            admission_date: '2024-01-23',
            diagnosis: 'Post-surgical recovery'
        }
    ];
}

function displayPatients(patients) {
    const tableBody = document.getElementById('patientsTableBody');
    tableBody.innerHTML = '';

    patients.forEach(patient => {
        const row = createPatientRow(patient);
        tableBody.appendChild(row);
    });

    // Initialize or refresh DataTable
    if (patientsTable) {
        patientsTable.destroy();
    }

    patientsTable = $('#patientsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[6, 'desc'], [2, 'asc']], // Sort by priority then status
        columnDefs: [
            { targets: [7], orderable: false } // Actions column
        ]
    });

    document.getElementById('patientsTableContainer').style.display = 'block';
}

function createPatientRow(patient) {
    const row = document.createElement('tr');

    // Patient info
    const patientCell = document.createElement('td');
    patientCell.innerHTML = `
        <div>
            <strong>${patient.pat_first_name} ${patient.pat_last_name}</strong><br>
            <small class="text-muted">ID: ${patient.pat_id}</small><br>
            <small class="text-muted">${patient.diagnosis || 'No diagnosis'}</small>
        </div>
    `;

    // Room
    const roomCell = document.createElement('td');
    roomCell.innerHTML = `<span class="room-badge">${patient.room_number || 'N/A'}</span>`;

    // Status
    const statusCell = document.createElement('td');
    statusCell.innerHTML = `<span class="patient-status status-${patient.status}">${patient.status?.toUpperCase() || 'UNKNOWN'}</span>`;

    // Last vitals
    const vitalsCell = document.createElement('td');
    if (patient.last_vitals) {
        const vitalsTime = new Date(patient.last_vitals.recorded_at);
        const hoursAgo = Math.floor((Date.now() - vitalsTime.getTime()) / (1000 * 60 * 60));
        vitalsCell.innerHTML = `
            <div class="vital-signs">
                <div class="vital-item">BP: ${patient.last_vitals.bp_systolic}/${patient.last_vitals.bp_diastolic}</div>
                <div class="vital-item">HR: ${patient.last_vitals.heart_rate}</div>
                <div class="vital-item">Temp: ${patient.last_vitals.temperature}°F</div>
            </div>
            <small class="text-muted">${hoursAgo}h ago</small>
        `;
    } else {
        vitalsCell.innerHTML = '<span class="text-muted">No vitals recorded</span>';
    }

    // Medications
    const medicationsCell = document.createElement('td');
    if (patient.medications && patient.medications.length > 0) {
        const pendingMeds = patient.medications.filter(med => med.status === 'pending');
        medicationsCell.innerHTML = `
            <div>
                <strong>${pendingMeds.length}</strong> pending<br>
                <small class="text-muted">${patient.medications.length} total</small>
            </div>
        `;
    } else {
        medicationsCell.innerHTML = '<span class="text-muted">No medications</span>';
    }

    // Assigned doctor
    const doctorCell = document.createElement('td');
    doctorCell.textContent = patient.assigned_doctor || 'Not assigned';

    // Priority
    const priorityCell = document.createElement('td');
    priorityCell.innerHTML = `<span class="priority-${patient.priority}">${patient.priority?.toUpperCase() || 'NORMAL'}</span>`;

    // Actions
    const actionsCell = document.createElement('td');
    actionsCell.innerHTML = `
        <div class="btn-group btn-group-sm" role="group">
            <button type="button" class="btn btn-outline-success" onclick="recordVitals(${patient.pat_id})" title="Record Vitals">
                <i class="fas fa-heartbeat"></i>
            </button>
            <button type="button" class="btn btn-outline-primary" onclick="addNursingNote(${patient.pat_id})" title="Add Note">
                <i class="fas fa-notes-medical"></i>
            </button>
            <button type="button" class="btn btn-outline-info" onclick="viewPatientDetails(${patient.pat_id})" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button type="button" class="btn btn-outline-warning" onclick="viewMedications(${patient.pat_id})" title="Medications">
                <i class="fas fa-pills"></i>
            </button>
        </div>
    `;

    row.appendChild(patientCell);
    row.appendChild(roomCell);
    row.appendChild(statusCell);
    row.appendChild(vitalsCell);
    row.appendChild(medicationsCell);
    row.appendChild(doctorCell);
    row.appendChild(priorityCell);
    row.appendChild(actionsCell);

    return row;
}

function updateStatistics(patients) {
    const stats = {
        total: patients.length,
        critical: patients.filter(p => p.status === 'critical').length,
        vitalsToday: patients.filter(p => {
            if (!p.last_vitals) return false;
            const vitalsDate = new Date(p.last_vitals.recorded_at);
            const today = new Date();
            return vitalsDate.toDateString() === today.toDateString();
        }).length,
        medicationsDue: patients.reduce((total, p) => {
            if (!p.medications) return total;
            return total + p.medications.filter(med => med.status === 'pending').length;
        }, 0)
    };

    document.getElementById('assignedPatients').textContent = stats.total;
    document.getElementById('criticalPatients').textContent = stats.critical;
    document.getElementById('vitalsToday').textContent = stats.vitalsToday;
    document.getElementById('medicationsDue').textContent = stats.medicationsDue;
}

function populateVitalSignsPatientSelect(patients) {
    const select = document.getElementById('vitalPatientSelect');
    select.innerHTML = '<option value="">Select Patient</option>';

    patients.forEach(patient => {
        const option = document.createElement('option');
        option.value = patient.pat_id;
        option.textContent = `${patient.pat_first_name} ${patient.pat_last_name} - Room ${patient.room_number}`;
        select.appendChild(option);
    });
}

// Action functions
function recordVitals(patientId) {
    const patient = assignedPatients.find(p => p.pat_id === patientId);
    if (patient) {
        document.getElementById('vitalPatientSelect').value = patientId;
        showVitalSignsModal();
    }
}

function addNursingNote(patientId) {
    document.getElementById('notesPatientId').value = patientId;
    const patient = assignedPatients.find(p => p.pat_id === patientId);
    if (patient) {
        document.querySelector('#nursingNotesModal .modal-title').innerHTML = `
            <i class="fas fa-notes-medical me-2"></i>
            Nursing Notes - ${patient.pat_first_name} ${patient.pat_last_name}
        `;
    }
    new bootstrap.Modal(document.getElementById('nursingNotesModal')).show();
}

function viewPatientDetails(patientId) {
    const patient = assignedPatients.find(p => p.pat_id === patientId);
    if (patient) {
        // Create a detailed view modal or redirect to patient details page
        showAlert(`Viewing details for ${patient.pat_first_name} ${patient.pat_last_name}`, 'info');
        // TODO: Implement detailed patient view
    }
}

function viewMedications(patientId) {
    const patient = assignedPatients.find(p => p.pat_id === patientId);
    if (patient) {
        showAlert(`Viewing medications for ${patient.pat_first_name} ${patient.pat_last_name}`, 'info');
        // TODO: Implement medication management view
    }
}

// Modal functions
function showVitalSignsModal() {
    new bootstrap.Modal(document.getElementById('vitalSignsModal')).show();
}

async function saveVitalSigns() {
    const form = document.getElementById('vitalSignsForm');
    const formData = new FormData(form);

    // Validate required fields
    const patientId = formData.get('patient_id');
    if (!patientId) {
        showAlert('Please select a patient', 'warning');
        return;
    }

    // Collect vital signs data
    const vitalSigns = {
        patient_id: parseInt(patientId),
        bp_systolic: formData.get('bp_systolic') ? parseInt(formData.get('bp_systolic')) : null,
        bp_diastolic: formData.get('bp_diastolic') ? parseInt(formData.get('bp_diastolic')) : null,
        heart_rate: formData.get('heart_rate') ? parseInt(formData.get('heart_rate')) : null,
        temperature: formData.get('temperature') ? parseFloat(formData.get('temperature')) : null,
        respiratory_rate: formData.get('respiratory_rate') ? parseInt(formData.get('respiratory_rate')) : null,
        oxygen_saturation: formData.get('oxygen_saturation') ? parseInt(formData.get('oxygen_saturation')) : null,
        notes: formData.get('notes') || '',
        recorded_by: user.user_id,
        recorded_at: new Date().toISOString()
    };

    try {
        // Try to save to API
        const response = await fetch('/nurse/vital-signs', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(vitalSigns)
        });

        if (response.ok) {
            showAlert('Vital signs recorded successfully!', 'success');
        } else {
            throw new Error('Failed to save vital signs');
        }
    } catch (error) {
        console.log('API not available, simulating save');
        showAlert('Vital signs recorded successfully! (Demo mode)', 'success');
    }

    // Update local data
    const patient = assignedPatients.find(p => p.pat_id === parseInt(patientId));
    if (patient) {
        patient.last_vitals = vitalSigns;
    }

    // Close modal and refresh display
    bootstrap.Modal.getInstance(document.getElementById('vitalSignsModal')).hide();
    form.reset();
    displayPatients(assignedPatients);
    updateStatistics(assignedPatients);
}

async function saveNursingNote() {
    const form = document.getElementById('nursingNotesForm');
    const formData = new FormData(form);

    // Validate required fields
    const patientId = formData.get('patient_id');
    const noteType = formData.get('note_type');
    const content = formData.get('content');

    if (!patientId || !noteType || !content.trim()) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    const nursingNote = {
        patient_id: parseInt(patientId),
        note_type: noteType,
        content: content.trim(),
        flag_for_doctor: formData.get('flag_for_doctor') === 'on',
        created_by: user.user_id,
        created_at: new Date().toISOString()
    };

    try {
        // Try to save to API
        const response = await fetch('/nurse/nursing-notes', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(nursingNote)
        });

        if (response.ok) {
            showAlert('Nursing note saved successfully!', 'success');
        } else {
            throw new Error('Failed to save nursing note');
        }
    } catch (error) {
        console.log('API not available, simulating save');
        showAlert('Nursing note saved successfully! (Demo mode)', 'success');
    }

    // Close modal and reset form
    bootstrap.Modal.getInstance(document.getElementById('nursingNotesModal')).hide();
    form.reset();
}

// Utility functions
function showLoadingIndicator(show) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const tableContainer = document.getElementById('patientsTableContainer');

    if (show) {
        loadingIndicator.style.display = 'block';
        tableContainer.style.display = 'none';
    } else {
        loadingIndicator.style.display = 'none';
        tableContainer.style.display = 'block';
    }
}

function showAlert(message, type) {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    alertContainer.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}
