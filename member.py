from photocard import Photocard

# A Blackpink member

class Member(object):

    __member_names = ["JENNIE", "ROSÉ", "LISA", "JISOO"]

    def __init__(self, name, music_level, acting_level,
                fashion_level, charm_level, photocards):
        if name not in self.__member_names:
            raise ValueError("The names of the Blackpink members are JENNIE, ROSÉ, LISA and JISOO")
        self.__name = name
        self.__music = music_level
        self.__acting = acting_level
        self.__fashion = fashion_level
        self.__charm = charm_level
        self.__photocards = photocards
        
    def get_name(self):
        return self.__name
        

if __name__ == "__main__":
    jennie = Member("JENNIE", 6, 6, 6, 6, [])
    jendeukie = Member("JENNIE", 6, 6, 6, 6, [])
    rosé = Member("ROSÉ", 6, 6, 6, 6, [])
    lisa = Member("LISA", 6, 6, 6, 6, [])
    # jisoo = Member("JISOO", 6, 6, 6, 6, [])