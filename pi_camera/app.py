from flask import Flask, render_template, send_file
from PIL import Image
from picamera2 import Picamera2
import io

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888'}))
picam2.start()


def capture_image_bytes() -> bytes:
    frame = picam2.capture_array()
    pil_image = Image.fromarray(frame)
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
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
    app.run(host='0.0.0.0', debug=True, port=8008)
