from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Load the serialized model
with open('heart_disease_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def index():
    # Render the main index.html page
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    data = request.get_json(force=True)
    # Print the received values for debugging
    print("Received features:", data)
    feature_names = ['age', 'sex_encoded', 'cp', 'trestbps', 'chol', 'fbs_encoded', 'restecg_encoded', 
                      'thalach', 'exang_encoded', 'oldpeak', 'slope', 'ca', 'thal']
    
    # Extract features from the request data
    features = {
        'age': [data['age']],
        'sex_encoded': [data['sex_encoded']],
        'cp': [data['cp']],
        'trestbps': [data['trestbps']],
        'chol': [data['chol']],
        'fbs_encoded': [data['fbs_encoded']],
        'restecg_encoded': [data['restecg_encoded']],
        'thalach': [data['thalach']],
        'exang_encoded': [data['exang_encoded']],
        'oldpeak': [data['oldpeak']],
        'slope': [data['slope']],
        'ca': [data['ca']],
        'thal': [data['thal']]
    }

    # Convert features to a DataFrame and apply scaling
    features_df = pd.DataFrame(features, columns=feature_names)
    features_scaled = scaler.transform(features_df)

    prediction = model.predict(features_scaled)[0]
    result = 'Heart Disease' if prediction == 1 else 'No Heart Disease'
  
    return jsonify({'prediction': result, 'ok': 'true'})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)
