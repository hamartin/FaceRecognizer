'''
This file represents the Simple Moving Average used to keep track of FPS.

A lot/most of the code here was taken from the following places.
  - https://www.programcreek.com/python/?code=RedisGears%2FEdgeRealtimeVideoAnalytics%2FEdgeRealtimeVideoAnalytics-master%2Fapp%2Fcapture.py
'''


class SimpleMovingAverage():

    '''This class represents the Simple Moving Average used to keep track of FPS.'''

    def __init__(self, value=0.0, count=7):
        self._count = int(count)
        self._current = float(value)
        self._samples = [self._current] * self._count

    def __str__(self):
        return str(round(self._current, 3))

    def __repr__(self):
        return "SimpleMovingAverage(value={0}, count={1})".format(self._current, self._count)

    def add(self, value):
        '''Adds value to the moving average and removes value going out of the moving average field.'''
        v = float(value)
        self._samples.insert(0, v)
        o = self._samples.pop()
        self._current = self._current + (v-o)/self._count

    def getCurrent(self):
        '''Returns the current value.'''
        return self._current
