from globals import Stat, member_names, stats_names

class Member(object):

    __instances = {}
    __stats_scores = [100, 150, 201, 254, 309,
                      366, 425, 485, 548, 613,
                      680, 749, 820, 894, 970,
                      1049, 1131, 1215, 1302,
                      1392, 1485, 1581, 1681,
                      1784, 1891, 2001, 2115,
                      2233, 2355, 2481, 2611,
                      2746, 2885, 3029, 3178,
                      3332]  # the score of a stat is at level (its index + 1)

    def __init__(self, name, music_level, acting_level,
                fashion_level, charm_level):
        if name not in member_names:
            raise ValueError("The names of the Blackpink members are JENNIE, ROSÉ, LISA and JISOO")
        self.__name = name
        self.__music = music_level
        self.__acting = acting_level
        self.__fashion = fashion_level
        self.__charm = charm_level
        self.__photocards = []

    def __new__(cls, name, music_level, acting_level,
                fashion_level, charm_level):
        if name not in member_names:
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
    
    def get_photocards(self):
        return self.__photocards.copy()

    def add_photocard(self, photocard):
        self.__photocards.append(photocard)

    def remove_photocard(self, photocard):
        self.__photocards.remove(photocard)

    def get_number_of_photocards(self):
        return len(self.__photocards)
    
    def get_level(self):
        return min(self.get_stats_levels().values())
    
    def set_stat_level(self, stat, level):
        if level not in range(1, len(self.__stats_scores) + 1):
            raise ValueError(f"Stat level must range from 1 to {len(self.__stats_scores)}")
        if stat == Stat.MUSIC:
            self.__music = level
        elif stat == Stat.ACTING:
            self.__acting = level
        elif stat == Stat.FASHION:
            self.__fashion = level
        elif stat == Stat.CHARM:
            self.__charm = level

    def level_up_stat(self, stat):
        current_level = 0  # initialize
        if stat == Stat.MUSIC:
            current_level = self.__music
        elif stat == Stat.ACTING:
            current_level = self.__acting
        elif stat == Stat.FASHION:
            current_level = self.__fashion
        elif stat == Stat.CHARM:
            current_level = self.__charm
        return self.set_stat_level(stat, current_level + 1)
    
    def get_stats_levels(self):
        return dict(zip(Stat, [self.__music, self.__acting, self.__fashion, self.__charm]))

    def get_stats_points(self):
        stats_levels = [self.__music, self.__acting, self.__fashion, self.__charm]
        return dict(zip(Stat, [self.__stats_scores[l - 1] for l in stats_levels]))

    def display_member_info(self):
        print(f"LV.{self.get_level()}", self.get_name())
        print("|".join([f"{stats_names[stat.value - 1]}: {level}" for stat, level in self.get_stats_levels().items()]))
        print(f"{self.get_number_of_photocards()} photocards")

# Member stats: 100, 150, 201, 254, 309, 366, 425, 485, 548, 613, 680, 749, 820, 894, 970, 1049, 1131, 1215, 1302, 1392, 1485, 1581, 1681, 1784, 1891, 2001, 2115, 2233, 2355, 2481, 2611, 2746, 2885, 3029, 3178, 3332
# Increases: 50, 51, 53, 55, 57, 59, 60, 63, 65, 67, 69, 71, 74, 76, 79, 82, 84, 87, 90, 93, 96, 100, 103, 107, 110, 114, 118, 122, 126, 130, 135, 139, 144, 149, 154