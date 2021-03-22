from flask import Flask, Response, stream_with_context, render_template, request
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


def gen_data(camera, detector, num, custom_video):
    global last
    while True:
        _, count = camera.get_detecting_frame(detector, num)
        name = ""
        video = ''
        busi_message = ""

        if (num == 1):
            name = "Парковка на улице Ленина"
            video = 'http://localhost:5000/one-park'
        elif (num == 2):
            name = "Парковка на улице Анохина"
            video = 'http://localhost:5000/two-park'
        else:
            name = "Безымянная парковка"

        if custom_video is not None:
            video = custom_video

        if (count <= 3):
            busi_message = "Низкая загруженность парковки"
        elif (3 < count < 8):
            busi_message = "Средняя загруженность парковки"
        elif (count >= 8):
            busi_message = "Высокая загруженность парковки"

        resp = {"name": name, "car_count": count, "workload": busi_message, "video": video}
        yield render_template('index.html', resp=resp)


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <p><a href="http://localhost:5000/one-park-data">Парковка на улице Ленина</a></p>
    <p><a href="http://localhost:5000/two-park-data">Парковка на улице Анохина</a></p>
    <p><a href="http://localhost:5000/one-park-data-speed">Парковка на улице Ленина (ускоренная)</a></p>
    <p><a href="http://localhost:5000/two-park-data-speed">Парковка на улице Анохина (ускоренная)</a></p>
</body>
</html>
    '''


# видео
@app.route('/one-park')
def video_one_feed():
    return Response(gen(VideoCamera("videos/ленина ускорен.mp4"), Detector("detectors/cascade20.xml"), 1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/two-park')
def video_two_feed():
    return Response(gen(VideoCamera("videos/анохина ускорен.mp4"), Detector("detectors/cascade.xml"), 2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/one-park-data-speed')
def video_one_data_speed():
    response = gen_data(VideoCamera("videos/ленина ускорен.mp4"), Detector("detectors/cascade20.xml"), 1)

    return Response(stream_with_context(response))


@app.route('/two-park-data-speed')
def video_two_data_speed():
    response = gen_data(VideoCamera("videos/анохина ускорен.mp4"), Detector("detectors/cascade20.xml"), 2)

    return Response(stream_with_context(response))


@app.route('/one-park-data')
def video_one_data():
    response = gen_data(VideoCamera("videos/ленина.mp4"), Detector("detectors/cascade20.xml"), 1)

    return Response(stream_with_context(response))


@app.route('/two-park-data')
def video_two_data():
    response = gen_data(VideoCamera("videos/анохина.mp4"), Detector("detectors/cascade20.xml"), 2)

    return Response(stream_with_context(response))


# @app.route('/custom')
# def custom():
#     # путь до видео
#     path = request.args.get('path')
#     # путь к нейронке
#     detector = request.args.get('detector')
#     # номер парковки - 1 - Ленина, 2 - Анохина
#     park = request.args.get('park')
#     response = gen_data(VideoCamera(path), Detector(detector), park, path)
#
#     return Response(stream_with_context(response))


if __name__ == '__main__':
    app.run(host='localhost')
