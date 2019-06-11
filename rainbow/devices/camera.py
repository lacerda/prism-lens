"""
Yields inputs from a sensor
"""

from .common import Device

import cv2


PROPERTY_WIDTH = 3
PROPERTY_HEIGHT = 4

class Camera(Device):
    def __init__(self, index=0):
        self.index = 0
        self.cap = cv2.VideoCapture(index)

    def set_resolution(self, width, height):
        self.cap.set(PROPERTY_WIDTH, width)
        self.cap.set(PROPERTY_HEIGHT, height)
        return self.get_resolution()

    def get_resolution(self):
        width, height = self.cap.get(PROPERTY_WIDTH), self.cap.get(PROPERTY_HEIGHT)
        return width, height

    def __next__(self):
        im = self.cap.read()
        return im[1]

    def __del__(self):
        self.cap.release()