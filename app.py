from flask import Flask, request, jsonify, abort, render_template_string
import joblib
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.joblib')

# Define class labels
class_labels = {
    0: {'label': 'Safe to Use', 'icon': 'green check.png'},
    1: {'label': 'Content Modified', 'icon': 'cancel.png'},
    2: {'label': 'Phishing', 'icon': 'cancel.png'},
    3: {'label': 'Malware', 'icon': 'cancel.png'}
}

def preprocess_url(url):
    # Remove 'www.' from the URL
    url = url.replace('www.', '')

    # Extract features from the URL
    features = {}

    # Length of the URL
    features['url_len'] = len(url)

    # Number of letters in the URL
    features['letters'] = sum(char.isalpha() for char in url)

    # Number of digits in the URL
    features['digits'] = sum(char.isdigit() for char in url)

    # Check for special characters in the URL
    special_chars = "@?-=.#%+$!*,//"
    for char in special_chars:
        features[char] = url.count(char)

    # Check if the URL contains a shortening service
    features['Shortining_Service'] = 1 if re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|'
                                                     'tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|'
                                                     'tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                                                     'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|'
                                                     'snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|'
                                                     'wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                                                     'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|'
                                                     'ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|'
                                                     'u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|'
                                                     'prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|'
                                                     '1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url) else 0

    # Check if the URL is abnormal
    features['abnormal_url'] = 1 if re.search(urlparse(url).hostname, url) else 0

    # Check if the URL uses HTTPS
    features['https'] = 1 if urlparse(url).scheme == 'https' else 0

    # Check if the URL has an IP address
    features['having_ip_address'] = 1 if re.search(
        '((?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.){3}(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])', url) else 0

    return features                 

@app.route('/predict', methods=['POST'])
def predict():
    # Get the URL from the request data
    url = request.json.get('url')

    # Check if URL is provided
    if not url:
        abort(400, description="URL is missing in the request")

    # Preprocess the URL to extract features
    features = preprocess_url(url)

    # Convert features to a format suitable for prediction
    features_for_prediction = [list(features.values())]

    # Make a prediction using the loaded model
    prediction = model.predict(features_for_prediction)[0]

    # Convert prediction to a regular Python integer
    prediction = int(prediction)

    # Get the class label for the prediction
    class_info = class_labels.get(prediction, {'label': 'Unknown', 'icon': 'unknown.png'})

    # Return the prediction result as JSON
    result = {
        'url': url,
        'prediction': {
            'class': class_info['label'],
            'class_icon': class_info['icon']
        }
    }

    return jsonify(result)

# Error handler for 400 Bad Request errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description}), 400

if __name__ == '__main__':
    app.run(debug=True)
