import cv2
from calculator import Calculator

class Detector(object):
    def __init__(self, path_to_classifier):
        self.classifier = path_to_classifier
        self.cascade = cv2.CascadeClassifier(path_to_classifier)
        self.calculator = Calculator()

    def detect(self, frames):
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        cars = self.cascade.detectMultiScale(gray, 1.1, 7)

        for (x, y, w, h) in cars:
            if (self.calculator.inPolygon(x, y, [552, 1507, 1551, 470], [485, 679, 808, 555]) > 0):
                print(f'{x} {y} {w} {h}')

                cv2.rectangle(frames, (x, y), (x + w, y + h), (72, 220, 251), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frames, 'Car', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
        return frames
