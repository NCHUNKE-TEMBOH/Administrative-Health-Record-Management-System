// Patient Health Records JavaScript

// Authentication check
const token = localStorage.getItem('token');
const user = JSON.parse(localStorage.getItem('user') || '{}');

if (!token || (user.role !== 'patient' && user.role !== 'admin')) {
    window.location.href = '/login.html';
}

let healthRecords = [];
let recordsTable;
let vitalsChart;
let vitalSignsData = [];

// Initialize page
$(document).ready(function() {
    initializePage();
});

function initializePage() {
    loadPatientInfo();
    loadHealthRecords();
    loadVitalSignsData();
    setupEventListeners();
}

function setupEventListeners() {
    // Record type filter
    $('#recordTypeFilter').on('change', function() {
        if (recordsTable) {
            recordsTable.column(1).search(this.value).draw();
        }
    });
}

async function loadPatientInfo() {
    try {
        // Try to load patient info from API
        let patientInfo;
        try {
            const response = await fetch(`/patient/${user.user_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                patientInfo = await response.json();
            } else {
                throw new Error('API not available');
            }
        } catch (error) {
            console.log('Using sample patient data');
            patientInfo = getSamplePatientInfo();
        }

        displayPatientInfo(patientInfo);
    } catch (error) {
        console.error('Error loading patient info:', error);
        displayPatientInfo(getSamplePatientInfo());
    }
}

function getSamplePatientInfo() {
    return {
        pat_id: user.user_id || 1001,
        pat_first_name: user.first_name || 'Jane',
        pat_last_name: user.last_name || 'Doe',
        pat_dob: '1988-07-22',
        pat_age: 35,
        pat_gender: 'Female',
        blood_type: 'A+',
        primary_doctor: 'Dr. Sarah Johnson',
        last_visit: '2024-01-20',
        pat_insurance_no: 'INS001234',
        pat_ph_no: '(555) 123-4567',
        pat_email: user.email || 'jane.doe@email.com',
        pat_address: '123 Main Street, Anytown, ST 12345',
        emergency_contact_name: 'John Doe (Spouse)',
        emergency_contact_phone: '(555) 987-6543',
        allergies: 'Penicillin, Shellfish',
        medical_conditions: 'Hypertension (controlled)',
        current_medications: 'Lisinopril 10mg daily',
        insurance_provider: 'Blue Cross Blue Shield',
        insurance_group: 'Group #12345',
        marital_status: 'Married',
        occupation: 'Marketing Manager',
        height: '5\'6"',
        weight: '140 lbs',
        bmi: '22.6',
        smoking_status: 'Never smoker',
        alcohol_use: 'Occasional social drinking',
        exercise_frequency: '4-5 times per week',
        family_history: 'Mother: Breast cancer, Father: Hypertension',
        preferred_pharmacy: 'Central Pharmacy - 456 Oak Street, Anytown, ST 12345',
        preferred_language: 'English',
        admission_date: '2023-06-15',
        registration_date: '2023-06-15'
    };
}

function displayPatientInfo(patient) {
    // Basic Information
    document.getElementById('patientId').textContent = patient.pat_id;
    document.getElementById('patientName').textContent = `${patient.pat_first_name} ${patient.pat_last_name}`;
    document.getElementById('patientDob').textContent = new Date(patient.pat_dob).toLocaleDateString();
    document.getElementById('patientAge').textContent = patient.pat_age || calculateAge(patient.pat_dob);
    document.getElementById('patientGender').textContent = patient.pat_gender || 'Not specified';
    document.getElementById('maritalStatus').textContent = patient.marital_status || 'Not specified';

    // Contact Information
    document.getElementById('patientPhone').textContent = patient.pat_ph_no || 'Not provided';
    document.getElementById('patientEmail').textContent = patient.pat_email || 'Not provided';
    document.getElementById('patientAddress').textContent = patient.pat_address || 'Not provided';
    document.getElementById('emergencyContact').textContent = patient.emergency_contact_name || 'Not provided';
    document.getElementById('emergencyPhone').textContent = patient.emergency_contact_phone || 'Not provided';
    document.getElementById('preferredLanguage').textContent = patient.preferred_language || 'English';

    // Medical Information
    document.getElementById('bloodType').textContent = patient.blood_type || 'Unknown';
    document.getElementById('patientHeight').textContent = patient.height || 'Not recorded';
    document.getElementById('patientWeight').textContent = patient.weight || 'Not recorded';
    document.getElementById('patientBMI').textContent = patient.bmi || 'Not calculated';
    document.getElementById('primaryDoctor').textContent = patient.primary_doctor || 'Not assigned';
    document.getElementById('lastVisit').textContent = patient.last_visit ? new Date(patient.last_visit).toLocaleDateString() : 'No recent visits';

    // Allergies & Conditions
    document.getElementById('allergies').textContent = patient.allergies || 'No known allergies';
    document.getElementById('medicalConditions').textContent = patient.medical_conditions || 'None reported';
    document.getElementById('currentMedications').textContent = patient.current_medications || 'None';

    // Lifestyle Information
    document.getElementById('smokingStatus').textContent = patient.smoking_status || 'Not specified';
    document.getElementById('alcoholUse').textContent = patient.alcohol_use || 'Not specified';
    document.getElementById('exerciseFrequency').textContent = patient.exercise_frequency || 'Not specified';
    document.getElementById('occupation').textContent = patient.occupation || 'Not specified';

    // Insurance & Pharmacy
    document.getElementById('insuranceProvider').textContent = patient.insurance_provider || 'Not provided';
    document.getElementById('insuranceNumber').textContent = patient.pat_insurance_no || 'Not provided';
    document.getElementById('insuranceGroup').textContent = patient.insurance_group || 'Not provided';
    document.getElementById('preferredPharmacy').textContent = patient.preferred_pharmacy || 'Not specified';

    // Family History
    document.getElementById('familyHistory').textContent = patient.family_history || 'No significant family history reported';
}

function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }

    return age + ' years';
}

async function loadHealthRecords() {
    try {
        showLoadingIndicator(true);
        
        // Try to load from API first
        let records = [];
        try {
            const response = await fetch(`/patient/${user.user_id}/health-records`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                records = await response.json();
            } else {
                throw new Error('API not available');
            }
        } catch (error) {
            console.log('Using sample health records');
            records = getSampleHealthRecords();
        }

        healthRecords = records;
        displayHealthRecords(records);
        updateHealthSummary(records);
        
    } catch (error) {
        console.error('Error loading health records:', error);
        showAlert('Error loading health records: ' + error.message, 'danger');
    } finally {
        showLoadingIndicator(false);
    }
}

function getSampleHealthRecords() {
    const patientName = `${user.first_name || 'Jane'} ${user.last_name || 'Doe'}`;

    return [
        {
            record_id: 1,
            record_date: '2024-01-20',
            record_type: 'diagnosis',
            title: 'Hypertension Diagnosis',
            description: 'Patient diagnosed with stage 1 hypertension. Blood pressure consistently elevated above 140/90 mmHg.',
            provider: 'Dr. Sarah Johnson',
            status: 'Active',
            details: {
                diagnosis_code: 'I10',
                severity: 'Mild to Moderate',
                treatment_plan: 'Lifestyle modifications and medication therapy',
                follow_up: 'Monthly blood pressure monitoring'
            }
        },
        {
            record_id: 2,
            record_date: '2024-01-20',
            record_type: 'prescription',
            title: 'Lisinopril 10mg',
            description: 'ACE inhibitor prescribed for blood pressure management. Take once daily with or without food.',
            provider: 'Dr. Sarah Johnson',
            status: 'Active',
            details: {
                medication: 'Lisinopril',
                dosage: '10mg',
                frequency: 'Once daily',
                duration: '90 days',
                refills: '2 remaining',
                instructions: 'Take at the same time each day. Monitor blood pressure regularly.'
            }
        },
        {
            record_id: 3,
            record_date: '2024-01-18',
            record_type: 'lab-result',
            title: 'Comprehensive Metabolic Panel',
            description: 'Complete blood chemistry panel including glucose, electrolytes, kidney and liver function tests.',
            provider: 'City Medical Laboratory',
            status: 'Completed',
            details: {
                test_name: 'Comprehensive Metabolic Panel (CMP)',
                glucose: '95 mg/dL (Normal: 70-100)',
                sodium: '140 mEq/L (Normal: 136-145)',
                potassium: '4.2 mEq/L (Normal: 3.5-5.0)',
                creatinine: '1.0 mg/dL (Normal: 0.7-1.3)',
                bun: '15 mg/dL (Normal: 7-20)',
                notes: 'All values within normal limits'
            }
        },
        {
            record_id: 4,
            record_date: '2024-01-15',
            record_type: 'appointment',
            title: 'Annual Physical Examination',
            description: 'Comprehensive annual physical examination including vital signs, system review, and preventive care.',
            provider: 'Dr. Sarah Johnson',
            status: 'Completed',
            details: {
                appointment_type: 'Annual Physical',
                duration: '45 minutes',
                vital_signs: 'BP: 145/92, HR: 78, Temp: 98.6°F, Weight: 180 lbs',
                assessment: 'Generally healthy with elevated blood pressure',
                recommendations: 'Start antihypertensive medication, dietary changes, regular exercise'
            }
        },
        {
            record_id: 5,
            record_date: '2024-01-10',
            record_type: 'lab-result',
            title: 'Lipid Panel',
            description: 'Cholesterol and triglyceride levels assessment for cardiovascular risk evaluation.',
            provider: 'City Medical Laboratory',
            status: 'Completed',
            details: {
                test_name: 'Lipid Panel',
                total_cholesterol: '195 mg/dL (Normal: <200)',
                ldl: '125 mg/dL (Normal: <100)',
                hdl: '45 mg/dL (Normal: >40)',
                triglycerides: '150 mg/dL (Normal: <150)',
                notes: 'LDL slightly elevated, recommend dietary modifications'
            }
        },
        {
            record_id: 6,
            record_date: '2023-12-20',
            record_type: 'procedure',
            title: 'Electrocardiogram (ECG)',
            description: 'Routine ECG to assess heart rhythm and electrical activity.',
            provider: 'Dr. Michael Chen - Cardiology',
            status: 'Completed',
            details: {
                procedure_name: 'Electrocardiogram (ECG)',
                indication: 'Hypertension workup',
                findings: 'Normal sinus rhythm, no acute changes',
                interpretation: 'Normal ECG',
                recommendations: 'Continue current treatment plan'
            }
        },
        {
            record_id: 7,
            record_date: '2023-11-15',
            record_type: 'prescription',
            title: 'Metformin 500mg',
            description: 'Diabetes medication for blood sugar control. Take twice daily with meals.',
            provider: 'Dr. Sarah Johnson',
            status: 'Discontinued',
            details: {
                medication: 'Metformin',
                dosage: '500mg',
                frequency: 'Twice daily',
                duration: '90 days',
                reason_discontinued: 'Patient no longer diabetic after lifestyle changes',
                date_discontinued: '2024-01-01'
            }
        },
        {
            record_id: 8,
            record_date: '2023-10-30',
            record_type: 'appointment',
            title: 'Diabetes Follow-up',
            description: 'Follow-up appointment for diabetes management and blood sugar monitoring.',
            provider: 'Dr. Sarah Johnson',
            status: 'Completed',
            details: {
                appointment_type: 'Follow-up Visit',
                duration: '30 minutes',
                hba1c: '5.8% (Excellent control)',
                blood_glucose: '88 mg/dL (Normal)',
                assessment: 'Excellent diabetes control with lifestyle modifications',
                plan: 'Continue current lifestyle, consider discontinuing medication'
            }
        },
        {
            record_id: 9,
            record_date: '2023-09-20',
            record_type: 'lab-result',
            title: 'Hemoglobin A1C',
            description: 'Three-month average blood sugar level test for diabetes monitoring.',
            provider: 'City Medical Laboratory',
            status: 'Completed',
            details: {
                test_name: 'Hemoglobin A1C',
                result: '5.8%',
                reference_range: '<7% (Good control)',
                previous_result: '6.2% (3 months ago)',
                trend: 'Improving',
                notes: 'Excellent improvement in diabetes control'
            }
        },
        {
            record_id: 10,
            record_date: '2023-08-15',
            record_type: 'diagnosis',
            title: 'Type 2 Diabetes Mellitus - Resolved',
            description: 'Type 2 diabetes successfully managed through lifestyle modifications and medication.',
            provider: 'Dr. Sarah Johnson',
            status: 'Resolved',
            details: {
                diagnosis_code: 'E11.9',
                resolution_date: '2024-01-01',
                treatment_duration: '18 months',
                resolution_method: 'Lifestyle modifications (diet and exercise)',
                current_status: 'Normal glucose tolerance, no medication required'
            }
        }
    ];
}

function displayHealthRecords(records) {
    const tableBody = document.getElementById('recordsTableBody');
    tableBody.innerHTML = '';

    records.forEach(record => {
        const row = createRecordRow(record);
        tableBody.appendChild(row);
    });

    // Initialize or refresh DataTable
    if (recordsTable) {
        recordsTable.destroy();
    }

    recordsTable = $('#recordsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[0, 'desc']], // Sort by date descending
        columnDefs: [
            { targets: [5], orderable: false } // Actions column
        ]
    });

    document.getElementById('recordsTableContainer').style.display = 'block';
}

function createRecordRow(record) {
    const row = document.createElement('tr');

    // Date
    const dateCell = document.createElement('td');
    dateCell.textContent = new Date(record.record_date).toLocaleDateString();

    // Type
    const typeCell = document.createElement('td');
    typeCell.innerHTML = `<span class="record-type type-${record.record_type}">${record.record_type.replace('-', ' ').toUpperCase()}</span>`;

    // Description
    const descCell = document.createElement('td');
    descCell.innerHTML = `
        <div>
            <strong>${record.title}</strong><br>
            <small class="text-muted">${record.description.substring(0, 100)}${record.description.length > 100 ? '...' : ''}</small>
        </div>
    `;

    // Provider
    const providerCell = document.createElement('td');
    providerCell.textContent = record.provider;

    // Status
    const statusCell = document.createElement('td');
    const statusClass = record.status.toLowerCase() === 'active' ? 'success' :
                       record.status.toLowerCase() === 'completed' ? 'info' :
                       record.status.toLowerCase() === 'resolved' ? 'primary' : 'secondary';
    statusCell.innerHTML = `<span class="badge bg-${statusClass}">${record.status}</span>`;

    // Actions
    const actionsCell = document.createElement('td');
    actionsCell.innerHTML = `
        <div class="btn-group btn-group-sm" role="group">
            <button type="button" class="btn btn-outline-info" onclick="viewRecordDetails(${record.record_id})" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary" onclick="downloadRecord(${record.record_id})" title="Download">
                <i class="fas fa-download"></i>
            </button>
        </div>
    `;

    row.appendChild(dateCell);
    row.appendChild(typeCell);
    row.appendChild(descCell);
    row.appendChild(providerCell);
    row.appendChild(statusCell);
    row.appendChild(actionsCell);

    return row;
}

function updateHealthSummary(records) {
    const summary = {
        activePrescriptions: records.filter(r => r.record_type === 'prescription' && r.status === 'Active').length,
        labResults: records.filter(r => r.record_type === 'lab-result').length,
        totalAppointments: records.filter(r => r.record_type === 'appointment').length,
        vitalSigns: records.filter(r => r.record_type === 'vital-signs').length + 15 // Add some for demo
    };

    document.getElementById('activePrescriptions').textContent = summary.activePrescriptions;
    document.getElementById('labResults').textContent = summary.labResults;
    document.getElementById('totalAppointments').textContent = summary.totalAppointments;
    document.getElementById('vitalSigns').textContent = summary.vitalSigns;
}

function viewRecordDetails(recordId) {
    const record = healthRecords.find(r => r.record_id === recordId);
    if (!record) {
        showAlert('Record not found', 'danger');
        return;
    }

    const modalContent = document.getElementById('recordDetailsContent');
    modalContent.innerHTML = generateRecordDetailsHTML(record);

    new bootstrap.Modal(document.getElementById('recordDetailsModal')).show();
}

function generateRecordDetailsHTML(record) {
    let detailsHTML = `
        <div class="row mb-3">
            <div class="col-md-6">
                <h6>Record Information</h6>
                <table class="table table-borderless">
                    <tr><td><strong>Date:</strong></td><td>${new Date(record.record_date).toLocaleDateString()}</td></tr>
                    <tr><td><strong>Type:</strong></td><td><span class="record-type type-${record.record_type}">${record.record_type.replace('-', ' ').toUpperCase()}</span></td></tr>
                    <tr><td><strong>Provider:</strong></td><td>${record.provider}</td></tr>
                    <tr><td><strong>Status:</strong></td><td><span class="badge bg-info">${record.status}</span></td></tr>
                </table>
            </div>
            <div class="col-md-6">
                <h6>Description</h6>
                <p>${record.description}</p>
            </div>
        </div>
    `;

    if (record.details) {
        detailsHTML += `
            <div class="row">
                <div class="col-12">
                    <h6>Detailed Information</h6>
                    <div class="card">
                        <div class="card-body">
        `;

        Object.entries(record.details).forEach(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            detailsHTML += `
                <div class="row mb-2">
                    <div class="col-md-4"><strong>${label}:</strong></div>
                    <div class="col-md-8">${value}</div>
                </div>
            `;
        });

        detailsHTML += `
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    return detailsHTML;
}

function downloadRecord(recordId) {
    const record = healthRecords.find(r => r.record_id === recordId);
    if (record) {
        showAlert(`Downloading record: ${record.title}`, 'info');
        // TODO: Implement actual download functionality
    }
}

function exportHealthRecords() {
    showAlert('Exporting health records...', 'info');
    // TODO: Implement export functionality
}

function printRecord() {
    window.print();
}

// Utility functions
function showLoadingIndicator(show) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const tableContainer = document.getElementById('recordsTableContainer');

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

// Vital Signs Chart Functions
async function loadVitalSignsData() {
    try {
        // Try to load from API first
        let vitals = [];
        try {
            const response = await fetch(`/patient/${user.user_id}/vital-signs`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                vitals = await response.json();
            } else {
                throw new Error('API not available');
            }
        } catch (error) {
            console.log('Using sample vital signs data');
            vitals = getSampleVitalSignsData();
        }

        vitalSignsData = vitals;
        initializeVitalsChart();
        updateLatestVitals();

    } catch (error) {
        console.error('Error loading vital signs:', error);
        vitalSignsData = getSampleVitalSignsData();
        initializeVitalsChart();
        updateLatestVitals();
    }
}

function getSampleVitalSignsData() {
    const data = [];
    const now = new Date();

    // Generate 30 days of sample vital signs data
    for (let i = 29; i >= 0; i--) {
        const date = new Date(now);
        date.setDate(date.getDate() - i);

        // Generate realistic vital signs with some variation for female patient
        const baseHR = 75; // Slightly higher for females
        const baseSystolic = 120;
        const baseDiastolic = 80;
        const baseTemp = 98.6;
        const baseWeight = 140; // Updated for Jane Doe

        data.push({
            date: date.toISOString().split('T')[0],
            heart_rate: baseHR + Math.floor(Math.random() * 20) - 10, // 65-85
            systolic_bp: baseSystolic + Math.floor(Math.random() * 30) - 15, // 105-135
            diastolic_bp: baseDiastolic + Math.floor(Math.random() * 20) - 10, // 70-90
            temperature: (baseTemp + (Math.random() * 2) - 1).toFixed(1), // 97.6-99.6
            weight: (baseWeight + (Math.random() * 10) - 5).toFixed(1), // 135-145
            recorded_at: date.toISOString()
        });
    }

    return data;
}

function initializeVitalsChart() {
    const ctx = document.getElementById('vitalsChart').getContext('2d');

    // Destroy existing chart if it exists
    if (vitalsChart) {
        vitalsChart.destroy();
    }

    vitalsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Vital Signs Trends'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });

    // Initial chart update
    updateVitalsChart();
}

function updateVitalsChart() {
    const vitalType = document.getElementById('vitalTypeSelect').value;
    const timeRange = parseInt(document.getElementById('timeRangeSelect').value);

    // Filter data by time range
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - timeRange);

    const filteredData = vitalSignsData.filter(vital =>
        new Date(vital.date) >= cutoffDate
    );

    // Prepare chart data based on vital type
    let datasets = [];
    let yAxisLabel = '';

    switch (vitalType) {
        case 'blood_pressure':
            datasets = [
                {
                    label: 'Systolic BP',
                    data: filteredData.map(vital => vital.systolic_bp),
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'Diastolic BP',
                    data: filteredData.map(vital => vital.diastolic_bp),
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.1
                }
            ];
            yAxisLabel = 'Blood Pressure (mmHg)';
            break;

        case 'heart_rate':
            datasets = [{
                label: 'Heart Rate',
                data: filteredData.map(vital => vital.heart_rate),
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                tension: 0.1
            }];
            yAxisLabel = 'Heart Rate (bpm)';
            break;

        case 'temperature':
            datasets = [{
                label: 'Temperature',
                data: filteredData.map(vital => parseFloat(vital.temperature)),
                borderColor: 'rgb(255, 205, 86)',
                backgroundColor: 'rgba(255, 205, 86, 0.1)',
                tension: 0.1
            }];
            yAxisLabel = 'Temperature (°F)';
            break;

        case 'weight':
            datasets = [{
                label: 'Weight',
                data: filteredData.map(vital => parseFloat(vital.weight)),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                tension: 0.1
            }];
            yAxisLabel = 'Weight (lbs)';
            break;
    }

    // Update chart
    vitalsChart.data.labels = filteredData.map(vital =>
        new Date(vital.date).toLocaleDateString()
    );
    vitalsChart.data.datasets = datasets;
    vitalsChart.options.scales.y.title.text = yAxisLabel;
    vitalsChart.update();
}

function updateLatestVitals() {
    if (vitalSignsData.length === 0) return;

    const latest = vitalSignsData[vitalSignsData.length - 1];

    document.getElementById('latestBP').textContent = `${latest.systolic_bp}/${latest.diastolic_bp}`;
    document.getElementById('latestHR').textContent = `${latest.heart_rate} bpm`;
    document.getElementById('latestTemp').textContent = `${latest.temperature}°F`;
    document.getElementById('latestWeight').textContent = `${latest.weight} lbs`;
}
