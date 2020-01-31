"""Navigation Controller Module"""
from enum import Enum


class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class NavControl:
    """Control navigation requests.

        To subscribe pass your callback function to subscribe()
        Your callback function should accept a direction and a distance.

        If an invalid direction is passed in a ValueError will be raised.

        go() is the public function called to effect navigation.
        If go() is called without arguments, it will repeat the last
        direction and distance. If it is called without a distance it will
        repeat the last distance. And if it is called without a direction
        it will repeat the last direction. If you want to call with a distance
        but no direction, you must do so with named argument for your distance.
    """

    def __init__(self):
        self.callbacks = set()
        self.distance = 1
        self.direction = Directions.NORTH

    def subscribe(self, callback):
        self.callbacks.add(callback)

    def unsubscribe(self, callback):
        self.callbacks.remove(callback)

    def _notify(self):
        # print("NAV", self.direction, self.distance)
        for callback in self.callbacks:
            callback(self.direction, self.distance)

    def go(self, direction: Directions = None, distance: int = None):
        if direction is not None:
            if isinstance(direction, Directions):
                self.direction = direction
            else:
                raise ValueError("Direction must a value of Directions")

        if distance is not None:
            if distance != 0:
                self.distance = distance
            else:
                raise ValueError("Distance can not be 0")

        self._notify()
