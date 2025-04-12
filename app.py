from flask import Flask, render_template, request, jsonify
from pypmml import Model
import os
import pandas as pd

app = Flask(__name__)

model_path = 'winemodelv2.pmml'

# Load the model
if os.path.exists(model_path):
    try:
        model = Model.load(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading the model: {e}")
        model = None
else:
    print("Model file not found.")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500

    data = request.json
    try:
        # Prepare the input exactly as expected by the PMML model
        prediction_input = {
            'fixed acidity': float(data['fixed_acidity']),
            'volatile acidity': float(data['volatile_acidity']),
            'citric acid': float(data['citric_acid']),
            'residual sugar': float(data['residual_sugar']),
            'chlorides': float(data['chlorides']),
            'free sulfur dioxide': float(data['free_sulfur_dioxide']),
            'total sulfur dioxide': float(data['total_sulfur_dioxide']),
            'density': float(data['density']),
            'pH': float(data['pH']),
            'sulphates': float(data['sulphates']),
            'alcohol': float(data['alcohol']),
        }

        # Run prediction
        prediction = model.predict(prediction_input)

        # Extract predicted value from model output
        quality = int(prediction['predicted_quality'])

        # Add optional category for fun
        if quality >= 7:
            category = "Excellent 🍷"
        elif quality >= 5:
            category = "Good 👍"
        else:
            category = "Needs improvement 😬"

        return jsonify({
            'quality': quality,
            'category': category
        })

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 400

def quality_category(q):
    """Optional helper to assign quality label"""
    if q >= 7:
        return "Good"
    elif q >= 5:
        return "Average"
    else:
        return "Poor"

if __name__ == '__main__':
    app.run(debug=True)
