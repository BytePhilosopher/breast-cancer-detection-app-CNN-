from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # ← KEY FIX

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_model("model/model.h5")
LABELS = ["benign", "malignant"]


# Home route
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Breast Cancer Detection API is running!"})

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        img = load_img(filepath, target_size=(64, 64))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0][0]
        label = LABELS[int(prediction >= 0.5)]

        return jsonify({
            "prediction_score": float(prediction),
            "predicted_class": label
        })
    except Exception as e:
        print("❌ INTERNAL ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# @app.route('/predict', methods=['OPTIONS'])
# def handle_options_predict():
#     response = app.make_default_options_response()
#     headers = response.headers

#     # Adjust to your frontend URL:
#     headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#     headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#     headers['Access-Control-Allow-Headers'] = 'Content-Type'

#     return response

if __name__ == "__main__":
    app.run(debug=True, port=8000)
