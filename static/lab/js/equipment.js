// Equipment Management JavaScript

// Sample equipment data
const equipmentData = [
    {
        id: 'EQ001',
        name: 'Hematology Analyzer HA-2000',
        type: 'Hematology',
        status: 'operational',
        lastMaintenance: '2024-01-10',
        nextService: '2024-02-10',
        location: 'Lab Room A',
        manufacturer: 'MedTech Inc.',
        model: 'HA-2000',
        serialNumber: 'HT2000-001'
    },
    {
        id: 'EQ002',
        name: 'Chemistry Analyzer CA-500',
        type: 'Chemistry',
        status: 'operational',
        lastMaintenance: '2024-01-12',
        nextService: '2024-02-12',
        location: 'Lab Room B',
        manufacturer: 'BioSystems',
        model: 'CA-500',
        serialNumber: 'BS500-002'
    },
    {
        id: 'EQ003',
        name: 'Microbiology Incubator MI-300',
        type: 'Microbiology',
        status: 'maintenance',
        lastMaintenance: '2024-01-08',
        nextService: '2024-01-15',
        location: 'Lab Room C',
        manufacturer: 'LabEquip Co.',
        model: 'MI-300',
        serialNumber: 'LE300-003'
    },
    {
        id: 'EQ004',
        name: 'PCR Machine PCR-100',
        type: 'Molecular',
        status: 'calibration',
        lastMaintenance: '2024-01-14',
        nextService: '2024-02-14',
        location: 'Lab Room D',
        manufacturer: 'GeneTech',
        model: 'PCR-100',
        serialNumber: 'GT100-004'
    },
    {
        id: 'EQ005',
        name: 'Centrifuge CF-400',
        type: 'General',
        status: 'operational',
        lastMaintenance: '2024-01-11',
        nextService: '2024-02-11',
        location: 'Lab Room A',
        manufacturer: 'SpinTech',
        model: 'CF-400',
        serialNumber: 'ST400-005'
    },
    {
        id: 'EQ006',
        name: 'Microscope MS-200',
        type: 'Microscopy',
        status: 'operational',
        lastMaintenance: '2024-01-09',
        nextService: '2024-02-09',
        location: 'Lab Room B',
        manufacturer: 'OptiView',
        model: 'MS-200',
        serialNumber: 'OV200-006'
    },
    {
        id: 'EQ007',
        name: 'Spectrophotometer SP-150',
        type: 'Chemistry',
        status: 'operational',
        lastMaintenance: '2024-01-13',
        nextService: '2024-02-13',
        location: 'Lab Room C',
        manufacturer: 'SpectraLab',
        model: 'SP-150',
        serialNumber: 'SL150-007'
    },
    {
        id: 'EQ008',
        name: 'Autoclave AC-300',
        type: 'Sterilization',
        status: 'operational',
        lastMaintenance: '2024-01-07',
        nextService: '2024-02-07',
        location: 'Sterilization Room',
        manufacturer: 'SterilTech',
        model: 'AC-300',
        serialNumber: 'ST300-008'
    },
    {
        id: 'EQ009',
        name: 'Blood Gas Analyzer BG-100',
        type: 'Blood Gas',
        status: 'operational',
        lastMaintenance: '2024-01-15',
        nextService: '2024-02-15',
        location: 'Emergency Lab',
        manufacturer: 'GasLab',
        model: 'BG-100',
        serialNumber: 'GL100-009'
    },
    {
        id: 'EQ010',
        name: 'Coagulation Analyzer CG-200',
        type: 'Coagulation',
        status: 'operational',
        lastMaintenance: '2024-01-06',
        nextService: '2024-02-06',
        location: 'Lab Room A',
        manufacturer: 'CoagTech',
        model: 'CG-200',
        serialNumber: 'CT200-010'
    },
    {
        id: 'EQ011',
        name: 'Immunoassay Analyzer IA-400',
        type: 'Immunology',
        status: 'operational',
        lastMaintenance: '2024-01-05',
        nextService: '2024-02-05',
        location: 'Lab Room D',
        manufacturer: 'ImmunoLab',
        model: 'IA-400',
        serialNumber: 'IL400-011'
    },
    {
        id: 'EQ012',
        name: 'Refrigerator RF-500',
        type: 'Storage',
        status: 'operational',
        lastMaintenance: '2024-01-04',
        nextService: '2024-02-04',
        location: 'Storage Room',
        manufacturer: 'ColdTech',
        model: 'RF-500',
        serialNumber: 'CT500-012'
    },
    {
        id: 'EQ013',
        name: 'Freezer FZ-200',
        type: 'Storage',
        status: 'operational',
        lastMaintenance: '2024-01-03',
        nextService: '2024-02-03',
        location: 'Storage Room',
        manufacturer: 'ColdTech',
        model: 'FZ-200',
        serialNumber: 'CT200-013'
    },
    {
        id: 'EQ014',
        name: 'Water Purification System WP-100',
        type: 'Utilities',
        status: 'operational',
        lastMaintenance: '2024-01-02',
        nextService: '2024-02-02',
        location: 'Utility Room',
        manufacturer: 'PureWater',
        model: 'WP-100',
        serialNumber: 'PW100-014'
    },
    {
        id: 'EQ015',
        name: 'Fume Hood FH-300',
        type: 'Safety',
        status: 'offline',
        lastMaintenance: '2024-01-01',
        nextService: '2024-01-16',
        location: 'Lab Room C',
        manufacturer: 'SafetyFirst',
        model: 'FH-300',
        serialNumber: 'SF300-015'
    }
];

// Sample maintenance schedule data
const maintenanceData = [
    {
        equipment: 'Hematology Analyzer HA-2000',
        maintenanceType: 'Preventive Maintenance',
        scheduledDate: '2024-02-10',
        technician: 'Michael Chen',
        priority: 'Medium',
        status: 'Scheduled'
    },
    {
        equipment: 'Chemistry Analyzer CA-500',
        maintenanceType: 'Calibration',
        scheduledDate: '2024-01-20',
        technician: 'Sarah Wilson',
        priority: 'High',
        status: 'Scheduled'
    },
    {
        equipment: 'Microbiology Incubator MI-300',
        maintenanceType: 'Repair',
        scheduledDate: '2024-01-16',
        technician: 'David Rodriguez',
        priority: 'High',
        status: 'In Progress'
    },
    {
        equipment: 'PCR Machine PCR-100',
        maintenanceType: 'Calibration',
        scheduledDate: '2024-01-18',
        technician: 'Michael Chen',
        priority: 'Medium',
        status: 'Scheduled'
    },
    {
        equipment: 'Fume Hood FH-300',
        maintenanceType: 'Emergency Repair',
        scheduledDate: '2024-01-16',
        technician: 'David Rodriguez',
        priority: 'Critical',
        status: 'Scheduled'
    }
];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadEquipment();
    loadMaintenanceSchedule();
    updateStatistics();
    initializeDataTables();
});

// Load equipment data
function loadEquipment() {
    const tbody = document.getElementById('equipmentTableBody');
    tbody.innerHTML = '';

    equipmentData.forEach(equipment => {
        const row = document.createElement('tr');
        const daysTillService = getDaysUntilService(equipment.nextService);
        
        row.innerHTML = `
            <td><strong>${equipment.id}</strong></td>
            <td>${equipment.name}</td>
            <td>${equipment.type}</td>
            <td><span class="status-badge status-${equipment.status}">${equipment.status.toUpperCase()}</span></td>
            <td>${formatDate(equipment.lastMaintenance)}</td>
            <td>${formatDate(equipment.nextService)} ${daysTillService <= 7 ? '<span class="badge bg-warning">Due Soon</span>' : ''}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewEquipmentDetails('${equipment.id}')" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="scheduleMaintenance('${equipment.id}')" title="Schedule Maintenance">
                        <i class="fas fa-calendar-plus"></i>
                    </button>
                    <button class="btn btn-outline-info" onclick="viewMaintenanceHistory('${equipment.id}')" title="History">
                        <i class="fas fa-history"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Load maintenance schedule
function loadMaintenanceSchedule() {
    const tbody = document.getElementById('maintenanceTableBody');
    tbody.innerHTML = '';

    maintenanceData.forEach(maintenance => {
        const row = document.createElement('tr');
        const priorityClass = maintenance.priority.toLowerCase();
        
        row.innerHTML = `
            <td>${maintenance.equipment}</td>
            <td>${maintenance.maintenanceType}</td>
            <td>${formatDate(maintenance.scheduledDate)}</td>
            <td>${maintenance.technician}</td>
            <td><span class="badge bg-${getPriorityColor(maintenance.priority)}">${maintenance.priority}</span></td>
            <td><span class="status-badge status-${maintenance.status.toLowerCase().replace(' ', '-')}">${maintenance.status}</span></td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewMaintenanceDetails('${maintenance.equipment}')" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="completeMaintenance('${maintenance.equipment}')" title="Complete">
                        <i class="fas fa-check"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Update statistics
function updateStatistics() {
    const operational = equipmentData.filter(eq => eq.status === 'operational').length;
    const maintenance = equipmentData.filter(eq => eq.status === 'maintenance').length;
    const offline = equipmentData.filter(eq => eq.status === 'offline').length;
    
    document.getElementById('totalEquipment').textContent = equipmentData.length;
    document.getElementById('operationalEquipment').textContent = operational;
    document.getElementById('maintenanceEquipment').textContent = maintenance;
    document.getElementById('offlineEquipment').textContent = offline;
}

// Initialize DataTables
function initializeDataTables() {
    $('#equipmentTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[0, 'asc']], // Sort by equipment ID
        columnDefs: [
            { orderable: false, targets: [6] } // Disable sorting for actions column
        ]
    });

    $('#maintenanceTable').DataTable({
        responsive: true,
        pageLength: 10,
        order: [[2, 'asc']], // Sort by scheduled date
        columnDefs: [
            { orderable: false, targets: [6] } // Disable sorting for actions column
        ]
    });
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function getDaysUntilService(serviceDateString) {
    const serviceDate = new Date(serviceDateString);
    const today = new Date();
    const diffTime = serviceDate - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

function getPriorityColor(priority) {
    switch(priority.toLowerCase()) {
        case 'critical': return 'danger';
        case 'high': return 'warning';
        case 'medium': return 'info';
        case 'low': return 'secondary';
        default: return 'secondary';
    }
}

// Action functions
function addEquipment() {
    showAlert('Add Equipment form will be displayed.', 'info');
}

function refreshEquipment() {
    loadEquipment();
    updateStatistics();
    showAlert('Equipment data refreshed.', 'success');
}

function viewEquipmentDetails(equipmentId) {
    const equipment = equipmentData.find(eq => eq.id === equipmentId);
    if (equipment) {
        alert(`Equipment Details:\n\nID: ${equipment.id}\nName: ${equipment.name}\nType: ${equipment.type}\nStatus: ${equipment.status}\nLocation: ${equipment.location}\nManufacturer: ${equipment.manufacturer}\nModel: ${equipment.model}\nSerial Number: ${equipment.serialNumber}\nLast Maintenance: ${equipment.lastMaintenance}\nNext Service: ${equipment.nextService}`);
    }
}

function scheduleMaintenance(equipmentId) {
    showAlert('Maintenance scheduling form will be displayed.', 'info');
}

function viewMaintenanceHistory(equipmentId) {
    showAlert(`Maintenance history for ${equipmentId} displayed.`, 'info');
}

function viewMaintenanceDetails(equipment) {
    const maintenance = maintenanceData.find(m => m.equipment === equipment);
    if (maintenance) {
        alert(`Maintenance Details:\n\nEquipment: ${maintenance.equipment}\nType: ${maintenance.maintenanceType}\nScheduled: ${maintenance.scheduledDate}\nTechnician: ${maintenance.technician}\nPriority: ${maintenance.priority}\nStatus: ${maintenance.status}`);
    }
}

function completeMaintenance(equipment) {
    showAlert(`Maintenance completion form for ${equipment} will be displayed.`, 'success');
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
