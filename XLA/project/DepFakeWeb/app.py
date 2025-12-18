import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import io

# Khởi tạo Flask app
app = Flask(__name__)

# Tải model đã train
model = None
class_names = []
try:
    model = tf.keras.models.load_model("deepFakeCNN.keras")
    class_names = ["Fake", "Real"]
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure 'deepFakeCNN.keras' is in the same directory as this script.")

# Thư mục lưu ảnh tạm thời
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hàm tiền xử lý ảnh
def preprocess_image(image_path):
    img = None
    try:
        print(f"Preprocessing image: {image_path}") # Debug print
        img = Image.open(image_path).convert("RGB")
        print(f"Image opened, mode: {img.mode}, size: {img.size}") # Debug print
        img = img.resize((256, 256))
        print(f"Image resized to: {img.size}") # Debug print
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        print(f"Shape of img_array after preprocessing: {img_array.shape}") # Debug print
        return img_array
    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
        return None
    except IOError as e:
        print(f"Error opening image: {e}")
        print(f"IOError details: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in preprocess_image: {e}")
        return None
    finally:
        if img:
            img.close() # Đảm bảo đóng file trong finally block

# Endpoint dự đoán
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Please check server logs."}), 500

    if 'file' not in request.files:
        print("Error: No file part in the request") # Debug print
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        print("Error: No selected file") # Debug print
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            # print(f"Saving file to: {file_path}")
            # file.save(file_path)

            image = Image.open(io.BytesIO(file.read())).convert("RGB")
            image = image.resize((256, 256))
            img_array = np.array(image) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            print(f"Shape of img_array: {img_array.shape}")

            predictions = model.predict(img_array)
            print(f"Predictions: {predictions}")
            predicted_class = class_names[int(predictions[0] > 0.5)]
            confidence = float(predictions[0])
            print(f"Predicted class: {predicted_class}, Confidence: {confidence}")

            # os.remove(file_path) # Comment out việc xóa file tạm
            return jsonify({"class": predicted_class, "confidence": confidence})

        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({"error": "Internal server error during prediction"}), 500

    return jsonify({"error": "Something went wrong"}), 500

# Endpoint để hiển thị trang HTML
@app.route("/")
def index():
    return render_template("index.html")

# Để phục vụ các file tĩnh (nếu bạn có thêm CSS, JS...)
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<filename>')
def serve_static(filename):
    root_path = os.path.dirname(os.path.abspath(__file__)) # Lấy đường dẫn thư mục gốc
    return send_from_directory(root_path, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)