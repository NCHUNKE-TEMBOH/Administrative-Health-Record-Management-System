// Quality Control Management JavaScript

// Sample QC test data
const qcTestsData = [
    {
        id: 'QC001',
        testType: 'Complete Blood Count',
        controlLevel: 'Normal',
        expectedRange: '4.5-5.5 x10^6/μL',
        actualResult: '5.1 x10^6/μL',
        status: 'passed',
        date: '2024-01-15 08:30',
        technician: 'Michael Chen'
    },
    {
        id: 'QC002',
        testType: 'Glucose',
        controlLevel: 'High',
        expectedRange: '250-300 mg/dL',
        actualResult: '275 mg/dL',
        status: 'passed',
        date: '2024-01-15 09:15',
        technician: 'Sarah Wilson'
    },
    {
        id: 'QC003',
        testType: 'Cholesterol',
        controlLevel: 'Low',
        expectedRange: '80-120 mg/dL',
        actualResult: '95 mg/dL',
        status: 'passed',
        date: '2024-01-15 10:00',
        technician: 'Michael Chen'
    },
    {
        id: 'QC004',
        testType: 'Hemoglobin',
        controlLevel: 'Normal',
        expectedRange: '12-16 g/dL',
        actualResult: '18.2 g/dL',
        status: 'failed',
        date: '2024-01-15 10:45',
        technician: 'Sarah Wilson'
    },
    {
        id: 'QC005',
        testType: 'Creatinine',
        controlLevel: 'High',
        expectedRange: '2.0-3.0 mg/dL',
        actualResult: '3.5 mg/dL',
        status: 'failed',
        date: '2024-01-15 11:30',
        technician: 'Michael Chen'
    },
    {
        id: 'QC006',
        testType: 'Liver Enzymes',
        controlLevel: 'Normal',
        expectedRange: '10-40 U/L',
        actualResult: '25 U/L',
        status: 'passed',
        date: '2024-01-15 12:15',
        technician: 'Sarah Wilson'
    },
    {
        id: 'QC007',
        testType: 'Electrolytes',
        controlLevel: 'Low',
        expectedRange: '135-145 mEq/L',
        actualResult: '140 mEq/L',
        status: 'passed',
        date: '2024-01-15 13:00',
        technician: 'Michael Chen'
    },
    {
        id: 'QC008',
        testType: 'Thyroid Function',
        controlLevel: 'High',
        expectedRange: '8-12 μIU/mL',
        actualResult: '10.5 μIU/mL',
        status: 'passed',
        date: '2024-01-15 13:45',
        technician: 'Sarah Wilson'
    },
    {
        id: 'QC009',
        testType: 'Cardiac Markers',
        controlLevel: 'Normal',
        expectedRange: '0-0.04 ng/mL',
        actualResult: '0.02 ng/mL',
        status: 'passed',
        date: '2024-01-15 14:30',
        technician: 'Michael Chen'
    },
    {
        id: 'QC010',
        testType: 'Coagulation',
        controlLevel: 'Normal',
        expectedRange: '11-13 seconds',
        actualResult: '12.1 seconds',
        status: 'passed',
        date: '2024-01-15 15:15',
        technician: 'Sarah Wilson'
    },
    {
        id: 'QC011',
        testType: 'Urinalysis',
        controlLevel: 'Low',
        expectedRange: '1.003-1.030',
        actualResult: '1.015',
        status: 'passed',
        date: '2024-01-15 16:00',
        technician: 'Michael Chen'
    },
    {
        id: 'QC012',
        testType: 'Blood Gas',
        controlLevel: 'High',
        expectedRange: '7.35-7.45',
        actualResult: '7.40',
        status: 'passed',
        date: '2024-01-15 16:45',
        technician: 'Sarah Wilson'
    }
];

// Sample calibration data
const calibrationData = [
    {
        equipment: 'Hematology Analyzer HA-2000',
        lastCalibration: '2024-01-10',
        nextDue: '2024-01-17',
        status: 'calibrated',
        technician: 'Michael Chen'
    },
    {
        equipment: 'Chemistry Analyzer CA-500',
        lastCalibration: '2024-01-12',
        nextDue: '2024-01-19',
        status: 'calibrated',
        technician: 'Sarah Wilson'
    },
    {
        equipment: 'Microbiology Incubator MI-300',
        lastCalibration: '2024-01-08',
        nextDue: '2024-01-15',
        status: 'maintenance',
        technician: 'Michael Chen'
    },
    {
        equipment: 'PCR Machine PCR-100',
        lastCalibration: '2024-01-14',
        nextDue: '2024-01-21',
        status: 'calibrated',
        technician: 'Sarah Wilson'
    },
    {
        equipment: 'Centrifuge CF-400',
        lastCalibration: '2024-01-11',
        nextDue: '2024-01-18',
        status: 'calibrated',
        technician: 'Michael Chen'
    }
];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadQCTests();
    loadCalibrationSchedule();
    initializeDataTables();
});

// Load QC tests data
function loadQCTests() {
    const tbody = document.getElementById('qcTestsTableBody');
    tbody.innerHTML = '';

    qcTestsData.forEach(test => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${test.id}</strong></td>
            <td>${test.testType}</td>
            <td>${test.controlLevel}</td>
            <td>${test.expectedRange}</td>
            <td>${test.actualResult}</td>
            <td><span class="status-badge status-${test.status}">${test.status.toUpperCase()}</span></td>
            <td>${formatDateTime(test.date)}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewQCDetails('${test.id}')" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-info" onclick="printQCReport('${test.id}')" title="Print Report">
                        <i class="fas fa-print"></i>
                    </button>
                    ${test.status === 'failed' ? 
                        `<button class="btn btn-outline-warning" onclick="investigateFailure('${test.id}')" title="Investigate">
                            <i class="fas fa-search"></i>
                        </button>` : ''
                    }
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Load calibration schedule
function loadCalibrationSchedule() {
    const tbody = document.getElementById('calibrationTableBody');
    tbody.innerHTML = '';

    calibrationData.forEach(cal => {
        const row = document.createElement('tr');
        const daysDue = getDaysUntilDue(cal.nextDue);
        const statusClass = daysDue <= 0 ? 'maintenance' : cal.status;
        
        row.innerHTML = `
            <td>${cal.equipment}</td>
            <td>${formatDate(cal.lastCalibration)}</td>
            <td>${formatDate(cal.nextDue)} ${daysDue <= 3 ? '<span class="badge bg-warning">Due Soon</span>' : ''}</td>
            <td><span class="status-badge status-${statusClass}">${statusClass.toUpperCase()}</span></td>
            <td>${cal.technician}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="performCalibration('${cal.equipment}')" title="Calibrate">
                        <i class="fas fa-tools"></i>
                    </button>
                    <button class="btn btn-outline-info" onclick="viewCalibrationHistory('${cal.equipment}')" title="History">
                        <i class="fas fa-history"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Initialize DataTables
function initializeDataTables() {
    $('#qcTestsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[6, 'desc']], // Sort by date descending
        columnDefs: [
            { orderable: false, targets: [7] } // Disable sorting for actions column
        ]
    });

    $('#calibrationTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[2, 'asc']], // Sort by next due date ascending
        columnDefs: [
            { orderable: false, targets: [5] } // Disable sorting for actions column
        ]
    });
}

// Utility functions
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function getDaysUntilDue(dueDateString) {
    const dueDate = new Date(dueDateString);
    const today = new Date();
    const diffTime = dueDate - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

// Action functions
function runQCTest() {
    showAlert('QC Test initiated. Please follow standard operating procedures.', 'info');
}

function viewQCDetails(testId) {
    const test = qcTestsData.find(t => t.id === testId);
    if (test) {
        alert(`QC Test Details:\n\nTest ID: ${test.id}\nType: ${test.testType}\nControl Level: ${test.controlLevel}\nExpected: ${test.expectedRange}\nActual: ${test.actualResult}\nStatus: ${test.status}\nTechnician: ${test.technician}`);
    }
}

function printQCReport(testId) {
    showAlert('QC report sent to printer.', 'success');
}

function investigateFailure(testId) {
    showAlert('Failure investigation protocol initiated. Please document findings.', 'warning');
}

function performCalibration(equipment) {
    showAlert(`Calibration procedure started for ${equipment}. Follow calibration protocol.`, 'info');
}

function viewCalibrationHistory(equipment) {
    showAlert(`Calibration history for ${equipment} displayed.`, 'info');
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 5000);
}
