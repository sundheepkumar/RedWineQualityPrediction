import pickle
import numpy as np

# Test script to verify model functionality

# Load the trained model
def load_model(file_path):
    try:
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
        return model
    except FileNotFoundError:
        print(f"Error: Model file '{file_path}' not found. Ensure the file exists.")
        return None
    except pickle.UnpicklingError:
        print("Error: Unable to unpickle the model file. Check the file format and source.")
        return None
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

# Define sample input for testing
def test_model(model):
    if model is None:
        print("Cannot test model. Model failed to load.")
        return

    try:
        # Replace these values with realistic test data
        sample_input = np.array([
            7.4,  # fixed_acidity
            0.7,  # volatile_acidity
            0.0,  # citric_acid
            1.9,  # residual_sugar
            0.076,  # chlorides
            11.0,  # free_sulfur_dioxide
            34.0,  # total_sulfur_dioxide
            0.9978,  # density
            3.51,  # pH
            0.56,  # sulphates
            9.4    # alcohol
        ]).reshape(1, -1)  # Reshape to 2D array as expected by model

        # Perform prediction
        prediction = model.predict(sample_input)
        print(f"Prediction result: {prediction[0]}")
    except Exception as e:
        print(f"Error during prediction: {e}")

if __name__ == "__main__":
    # Path to your model file
    model_file = 'wineprediction.model'

    # Load and test the model
    model = load_model(model_file)
    test_model(model)