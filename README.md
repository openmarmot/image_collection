# image_collection
a collection of utilities that are useful for .. image collection

## Detection Server

A Flask-based object detection service using Ultralytics YOLO models.
Tested on a DGX Spark

Nvidia GPU recommended. I tested it on a Nvidia DGX Spark.

- **Web UI**: Visit `http://localhost:5000` to upload images and view detections
- **API**: POST to `http://localhost:5000/upload` with an image file

![screenshot](/screenshots/detection_server.png "detection_server")

## Pi Camera

A Flask-based Raspberry Pi camera server using `picamera2`.
Tested on a Raspberry Pi 5.

- **Web UI**: Visit `http://localhost:8008` to view and capture images
- **API**: GET `http://localhost:8008/capture_image` returns a JPEG
