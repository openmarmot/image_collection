from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO
from PIL import Image
import io
import base64
import cv2
import torch

app = Flask(__name__)

# Device detection
if torch.cuda.is_available():
    device = 0
    print(f"Torch GPU : {torch.cuda.get_device_name(0)}")
else:
    device = 'cpu'
    print('Warning! GPU not detected. Running on CPU')

# Load model
model_path = "yolo26s.pt"
model = YOLO(model_path).to(device)
model_display_name = model_path.replace(".pt", "").upper()


def process_image(image_bytes: bytes, include_annotated: bool = False) -> dict:
    """Single place where YOLO runs — works with ALL ultralytics versions"""
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Run YOLO
    results = model(image, conf=0.25, verbose=False)

    # Make sure we have a single Results object (handles both old and new ultralytics)
    result = results[0] if isinstance(results, list) else results

    # Manual detection extraction (replaces .tojson() — works everywhere)
    detections_list = []
    if result.boxes is not None:
        for box in result.boxes:
            cls_id = int(box.cls[0].item())          # .item() for safety
            conf = float(box.conf[0].item())
            class_name = result.names[cls_id]
            detections_list.append({
                "name": class_name,
                "class": cls_id,
                "confidence": conf,
                "box": box.xyxy[0].tolist() if hasattr(box, 'xyxy') else None
            })

    # Speed stats
    speed = result.speed
    total_time = round(speed['preprocess'] + speed['inference'] + speed['postprocess'], 2)

    response_data = {
        "success": True,
        "model": model_display_name,
        "num_detections": len(detections_list),
        "detections": detections_list,
        "speed_ms": {
            "total": total_time,
            "preprocess": round(speed['preprocess'], 2),
            "inference": round(speed['inference'], 2),
            "postprocess": round(speed['postprocess'], 2)
        }
    }

    # Optional annotated image
    if include_annotated:
        annotated_array = result.plot()
        annotated_rgb = cv2.cvtColor(annotated_array, cv2.COLOR_BGR2RGB)
        annotated_pil = Image.fromarray(annotated_rgb)
        buffered = io.BytesIO()
        annotated_pil.save(buffered, format="JPEG")
        response_data["annotated_image"] = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return response_data

@app.route('/', methods=['GET', 'POST'])
def index():
    """Web UI"""
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        if file.filename == '':
            return "No file selected", 400

        image_bytes = file.read()
        data = process_image(image_bytes, include_annotated=True)

        return render_template('index.html',
                               model_display_name=data["model"],
                               annotated_image=data.get("annotated_image"),
                               detections=data["detections"],
                               speed=data["speed_ms"],
                               total_time=data["speed_ms"]["total"])

    return render_template('index.html', model_display_name=model_display_name)


@app.route('/upload', methods=['POST'])
def api_upload():
    """API for laptop_collector.py"""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400

    include_annotated = request.form.get('include_annotated', 'false').lower() in ('true', '1', 'yes')

    try:
        image_bytes = file.read()
        data = process_image(image_bytes, include_annotated=include_annotated)
        return jsonify(data)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
