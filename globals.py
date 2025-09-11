from enum import Enum
from colors import Color

stats_names = ["Music", "Acting", "Fashion", "Charm"]
piece_colors = ["Green", "Yellow", "Blue", "Red"]
member_names = ["JISOO", "JENNIE", "ROSÉ", "LISA"]


class Stat(Enum):
    MUSIC = 1
    ACTING = 2
    FASHION = 3
    CHARM = 4


color_by_stat = dict(zip(Color, Stat))