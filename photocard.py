from piece import Piece
from shapes import Square, Domino, ThreeSquareShape, FourSquareShape, FiveSquareShape
from colors import Color
from globals import Stat, stats_names, member_names

from abc import ABC, abstractmethod
from enum import Enum
import re

piece_colors = ["Green", "Yellow", "Blue", "Red"]
suits = ["Summer Trip", "Autumn Trip", "Hanok",
         "Resting", "Leisurely", "Dreamy", "Bored",
         "Fairy", "Colorful", "Princess", "Summer Photo Shoot"]  # every 1-4 star photocard's name starts with either of these strings
shapes_1_to_4_stars = [Square.SQUARE, Domino.DOMINO] + list(ThreeSquareShape) + list(FourSquareShape)

five_square_shapes_strings = ["F", "F-MIRROR", "I", "L", "L-MIRROR",
                              "N", "N-MIRROR", "P", "P-MIRROR",
                              "T", "U", "V", "W", "X",
                              "Y", "Y-MIRROR", "Z", "Z-MIRROR"]

suit_by_shape = dict(zip(suits, shapes_1_to_4_stars))  # for 1-4 star photocards, the suit of the photocard determines the shape of the piece


class FiveStarPhotocardVersion(Enum):
    BASE = 1
    LUCKY = 2


# Stats are ordered in increasing order of strength.
shape_by_base_stats = {
    Square.SQUARE: [24, 25, 25, 26],
    Domino.DOMINO: [48, 60, 60, 72],
    ThreeSquareShape.I: [67, 112, 112, 159],
    ThreeSquareShape.L: [90, 90, 126, 144],
    FourSquareShape.I: [80, 160, 240, 320],
    FourSquareShape.O: [176, 200, 200, 224],
    FourSquareShape.T: [160, 160, 200, 280],
    FourSquareShape.J: [80, 200, 240, 280],
    FourSquareShape.L: [120, 160, 200, 320],
    FourSquareShape.S: [120, 200, 200, 280],
    FourSquareShape.Z: [120, 160, 240, 280],
    FiveSquareShape.F: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.F_MIRROR: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                               FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.I: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.L: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.L_MIRROR: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                               FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.N: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.N_MIRROR: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                               FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.P: {FiveStarPhotocardVersion.BASE: [300, 360, 375, 465],
                        FiveStarPhotocardVersion.LUCKY: [550, 610, 625, 715]},
    FiveSquareShape.P_MIRROR: {FiveStarPhotocardVersion.BASE: [300, 375, 375, 450],
                               FiveStarPhotocardVersion.LUCKY: [550, 625, 625, 700]},
    FiveSquareShape.T: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.U: {FiveStarPhotocardVersion.BASE: [225, 375, 420, 480],
                        FiveStarPhotocardVersion.LUCKY: [475, 625, 670, 730]},
    FiveSquareShape.V: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},  # so far there are no photocards with this piece shape
    FiveSquareShape.W: {FiveStarPhotocardVersion.BASE: [150, 435, 450, 465],
                        FiveStarPhotocardVersion.LUCKY: [400, 685, 700, 715]},
    FiveSquareShape.X: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.Y: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.Y_MIRROR: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                               FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.Z: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                        FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
    FiveSquareShape.Z_MIRROR: {FiveStarPhotocardVersion.BASE: [75, 225, 450, 750],
                               FiveStarPhotocardVersion.LUCKY: [325, 475, 700, 1000]},
}

# They changed some of the boosts smh
# For 3-5 star photocards, boosts normally change when the levels reaches 11, 21, 31, or 41
# The boost from level 10*number_of_stars - 1 to 10*number_of_stars is unique
# For exceptional circumstances where the boost changes within a plateau,
# all boosts will be indicated and they are preceded by the amount of times they are applied.
shape_by_boosts = {
    Square.SQUARE: [[5, 5, 5, 5], [10, 10, 10, 10]],
    Domino.DOMINO: [[9, 11, 11, 13], [22, 27, 27, 32]],
    ThreeSquareShape.I: [[10, 18, 18, 25],
                         [11, 19, 19, 26],
                         [12, 20, 20, 27],
                         [18, 30, 30, 42]],
    ThreeSquareShape.L: [[14, 14, 20, 23],
                         [15, 15, 21, 24],
                         [16, 16, 22, 25],
                         [24, 24, 33, 39]],
    FourSquareShape.I: [[10, 20, 30, 40],
                        [10, 21, 32, 41],
                        [10, 21, 33, 44],
                        [(4, [11, 23, 34, 45]), (5, [12, 23, 34, 44])], # 34 to 39: +12 for weak, +44 for strong exceptionally
                        [17, 33, 48, 65]],
    FourSquareShape.O: [[22, 25, 25, 28],
                        [23, 26, 26, 29],
                        [24, 27, 27, 30],
                        [25, 28, 28, 32],
                        [35, 41, 41, 46]], # boosts are consistent
    FourSquareShape.T: [[20, 20, 25, 35],
                        [21, 21, 26, 36],
                        [22, 22, 27, 37],
                        [22, 22, 28, 41],
                        [32, 32, 41, 58]],
    FourSquareShape.J: [[10, 25, 30, 35],
                        [10, 26, 31, 37],
                        [10, 27, 33, 38],
                        [12, 29, 34, 38],
                        [17, 40, 49, 57]],
    FourSquareShape.L: [[15, 20, 25, 40],
                        [(9, [15, 20, 26, 43]), (1, [16, 20, 26, 42])], # 19 to 20: +16 for weak, +42 for strong exceptionally
                        [16, 22, 27, 43],
                        [17, 23, 29, 44],
                        [25, 33, 40, 65]],
    FourSquareShape.S: [[15, 25, 25, 35],
                        [15, 26, 26, 37],
                        [17, 27, 27, 37],
                        [17, 29, 29, 38],
                        [24, 40, 40, 59]],
    FourSquareShape.Z: [[15, 20, 30, 35],
                        [15, 21, 31, 37],
                        [16, 21, 33, 38],
                        [17, 23, 34, 39],
                        [25, 33, 48, 57]],
    FiveSquareShape.F: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.F_MIRROR: [[5, 18, 40, 70],
                               [6, 20, 42, 70],
                               [7, 22, 43, 71],
                               [8, 23, 44, 73],
                               [10, 24, 46, 74],
                               [12, 44, 81, 140]],
    FiveSquareShape.I: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.L: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.L_MIRROR:  [[5, 18, 40, 70],
                                [6, 20, 42, 70],
                                [7, 22, 43, 71],
                                [8, 23, 44, 73],
                                [10, 24, 46, 74],
                                [12, 44, 81, 140]],
    FiveSquareShape.N:  [[5, 18, 40, 70],
                         [6, 20, 42, 70],
                         [7, 22, 43, 71],
                         [8, 23, 44, 73],
                         [10, 24, 46, 74],
                         [12, 44, 81, 140]],
    FiveSquareShape.N_MIRROR:  [[5, 18, 40, 70],
                                [6, 20, 42, 70],
                                [7, 22, 43, 71],
                                [8, 23, 44, 73],
                                [10, 24, 46, 74],
                                [12, 44, 81, 140]],
    FiveSquareShape.P: [[27, 31, 33, 42],
                        [27, 33, 35, 43],
                        [29, 35, 36, 43],
                        [30, 36, 36, 46],
                        [31, 37, 38, 48],
                        [48, 64, 78, 87]],
    FiveSquareShape.P_MIRROR: [[26, 33, 33, 41],
                               [28, 34, 34, 42],
                               [28, 36, 36, 43],
                               [30, 37, 37, 44],
                               [31, 39, 39, 45],
                               [57, 69, 69, 82]],
    FiveSquareShape.T: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],   
                        [12, 44, 81, 140]],
    FiveSquareShape.U: [[18, 33, 38, 44],
                        [20, 34, 39, 45],
                        [22, 36, 40, 45],
                        [23, 37, 41, 47],
                        [24, 39, 43, 48],   
                        [44, 69, 73, 91]],
    FiveSquareShape.V: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.W: [[12, 39, 40, 42],
                        [13, 40, 42, 43],
                        [15, 42, 43, 43],
                        [15, 43, 44, 46],
                        [16, 44, 46, 48],
                        [33, 76, 81, 87]],
    FiveSquareShape.X: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.Y: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.Y_MIRROR: [[5, 18, 40, 70],
                               [6, 20, 42, 70],
                               [7, 22, 43, 71],
                               [8, 23, 44, 73],
                               [10, 24, 46, 74],
                               [12, 44, 81, 140]],
    FiveSquareShape.Z: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.Z_MIRROR: [[5, 18, 40, 70],
                               [6, 20, 42, 70],
                               [7, 22, 43, 71],
                               [8, 23, 44, 73],
                               [10, 24, 46, 74],
                               [12, 44, 81, 140]],
}

# May 2024 update: limit break allows 1-4 star photocards to be levelled up 10 levels higher
# December 2024 update: limit break applied to 5-star photocards
# For 1-4 star photocards, first and second boosts are applied 4 times, the last two only once



# 5-star photocards limit break (every boost is for every level):
# F:        [8, 25, 48, 80], [8, 24, 49, 80]
# F-MIRROR: [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# I:
# L:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# L-MIRROR: [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158] 
# N:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# N-MIRROR:
# P:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84]
# P-MIRROR: [32, 41, 41, 47], [32, 40, 40, 49], [33, 40, 40, 48], [31, 41, 41, 48], [34, 42, 42, 51], [34, 42, 42, 51], [34, 42, 42, 51], [33, 43, 43, 50]
# T:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# U:        [24, 41, 45, 51], [25, 40, 45, 51], [24, 40, 45, 52], [24, 41, 45, 51], [25, 42, 48, 54], [26, 42, 47, 54], [25, 42, 47, 55], [25, 43, 48, 53], [26, 42, 47, 54], [47, 79, 88, 102]
# V:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# W:        [16, 47, 48, 50], [16, 47, 49, 49], [16, 47, 48, 50], [16, 46, 48, 51], [17, 49, 51, 52], [17, 49, 51, 52], [17, 49, 50, 53], [17, 49, 51, 52]
# X:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# Y:
# Y-MIRROR: [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# Z:        [8, 25, 48, 80], [8, 24, 49, 80], [8, 24, 48, 81], [9, 24, 48, 80], [8, 25, 51, 85], [8, 26, 51, 84], [9, 25, 50, 85], [8, 26, 51, 84], [8, 25, 51, 85], [16, 47, 95, 158]
# Z-MIRROR:

# For 4-star photocards for example:
# Boost 1 is applied from level 40 to 44
# Boost 2 is applied from level 44 to 48
# Boost 3 is applied from level 48 to 49
# Boost 4 is applied from level 49 to 50
# The boosts filled with 0s are the ones I haven't found yet (gotta farm stardust and dream puzzles!)
# I still need to find the pattern in the boosts for 5-star photocards
shape_by_boosts_limit_break = {
    Square.SQUARE: [[5, 5, 5, 6], [5, 6, 6, 5], [5, 5, 5, 7], [11, 12, 12, 11]],  # ALL GOOD!
    Domino.DOMINO: [[9, 12, 12, 13], [10, 12, 12, 14], [10, 12, 12, 14], [24, 30, 30, 37]],
    ThreeSquareShape.I: [[12, 21, 21, 28], [13, 22, 22, 29], [14, 23, 23, 30], [21, 35, 35, 47]],
    ThreeSquareShape.L: [[16, 16, 23, 27], [17, 17, 24, 28], [18, 18, 25, 29], [28, 28, 39, 43]],
    FourSquareShape.I: [[12, 24, 36, 46], [13, 25, 38, 48], [13, 25, 38, 49], [19, 37, 57, 74]],
    FourSquareShape.O: [[26, 30, 30, 32], [27, 31, 31, 35], [28, 31, 31, 35], [41, 47, 47, 52]],
    FourSquareShape.T: [[23, 23, 29, 43], [24, 24, 31, 45], [25, 25, 31, 44], [37, 37, 46, 67]],
    FourSquareShape.J: [[12, 30, 36, 40], [13, 31, 38, 42], [13, 32, 38, 42], [19, 47, 57, 64]],
    FourSquareShape.L: [[18, 24, 30, 46], [19, 25, 31, 49], [19, 25, 32, 49], [29, 37, 47, 74]],
    FourSquareShape.S: [[17, 29, 29, 43], [18, 31, 31, 44], [18, 31, 31, 45], [28, 46, 46, 67]],
    FourSquareShape.Z: [[18, 24, 35, 41], [19, 25, 37, 43], [19, 25, 37, 44], [29, 37, 56, 65]],
    FiveSquareShape.F: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.F_MIRROR: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.I: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.L: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.L_MIRROR: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.N: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.N_MIRROR: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.P: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.P_MIRROR: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.T: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.U: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.V: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.W: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.X: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.Y: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.Y_MIRROR: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.Z: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    FiveSquareShape.Z_MIRROR: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
}


class Photocard(ABC):

    def __init__(self, name, level, piece_shape, piece_color):
        self.__member_name = self.check_member_name(name) # Get name of the Blackpink member
        self.__photocard_name = name
        self.__piece = Piece(piece_shape, piece_color)
        self.__max_level_before_limit_break = 10 * self.get_stars()
        self.__base_points = self._get_base_stats()
        self.__boosts = [self.rearranged_points_list(lst, piece_color.value) if isinstance(lst[0], int)
                         else [(tup[0], self.rearranged_points_list(tup[1], piece_color.value)) for tup in lst]
                         for lst in shape_by_boosts[piece_shape].copy()]
        if level not in range(1, self.get_max_level() + 1):
            raise ValueError(f"this photocard's level must be between 1 to {self.get_max_level()}")
        self.__level = level
        self._stats = self.calculate_stats(level)

    @abstractmethod
    def _get_base_stats(self):
        """Returns the stats of the photocard at level 1."""
        pass

    @staticmethod
    def check_member_name(name):
        """Checks if the name of the photocard is valid.
        It is valid only if it contains the name of exactly one Blackpink member.
        Returns the name of the Blackpink member if valid, raise ValueError otherwise."""

        # test if exactly one member name is in the photocard name
        member_name_set = set([word.strip("'s") for word in name.split(" ")]).intersection(member_names)
        if len(member_name_set) != 1:
            raise ValueError("name of the photocard must contain the name of exactly one Blackpink member")
        return member_name_set.pop()
    
    @staticmethod
    def rearranged_points_list(lst, n):
        """Takes the list containing the scores of the stats (originally in increasing order) and returns
        an adjusted verison of it where each score correspond to its respective stat.
        The first stat is for music (green), the second stat is for acting (yellow),
        the third stat is for fashion (blue) and the last stat is for charm (red)."""
        nb_colors = len(Color)
        return lst[-1 * n % nb_colors:] + lst[:-1 * n % nb_colors]
    
    @staticmethod
    def updated_score(points, boosts, level_increase=1):
        """Both points and boosts are iterables containing 4 integers.
        level_increase is an integer from 1 to 10.
        Returns an updated list of points where each stat's score
        is added by the boost times the level_increase."""
        total_boosts = [boost*level_increase for boost in boosts]
        return [sum(pair) for pair in zip(points, total_boosts)]
    
    def calculate_stats(self, level):
        """Takes the level of a photocard, calculates the score for each stat when the photocard is at said level
        and returns a dictionary consisting of (stat: score) pairs."""
         # 1-2 stars: boost from max_level-1 to max_level is different than for all other levels
        if level > self.get_max_level():
            raise ValueError(f"level must be between 1 and {self.get_max_level()} inclusively")
        points = self.__base_points.copy()
        # Limit break boosts for 1 to 4-star photocards
        if self.get_stars() < 5 and level > self.__max_level_before_limit_break:
            piece_color_value = self.get_piece().get_color().value
            piece_shape = self.get_piece().get_shape()
            limit_break_boosts = [self.rearranged_points_list(lst, piece_color_value) for lst in shape_by_boosts_limit_break[piece_shape].copy()]
            limit_break_increase = level - self.__max_level_before_limit_break
            level = self.__max_level_before_limit_break
            for i in range(4):
                # The first and second one are applied at most 4 times, the last two are applied at most once.
                upper_bound = 4 if i <= 1 else 1
                level_increase_for_current_boost = min(limit_break_increase, upper_bound)
                points = self.updated_score(points, limit_break_boosts[i], level_increase_for_current_boost)
                limit_break_increase -= level_increase_for_current_boost
        if self.get_stars() <= 2:
            # regular boost will be applied when levelling up to anywhere from 2 to the second-to-last level
            number_of_boosts = min(level - 1, self.__max_level_before_limit_break - 2)
            points = self.updated_score(points, self.__boosts[0], number_of_boosts)
            if level == self.__max_level_before_limit_break:
                points = self.updated_score(points, self.__boosts[1])
        else:
            # Boosts change at every 10 levels
            last_boost_index = (level - 1) // 10
            if level == self.__max_level_before_limit_break:
                last_boost_index += 1
            remaining_level_increase = level - 1  # We add to the level 1 stats which are already defined above
            for i in range(last_boost_index + 1):
                # This implementation works but there could be an easier one!
                max_level_increase_for_current_boost = 9 if i in [0, len(self.__boosts) - 2] else (1 if i == len(self.__boosts) - 1 else 10)
                level_increase_for_current_boost = min(remaining_level_increase, max_level_increase_for_current_boost)
                if isinstance(self.__boosts[i][0], tuple):  # The boost changes within the plateau for some stupid reason
                    for frequency_and_boost in self.__boosts[i]:
                        (frequency, boost) = frequency_and_boost
                        actual_frequency = min(frequency, level_increase_for_current_boost)
                        points = self.updated_score(points, boost, actual_frequency)
                        remaining_level_increase -= actual_frequency
                else:
                    points = self.updated_score(points, self.__boosts[i], level_increase_for_current_boost)
                    remaining_level_increase -= level_increase_for_current_boost
        return dict(zip(Stat, points))
    
    def base_total_score(self):
        """Returns the sum of all stats from the photocard"""
        return sum(self.get_stats().values())
    
    def __repr__(self):
        return f"Photocard(name={self.get_photocard_name()}, level={self.get_level()}, Piece={self.get_piece()})"

    def __str__(self):
        return f"Photocard with name={self.get_photocard_name()}, level={self.get_level()}, Piece={self.get_piece()}"
    
    def get_photocard_name(self):
        return self.__photocard_name
    
    def get_member_name(self):
        return self.__member_name
    
    def get_piece(self):
        return self.__piece

    def get_piece_shape(self):
        return self.get_piece().get_shape()
    
    def get_piece_color(self):
        return self.get_piece().get_color()
    
    def get_stars(self):
        return self.get_piece().get_number_of_squares()
    
    @abstractmethod
    def get_max_level(self):
        pass
    
    def get_level(self):
        return self.__level

    def set_level(self, level):
        if level not in range(1, self.get_max_level() + 1):
            raise ValueError(f"level of this photocard must range from 1 to {self.get_max_level()}")
        self.__level = level
        self._stats = self.calculate_stats(level)  # not the most optimal way to change points

    def level_up(self):
        if not self.is_max_level():
            self.__level += 1
            self._stats = self.calculate_stats(self.get_level())  # not the most optimal way to change points

    def set_to_max_level(self):
        self.__level = self.get_max_level()
        self._stats = self.calculate_stats(self.get_level())  # not the most optimal way to change points

    def is_max_level(self):
        return self.get_level() == self.get_max_level()

    def get_stats(self):
        return self._stats.copy()
    
    def display_photocard_info(self):
        print(self.get_photocard_name(), self.get_stars()*"☆")
        print(f"LV. {self.get_level()}")
        print("|".join([f"{stats_names[stat.value - 1]}: {point}" for stat, point in self.get_stats().items()]))
        print(f"Piece: {self.get_piece_shape()} {self.get_piece_color()}")


class Photocard1to4Stars(Photocard):
    """For 1-4 star photocards, the shape of the piece is solely dictated by the name of the photocard."""

    def __init__(self, name, level):
        suit, color_number = [values.strip() for values in name.split(self.check_member_name(name))]
        if suit not in suit_by_shape.keys():
            raise ValueError(f"name for a 1-4 star photocard should start with either of the following:\n{', '.join(suit_by_shape.keys())}")
        if not re.match(r"#[1-4]", color_number):
            raise ValueError("end of the photocard name must end with '#' followed by a number from 1 to 4")
        color_number = int(color_number[1])  # the first character is '#'
        piece_color = None
        for color in Color:  # find color
            if color.value == color_number:
                piece_color = color
                break
        super().__init__(name, level, suit_by_shape[suit], piece_color)
        
    def __eq__(self, other):
        if isinstance(other, Photocard1to4Stars):
            return self.get_piece() == other.get_piece() and self.get_member_name() == self.get_member_name()
        else:
            return False
    
    def _get_base_stats(self):
        return self.rearranged_points_list(shape_by_base_stats[self.get_piece_shape()].copy(), self.get_piece_color().value)

    def get_max_level(self):
        """The maximum level of a 1 to 4-star photocard used to be 10 * number of stars.
        Since the May 2024 update, the maximum level of 1 to 4-star photocards is increased by 10."""
        return 10 * self.get_stars() + 10

class Photocard5Stars(Photocard):

    __signature_boosts = [0, 100, 210, 330, 470, 650]
    __trendy_up_boosts = [0, 35, 85, 175]
    __MAX_SIGNATURE = 5
    __MAX_TRENDY_UP = 3
    __trendy_up_by_min_level = {0: 1, 1: 10, 2: 15, 3: 20}

    def __init__(self, name, level, piece_shape, piece_color, signature, trendy_up):
        if signature > self.__MAX_SIGNATURE:
            raise ValueError("Signature value must be from 0 to 5")
        if trendy_up > self.__MAX_TRENDY_UP:
            raise ValueError("Trendy Up value must be from 0 to 3")
        if level < self.__trendy_up_by_min_level[trendy_up]:
            raise ValueError(f"Trendy Up {trendy_up} is only possible from level {self.__trendy_up_by_min_level[trendy_up]}")
        if not isinstance(piece_shape, FiveSquareShape):
            raise ValueError("piece_shape must be a FiveSquareShape")
        self.__version = FiveStarPhotocardVersion.LUCKY if name.startswith("Lucky ") else FiveStarPhotocardVersion.BASE
        super().__init__(name, level, piece_shape, piece_color)
        self.__signature = signature
        self.__trendy_up = trendy_up
        self.__boost_stats(self.__signature_boosts[signature] + self.__trendy_up_boosts[trendy_up])

    def __eq__(self, other):
        if isinstance(other, Photocard5Stars):
            return self.get_piece() == other.get_piece() and self.get_photocard_name() == other.get_photocard_name
        else:
            return False
        
    def _get_base_stats(self):
        """Returns the stats of the photocard at level 1."""
        return self.rearranged_points_list(shape_by_base_stats[self.get_piece_shape()][self.get_photocard_version()].copy(),
                                           self.get_piece_color().value)

    def __repr__(self):
        return super().__repr__() + f", signature={self.get_signature()}, trendy_up={self.get_trendy_up()})"

    def __str__(self):
        return super().__str__() + f", signature={self.get_signature()}, trendy_up={self.get_trendy_up()})"

    def __boost_stats(self, points):
        """Takes a number of points and increases each stat by that number of points."""
        for stat in self._stats:
            self._stats[stat] += points

    def set_level(self, level):
        # Set highest possible trendy up for the new level
        if level < self.get_level():
            new_trendy_up = 0
            for trendy_up in range(3, -1, -1):
                if level >= self.__trendy_up_by_min_level[trendy_up]:
                    new_trendy_up = trendy_up
                    break
            if new_trendy_up != self.get_trendy_up():
                print(f"Trendy Up set to {new_trendy_up} as the new level is under {self.__trendy_up_by_min_level[new_trendy_up]}")
            self.set_trendy_up(new_trendy_up)
        super().set_level(level)
        self.__boost_stats(self.__signature_boosts[self.get_signature()] +
                           self.__trendy_up_boosts[self.get_trendy_up()])
        
    def level_up(self):
        super().level_up()
        self.__boost_stats(self.__signature_boosts[self.get_signature()] +
                           self.__trendy_up_boosts[self.get_trendy_up()])
        
    def get_max_level(self):
        return 10 * self.get_stars()
        
    def set_to_max_level(self):
        super().set_to_max_level()
        self.__boost_stats(self.__signature_boosts[self.get_signature()] +
                           self.__trendy_up_boosts[self.get_trendy_up()])

    def get_signature(self):
        return self.__signature

    def get_trendy_up(self):
        return self.__trendy_up
    
    def set_signature(self, signature):
        if signature not in range(len(self.__signature_boosts)):
            print("Signature value must be from 0 to 5")
        else:
            old_signature = self.__signature
            self.__signature = signature
            self.__boost_stats(self.__signature_boosts[signature] - self.__signature_boosts[old_signature])

    def set_trendy_up(self, trendy_up):
        if trendy_up not in range(len(self.__trendy_up_boosts)):
            print("Trendy Up value must be from 0 to 3")
        else:
            old_trendy_up = self.__trendy_up
            self.__trendy_up = trendy_up
            self.__boost_stats(self.__trendy_up_boosts[trendy_up] - self.__trendy_up_boosts[old_trendy_up])

    def add_signature(self):
        if self.is_max_signature():
            print("Signature is at its maximum level, which is 5")
            return
        self.set_signature(self.get_signature() + 1)
    
    def add_trendy_up(self):
        if self.is_max_trendy_up():
            print("Trendy Up is at its maximum level, which is 3")
            return
        self.set_trendy_up(self.get_trendy_up() + 1)

    def set_to_max_signature(self):
        self.set_signature(self.__MAX_SIGNATURE)
    
    def is_max_signature(self):
        return self.get_signature() == self.__MAX_SIGNATURE
    
    def set_to_max_trendy_up(self):
        self.set_trendy_up(self.__MAX_TRENDY_UP)
    
    def is_max_trendy_up(self):
        return self.get_trendy_up() == self.__MAX_TRENDY_UP

    def get_photocard_version(self):
        return self.__version
    
    def is_lucky(self):
        return self.__version == FiveStarPhotocardVersion.LUCKY
    
    def display_photocard_info(self):
        super().display_photocard_info()
        print(f"Signature: {self.get_signature()}")
        print(f"Trendy Up: {self.get_trendy_up()}")


if __name__ == "__main__":
    card = Photocard1to4Stars("Leisurely JENNIE #4", 37)
    card.set_to_max_level()
    card.display_photocard_info()
    card = Photocard5Stars("Christmas Eve JISOO", 25, FiveSquareShape.X, Color.GREEN, 0, 3)
    card.set_level(1)
    card.display_photocard_info()
    card = Photocard5Stars("Lucky LISA's Vanity", 50, FiveSquareShape.T, Color.RED, 4, 3)
    card.display_photocard_info()