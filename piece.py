from colors import Color
from shapes import *
from abc import ABC, abstractmethod

class Piece(object):

    __shape_by_number_of_squares = {
        Square: 1,
        Domino: 2,
        ThreeSquareShape: 3,
        FourSquareShape: 4,
        FiveSquareShape: 5
    }

    def __init__(self, shape, color):
        if not isinstance(color, Color):
            raise TypeError("color must be of type Color")
        self.__shape = shape
        self.__color = color

    def __eq__(self, other):
        return self.get_shape() == other.get_shape() and self.get_color() == other.get_color()

    def __str__(self):
        return f"Piece({self.get_shape()}, {self.get_color()})"

    def get_color(self):
        return self.__color
    
    def get_shape(self):
        return self.__shape

    def get_number_of_squares(self):
        return self.__shape_by_number_of_squares[type(self.get_shape())]
    

# board = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(8)]

# pieces = (

#     [[1, 1],
#      [1, 1]],

#     [[2, 0, 0],
#      [2, 0, 0],
#      [2, 2, 2]],

#     [[0, 3, 0],
#      [3, 3, 3],
#      [0, 3, 0]],

#     [[4, 4, 4, 4, 4]],
#     ...
#     )

# def rotate_piece(piece):
#     return [list(row[::-1]) for row in zip(*piece)]

# def reflect_piece(piece):
#     return [row[::-1] for row in piece]


if __name__ == "__main__":
    piece1 = Piece(Color.RED, Square())
    print(piece1.get_color())
    print(piece1.get_number_of_squares())
    print(piece1.get_shape())
    piece2 = Piece(Color.BLUE, Domino())
    print(piece2.get_color())
    print(piece2.get_number_of_squares())
    print(piece2.get_shape())
    piece3 = Piece(Color.YELLOW, ThreeSquareShape.L)
    print(piece3.get_color())
    print(piece3.get_number_of_squares())
    print(piece3.get_shape())
    piece4 = Piece(Color.GREEN, FourSquareShape.T)
    print(piece4.get_color())
    print(piece4.get_number_of_squares())
    print(piece4.get_shape())
    piece5 = Piece(Color.YELLOW, FiveSquareShape.W)
    print(piece5.get_color())
    print(piece5.get_number_of_squares())
    print(piece5.get_shape())