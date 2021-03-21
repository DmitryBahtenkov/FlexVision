from flask import Flask, Response, stream_with_context, render_template
import itertools
import numpy as np

from camera import VideoCamera
from detector import Detector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'
app.debug = True
app.templates_auto_reload = True
response = dict()

# при обращении функция вечно возвращает кадры в спец. формате
def gen(camera, detector, num):
    while True:
        frame, _ = camera.get_detecting_frame(detector, num)
        yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_data(camera, detector, num):
    global last
    while True:
        _, count = camera.get_detecting_frame(detector, num)
        name = ""
        busi_message = ""
        if(num == 1):
            name = "Парковка на улице Ленина"
        elif (num == 2):
            name = "Парковка на улице Анохина"
        else:
            name = "Безымянная парковка"

        if(count <= 3):
            busi_message = "Низкая загруженность парковки"
        elif(3 < count < 8):
            busi_message = "Средняя загруженность парковки"
        elif(count >= 8):
            busi_message = "Высокая загруженность парковки"

        resp = {"name":name, "car_count":count, "workload":busi_message}
        yield render_template('index.html', resp=resp)


@app.route('/')
def index():
    return "Hello!"


# видео
@app.route('/one-park')
def video_one_feed():
    return Response(gen(VideoCamera("videos/1.mp4"), Detector("detectors/cascade20.xml"), 1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/two-park')
def video_two_feed():
    return Response(gen(VideoCamera("videos/2.mp4"), Detector("detectors/cascade.xml"), 2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/one-park-data')
def video_one_data():
    response = gen_data(VideoCamera("videos/1.mp4"), Detector("detectors/cascade20.xml"), 1)

    return Response(stream_with_context(response))


@app.route('/two-park-data')
def video_two_data():
    return Response(gen_data(VideoCamera("videos/2.mp4"), Detector("detectors/cascade.xml"), 2))

if __name__ == '__main__':
    app.run(host='localhost')
