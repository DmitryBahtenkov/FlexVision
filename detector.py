import cv2
from calculator import Calculator
import numpy as np

THRESHHOLD = 0.25
parking_place = np.array([
    [1294, 638, 1460, 792],
    [1166, 614, 1336, 769],
    [1063, 590, 1182, 732],
    [969, 568, 1074, 697],
    [873, 554, 972, 679],
    [781, 538, 871, 654],
    [720, 518, 788, 634],
    [661, 509, 713, 615],
    [604, 495, 652, 597],
    [567, 490, 569, 577],
])

def countIou(bboxes1, bboxes2):
    if not bboxes1.any() or not bboxes2.any():
        return [[]]
    x11, y11, x12, y12 = np.split(bboxes1, 4, axis=1)
    x21, y21, x22, y22 = np.split(bboxes2, 4, axis=1)

    xA = np.maximum(x11, np.transpose(x21))
    yA = np.maximum(y11, np.transpose(y21))
    xB = np.minimum(x12, np.transpose(x22))
    yB = np.minimum(y12, np.transpose(y22))
    interArea = np.maximum((xB - xA + 1), 0) * np.maximum((yB - yA + 1), 0)
    boxAArea = (x12 - x11 + 1) * (y12 - y11 + 1)
    boxBArea = (x22 - x21 + 1) * (y22 - y21 + 1)
    iou = interArea / (boxAArea + np.transpose(boxBArea) - interArea)
    return iou

class Detector(object):
    def __init__(self, path_to_classifier):
        self.classifier = path_to_classifier
        self.cascade = cv2.CascadeClassifier(path_to_classifier)
        self.calculator = Calculator()

    def detect(self, frames, num):
        if(num == 1):
            return self.detect_one_alternate(frames)
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

        return frames, busi_places

    def detect_one_alternate(self, frames):
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(25, 25)
        )

        # Массив координат всех найденных автомобилей
        car_places = []

        for (x, y, w, h) in faces:
            if (self.calculator.inPolygon(x + (w / 2), y + (h / 2), [552, 1507, 1551, 470], [485, 679, 808, 555]) > 0):
                # Рисуем квадраты вокруг лиц
                cv2.rectangle(frames, (x, y), (x + w, y + h), (255, 255, 0), 2)
                 # Заполняем массив
                car_places.append([x, y, x + w, y + h])

        # Вычиление пересечений, итог - двумерный массив
        places = countIou(parking_place, np.array(car_places))
        # Счетчик занятых мест
        busi_places = 0
        for p in places:
            if len(p) == 0:
                continue
            if np.max(p) > THRESHHOLD:
                busi_places += 1

        return frames, busi_places