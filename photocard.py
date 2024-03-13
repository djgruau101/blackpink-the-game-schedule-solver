from piece import Piece
from shapes import Square, Domino, ThreeSquareShape, FourSquareShape, FiveSquareShape
from colors import Color

from enum import Enum
from abc import ABC, abstractmethod
import re

stats_names = ["music", "acting", "fashion", "charm"]
member_names = ["JISOO", "JENNIE", "ROSÉ", "LISA"]
suit_by_shape = {  # for 1-4 star cards, the suit of the photocard determines the shape of the piece
    "Summer Trip": Square.SQUARE, # 1 square
    "Autumn Trip": Domino.DOMINO, # 2 squares
    "Resting": ThreeSquareShape.L,
    "Hanok": ThreeSquareShape.I,
    "Leisurely": FourSquareShape.I,
    "Dreamy": FourSquareShape.O,
    "Bored": FourSquareShape.T,
    "Fairy": FourSquareShape.J,
    "Colorful": FourSquareShape.L,
    "Princess": FourSquareShape.S,
    "Summer Photo Shoot": FourSquareShape.Z,
}

# I don't know the base stats for every shape yet
# Stats are ordered in increasing order of strength
shape_by_base_stats = {  # for 1-4 star cards, the suit of the photocard determines the shape of the piece
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
    FiveSquareShape.F: [0, 0, 0, 0],
    FiveSquareShape.F_MIRROR: [75, 225, 450, 750],
    FiveSquareShape.I: [0, 0, 0, 0],
    FiveSquareShape.L: [0, 0, 0, 0],
    FiveSquareShape.L_MIRROR: [0, 0, 0, 0],
    FiveSquareShape.N: [75, 225, 450, 750],
    FiveSquareShape.N_MIRROR: [75, 225, 450, 750],
    FiveSquareShape.P: [0, 0, 0, 0],
    FiveSquareShape.P_MIRROR: [300, 375, 375, 450],
    FiveSquareShape.T: [75, 225, 450, 750],
    FiveSquareShape.U: [225, 375, 420, 480],
    FiveSquareShape.V: [0, 0, 0, 0],
    FiveSquareShape.W: [150, 435, 450, 465],
    FiveSquareShape.X: [75, 225, 450, 750],
    FiveSquareShape.Y: [0, 0, 0, 0],
    FiveSquareShape.Y_MIRROR: [0, 0, 0, 0],
    FiveSquareShape.Z: [0, 0, 0, 0],
    FiveSquareShape.Z_MIRROR: [0, 0, 0, 0],
}

shape_by_boosts = {
    Square.SQUARE: [[5, 5, 5, 5], [10, 10, 10, 10]],
    Domino.DOMINO: [[9, 11, 11, 13], [22, 27, 27, 32]],
    ThreeSquareShape.I: [[10, 18, 18, 25],
                         [11, 19, 19, 26],
                         [12, 20, 20, 27],
                         [25, 23, 23, 49]],
    ThreeSquareShape.L: [[14, 20, 20, 23],
                         [15, 21, 21, 24],
                         [16, 22, 22, 25],
                         [24, 33, 33, 39]],
    FourSquareShape.I: [[9, 20, 31, 40],
                        [9, 21, 32, 42],
                        [11, 21, 33, 43],
                        [13, 23, 32, 45],
                        [22, 33, 43, 65]],
    FourSquareShape.O: [[22, 25, 25, 28],
                        [23, 26, 26, 29],
                        [24, 27, 27, 30],
                        [25, 28, 28, 32],
                        [31, 43, 43, 46]],
    FourSquareShape.T: [[20, 20, 25, 35],
                        [21, 21, 26, 36],
                        [22, 22, 26, 38],
                        [22, 22, 29, 40],
                        [32, 32, 44, 55]],
    FourSquareShape.J: [[10, 25, 30, 35],
                        [10, 27, 31, 36],
                        [10, 27, 33, 38],
                        [12, 28, 34, 39],
                        [22, 33, 44, 64]],
    FourSquareShape.L: [[14, 20, 26, 40],
                        [16, 20, 26, 42],
                        [16, 22, 27, 43],
                        [18, 23, 28, 44],
                        [22, 33, 34, 74]],
    FourSquareShape.S: [[15, 25, 25, 35],
                        [15, 26, 26, 37],
                        [17, 27, 27, 37],
                        [17, 29, 29, 38],
                        [22, 34, 34, 73]],
    FourSquareShape.Z: [[15, 20, 30, 35],
                        [15, 21, 31, 37],
                        [16, 21, 33, 38],
                        [18, 23, 34, 38],
                        [23, 33, 44, 63]],
    FiveSquareShape.F: [[],
                        [],
                        [],
                        [],
                        [],
                        []],
    FiveSquareShape.F_MIRROR: [[5, 18, 40, 70],
                               [6, 20, 42, 70],
                               [7, 22, 43, 71],
                               [8, 23, 44, 73],
                               [10, 24, 46, 74],
                               []],
    FiveSquareShape.I: [[],
                        [],
                        [],
                        [],
                        [],
                        []],
    FiveSquareShape.L: [[],
                        [],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        [12, 44, 81, 140]],
    FiveSquareShape.L_MIRROR:  [[],
                                [],
                                [],
                                [],
                                [],
                                []],
    FiveSquareShape.N:  [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [],
                        [],
                        []],
    FiveSquareShape.N_MIRROR:  [[5, 18, 40, 70],
                                [6, 20, 42, 70],
                                [7, 22, 43, 71],
                                [8, 23, 44, 73],
                                [10, 24, 46, 74],
                                []],
    FiveSquareShape.P: [[],
                        [],
                        [29, 35, 36, 43],
                        [30, 36, 36, 46],
                        [31, 37, 38, 48],
                        [48, 64, 78, 87]],
    FiveSquareShape.P_MIRROR: [[26, 33, 33, 41],
                               [28, 34, 34, 42],
                               [28, 36, 36, 43],
                               [30, 37, 37, 44],
                               [31, 39, 39, 45],
                               []],
    FiveSquareShape.T: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],   
                        []],
    FiveSquareShape.U: [[18, 33, 38, 44],
                        [20, 34, 39, 45],
                        [22, 36, 40, 45],
                        [23, 37, 41, 47],
                        [24, 39, 43, 48],   
                        []],
    FiveSquareShape.V: [[],
                        [],
                        [],
                        [],
                        [],
                        []],
    FiveSquareShape.W: [[12, 39, 40, 42],
                        [13, 40, 42, 43],
                        [15, 42, 43, 43],
                        [15, 43, 44, 46],
                        [],
                        []],
    FiveSquareShape.X: [[5, 18, 40, 70],
                        [6, 20, 42, 70],
                        [7, 22, 43, 71],
                        [8, 23, 44, 73],
                        [10, 24, 46, 74],
                        []],
    FiveSquareShape.Y: [[],
                        [],
                        [],
                        [],
                        [],
                        []],
    FiveSquareShape.Y_MIRROR: [[],
                               [],
                               [],
                               [],
                               [],
                               []],
    FiveSquareShape.Z: [[],
                        [],
                        [],
                        [],
                        [],
                        []],
    FiveSquareShape.Z_MIRROR: [[],
                               [],
                               [],
                               [],
                               [],
                               []],
}


class Stat(Enum):
    MUSIC: 1
    ACTING: 2
    FASHION: 3
    CHARM: 4


# One subclass for 1-4 stars, one subclass for 5 stars (since only them have trendy up and signature functionality)

class Photocard(ABC):

    def __init__(self, name, level, piece_shape, piece_color):
        self.__member_name = self.check_member_name(name) # Get name of the Blackpink member
        self.__photocard_name = name
        self.__piece = Piece(piece_shape, piece_color)
        points = self.rearranged_points_list(shape_by_base_stats[piece_shape].copy(), piece_color.value)
        boosts = [self.rearranged_points_list(lst, piece_color.value) for lst in shape_by_boosts[piece_shape].copy()]
        if level > self.get_max_level():
            raise ValueError(f"This photocard cannot exceed level {self.get_max_level()}")
        self.__level = level      
        # 2 stars or less: boost from max_level-1 to max_level is different than for all other levels
        if self.get_stars() <= 2:
            # regular boost will be applied when levelling up to anywhere from 2 to the second-to-last level
            number_of_boosts = min(level - 1, self.get_max_level() - 2)
            for _ in range(number_of_boosts):
                points = [sum(pair) for pair in zip(points, boosts[0])]
            if level == self.get_max_level():
                points = [sum(pair) for pair in zip(points, boosts[1])]

        self.__stats = dict()

    @staticmethod
    def check_member_name(name):
        """Checks if the name of the photocard is valid.
        It is valid only if it contains the name of exactly one Blackpink member.
        Returns the name of the Blackpink member if valid."""
        member_name_set = set([word.strip("'s") for word in name.split(" ")]).intersection(member_names)  # test if exactly one member name is in the photocard name
        if len(member_name_set) != 1:
            raise ValueError("Name of the photocard must contain the name of exactly one Blackpink member")
        return member_name_set.pop()
    
    @staticmethod
    def rearranged_points_list(lst, n):
        """Takes the list containing the scores of the stats (originally in increasing order) and returns
        an adjusted verison of it where each score correspond to its respective stat.
        The first stat is for music (green), the second stat is for acting (yellow),
        the third stat is for fashion (blue) and the last stat is for charm (red)."""
        return lst[-1 * n % len(Color):] + lst[:-1 * n % len(Color)]
    
    @staticmethod
    def updated_score(points, boosts):
        """Both points and boosts are iterables containing 4 integers.
        Returns an updated list of points where each stat's score
        is added by the boost."""
        return [sum(pair) for pair in zip(points, boosts)]
    
    def get_photocard_name(self):
        return self.__photocard_name
    
    def get_member_name(self):
        return self.__member_name
    
    def get_piece(self):
        return self.__piece

    def get_piece_shape(self):
        return self.get_piece().get_shape()
    
    def get_stars(self):
        return self.get_piece().get_number_of_squares()
    
    def get_max_level(self):
        return self.get_stars() * 10
    
    def get_level(self):
        return self.__level

    def set_level(self, level):
        if level not in range(1, self.get_max_level()+1):
            raise ValueError(f"The level of this card must range from 1 to {self.get_max_level()}")
        self.__level = level

    def get_stats(self):
        return self.__stats


class Photocard1to4Stars(Photocard):

    def __init__(self, name, level):

        # Get name of the Blackpink member
        self.__member_name = self.check_member_name(name)

        # Initialize member name, photocard name, level and piece
        suit, color_number = [values.strip() for values in name.split(self.__member_name)]
        if suit not in suit_by_shape.keys():
            raise ValueError(f"The card name for a 1-4 star photocard should start with either of the following:\n{', '.join(suit_by_shape.keys())}")
        if not re.match(r"#[1-4]", color_number):
            raise ValueError("The end of the card name must end with '#' followed by a number from 1 to 4")
        color_number = int(color_number[1])  # the first character is '#'
        piece_color = None
        for color in Color:  # find color
            if color.value == color_number:
                piece_color = color
                break
        super().__init__(name, level, suit_by_shape[suit], piece_color)
        
    def __eq__(self, other):
        return isinstance(other, Photocard1to4Stars) and self.get_piece() == other.get_piece() and self.get_member_name() == self.get_member_name()
    

class Photocard5Stars(Photocard):

    __trendy_up_boosts = [0, 35, 85, 175]
    __signature_boosts = [0, 100, 210, 330, 470, 650]

    def __init__(self, name, level, piece_shape, piece_color, trendy_up, signature):
        pass


# 1-4 star cards: constructor takes name and level only (the name determines the piece and therefore the strong stat)
# 5 star cards: constructor takes name, piece shape, piece color and level. Piece color determines strong stat.

if __name__ == "__main__":
    p = Photocard1to4Stars("Autumn Trip JISOO #1", 19)
    assert p.get_piece() == Piece(Domino.DOMINO, Color.GREEN)
    p.set_level(3)
    assert p.get_level() == 3
    p = Photocard1to4Stars("Bored LISA #3", 35)
    assert p.get_piece() == Piece(FourSquareShape.T, Color.BLUE)
    assert p.get_photocard_name() == "Bored LISA #3"
    assert p.get_member_name() == "LISA"
    assert p.get_stars() == 4
    assert p.get_max_level() == 40

# My 5-star cards:
    # Max level 50
    # P:
    # Reading Jisoo #2 (blue), Coloring Book Jennie #2 (red):
    #   Level 21 stats: (842, 1004, 1058, 1316) without trendy up
    #   (+29, +35, +36, +43) lvl 21-30
    #   (+30, +36, +36, +46) lvl 31-40
    #   (+31, +37, +38, +48) lvl 41-49
    #   (+48, +64, +78, +87) lvl 49->50
    #
    # L:
    # Camping Site Jisoo #2 (green):
    #   Level 20 stats: (180, 587, 1230, 2080) without trendy up
    #   (+7, +22, +43, +71) lvl 20-30
    #   (+8, +23, +44, +73) lvl 31-40
    #   (+10, +24, +46, +74) lvl 41-49
    #   (+12, +44, +81, +140) lvl 49->50
    #
    # P-mirror:
    # Candle Jisoo #1 (red):
    #   Level 1 stats: (300, 375, 375, 450)
    #   (+26, +33, +33, +41) lvl 1-10
    #   (+28, +34, +34, +42) lvl 11-20
    #   (+28, +36, +36, +43) lvl 21-30
    #   (+30, +37, +37, +44) lvl 31-40
    #   (+31, +39, +39, +45) lvl 41-49
    #   lvl 49->50 tbd
    #
    # T:
    # Lisa's Outing (green):
    #   Level 1 stats: (75, 225, 450, 750)
    #   (+5, +18, +40, +70) lvl 1-10
    #   (+6, +20, +42, +70) lvl 11-20
    #   (+7, +22, +43, +71) lvl 21-30
    #   (+8, +23, +44, +73) lvl 31-40
    #   (+10, +24, +46, +74) lvl 41-49
    #   lvl 49->50 tbd
    #
    # F-mirror:
    # Pajama Jisoo #1 (green):
    #   Level 1 stats: (75, 225, 450, 750)
    #   (+5, +18, +40, +70) lvl 1-10
    #   (+6, +20, +42, +70) lvl 11-20
    #   (+7, +22, +43, +71) lvl 21-30
    #   (+8, +23, +44, +73) lvl 31-40
    #   (+10, +24, +46, +74) lvl 41-49
    #   lvl 49->50 tbd
    #
    # X:
    # Christmas Morning Rosé (red):
    #   Level 1 stats: (75, 225, 450, 750)
    #   (+5, +18, +40, +70) lvl 1-10
    #   (+6, +20, +42, +70) lvl 11-20
    #   (+7, +22, +43, +71) lvl 21-30
    #   (+8, +23, +44, +73) lvl 31-40
    #   (+10, +24, +46, +74) lvl 41-49
    #   lvl 49->50 tbd
    #
    # U:
    # Dawn Walk Lisa #2 (blue), Valentine's Day Jisoo (green), Lisa's Chocolate (blue):
    #   Level 1 stats: (225, 375, 420, 480)
    #   (+18, +33, +38, +44) lvl 1-10
    #   (+20, +34, +39, +45) lvl 11-20
    #   (+22, +36, +40, +45) lvl 21-30
    #   (+23, +37, +41, +47) lvl 31-40 
    #   (+24, +39, +43, +48) lvl 41-49
    #   lvl 49->50 tbd
    #
    # N-mirror:
    # Exercising Lisa #1 (blue), Neon Sign Lisa #1 (red), Ball Game Jennie #1 (yellow):
    #   Level 1 stats: (75, 225, 450, 750)
    #   (+5, +18, +40, +70) lvl 1-10
    #   (+6, +20, +42, +70) lvl 11-20
    #   (+7, +22, +43, +71) lvl 21-30
    #   (+8, +23, +44, +73) lvl 31-40
    #   (+10, +24, +46, +74) lvl 41-49
    #   lvl 49->50 tbd
    #
    # N:
    # Ball Game Jennie #2 (yellow):
    #   Level 1 stats: (75, 225, 450, 750)
    #   (+5, +18, +40, +70) lvl 1-10
    #   (+6, +20, +42, +70) lvl 11-20
    #   (+7, +22, +43, +71) lvl 21-30
    #
    # W:
    # Rosé on the Phone #2 (red):
    #   Level 1 stats: (150, 435, 450, 465)
    #   (+12, +39, +40, +42) lvl 1-10
    #   (+13, +40, +42, +43) lvl 11-20
    #   (+15, +42, +43, +43) lvl 21-30
    #   (15,43,44,46) lvl 31-40

    # Trendy Up: +140 (+35 each), then +200 (+50 each, +340 total), then +360 (+700 total)
    # Trendy Up 1: min level 10, Trendy Up 2: min level 15, Trendy Up 3: min level 20

# Member stats: 100, 150, 201, 254, 309, 366, 425, 485, 548, 613
# Increases: 50, 51, 53, 55, 57, 59, 60, 63, 65