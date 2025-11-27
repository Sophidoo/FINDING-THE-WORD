// Game-specific JavaScript functions

function showAlert(title, text = '', icon = 'success', timer = null) {
    Swal.fire({
        title: title,
        text: text,
        icon: icon,          // success, error, warning, info, question
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: timer || 3000,
        timerProgressBar: true,
    });
}

// Word selection functionality
let selectedCells = [];
let isSelecting = false;

function initializeGridSelection() {
    const cells = document.querySelectorAll('.grid-cell');

    cells.forEach(cell => {
        cell.addEventListener('mousedown', startSelection);
        cell.addEventListener('mouseenter', continueSelection);
        cell.addEventListener('mouseup', endSelection);

        // Touch events for mobile
        cell.addEventListener('touchstart', startSelection);
        cell.addEventListener('touchmove', continueSelection);
        cell.addEventListener('touchend', endSelection);
    });

    document.addEventListener('mouseup', endSelection);
}

function startSelection(e) {
    e.preventDefault();
    isSelecting = true;
    selectedCells = [];
    addToSelection(this);
}

function continueSelection(e) {
    if (!isSelecting) return;
    e.preventDefault();
    addToSelection(this);
}

function endSelection() {
    if (!isSelecting) return;
    isSelecting = false;

    if (selectedCells.length > 0) {
        const selectedWord = selectedCells.map(cell => cell.textContent).join('');
        document.getElementById('wordInput').value = selectedWord;

        // Auto-submit if word is long enough
        if (selectedWord.length >= 3) {
            submitWord();
        }
    }

    // Clear selection after a delay
    setTimeout(() => {
        selectedCells.forEach(cell => cell.classList.remove('selected'));
        selectedCells = [];
    }, 500);
}

function addToSelection(cell) {
    if (!selectedCells.includes(cell)) {
        cell.classList.add('selected');
        selectedCells.push(cell);
    }
}

// Utility function to show alerts
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.custom-alert');
    existingAlerts.forEach(alert => alert.remove());

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} custom-alert alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.querySelector('main').insertBefore(alertDiv, document.querySelector('main').firstChild);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    };

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, { ...defaultOptions, ...options });

        // Check if response is HTML (error) instead of JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            console.error('Server returned HTML instead of JSON:', text.substring(0, 200));
            throw new Error('Server error: Received HTML response instead of JSON');
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `API request failed with status ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API CALL FAILED →', error);
        if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
            showAlert('Connection Lost', 'Check your internet or server', 'error');
        } else {
            showAlert('Error', error.message || 'Something went wrong', 'error');
        }
        throw error;
    }
}

