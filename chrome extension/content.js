// This event listener runs when a message is received from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'classify_url') {
        // Extract the URL from the message
        const url = message.url;
        // Call your classifyUrl function here passing the URL for classification
        classifyUrl(url);
    }
});

// Your classifyUrl function implementation goes here
function classifyUrl(url) {
    // Call your prediction endpoint with the provided URL
    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
        // Process the prediction result as needed
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
