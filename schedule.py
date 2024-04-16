from board import Board
from photocard import Photocard1to4Stars, Photocard5Stars
from member import Member
from globals import *

class Schedule(object):
    def __init__(self, board, conditions):
        self.__board = board
        self.__conditions = conditions

    def calculate_points_photocard(self, photocard, member):
        """Calculates the number of points given by a photocard played in full
        (cleared the same amount of squares as its piece)."""
        stat = color_by_stat[photocard.get_piece_color()]
        return photocard.base_total_score() + member.get_stats_points()[stat]
    
if __name__ == "__main__":
    s = Schedule([[0],[0]], ["d"])
    sooya = Member("JISOO", 16, 16, 16, 16)
    jendeukie = Member("JENNIE", 16, 16, 16, 16)
    chae = Member("ROSÉ", 17, 16, 16, 16)
    lalisa = Member("LISA", 16, 16, 16, 16)
    p = Photocard1to4Stars("Bored ROSÉ #1", 10)
    members = [sooya, jendeukie, chae, lalisa]

    print(s.calculate_points_photocard(p, chae))


# Regular schedules:
# Photocard point calculation: card base score (sum of stats) + score for member level
# Test again once a member's level changes
#
# Using bigger piece for required amount of squares:
#
# 2-star: 1289 (LV. 1), 1333 (LV. 2), 1377 (LV. 3), 1421 (LV. 4), 1465 (LV. 5) (member is at level 16 so +1049):
# ONE SQUARE: 1133 (LV. 1), 1149 (LV. 2), 1165 (LV. 3), 1180 (LV. 4), 1196 (LV. 5)
#
# 
# Level 1 3-star: 1499 (member is at level 16)
# TWO SQUARES: 1253
# ONE SQUARE: 1137
#
# Level 10 4-star: 2749 (member is at level 16)
# THREE SQUARES: 1890
# TWO SQUARES: 1508
# ONE SQUARE: 1246
#
#
#
# 5-STAR:
#
# Level 1, base signature and base trendy up: 2549 (member is at level 16)
# FOUR SQUARES: 1793
# THREE SQUARES: 1472
# TWO SQUARES: 1277
# ONE SQUARE: 1145
#
# Level 20, base signature and base trendy up: 5126 (member is at level 16)
# FOUR SQUARES: 3071 
# THREE SQUARES: 2198
# TWO SQUARES: 1668
# ONE SQUARE: 1309
#
# Level 25, base signature and level 2 trendy up: 6181 (member is at level 16)
# FOUR SQUARES: 3594
# THREE SQUARES: 2496
# TWO SQUARES: 1829
# ONE SQUARE: 1377