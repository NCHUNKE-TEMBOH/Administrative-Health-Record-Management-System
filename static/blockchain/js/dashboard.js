// Blockchain Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    // Initialize dashboard
    loadBlockchainData();
    
    // Auto-refresh every 30 seconds
    setInterval(loadBlockchainData, 30000);
});

function loadBlockchainData() {
    console.log('Loading blockchain data...');

    fetch('/api/blockchain/chain')
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Blockchain data received:', data);
            if (data.chain && Array.isArray(data.chain)) {
                window.medicalBlockchain = { chain: data.chain };
                updateStatistics();
                loadBlocks();
                loadAuditTrail();
                showAlert('Blockchain data loaded successfully!', 'success');
            } else {
                throw new Error('Invalid blockchain data format');
            }
        })
        .catch(error => {
            console.error('Blockchain loading error:', error);
            showAlert(`Failed to load blockchain data: ${error.message}`, 'danger');

            // Initialize with empty blockchain if server fails
            window.medicalBlockchain = { chain: [] };
            updateStatistics();
            loadBlocks();
            loadAuditTrail();
        });
}

function updateStatistics() {
    const blockchain = window.medicalBlockchain;
    const stats = {
        totalBlocks: blockchain.chain.length,
        medicalRecords: blockchain.chain.filter(b => b.data.type === 'medical_record').length,
        vitalSigns: blockchain.chain.filter(b => b.data.type === 'vital_signs').length,
        prescriptions: blockchain.chain.filter(b => b.data.type === 'prescription').length,
        labResults: blockchain.chain.filter(b => b.data.type === 'lab_result').length,
        isValid: blockchain.isValid !== undefined ? blockchain.isValid : true,
        lastBlockHash: blockchain.chain.length > 0 ? blockchain.chain[blockchain.chain.length-1].hash : ''
    };
    document.getElementById('totalBlocks').textContent = stats.totalBlocks;
    document.getElementById('medicalRecords').textContent = stats.medicalRecords;
    document.getElementById('vitalSigns').textContent = stats.vitalSigns;
    document.getElementById('prescriptions').textContent = stats.prescriptions;
    document.getElementById('labResults').textContent = stats.labResults;
    const validityElement = document.getElementById('chainValidity');
    const validityIcon = document.getElementById('validityIcon');
    if (stats.isValid) {
        validityElement.textContent = 'Valid';
        validityElement.className = 'text-success';
        validityIcon.className = 'fas fa-check-circle fa-2x mb-2 text-success';
    } else {
        validityElement.textContent = 'Invalid';
        validityElement.className = 'text-danger';
        validityIcon.className = 'fas fa-exclamation-triangle fa-2x mb-2 text-danger';
    }
}

function loadBlocks() {
    const blockchain = window.medicalBlockchain;
    const container = document.getElementById('blocksContainer');
    container.innerHTML = '';
    if (!blockchain || !blockchain.chain) return;
    blockchain.chain.forEach((block, index) => {
        const blockCard = createBlockCard(block, index);
        container.appendChild(blockCard);
    });
}

function createBlockCard(block, index) {
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-4 mb-3';
    
    const typeIcon = getTypeIcon(block.data.type);
    const typeColor = getTypeColor(block.data.type);
    
    col.innerHTML = `
        <div class="block-card p-3" style="background: ${typeColor}">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h5><i class="${typeIcon}"></i> Block #${block.index}</h5>
                <small>${formatDateTime(block.timestamp)}</small>
            </div>
            <div class="mb-2">
                <strong>Type:</strong> ${block.data.type || 'Unknown'}
            </div>
            ${block.data.patientId || block.data.pat_id ? 
                `<div class="mb-2"><strong>Patient ID:</strong> ${block.data.patientId || block.data.pat_id}</div>` : ''
            }
            <div class="mb-2">
                <strong>Hash:</strong>
                <div class="hash-display">${block.hash}</div>
            </div>
            <div class="mb-2">
                <strong>Previous Hash:</strong>
                <div class="hash-display">${block.previousHash}</div>
            </div>
            <div class="text-center">
                <button class="btn btn-light btn-sm" onclick="viewBlockDetails(${block.index})">
                    <i class="fas fa-eye"></i> View Details
                </button>
            </div>
        </div>
    `;
    
    return col;
}

function getTypeIcon(type) {
    const icons = {
        'genesis': 'fas fa-star',
        'medical_record': 'fas fa-file-medical',
        'vital_signs': 'fas fa-heartbeat',
        'prescription': 'fas fa-pills',
        'lab_result': 'fas fa-flask'
    };
    return icons[type] || 'fas fa-cube';
}

function getTypeColor(type) {
    const colors = {
        'genesis': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'medical_record': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'vital_signs': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'prescription': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'lab_result': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    };
    return colors[type] || 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)';
}

function loadAuditTrail() {
    const blockchain = window.medicalBlockchain;
    const tbody = document.getElementById('auditTableBody');
    tbody.innerHTML = '';
    if (!blockchain || !blockchain.chain) return;
    blockchain.chain.forEach((block, idx) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>#${block.index}</strong></td>
            <td>${formatDateTime(block.timestamp)}</td>
            <td><span class="badge bg-primary">${block.data.type}</span></td>
            <td><code class="small">${block.hash.substring(0, 16)}...</code></td>
            <td><code class="small">${block.previousHash.substring(0, 16)}...</code></td>
            <td><code class="small">${block.dataHash ? block.dataHash.substring(0, 16) : ''}...</code></td>
        `;
        tbody.appendChild(row);
    });
}

function loadPatientRecords() {
    const patientId = document.getElementById('patientSelect').value;
    const container = document.getElementById('patientRecordsContainer');
    
    if (!patientId) {
        container.innerHTML = '<p class="text-muted">Select a patient to view their blockchain records</p>';
        return;
    }

    const records = window.BlockchainUtils.getPatientRecords(patientId);
    
    if (records.length === 0) {
        container.innerHTML = '<p class="text-warning">No blockchain records found for this patient</p>';
        return;
    }

    container.innerHTML = '';
    records.forEach(block => {
        const recordCard = createPatientRecordCard(block);
        container.appendChild(recordCard);
    });
}

function createPatientRecordCard(block) {
    const card = document.createElement('div');
    card.className = 'card mb-3';
    
    const typeIcon = getTypeIcon(block.data.type);
    
    card.innerHTML = `
        <div class="card-header">
            <h6><i class="${typeIcon}"></i> ${block.data.type.replace('_', ' ').toUpperCase()} - Block #${block.index}</h6>
            <small class="text-muted">${formatDateTime(block.timestamp)}</small>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <strong>Block Hash:</strong><br>
                    <code class="small">${block.hash}</code>
                </div>
                <div class="col-md-6">
                    <strong>Data Summary:</strong><br>
                    ${getDataSummary(block.data)}
                </div>
            </div>
        </div>
    `;
    
    return card;
}

function getDataSummary(data) {
    let summary = '';
    if (data.type === 'vital_signs') {
        summary = `BP: ${data.blood_pressure_systolic || 'N/A'}/${data.blood_pressure_diastolic || 'N/A'}, HR: ${data.heart_rate || 'N/A'}, Temp: ${data.temperature || 'N/A'}°F`;
    } else if (data.type === 'prescription') {
        summary = `Medication: ${data.medication_name || 'N/A'}, Dosage: ${data.dosage || 'N/A'}`;
    } else if (data.type === 'lab_result') {
        summary = `Test: ${data.test_type || 'N/A'}, Result: ${data.result_value || 'N/A'}`;
    } else if (data.type === 'medical_record') {
        summary = `Diagnosis: ${data.diagnosis || 'N/A'}, Treatment: ${data.treatment || 'N/A'}`;
    } else {
        summary = 'Genesis block - System initialization';
    }
    return summary;
}

// Demo functions
function addSampleMedicalRecord() {
    const record = {
        type: 'medical_record',
        patientId: 1001,
        diagnosis: 'Hypertension Stage 1',
        treatment: 'Lifestyle modifications and ACE inhibitor',
        doctor: 'Dr. Sarah Johnson',
        notes: 'Patient responding well to treatment'
    };
    fetch('/api/blockchain/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(record)
    })
    .then(response => response.json())
    .then(() => {
        showAlert('Medical record added to blockchain!', 'success');
        loadBlockchainData();
    })
    .catch(() => showAlert('Failed to add medical record.', 'danger'));
}

function addSampleVitalSigns() {
    const vitals = {
        type: 'vital_signs',
        patientId: 1001,
        blood_pressure_systolic: 135,
        blood_pressure_diastolic: 85,
        heart_rate: 72,
        temperature: 98.6,
        nurse: 'Emily Davis'
    };
    fetch('/api/blockchain/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(vitals)
    })
    .then(response => response.json())
    .then(() => {
        showAlert('Vital signs added to blockchain!', 'success');
        loadBlockchainData();
    })
    .catch(() => showAlert('Failed to add vital signs.', 'danger'));
}

function addSamplePrescription() {
    const prescription = {
        type: 'prescription',
        patientId: 1001,
        medication_name: 'Lisinopril',
        dosage: '10mg',
        frequency: 'Once daily',
        doctor: 'Dr. Sarah Johnson',
        pharmacist: 'David Wilson'
    };
    fetch('/api/blockchain/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prescription)
    })
    .then(response => response.json())
    .then(() => {
        showAlert('Prescription added to blockchain!', 'success');
        loadBlockchainData();
    })
    .catch(() => showAlert('Failed to add prescription.', 'danger'));
}

function addSampleLabResult() {
    const labResult = {
        type: 'lab_result',
        patientId: 1001,
        test_type: 'Complete Blood Count',
        result_value: 'WBC: 7.2, RBC: 4.8, Hgb: 14.5',
        status: 'Normal',
        technician: 'Michael Chen'
    };
    fetch('/api/blockchain/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(labResult)
    })
    .then(response => response.json())
    .then(() => {
        showAlert('Lab result added to blockchain!', 'success');
        loadBlockchainData();
    })
    .catch(() => showAlert('Failed to add lab result.', 'danger'));
}

// Utility functions
function refreshBlockchain() {
    loadBlockchainData();
    showAlert('Blockchain data refreshed!', 'info');
}

function validateBlockchain() {
    fetch('/api/blockchain/validate')
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                showAlert('Blockchain is valid and secure!', 'success');
            } else {
                showAlert('Blockchain validation failed! Data may be compromised.', 'danger');
            }
            loadBlockchainData();
        })
        .catch(() => showAlert('Failed to validate blockchain.', 'danger'));
}

function exportBlockchain() {
    const data = window.BlockchainUtils.exportData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `medical_blockchain_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showAlert('Blockchain data exported!', 'success');
}

function clearBlockchain() {
    if (confirm('Are you sure you want to clear the entire blockchain? This action cannot be undone.')) {
        localStorage.removeItem('medicalBlockchain');
        window.medicalBlockchain = new MedicalBlockchain();
        loadBlockchainData();
        showAlert('Blockchain cleared and reset to genesis block!', 'warning');
    }
}

function resetToGenesis() {
    clearBlockchain();
}

function showBlockchainInfo() {
    const stats = window.BlockchainUtils.getStats();
    const info = `
Blockchain Information:
- Total Blocks: ${stats.totalBlocks}
- Medical Records: ${stats.medicalRecords}
- Vital Signs: ${stats.vitalSigns}
- Prescriptions: ${stats.prescriptions}
- Lab Results: ${stats.labResults}
- Chain Valid: ${stats.isValid}
- Last Block Hash: ${stats.lastBlockHash}
    `;
    alert(info);
}

function viewBlockDetails(blockIndex) {
    const block = window.medicalBlockchain.chain[blockIndex];
    if (!block) return;
    
    const details = `
Block Details:

Index: ${block.index}
Timestamp: ${formatDateTime(block.timestamp)}
Type: ${block.data.type}
Hash: ${block.hash}
Previous Hash: ${block.previousHash}
Nonce: ${block.nonce}

Data:
${JSON.stringify(block.data, null, 2)}
    `;
    alert(details);
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
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
