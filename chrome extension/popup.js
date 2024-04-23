document.addEventListener('DOMContentLoaded', function () {
  // Get the active tab URL and populate the input field
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const url = tabs[0].url;
      document.getElementById('urlInput').value = url;
  });

  // Add event listener for the predict button click
  document.getElementById('predictButton').addEventListener('click', predictUrl);
});

function predictUrl() {
  const url = document.getElementById('urlInput').value;
  fetchPrediction(url);
}

function fetchPrediction(url) {
  fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
  })
  .then(response => response.json())
  .then(data => {
      // Display the prediction result
      displayResult(data);
  })
  .catch(error => {
      console.error('Error:', error);
      // Display error message
      displayResult({ prediction: 'Error occurred. Please try again.' });
  });
}

function displayResult(data) {
  const resultElement = document.getElementById('result');
  // Clear previous result
  resultElement.innerHTML = '';

  // Create a new paragraph element to display the prediction result
  const predictionParagraph = document.createElement('p');
  predictionParagraph.textContent = `${data.prediction.class}`;

  // Create an image element for the icon
  const iconImage = document.createElement('img');
  let iconFilename = '';
  if (data.prediction.class === 'Safe to Use') {
      iconFilename = 'green check.png';
  } else {
      iconFilename = 'cancel.png';
  }
  iconImage.src = `icons/${iconFilename}`;
  iconImage.alt = 'Prediction Icon';

  // Append the icon image and prediction text to the result element
  resultElement.appendChild(iconImage);
  resultElement.appendChild(predictionParagraph);
}

