from flask import Flask, render_template, send_file
from PIL import Image
from picamera2 import Picamera2
import io
import time

app = Flask(__name__)

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1920, 1080), "format": "RGB888"})
picam2.configure(config)
# AWB enabled for automatic white balance (best for most lighting)
picam2.set_controls({"AeEnable": True, "AwbEnable": True})
picam2.start()

time.sleep(2)


def capture_image_bytes() -> bytes:
    """Capture from the camera ISP with automatic white balance and the
    RGB channel order correction for this OV5647 sensor.
    """
    frame = picam2.capture_array()
    # On this OV5647 + picamera2 setup (especially on Pi 5), capture_array()
    # with RGB888 delivers data in BGR order. Swap to correct colors.
    frame = frame[:, :, ::-1]
    pil_image = Image.fromarray(frame)

    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG", quality=92)
    buffered.seek(0)
    return buffered.getvalue()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture_image')
def capture_image():
    image_bytes = capture_image_bytes()
    return send_file(
        io.BytesIO(image_bytes),
        mimetype='image/jpeg',
        as_attachment=False,
        download_name='capture.jpg'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False, port=8008)
