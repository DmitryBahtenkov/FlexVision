import cv2


class Detector(object):
    def __init__(self, path_to_classifier):
        self.classifier = path_to_classifier
        self.cascade = cv2.CascadeClassifier(path_to_classifier)

    def detect(self, frames):
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        cars = self.cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in cars:
            if (1511 > x > 490 and 812 > y > 496):
                print(f'{x} {y} {w} {h}')
                cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frames, 'Car', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
        return frames
