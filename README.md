# image_collection
a collection of utilities that are useful for .. image collection

## Detection Server

A Flask-based object detection service using Ultralytics YOLO models.
Tested on a DGX Spark

Nvidia GPU recommended. I tested it on a Nvidia DGX Spark.

- **Web UI**: Visit `http://localhost:5000` to upload images and view detections
- **API**: POST to `http://localhost:5000/upload` with an image file
