from board import Board

class Schedule(object):
    def __init__(self, board, conditions):
        self.__board = board
        self.__conditions = conditions