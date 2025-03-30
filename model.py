'''import cv2
import torch
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import io
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLOv8 model (Ensure you have the model downloaded)
model = YOLO("yolov8n.pt")  # Use 'yolov8s.pt' for a larger model

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        data = request.json
        image_bytes = io.BytesIO(data['image'])
        img = Image.open(image_bytes).convert("RGB")
        img = np.array(img)

        # Run YOLO inference
        results = model(img)

        detected_objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
                conf = box.conf[0].item()  # Confidence score
                cls = int(box.cls[0].item())  # Class index
                label = model.names[cls]  # Get class label
                
                detected_objects.append({
                    "label": label,
                    "confidence": conf,
                    "box": [x1, y1, x2, y2]
                })

        return jsonify({"objects": detected_objects})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='192.168.x.x', port=5000)'''
'''import cv2
import torch
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import io
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLOv8 model
model = YOLO("yolov8n.pt") 

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        data = request.json
        width, height = data['width'], data['height']
        pixel_array = np.array(data['image'], dtype=np.uint8)  # Convert to NumPy array

        # ✅ Ensure correct shape (H, W, 3) for RGB
        if pixel_array.size != width * height * 3:
            return jsonify({"error": "Incorrect image size received!"})

        img = pixel_array.reshape((height, width, 3))  # Reshape to (H, W, 3)

        # 🔹 Ensure OpenCV is in RGB format (some versions expect BGR)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert RGB → BGR if needed

        # Run YOLO inference
        results = model(img)

        detected_objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Convert coordinates to integers
                conf = float(box.conf[0].item())  # Confidence score
                cls = int(box.cls[0].item())  # Class index
                label = model.names[cls]  # Get class label
                
                detected_objects.append({
                    "label": label,
                    "confidence": conf,
                    "box": [x1, y1, x2, y2]
                })

        return jsonify({"objects": detected_objects})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='192.168.1.9', port=5000)'''
import cv2
import torch
import numpy as np
from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        # ✅ Read image from request
        file = request.files['image']
        image = Image.open(file).convert("RGB")
        image = np.array(image)

        # Run YOLO inference
        results = model(image)

        detected_objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(float, box.xyxy[0].tolist())  # ✅ Convert tensor to float list
                conf = float(box.conf[0].item())  # ✅ Convert tensor to float
                cls = int(box.cls[0].item())  # ✅ Convert tensor to int
                label = model.names[cls]

                detected_objects.append({
                    "label": label,
                    "confidence": conf,
                    "box": [x1, y1, x2, y2]
                })

        return jsonify({"objects": detected_objects})  # ✅ Now it's JSON serializable

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
