// AJAX requests
function loadProperties() {
    fetch('/api/properties')
        .then(response => response.json())
        .then(data => {
            updatePropertiesList(data);
        });
}

// Chart initialization
function initializeCharts() {
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: salesData,
        options: chartOptions
    });
}

function updatePropertyStatus(propertyId, newStatus) {
    fetch(`/api/properties/${propertyId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        updateUI(data);
    });
}

function loadDashboardCharts() {
    fetch('/api/analytics/sales')
        .then(response => response.json())
        .then(data => {
            createSalesChart(data);
            createLeadsChart(data);
        });
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value) {
            isValid = false;
            showError(input, 'This field is required');
        }
    });

    return isValid;
}

// Show loading animation
function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading';
    loading.innerHTML = `
        <img src="/static/images/logo.png" alt="Loading...">
    `;
    document.body.appendChild(loading);
}

// Hide loading animation
function hideLoading() {
    const loading = document.querySelector('.loading');
    if (loading) {
        loading.remove();
    }
}

// Use loading animation for AJAX requests
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('a:not([target="_blank"])');
    links.forEach(link => {
        link.addEventListener('click', () => {
            showLoading();
        });
    });
}); 