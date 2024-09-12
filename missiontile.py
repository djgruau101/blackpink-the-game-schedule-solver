class MissionTile(object):

    def __init__(self, type, brush_color):
        self.__type = type # none, color, member, double, crate, cover (boolean), brush
        self.__brush_color = brush_color  # None if no brush