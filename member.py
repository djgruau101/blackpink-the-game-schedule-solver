from photocard import Photocard
from globals import *

class Member(object):

    __member_names = ["JENNIE", "ROSÉ", "LISA", "JISOO"]
    __instances = {}

    def __init__(self, name, music_level, acting_level,
                fashion_level, charm_level):
        if name not in self.__member_names:
            raise ValueError("The names of the Blackpink members are JENNIE, ROSÉ, LISA and JISOO")
        self.__name = name
        self.__music = music_level
        self.__acting = acting_level
        self.__fashion = fashion_level
        self.__charm = charm_level
        self.__photocards = []

    def __new__(cls, name, music_level, acting_level,
                fashion_level, charm_level):
        if name not in cls.__member_names:
            raise ValueError(f"'{name}' is not a member of Blackpink")
        if name not in cls.__instances:
            cls.__instances[name] = super().__new__(cls)
        else:
            raise ValueError(f"There already exists an instance of name '{name}'")
        return cls.__instances[name]
    
    def __repr__(self):
        return f"Member({self.get_name()})"
    
    def __str__(self):
        return f"Member with name={self.get_name()}"
        
    def get_name(self):
        return self.__name
    
    def get_stats(self):
        return dict(zip(Stat, [self.__music, self.__acting, self.__fashion, self.__charm]))
    
    def get_photocards(self):
        return self.__photocards.copy()

    def add_photocard(self, photocard):
        self.__photocards.append(photocard)

    def remove_photocard(self, photocard):
        self.__photocards.remove(photocard)

    def get_number_of_photocards(self):
        return len(self.__photocards)
    
    def get_level(self):
        return min(self.get_stats().values())
    
    def display_member_info(self):
        print(f"LV.{self.get_level()}", self.get_name())
        print("|".join([f"{stats_names[stat.value - 1]}: {point}" for stat, point in self.get_stats().items()]))
        print(f"{self.get_number_of_photocards()} photocards")

# Member stats: 100, 150, 201, 254, 309, 366, 425, 485, 548, 613, 680, 749, 820, 894, 970, 1049
# Increases: 50, 51, 53, 55, 57, 59, 60, 63, 65, 67, 69, 71, 74, 76, 79