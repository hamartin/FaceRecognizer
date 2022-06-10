'''
This file represents the device we are grabbing pictures from.

A lot/most of the code here was taken from the following places.
  - https://www.programcreek.com/python/?code=RedisGears%2FEdgeRealtimeVideoAnalytics%2FEdgeRealtimeVideoAnalytics-master%2Fapp%2Fcapture.py
'''


import time

import cv2

from .simplemovingaverage import SimpleMovingAverage


class VideoCapture:

    '''This class represents the devicee we are grabbing pictures from.'''

    def __init__(self, device, fps=30.0):
        # Note that device can be both a device ID and a FQPN to a file/device.
        self._device = device
        self._fps = fps
        self._count = 0
        self._ts = time.time()

        # Initialize the capture device itself and extract some settings.
        self._cap = cv2.VideoCapture(self._device)
        if not self._cap.isOpened():
            raise ValueError("Error opening video capture device.")
        self._lenght = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = self._cap.get(cv2.CAP_PROP_FPS)

        # If the device is an ID, do some initial setting up.
        self._isFile = not str(self._device).isdecimal()
        if not self._isFile:
            self._cap.set(cv2.CAP_PROP_FPS, self._fps)
        else:
            self._fps = self._cap.get(cv2.CAP_PROP_FPS)
            self._sma = SimpleMovingAverage(value=0.1, count=19)

    def __repr__(self):
        return "VideoCapture(device={0})".format(self._device)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        self._count = -1
        return self

    def __next__(self):
        self._count += 1

        # Respect the FPS for files.
        if self._isFile:
            delta = time.time() - time._ts
            self._sma.add(delta)
            time.sleep(max(0, (1.0 - self._sma.getCurrent()*self._fps)/self._fps))
            self._ts = time.time()

        # Get the frame from the input device.
        ret, frame = self._cap.read()
        if not ret:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self._cap.read()
        if not ret:
            raise RuntimeError("Error fetching frame from capture device.")

        # Preprocess the frame.
        # Assuming the frame comes from a webcamera.
        frame = cv2.flip(frame, 1)

        return self._count, frame

    def __exit__(self, exc_type, exc_value, traceback):
        self._cap.release()
        # This is only necessary if we have created a window and are displaying our grabbed frame 
        cv2.destroyAllWindows()
