chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete') {
        console.log('Tab updated:', tab.url);
        // Send a message to the content script to classify the URL
        chrome.tabs.sendMessage(tabId, { action: 'classify_url', url: tab.url });
    }
});
