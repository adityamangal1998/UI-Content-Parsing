function addUrlInput() {
    const urlInputs = document.getElementById('url-inputs');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'urls';
    input.placeholder = 'Enter URL';
    urlInputs.appendChild(input);
}

document.getElementById('scrape-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const urls = formData.getAll('urls');
    const scrapeButton = event.target.querySelector('button[type="submit"]');
    scrapeButton.disabled = true;
    showLoading('scrape-result');
    const response = await fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls }),
    });
    const result = await response.json();
    hideLoading('scrape-result');
    document.getElementById('scrape-result').innerText = result.message;
    scrapeButton.disabled = false;
});

async function askQuestion() {
    const question = document.getElementById('question').value;
    const urls = Array.from(document.getElementsByName('urls')).map(input => input.value);
    const askButton = document.querySelector('#chatbox button');
    askButton.disabled = true;
    showLoading('answer');
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, urls }),
    });
    const result = await response.json();
    hideLoading('answer');
    document.getElementById('answer').innerText = result.answer;
    askButton.disabled = false;
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = '<div class="loading">Loading...</div>';
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = '';
}
