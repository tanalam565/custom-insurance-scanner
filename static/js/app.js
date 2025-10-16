const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const submitBtn = document.getElementById('submitBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const error = document.getElementById('error');
const resetBtn = document.getElementById('resetBtn');

let currentRecordId = null;

// File input handlers
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
    }
});

// Drag and drop
const fileLabel = document.getElementById('fileLabel');

fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#764ba2';
    fileLabel.style.background = '#f0f1ff';
});

fileLabel.addEventListener('dragleave', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#667eea';
    fileLabel.style.background = '#f8f9ff';
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#667eea';
    fileLabel.style.background = '#f8f9ff';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = file.name;
    }
});

// Form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a file');
        return;
    }
    
    uploadForm.classList.add('hidden');
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Upload failed');
        }
        
        currentRecordId = data.record_id;
        displayResults(data.data);
        loadStats();
        loadRecords('all');
    } catch (err) {
        showError(err.message);
    } finally {
        loading.classList.add('hidden');
    }
});

function displayResults(data) {
    document.getElementById('insuranceCompany').textContent = data.insurance_company || '-';
    document.getElementById('detectedCompany').textContent = data.detected_company || '-';
    document.getElementById('policyNumber').textContent = data.policy_number || '-';
    document.getElementById('policyholderName').textContent = data.policyholder_name || '-';
    document.getElementById('propertyAddress').textContent = data.property_address || '-';
    document.getElementById('coverageAmount').textContent = data.coverage_amount || '-';
    document.getElementById('liabilityCoverage').textContent = data.liability_coverage || '-';
    document.getElementById('deductible').textContent = data.deductible || '-';
    document.getElementById('effectiveDate').textContent = data.effective_date || '-';
    document.getElementById('expirationDate').textContent = data.expiration_date || '-';
    document.getElementById('premiumAmount').textContent = data.premium_amount || '-';
    document.getElementById('processingTime').textContent = 
        data.processing_time ? `${data.processing_time.toFixed(2)}s` : '-';
    
    // Company badge
    const companyBadge = document.getElementById('companyBadge');
    companyBadge.textContent = data.detected_company || 'Unknown';
    
    // Confidence indicator
    const confidenceIndicator = document.getElementById('confidenceIndicator');
    const confidence = data.confidence_score || 0;
    confidenceIndicator.textContent = `Confidence: ${confidence.toFixed(1)}%`;
    
    if (confidence >= 80) {
        confidenceIndicator.className = 'confidence-indicator confidence-high';
    } else if (confidence >= 50) {
        confidenceIndicator.className = 'confidence-indicator confidence-medium';
    } else {
        confidenceIndicator.className = 'confidence-indicator confidence-low';
    }
    
    results.classList.remove('hidden');
}

async function exportData(format) {
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                format: format,
                record_ids: [currentRecordId]
            })
        });
        
        if (!response.ok) throw new Error('Export failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `insurance_data.${format === 'excel' ? 'xlsx' : format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (err) {
        showError('Export failed: ' + err.message);
    }
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    error.classList.remove('hidden');
    uploadForm.classList.remove('hidden');
}

function resetForm() {
    fileInput.value = '';
    fileName.textContent = 'Choose file or drag here';
    uploadForm.classList.remove('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
    currentRecordId = null;
}

resetBtn.addEventListener('click', resetForm);

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        document.getElementById('totalRecords').textContent = `Total: ${data.total_records}`;
        document.getElementById('needsReview').textContent = `Needs Review: ${data.needs_review}`;
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

async function loadRecords(filter = 'all') {
    try {
        const url = filter === 'review' 
            ? '/api/records?needs_review=true&limit=10'
            : '/api/records?limit=10';
        
        const response = await fetch(url);
        const records = await response.json();
        
        const recordsList = document.getElementById('recordsList');
        recordsList.innerHTML = '';
        
        if (records.length === 0) {
            recordsList.innerHTML = '<p style="text-align:center;color:#666;">No records found</p>';
            return;
        }
        
        records.forEach(record => {
            const div = document.createElement('div');
            div.className = 'record-item';
            div.innerHTML = `
                <div class="record-info">
                    <strong>${record.filename}</strong>
                    ${record.needs_review ? '<span class="needs-review-badge">Needs Review</span>' : ''}
                    <br>
                    <small>${record.detected_company} - ${record.confidence_score}% confidence</small>
                </div>
                <div class="record-actions">
                    <button onclick="viewRecord(${record.id})">View</button>
                    <button onclick="deleteRecord(${record.id})">Delete</button>
                </div>
            `;
            recordsList.appendChild(div);
        });
        
        // Update active tab
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');
    } catch (err) {
        console.error('Failed to load records:', err);
    }
}

async function viewRecord(id) {
    try {
        const response = await fetch(`/api/records/${id}`);
        const record = await response.json();
        
        currentRecordId = id;
        displayResults(record);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
        showError('Failed to load record');
    }
}

async function deleteRecord(id) {
    if (!confirm('Delete this record?')) return;
    
    try {
        await fetch(`/api/records/${id}`, { method: 'DELETE' });
        loadRecords('all');
        loadStats();
    } catch (err) {
        showError('Failed to delete record');
    }
}

// Load initial data
loadStats();
loadRecords('all');
