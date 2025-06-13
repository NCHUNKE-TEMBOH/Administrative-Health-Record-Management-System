// Pending Tests Management JavaScript

// Sample pending tests data
const pendingTestsData = [
    {
        test_id: 1001,
        pat_first_name: 'John',
        pat_last_name: 'Smith',
        test_type: 'Complete Blood Count',
        priority: 'stat',
        requested_date: '2024-01-15T06:30:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Patient experiencing chest pain'
    },
    {
        test_id: 1002,
        pat_first_name: 'Maria',
        pat_last_name: 'Garcia',
        test_type: 'Blood Culture',
        priority: 'stat',
        requested_date: '2024-01-15T07:15:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Suspected sepsis'
    },
    {
        test_id: 1003,
        pat_first_name: 'Jennifer',
        pat_last_name: 'Wilson',
        test_type: 'Pregnancy Test',
        priority: 'stat',
        requested_date: '2024-01-15T08:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        status: 'pending',
        sample_type: 'Urine',
        notes: 'Emergency department request'
    },
    {
        test_id: 1004,
        pat_first_name: 'Robert',
        pat_last_name: 'Taylor',
        test_type: 'Cardiac Enzymes',
        priority: 'stat',
        requested_date: '2024-01-15T08:45:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Possible MI'
    },
    {
        test_id: 1005,
        pat_first_name: 'Lisa',
        pat_last_name: 'Anderson',
        test_type: 'Comprehensive Metabolic Panel',
        priority: 'urgent',
        requested_date: '2024-01-15T09:30:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Pre-operative workup'
    },
    {
        test_id: 1006,
        pat_first_name: 'David',
        pat_last_name: 'Martinez',
        test_type: 'Thyroid Function Panel',
        priority: 'urgent',
        requested_date: '2024-01-15T10:15:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Follow-up thyroid levels'
    },
    {
        test_id: 1007,
        pat_first_name: 'Susan',
        pat_last_name: 'Lee',
        test_type: 'Liver Function Panel',
        priority: 'urgent',
        requested_date: '2024-01-15T11:00:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Elevated liver enzymes'
    },
    {
        test_id: 1008,
        pat_first_name: 'James',
        pat_last_name: 'White',
        test_type: 'Coagulation Panel',
        priority: 'urgent',
        requested_date: '2024-01-15T11:45:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Pre-surgical clearance'
    },
    {
        test_id: 1009,
        pat_first_name: 'Patricia',
        pat_last_name: 'Clark',
        test_type: 'Inflammatory Markers',
        priority: 'urgent',
        requested_date: '2024-01-15T12:30:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Suspected inflammatory condition'
    },
    {
        test_id: 1010,
        pat_first_name: 'Michael',
        pat_last_name: 'Johnson',
        test_type: 'Urinalysis',
        priority: 'normal',
        requested_date: '2024-01-15T13:15:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        status: 'pending',
        sample_type: 'Urine',
        notes: 'Routine screening'
    },
    {
        test_id: 1011,
        pat_first_name: 'Linda',
        pat_last_name: 'Brown',
        test_type: 'Lipid Panel',
        priority: 'normal',
        requested_date: '2024-01-15T14:00:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Annual physical exam'
    },
    {
        test_id: 1012,
        pat_first_name: 'Christopher',
        pat_last_name: 'Davis',
        test_type: 'Hemoglobin A1C',
        priority: 'normal',
        requested_date: '2024-01-15T14:45:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Diabetes monitoring'
    },
    {
        test_id: 1013,
        pat_first_name: 'Barbara',
        pat_last_name: 'Miller',
        test_type: 'Vitamin D Level',
        priority: 'normal',
        requested_date: '2024-01-15T15:30:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Vitamin deficiency screening'
    },
    {
        test_id: 1014,
        pat_first_name: 'Daniel',
        pat_last_name: 'Wilson',
        test_type: 'Prostate Specific Antigen',
        priority: 'normal',
        requested_date: '2024-01-15T16:15:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        status: 'pending',
        sample_type: 'Blood',
        notes: 'Prostate cancer screening'
    },
    {
        test_id: 1015,
        pat_first_name: 'Nancy',
        pat_last_name: 'Moore',
        test_type: 'Stool Culture',
        priority: 'normal',
        requested_date: '2024-01-15T17:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        status: 'pending',
        sample_type: 'Stool',
        notes: 'GI symptoms investigation'
    }
];

let allPendingTests = [...pendingTestsData];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadPendingTests();
    setupEventListeners();
});

function setupEventListeners() {
    // Filter event listeners
    document.getElementById('priorityFilter').addEventListener('change', filterTests);
    document.getElementById('testTypeFilter').addEventListener('change', filterTests);
    document.getElementById('patientSearch').addEventListener('input', filterTests);
}

function loadPendingTests() {
    try {
        displayPendingTests(allPendingTests);
        updateQuickStats(allPendingTests);
    } catch (error) {
        console.error('Error loading pending tests:', error);
        showError('Failed to load pending tests');
    }
}

function displayPendingTests(tests) {
    const tbody = document.getElementById('pendingTestsTableBody');

    if (tests.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center py-4">
                    <i class="fas fa-info-circle text-muted fa-2x mb-2"></i>
                    <p class="text-muted">No pending tests found</p>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = tests.map(test => `
        <tr class="${getPriorityRowClass(test.priority)}">
            <td><strong>#${test.test_id}</strong></td>
            <td>${test.pat_first_name} ${test.pat_last_name}</td>
            <td>
                <span class="badge bg-light text-dark">${test.test_type}</span>
            </td>
            <td>
                <span class="badge ${getPriorityBadgeClass(test.priority)}">
                    ${test.priority.toUpperCase()}
                </span>
            </td>
            <td>${formatDateTime(test.requested_date)}</td>
            <td>Dr. ${test.requested_by_first_name} ${test.requested_by_last_name}</td>
            <td>
                <span class="badge ${getWaitTimeBadgeClass(test.requested_date)}">
                    ${getWaitTime(test.requested_date)}
                </span>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewTestDetails(${test.test_id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="startTest(${test.test_id})" title="Start Test">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="btn btn-outline-info" onclick="addNote(${test.test_id})" title="Add Note">
                        <i class="fas fa-sticky-note"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function updateQuickStats(tests) {
    const pending = tests.filter(t => t.status === 'pending').length;
    const stat = tests.filter(t => t.priority === 'stat').length;
    const urgent = tests.filter(t => t.priority === 'urgent').length;
    const normal = tests.filter(t => t.priority === 'normal').length;

    document.getElementById('pendingCount').textContent = pending;
    document.getElementById('statCount').textContent = stat;
    document.getElementById('urgentCount').textContent = urgent;
    document.getElementById('normalCount').textContent = normal;
}

function filterTests() {
    const priorityFilter = document.getElementById('priorityFilter').value;
    const testTypeFilter = document.getElementById('testTypeFilter').value;
    const patientSearch = document.getElementById('patientSearch').value.toLowerCase();

    let filteredTests = allPendingTests.filter(test => {
        const matchesPriority = !priorityFilter || test.priority === priorityFilter;
        const matchesTestType = !testTypeFilter || test.test_type.toLowerCase().includes(testTypeFilter);
        const matchesPatient = !patientSearch ||
            `${test.pat_first_name} ${test.pat_last_name}`.toLowerCase().includes(patientSearch);

        return matchesPriority && matchesTestType && matchesPatient;
    });

    displayPendingTests(filteredTests);
}

// Utility functions
function getPriorityBadgeClass(priority) {
    switch (priority) {
        case 'stat': return 'bg-danger';
        case 'urgent': return 'bg-warning';
        case 'normal': return 'bg-secondary';
        default: return 'bg-secondary';
    }
}

function getPriorityRowClass(priority) {
    switch (priority) {
        case 'stat': return 'table-danger';
        case 'urgent': return 'table-warning';
        default: return '';
    }
}

function getWaitTime(requestedDate) {
    if (!requestedDate) return 'N/A';

    const requested = new Date(requestedDate);
    const now = new Date();
    const diffMs = now - requested;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
        return `${diffDays}d ${diffHours % 24}h`;
    } else {
        return `${diffHours}h`;
    }
}

function getWaitTimeBadgeClass(requestedDate) {
    if (!requestedDate) return 'bg-secondary';

    const requested = new Date(requestedDate);
    const now = new Date();
    const diffHours = (now - requested) / (1000 * 60 * 60);

    if (diffHours > 24) return 'bg-danger';
    if (diffHours > 8) return 'bg-warning';
    return 'bg-success';
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

// Action functions
function startTest(testId) {
    if (!confirm('Start processing this test? This will move it to the in-progress section.')) {
        return;
    }

    // Remove test from pending list (simulate moving to in-progress)
    allPendingTests = allPendingTests.filter(test => test.test_id !== testId);
    
    showSuccess('Test started successfully and moved to in-progress');
    loadPendingTests(); // Refresh the display
}

function viewTestDetails(testId) {
    const test = allPendingTests.find(t => t.test_id === testId);
    if (test) {
        alert(`Test Details:\n\nTest ID: ${test.test_id}\nPatient: ${test.pat_first_name} ${test.pat_last_name}\nTest Type: ${test.test_type}\nPriority: ${test.priority}\nSample Type: ${test.sample_type}\nRequested: ${formatDateTime(test.requested_date)}\nRequested By: Dr. ${test.requested_by_first_name} ${test.requested_by_last_name}\nNotes: ${test.notes}`);
    }
}

function addNote(testId) {
    const note = prompt('Add a note for this test:');
    if (note && note.trim()) {
        const test = allPendingTests.find(t => t.test_id === testId);
        if (test) {
            test.notes = test.notes ? `${test.notes}\n${note}` : note;
            showSuccess('Note added successfully');
        }
    }
}

function refreshPendingTests() {
    loadPendingTests();
    showSuccess('Pending tests refreshed');
}

function refreshPage() {
    location.reload();
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

function showError(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}
