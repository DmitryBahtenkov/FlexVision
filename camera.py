import cv2


class VideoCamera(object):
    def __init__(self, path):
        self.video = cv2.VideoCapture(path)


    def __del__(self):
        self.video.release()

    def get_clear_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_detecting_frame(self, detector, num):
        success, image = self.video.read()
        detector.detect(image, num)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()