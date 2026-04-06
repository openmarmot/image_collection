# image_collection
a collection of utilities that are useful for .. image collection

## Detection Server

A Flask-based object detection service using YOLO models.

### Setup

```bash
cd detection_server
./run.sh
```

### Usage

- **Web UI**: Visit `http://localhost:5000` to upload images and view detections
- **API**: POST to `http://localhost:5000/upload` with an image file

```bash
curl -X POST -F "image=@path/to/image.jpg" http://localhost:5000/upload
```

### Requirements

- Python 3.8+
- GPU recommended (CUDA-enabled PyTorch)
