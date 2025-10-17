// Global variables
let currentData = null;
let currentRecordId = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadHistory();
});

function setupEventListeners() {
    const fileInput = document.getElementById('fileInput');
    const uploadBox = document.getElementById('uploadBox');
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);
    
    // Click to upload
    uploadBox.addEventListener('click', (e) => {
        if (e.target === uploadBox || e.target.closest('.upload-box')) {
            fileInput.click();
        }
    });
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        displayFileInfo(file);
        uploadFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadBox').classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadBox').classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadBox').classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        displayFileInfo(file);
        uploadFile(file);
    }
}

function displayFileInfo(file) {
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileInfo').style.display = 'flex';
}

function clearFile() {
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Get selected company
    const company = document.getElementById('companySelect').value;
    formData.append('company', company);
    
    // Show processing
    document.getElementById('processingSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        // Hide processing
        document.getElementById('processingSection').style.display = 'none';
        
        if (result.success) {
            currentData = result.data;
            currentRecordId = result.record_id;
            displayResults(result);
            loadHistory();
        } else {
            showError(result.error || 'Upload failed');
        }
        
    } catch (error) {
        document.getElementById('processingSection').style.display = 'none';
        showError('Error uploading file: ' + error.message);
    }
}

function displayResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    
    // Company badge
    const companyBadge = document.getElementById('companyBadge');
    companyBadge.textContent = result.company.replace('_', ' ').toUpperCase();
    
    // Data grid
    const dataGrid = document.getElementById('dataGrid');
    dataGrid.innerHTML = '';
    
    const fields = [
        { key: 'insurance_company', label: 'Insurance Company' },
        { key: 'policy_number', label: 'Policy Number' },
        { key: 'date_prepared', label: 'Date Prepared' },
        { key: 'insurer_name', label: 'Insurer Name' },
        { key: 'insurer_address', label: 'Insurer Address' },
        { key: 'insurer_city_state', label: 'City, State' },
        { key: 'insurance_amount', label: 'Insurance Amount' },
    ];
    
    fields.forEach(field => {
        const value = result.data[field.key] || 'N/A';
        const item = document.createElement('div');
        item.className = 'data-item';
        item.innerHTML = `
            <div class="data-label">${field.label}</div>
            <div class="data-value">${value}</div>
        `;
        dataGrid.appendChild(item);
    });
    
    // Validation messages
    const validationMessages = document.getElementById('validationMessages');
    validationMessages.innerHTML = '';
    
    if (result.is_valid) {
        validationMessages.innerHTML = `
            <div class="validation-success">
                ✓ Data extracted successfully
            </div>
        `;
    } else {
        result.validation_errors.forEach(error => {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'validation-error';
            errorDiv.textContent = '⚠ ' + error;
            validationMessages.appendChild(errorDiv);
        });
    }
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

async function exportData(format) {
    if (!currentData) {
        showError('No data to export');
        return;
    }
    
    try {
        const response = await fetch(`/api/export/${format}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: currentData })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `renters_data.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            showError('Export failed');
        }
        
    } catch (error) {
        showError('Error exporting data: ' + error.message);
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/records?limit=10');
        const result = await response.json();
        
        if (result.success) {
            displayHistory(result.records);
        }
        
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function displayHistory(records) {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';
    
    if (records.length === 0) {
        historyList.innerHTML = '<p style="text-align: center; color: #64748b;">No records yet</p>';
        return;
    }
    
    records.forEach(record => {
        const item = document.createElement('div');
        item.className = 'history-item';
        
        const date = new Date(record.upload_date).toLocaleString();
        
        item.innerHTML = `
            <div class="history-info">
                <div class="history-company">${record.insurance_company || 'Unknown'}</div>
                <div class="history-details">
                    Policy: ${record.policy_number || 'N/A'} | 
                    ${date}
                </div>
            </div>
            <div class="history-actions">
                <button class="view-btn" onclick="viewRecord(${record.id})">View</button>
                <button class="delete-btn" onclick="deleteRecord(${record.id})">Delete</button>
            </div>
        `;
        
        historyList.appendChild(item);
    });
}

async function viewRecord(recordId) {
    try {
        const response = await fetch(`/api/records/${recordId}`);
        const result = await response.json();
        
        if (result.success) {
            currentData = result.record;
            currentRecordId = recordId;
            
            // Format for display
            const displayResult = {
                success: true,
                company: result.record.insurance_company,
                data: result.record,
                is_valid: result.record.extraction_status === 'success',
                validation_errors: result.record.error_message ? 
                    [result.record.error_message] : []
            };
            
            displayResults(displayResult);
        }
        
    } catch (error) {
        showError('Error viewing record: ' + error.message);
    }
}

async function deleteRecord(recordId) {
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/records/${recordId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            loadHistory();
            if (currentRecordId === recordId) {
                resetForm();
            }
        } else {
            showError('Failed to delete record');
        }
        
    } catch (error) {
        showError('Error deleting record: ' + error.message);
    }
}

function resetForm() {
    currentData = null;
    currentRecordId = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('processingSection').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showError(message) {
    alert('Error: ' + message);
}