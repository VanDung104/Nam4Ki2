import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template, send_from_directory
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

# Khởi tạo Flask app
app = Flask(__name__)

# Thư mục tĩnh để lưu file như a.png
app.static_folder = 'static'
app.static_url_path = 'D:/Nam4Ki2/DL/Project/web/static'

# Tải model đã train
model = tf.keras.models.load_model("D:/Nam4Ki2/DL/Project/web/27042025besst_modelhihi.keras")
class_names = ["Mèo", "Gà", "Chó", "Lợn"]  # Danh sách tên lớp tương ứng với đầu ra của model

# Thư mục lưu ảnh tạm thời
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Phục vụ file tĩnh (như a.png)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Trả về file index.html từ thư mục templates

# Endpoint dự đoán
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Đọc ảnh từ file upload vào bộ nhớ
        img = Image.open(io.BytesIO(file.read()))
        img = img.convert("RGB")
        img = img.resize((480, 480))

        # Chuyển ảnh sang array và tiền xử lý
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)

        # Dự đoán
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))

        # Tính phần trăm cho các lớp
        probabilities = predictions[0].tolist()
        class_probabilities = {
            class_name: round(prob * 100, 2)
            for class_name, prob in zip(class_names, probabilities)
        }

        return jsonify({
            "Lớp dự đoán": class_names[predicted_class_index],
            "Độ chính xác": round(confidence * 100, 2),
            "Độ chính xác các lớp": class_probabilities
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chạy server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)