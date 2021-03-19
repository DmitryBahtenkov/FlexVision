from flask import Flask, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
from camera import VideoCamera
from detector import Detector
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'
ALLOWED_EXTENSIONS = set(['mp4', 'flv'])


# при обращении функция вечно возвращает кадры в спец. формате
def gen(camera, detector):
    while True:
        frame = camera.get_detecting_frame(detector)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# страничка панели управления
@app.route('/')
def index():
    return "Hello!"


# видео
@app.route('/one-park')
def video_feed():
    return Response(gen(VideoCamera("videos/1.mp4"), Detector("detectors/cascade20.xml")),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='localhost')
