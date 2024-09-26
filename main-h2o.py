from flask import Flask, request, jsonify, render_template
import h2o
import pandas as pd
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Initialize H2O
h2o.init()

# Load the saved H2O model
model_path = './best_model/StackedEnsemble_AllModels_1_AutoML_2_20240914_144741'
model = h2o.load_model(model_path)

print("Model loaded")

def interpret_prediction(prediction):
    # Define a mapping from numerical values to labels
    if prediction == 0:
        return "Not Survived"
    else:
        return "Survived"

@app.route('/')
def index():
    # Render the main index.html page
    return render_template('index.html')
    
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request
    data = request.json
    print("Received data:", data)

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame([data])
    # Convert DataFrame to H2OFrame
    h2o_frame = h2o.H2OFrame(df)
    
    # Make prediction
    predictions = model.predict(h2o_frame)
    
    # Convert predictions to pandas DataFrame
    predictions_df = predictions.as_data_frame()
    
    # Extract the prediction value
    predict_value = predictions_df['predict'][0]
    
    # Print and return the result
    result = interpret_prediction(predict_value)
    print(f"The prediction is: {result}")

    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
