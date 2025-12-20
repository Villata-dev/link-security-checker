document.addEventListener('DOMContentLoaded', () => {
    const scanButton = document.getElementById('scan-button');
    const urlInput = document.getElementById('url-input');
    const resultsContainer = document.getElementById('results-container');
    const resultCard = document.getElementById('result-card');
    const resultMessage = document.getElementById('result-message');
    const loadingSpinner = document.getElementById('loading-spinner');

    scanButton.addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (!url) {
            alert('Please enter a URL to scan.');
            return;
        }

        // Show loading spinner and hide previous results
        loadingSpinner.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        resultsContainer.classList.remove('visible');

        fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            loadingSpinner.classList.add('hidden');
            displayResults(data);
        })
        .catch(error => {
            loadingSpinner.classList.add('hidden');
            displayError(error.message);
        });
    });

    function displayResults(data) {
        resultCard.className = 'card'; // Reset classes
        switch (data.status) {
            case 'SAFE':
                resultCard.classList.add('safe');
                resultMessage.textContent = `This link appears to be safe. Malicious detections: ${data.malicious_count}`;
                break;
            case 'DANGER':
                resultCard.classList.add('danger');
                resultMessage.textContent = `This link is potentially dangerous! Malicious detections: ${data.malicious_count}`;
                break;
            case 'WARNING':
                resultCard.classList.add('warning');
                resultMessage.textContent = `Use caution with this link. Malicious detections: ${data.malicious_count}`;
                break;
            default:
                resultMessage.textContent = 'Could not determine the status of the link.';
        }
        resultsContainer.classList.remove('hidden');
        setTimeout(() => resultsContainer.classList.add('visible'), 10);
    }

    function displayError(errorMessage) {
        resultCard.className = 'card danger'; // Use danger style for errors
        resultMessage.textContent = `Error: ${errorMessage}`;
        resultsContainer.classList.remove('hidden');
        setTimeout(() => resultsContainer.classList.add('visible'), 10);
    }
});
