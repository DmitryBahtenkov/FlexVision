import cv2
from calculator import Calculator

class Detector(object):
    def __init__(self, path_to_classifier):
        self.classifier = path_to_classifier
        self.cascade = cv2.CascadeClassifier(path_to_classifier)
        self.calculator = Calculator()

    def detect(self, frames, num):
        if(num == 1):
            return self.detect_one(frames)
        if(num == 2):
            return self.detect_two(frames)

    def detect_one(self, frames):
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        cars = self.cascade.detectMultiScale(gray, 1.1, 7)

        for (x, y, w, h) in cars:
            if (self.calculator.inPolygon(x, y, [552, 1507, 1551, 470], [485, 679, 808, 555]) > 0):
                print(f'{x} {y} {w} {h}')

                cv2.rectangle(frames, (x, y), (x + w, y + h), (72, 220, 251), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frames, 'Car', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
        return frames

    def detect_two(self, frames):
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(25, 25)
        )
        busi_places = 0
        # Рисуем квадраты вокруг лиц
        for (x, y, w, h) in faces:
            if w < 200 or h < 200:
                if (self.calculator.inPolygon(x + (w / 2), y + (h / 2), [130, 1215, 1100, 97], [365, 679, 787, 393]) > 0):
                    cv2.rectangle(frames, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    busi_places += 1
        if busi_places <= 3:
            print('Низкая заруженность')
        if 3 < busi_places <= 9:
            print('Средняя заруженность')
        if busi_places > 9:
            print('Высокая заруженность')

        return frames