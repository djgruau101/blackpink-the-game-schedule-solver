from enum import Enum


class ConveyorDirection(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    NONE = 5


class Tile(object):

    def __init__(self, block, conveyor_direction=ConveyorDirection.NONE):
        self.__block = block  # could be None
        self.__conveyor_direction = conveyor_direction

    def clear_block(self):
        self.__block = None

    def add_block(self, block):
        self.__block = block