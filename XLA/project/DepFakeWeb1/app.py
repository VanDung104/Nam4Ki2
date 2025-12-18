import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image
import io

# Khởi tạo Flask app
app = Flask(__name__)

# Tải model đã train
model = tf.keras.models.load_model("deepFakeCNN.keras")

class_names = ["Fake", "Real"]  

# Thư mục lưu ảnh tạm thời
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Hàm tiền xử lý ảnh
def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((256, 256))  # Resize theo kích thước model
    img_array = np.array(img) / 255.0  # Chuẩn hóa về [0,1]
    img_array = np.expand_dims(img_array, axis=0)  # Thêm batch dimension
    return img_array

# Endpoint dự đoán
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    # image = Image.open(io.BytesIO(file.read())) # Đọc ảnh từ request mà không lưu file
    # Tiền xử lý ảnh
    img_array = preprocess_image(file_path)
    # img_array = preprocess_image(image)

    # Dự đoán bằng model
    predictions = model.predict(img_array)
    predicted_class = class_names[int(predictions[0] > 0.5)]  # Model nhị phân (0/1)

    return jsonify({"class": predicted_class, "confidence": float(predictions[0])})

# Chạy server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)