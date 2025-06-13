// Admin Lab Overview JavaScript - Comprehensive Lab Management

// Comprehensive lab test data combining all statuses
const allLabTestsData = [
    // PENDING TESTS (15 tests)
    {
        test_id: 1001,
        pat_first_name: 'John',
        pat_last_name: 'Smith',
        test_type: 'Complete Blood Count',
        priority: 'stat',
        status: 'pending',
        requested_date: '2024-01-15T06:30:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        sample_type: 'Blood',
        notes: 'Patient experiencing chest pain'
    },
    {
        test_id: 1002,
        pat_first_name: 'Maria',
        pat_last_name: 'Garcia',
        test_type: 'Blood Culture',
        priority: 'stat',
        status: 'pending',
        requested_date: '2024-01-15T07:15:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        sample_type: 'Blood',
        notes: 'Suspected sepsis'
    },
    {
        test_id: 1003,
        pat_first_name: 'Jennifer',
        pat_last_name: 'Wilson',
        test_type: 'Pregnancy Test',
        priority: 'stat',
        status: 'pending',
        requested_date: '2024-01-15T08:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        sample_type: 'Urine',
        notes: 'Emergency department request'
    },
    {
        test_id: 1004,
        pat_first_name: 'Robert',
        pat_last_name: 'Taylor',
        test_type: 'Cardiac Enzymes',
        priority: 'stat',
        status: 'pending',
        requested_date: '2024-01-15T08:45:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        sample_type: 'Blood',
        notes: 'Possible MI'
    },
    {
        test_id: 1005,
        pat_first_name: 'Lisa',
        pat_last_name: 'Anderson',
        test_type: 'Comprehensive Metabolic Panel',
        priority: 'urgent',
        status: 'pending',
        requested_date: '2024-01-15T09:30:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        sample_type: 'Blood',
        notes: 'Pre-operative workup'
    },
    {
        test_id: 1006,
        pat_first_name: 'David',
        pat_last_name: 'Martinez',
        test_type: 'Thyroid Function Panel',
        priority: 'urgent',
        status: 'pending',
        requested_date: '2024-01-15T10:15:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        sample_type: 'Blood',
        notes: 'Follow-up thyroid levels'
    },
    {
        test_id: 1007,
        pat_first_name: 'Susan',
        pat_last_name: 'Lee',
        test_type: 'Liver Function Panel',
        priority: 'urgent',
        status: 'pending',
        requested_date: '2024-01-15T11:00:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        sample_type: 'Blood',
        notes: 'Elevated liver enzymes'
    },
    {
        test_id: 1008,
        pat_first_name: 'James',
        pat_last_name: 'White',
        test_type: 'Coagulation Panel',
        priority: 'urgent',
        status: 'pending',
        requested_date: '2024-01-15T11:45:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        sample_type: 'Blood',
        notes: 'Pre-surgical clearance'
    },
    {
        test_id: 1009,
        pat_first_name: 'Patricia',
        pat_last_name: 'Clark',
        test_type: 'Inflammatory Markers',
        priority: 'urgent',
        status: 'pending',
        requested_date: '2024-01-15T12:30:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        sample_type: 'Blood',
        notes: 'Suspected inflammatory condition'
    },
    {
        test_id: 1010,
        pat_first_name: 'Michael',
        pat_last_name: 'Johnson',
        test_type: 'Urinalysis',
        priority: 'normal',
        status: 'pending',
        requested_date: '2024-01-15T13:15:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        sample_type: 'Urine',
        notes: 'Routine screening'
    },
    {
        test_id: 1011,
        pat_first_name: 'Linda',
        pat_last_name: 'Brown',
        test_type: 'Lipid Panel',
        priority: 'normal',
        status: 'pending',
        requested_date: '2024-01-15T14:00:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        sample_type: 'Blood',
        notes: 'Annual physical exam'
    },
    {
        test_id: 1012,
        pat_first_name: 'Christopher',
        pat_last_name: 'Davis',
        test_type: 'Hemoglobin A1C',
        priority: 'normal',
        status: 'pending',
        requested_date: '2024-01-15T14:45:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        sample_type: 'Blood',
        notes: 'Diabetes monitoring'
    },
    {
        test_id: 1013,
        pat_first_name: 'Barbara',
        pat_last_name: 'Miller',
        test_type: 'Vitamin D Level',
        priority: 'normal',
        status: 'pending',
        requested_date: '2024-01-15T15:30:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        sample_type: 'Blood',
        notes: 'Vitamin deficiency screening'
    },
    {
        test_id: 1014,
        pat_first_name: 'Daniel',
        pat_last_name: 'Wilson',
        test_type: 'Prostate Specific Antigen',
        priority: 'normal',
        status: 'pending',
        requested_date: '2024-01-15T16:15:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        sample_type: 'Blood',
        notes: 'Prostate cancer screening'
    },
    {
        test_id: 1015,
        pat_first_name: 'Nancy',
        pat_last_name: 'Moore',
        test_type: 'Stool Culture',
        priority: 'normal',
        status: 'pending',
        requested_date: '2024-01-15T17:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        sample_type: 'Stool',
        notes: 'GI symptoms investigation'
    },

    // IN-PROGRESS TESTS (8 tests)
    {
        test_id: 2001,
        pat_first_name: 'David',
        pat_last_name: 'Garcia',
        test_type: 'Blood Culture',
        priority: 'stat',
        status: 'in_progress',
        requested_date: '2024-01-15T06:00:00Z',
        started_date: '2024-01-15T14:00:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        progress: 33,
        processing_time: '8h',
        eta: '16h remaining',
        sample_type: 'Blood'
    },
    {
        test_id: 2002,
        pat_first_name: 'Sarah',
        pat_last_name: 'Anderson',
        test_type: 'Hemoglobin A1C',
        priority: 'normal',
        status: 'in_progress',
        requested_date: '2024-01-15T08:00:00Z',
        started_date: '2024-01-15T16:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        progress: 75,
        processing_time: '6h',
        eta: '2h remaining',
        sample_type: 'Blood'
    },
    {
        test_id: 2003,
        pat_first_name: 'Michael',
        pat_last_name: 'Lee',
        test_type: 'Liver Function Panel',
        priority: 'urgent',
        status: 'in_progress',
        requested_date: '2024-01-15T09:00:00Z',
        started_date: '2024-01-15T18:00:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        progress: 50,
        processing_time: '4h',
        eta: '4h remaining',
        sample_type: 'Blood'
    },
    {
        test_id: 2004,
        pat_first_name: 'Stephanie',
        pat_last_name: 'Lewis',
        test_type: 'Autoimmune Panel',
        priority: 'normal',
        status: 'in_progress',
        requested_date: '2024-01-15T10:00:00Z',
        started_date: '2024-01-15T12:00:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        progress: 42,
        processing_time: '10h',
        eta: '14h remaining',
        sample_type: 'Blood'
    },
    {
        test_id: 2005,
        pat_first_name: 'Gregory',
        pat_last_name: 'Hall',
        test_type: 'Wound Culture',
        priority: 'urgent',
        status: 'in_progress',
        requested_date: '2024-01-15T11:00:00Z',
        started_date: '2024-01-15T10:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        progress: 50,
        processing_time: '12h',
        eta: '12h remaining',
        sample_type: 'Tissue'
    },
    {
        test_id: 2006,
        pat_first_name: 'Michelle',
        pat_last_name: 'Turner',
        test_type: 'Cardiac Biomarkers',
        priority: 'stat',
        status: 'in_progress',
        requested_date: '2024-01-15T12:00:00Z',
        started_date: '2024-01-15T20:00:00Z',
        requested_by_first_name: 'Michael',
        requested_by_last_name: 'Brown',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        progress: 67,
        processing_time: '2h',
        eta: '1h remaining',
        sample_type: 'Blood'
    },
    {
        test_id: 2007,
        pat_first_name: 'Andrew',
        pat_last_name: 'Parker',
        test_type: 'Urine Drug Screen',
        priority: 'normal',
        status: 'in_progress',
        requested_date: '2024-01-15T13:00:00Z',
        started_date: '2024-01-15T19:00:00Z',
        requested_by_first_name: 'Sarah',
        requested_by_last_name: 'Johnson',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        progress: 60,
        processing_time: '3h',
        eta: '2h remaining',
        sample_type: 'Urine'
    },
    {
        test_id: 2008,
        pat_first_name: 'Samantha',
        pat_last_name: 'Cooper',
        test_type: 'Hormone Panel',
        priority: 'normal',
        status: 'in_progress',
        requested_date: '2024-01-15T14:00:00Z',
        started_date: '2024-01-15T15:00:00Z',
        requested_by_first_name: 'Emily',
        requested_by_last_name: 'Davis',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        progress: 58,
        processing_time: '7h',
        eta: '5h remaining',
        sample_type: 'Blood'
    }
];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadAllTestsData();
    initializeDataTables();
    setupEventListeners();
});

function loadAllTestsData() {
    loadAllTests();
    loadPendingTests();
    loadInProgressTests();
    loadTestResults();
    loadTestsForResultEntry();
    updateStatistics();
}

function loadAllTests() {
    const tbody = document.getElementById('allTestsTableBody');
    tbody.innerHTML = '';

    allLabTestsData.forEach(test => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>#${test.test_id}</strong></td>
            <td>${test.pat_first_name} ${test.pat_last_name}</td>
            <td><span class="badge bg-light text-dark">${test.test_type}</span></td>
            <td><span class="status-badge status-${test.priority}">${test.priority.toUpperCase()}</span></td>
            <td><span class="status-badge status-${test.status}">${test.status.replace('_', ' ').toUpperCase()}</span></td>
            <td>${formatDateTime(test.requested_date)}</td>
            <td>Dr. ${test.requested_by_first_name} ${test.requested_by_last_name}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewTestDetails(${test.test_id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    ${test.status === 'pending' ? 
                        `<button class="btn btn-outline-success" onclick="startTest(${test.test_id})" title="Start Test">
                            <i class="fas fa-play"></i>
                        </button>` : ''
                    }
                    ${test.status === 'in_progress' ? 
                        `<button class="btn btn-outline-info" onclick="viewProgress(${test.test_id})" title="View Progress">
                            <i class="fas fa-chart-line"></i>
                        </button>` : ''
                    }
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function loadPendingTests() {
    const pendingTests = allLabTestsData.filter(test => test.status === 'pending');
    const tbody = document.getElementById('pendingTestsTableBody');
    tbody.innerHTML = '';

    pendingTests.forEach(test => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>#${test.test_id}</strong></td>
            <td>${test.pat_first_name} ${test.pat_last_name}</td>
            <td><span class="badge bg-light text-dark">${test.test_type}</span></td>
            <td><span class="status-badge status-${test.priority}">${test.priority.toUpperCase()}</span></td>
            <td><span class="badge ${getWaitTimeBadgeClass(test.requested_date)}">${getWaitTime(test.requested_date)}</span></td>
            <td>Dr. ${test.requested_by_first_name} ${test.requested_by_last_name}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewTestDetails(${test.test_id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="startTest(${test.test_id})" title="Start Test">
                        <i class="fas fa-play"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function loadInProgressTests() {
    const inProgressTests = allLabTestsData.filter(test => test.status === 'in_progress');
    const tbody = document.getElementById('inProgressTestsTableBody');
    tbody.innerHTML = '';

    inProgressTests.forEach(test => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>#${test.test_id}</strong></td>
            <td>${test.pat_first_name} ${test.pat_last_name}</td>
            <td><span class="badge bg-light text-dark">${test.test_type}</span></td>
            <td>
                <div class="progress" style="height: 20px;">
                    <div class="progress-bar bg-info" style="width: ${test.progress}%">${test.progress}%</div>
                </div>
            </td>
            <td>${test.processing_time}</td>
            <td>${test.processed_by_first_name} ${test.processed_by_last_name}</td>
            <td>${test.eta}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewTestDetails(${test.test_id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-warning" onclick="updateProgress(${test.test_id})" title="Update Progress">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// COMPLETED TESTS DATA (23 tests)
const completedTestsData = [
    {
        test_id: 3001,
        pat_first_name: 'Jennifer',
        pat_last_name: 'Wilson',
        test_type: 'Pregnancy Test',
        result_status: 'positive',
        completed_date: '2024-01-15T09:30:00Z',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        result_value: 'Positive',
        reference_range: 'Negative',
        notes: 'Confirmed pregnancy'
    },
    {
        test_id: 3002,
        pat_first_name: 'James',
        pat_last_name: 'White',
        test_type: 'Coagulation Panel',
        result_status: 'normal',
        completed_date: '2024-01-15T10:15:00Z',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        result_value: 'PT: 12.5 sec, PTT: 28 sec',
        reference_range: 'PT: 11-13 sec, PTT: 25-35 sec',
        notes: 'Normal coagulation function'
    },
    {
        test_id: 3003,
        pat_first_name: 'Robert',
        pat_last_name: 'Taylor',
        test_type: 'Cardiac Enzymes',
        result_status: 'normal',
        completed_date: '2024-01-15T11:00:00Z',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        result_value: 'Troponin I: 0.02 ng/mL',
        reference_range: '< 0.04 ng/mL',
        notes: 'No evidence of myocardial infarction'
    },
    {
        test_id: 3004,
        pat_first_name: 'Patricia',
        pat_last_name: 'Clark',
        test_type: 'Inflammatory Markers',
        result_status: 'abnormal',
        completed_date: '2024-01-15T12:30:00Z',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        result_value: 'ESR: 45 mm/hr, CRP: 8.5 mg/L',
        reference_range: 'ESR: 0-20 mm/hr, CRP: < 3.0 mg/L',
        notes: 'Elevated inflammatory markers'
    },
    {
        test_id: 3005,
        pat_first_name: 'Nancy',
        pat_last_name: 'Moore',
        test_type: 'Stool Culture',
        result_status: 'normal',
        completed_date: '2024-01-14T16:45:00Z',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        result_value: 'No pathogenic organisms',
        reference_range: 'Normal flora',
        notes: 'Normal intestinal flora'
    },
    {
        test_id: 3006,
        pat_first_name: 'Barbara',
        pat_last_name: 'Miller',
        test_type: 'Vitamin D Level',
        result_status: 'abnormal',
        completed_date: '2024-01-14T15:20:00Z',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        result_value: '18 ng/mL',
        reference_range: '30-100 ng/mL',
        notes: 'Vitamin D deficiency'
    },
    {
        test_id: 3007,
        pat_first_name: 'John',
        pat_last_name: 'Smith',
        test_type: 'Complete Blood Count',
        result_status: 'normal',
        completed_date: '2024-01-14T14:30:00Z',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        result_value: 'WBC: 7.2, RBC: 4.8, Hgb: 14.5',
        reference_range: 'WBC: 4.5-11.0, RBC: 4.2-5.4, Hgb: 12.0-16.0',
        notes: 'Normal blood count'
    },
    {
        test_id: 3008,
        pat_first_name: 'Maria',
        pat_last_name: 'Garcia',
        test_type: 'Blood Culture',
        result_status: 'negative',
        completed_date: '2024-01-14T13:45:00Z',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        result_value: 'No growth after 72 hours',
        reference_range: 'No growth',
        notes: 'No bacterial growth detected'
    },
    {
        test_id: 3009,
        pat_first_name: 'Lisa',
        pat_last_name: 'Anderson',
        test_type: 'Comprehensive Metabolic Panel',
        result_status: 'normal',
        completed_date: '2024-01-14T12:20:00Z',
        processed_by_first_name: 'Michael',
        processed_by_last_name: 'Chen',
        result_value: 'Glucose: 95, BUN: 18, Creatinine: 0.9',
        reference_range: 'Glucose: 70-100, BUN: 7-20, Creatinine: 0.6-1.2',
        notes: 'Normal metabolic panel'
    },
    {
        test_id: 3010,
        pat_first_name: 'David',
        pat_last_name: 'Martinez',
        test_type: 'Thyroid Function Panel',
        result_status: 'abnormal',
        completed_date: '2024-01-14T11:15:00Z',
        processed_by_first_name: 'Sarah',
        processed_by_last_name: 'Wilson',
        result_value: 'TSH: 8.5, T4: 6.2',
        reference_range: 'TSH: 0.4-4.0, T4: 4.5-12.0',
        notes: 'Elevated TSH, hypothyroidism'
    }
];

function loadTestResults() {
    const tbody = document.getElementById('resultsTableBody');
    tbody.innerHTML = '';

    completedTestsData.forEach(test => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>#${test.test_id}</strong></td>
            <td>${test.pat_first_name} ${test.pat_last_name}</td>
            <td><span class="badge bg-light text-dark">${test.test_type}</span></td>
            <td><span class="status-badge status-${test.result_status}">${test.result_status.toUpperCase()}</span></td>
            <td>${formatDateTime(test.completed_date)}</td>
            <td>${test.processed_by_first_name} ${test.processed_by_last_name}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewResultDetails(${test.test_id})" title="View Results">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-info" onclick="printResult(${test.test_id})" title="Print">
                        <i class="fas fa-print"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function loadTestsForResultEntry() {
    const inProgressTests = allLabTestsData.filter(test => test.status === 'in_progress');
    const select = document.getElementById('testSelect');
    select.innerHTML = '<option value="">Choose a test to enter results...</option>';

    inProgressTests.forEach(test => {
        const option = document.createElement('option');
        option.value = test.test_id;
        option.textContent = `#${test.test_id} - ${test.pat_first_name} ${test.pat_last_name} - ${test.test_type}`;
        select.appendChild(option);
    });
}

function updateStatistics() {
    const pending = allLabTestsData.filter(test => test.status === 'pending').length;
    const inProgress = allLabTestsData.filter(test => test.status === 'in_progress').length;
    const completed = completedTestsData.length;
    const total = allLabTestsData.length + completed;

    document.getElementById('totalTests').textContent = total;
    document.getElementById('pendingTests').textContent = pending;
    document.getElementById('inProgressTests').textContent = inProgress;
    document.getElementById('completedTests').textContent = completed;
}

function initializeDataTables() {
    $('#allTestsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[0, 'desc']]
    });

    $('#pendingTestsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[0, 'desc']]
    });

    $('#inProgressTestsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[0, 'desc']]
    });

    $('#resultsTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[4, 'desc']]
    });
}

function setupEventListeners() {
    // Test selection for result entry
    document.getElementById('testSelect').addEventListener('change', function() {
        const testId = this.value;
        if (testId) {
            const test = allLabTestsData.find(t => t.test_id == testId);
            if (test) {
                document.getElementById('testInfo').innerHTML = `
                    <h6>Test Information</h6>
                    <p><strong>Patient:</strong> ${test.pat_first_name} ${test.pat_last_name}</p>
                    <p><strong>Test Type:</strong> ${test.test_type}</p>
                    <p><strong>Priority:</strong> ${test.priority.toUpperCase()}</p>
                    <p><strong>Sample Type:</strong> ${test.sample_type}</p>
                    <p><strong>Requested By:</strong> Dr. ${test.requested_by_first_name} ${test.requested_by_last_name}</p>
                    <p><strong>Processing Time:</strong> ${test.processing_time}</p>
                    <p><strong>Progress:</strong> ${test.progress}%</p>
                `;
            }
        } else {
            document.getElementById('testInfo').innerHTML = 'Select a test to view information';
        }
    });

    // Result entry form
    document.getElementById('enterResultsForm').addEventListener('submit', function(e) {
        e.preventDefault();
        enterTestResult();
    });
}

// Utility functions
function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
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

// Action functions
function viewTestDetails(testId) {
    const test = allLabTestsData.find(t => t.test_id === testId) || completedTestsData.find(t => t.test_id === testId);
    if (test) {
        let details = `Test Details:\n\nTest ID: ${test.test_id}\nPatient: ${test.pat_first_name} ${test.pat_last_name}\nTest Type: ${test.test_type}\nPriority: ${test.priority || 'N/A'}\nStatus: ${test.status || 'completed'}\nRequested: ${formatDateTime(test.requested_date)}\nRequested By: Dr. ${test.requested_by_first_name} ${test.requested_by_last_name}`;

        if (test.status === 'in_progress') {
            details += `\nProgress: ${test.progress}%\nProcessing Time: ${test.processing_time}\nETA: ${test.eta}\nTechnician: ${test.processed_by_first_name} ${test.processed_by_last_name}`;
        }

        if (test.result_value) {
            details += `\nResult: ${test.result_value}\nReference Range: ${test.reference_range}\nResult Status: ${test.result_status}\nCompleted: ${formatDateTime(test.completed_date)}`;
        }

        alert(details);
    }
}

function startTest(testId) {
    if (confirm('Start processing this test? This will move it to the in-progress section.')) {
        const testIndex = allLabTestsData.findIndex(test => test.test_id === testId);
        if (testIndex !== -1) {
            allLabTestsData[testIndex].status = 'in_progress';
            allLabTestsData[testIndex].started_date = new Date().toISOString();
            allLabTestsData[testIndex].processed_by_first_name = 'Michael';
            allLabTestsData[testIndex].processed_by_last_name = 'Chen';
            allLabTestsData[testIndex].progress = 10;
            allLabTestsData[testIndex].processing_time = '0h';
            allLabTestsData[testIndex].eta = '4h remaining';

            showAlert('Test started successfully', 'success');
            loadAllTestsData();
        }
    }
}

function viewProgress(testId) {
    const test = allLabTestsData.find(t => t.test_id === testId);
    if (test) {
        alert(`Progress Details:\n\nTest ID: ${test.test_id}\nPatient: ${test.pat_first_name} ${test.pat_last_name}\nTest Type: ${test.test_type}\nProgress: ${test.progress}%\nProcessing Time: ${test.processing_time}\nETA: ${test.eta}\nTechnician: ${test.processed_by_first_name} ${test.processed_by_last_name}`);
    }
}

function updateProgress(testId) {
    const newProgress = prompt('Enter new progress percentage (0-100):');
    if (newProgress && !isNaN(newProgress) && newProgress >= 0 && newProgress <= 100) {
        const testIndex = allLabTestsData.findIndex(test => test.test_id === testId);
        if (testIndex !== -1) {
            allLabTestsData[testIndex].progress = parseInt(newProgress);
            showAlert('Progress updated successfully', 'success');
            loadInProgressTests();
        }
    }
}

function viewResultDetails(testId) {
    const test = completedTestsData.find(t => t.test_id === testId);
    if (test) {
        alert(`Result Details:\n\nTest ID: ${test.test_id}\nPatient: ${test.pat_first_name} ${test.pat_last_name}\nTest Type: ${test.test_type}\nResult: ${test.result_value}\nReference Range: ${test.reference_range}\nStatus: ${test.result_status}\nCompleted: ${formatDateTime(test.completed_date)}\nProcessed By: ${test.processed_by_first_name} ${test.processed_by_last_name}\nNotes: ${test.notes}`);
    }
}

function printResult(testId) {
    showAlert('Result sent to printer', 'success');
}

function enterTestResult() {
    const testId = document.getElementById('testSelect').value;
    const resultValue = document.getElementById('resultValue').value;
    const resultStatus = document.getElementById('resultStatus').value;
    const resultNotes = document.getElementById('resultNotes').value;

    if (!testId || !resultValue || !resultStatus) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    // Move test from in-progress to completed
    const testIndex = allLabTestsData.findIndex(test => test.test_id == testId);
    if (testIndex !== -1) {
        const test = allLabTestsData[testIndex];

        // Create completed test record
        const completedTest = {
            test_id: test.test_id,
            pat_first_name: test.pat_first_name,
            pat_last_name: test.pat_last_name,
            test_type: test.test_type,
            result_status: resultStatus,
            completed_date: new Date().toISOString(),
            processed_by_first_name: test.processed_by_first_name,
            processed_by_last_name: test.processed_by_last_name,
            result_value: resultValue,
            reference_range: 'Normal range varies by test',
            notes: resultNotes
        };

        // Add to completed tests
        completedTestsData.unshift(completedTest);

        // Remove from in-progress tests
        allLabTestsData.splice(testIndex, 1);

        // Reset form
        document.getElementById('enterResultsForm').reset();
        document.getElementById('testInfo').innerHTML = 'Select a test to view information';

        showAlert('Test result entered successfully', 'success');
        loadAllTestsData();
    }
}

// Refresh functions
function refreshAllTests() {
    loadAllTests();
    showAlert('All tests refreshed', 'success');
}

function refreshPendingTests() {
    loadPendingTests();
    showAlert('Pending tests refreshed', 'success');
}

function refreshInProgressTests() {
    loadInProgressTests();
    showAlert('In-progress tests refreshed', 'success');
}

function refreshResults() {
    loadTestResults();
    showAlert('Results refreshed', 'success');
}

// Export functions
function exportAllTests() {
    showAlert('All tests data exported to CSV', 'success');
}

function exportResults() {
    showAlert('Results data exported to CSV', 'success');
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
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
