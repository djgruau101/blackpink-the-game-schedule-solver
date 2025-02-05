from enum import Enum

class BlockType(Enum):
    NORMAL = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    RED = 5
    JISOO = 6
    JENNIE = 7
    ROSÉ = 8
    LISA = 9
    DOUBLE = 10
    DOUBLE_CRACKED = 11
    BOX = 12


class BrushColor(Enum):
    GREEN = 1
    YELLOW = 2
    BLUE = 3
    RED = 4
    NONE = 5


class Block(object):

    def __init__(self, block_type, has_cover, brush_color=BrushColor.NONE):
        if has_cover and brush_color != BrushColor.NONE:
            raise ValueError("covered blocks can not have a brush")
        if block_type == BlockType.CRATE and brush_color != BrushColor.NONE:
            raise ValueError("crate blocks can not have a brush")
        if block_type == BlockType.CRATE and has_cover:
            raise ValueError("crate blocks can not be covered")
        self.__block_type = block_type
        self.__has_cover = has_cover
        self.__brush_color = brush_color

    def get_block_type(self):
        return self.__block_type

    def remove_cover(self):
        self.__has_cover = False

    def has_cover(self):
        return self.__has_cover

    def add_brush(self, brush_color):
        if self.get_block_type() != BlockType.CRATE and not self.has_cover():
            self.__brush_color = brush_color
            if self.__block_type == BlockType.NORMAL:
                brush_color_by_block_type = {BrushColor.GREEN: BlockType.GREEN,
                                            BrushColor.YELLOW: BlockType.YELLOW,
                                            BrushColor.BLUE: BlockType.BLUE,
                                            BrushColor.RED: BlockType.RED}
                self.__block_type = brush_color_by_block_type[brush_color]
                return True
        return False

    def remove_brush(self):
        self.__brush_color = BrushColor.NONE

    def has_brush(self):
        return self.__brush_color != BrushColor.NONE


if __name__ == "__main__":
    b1 = Block(BlockType.NORMAL, False, BrushColor.BLUE)
    b1.add_brush(BrushColor.BLUE)
    print(b1.get_block_type())

    # test out rainbow blocks: blue->red->green->yellow, Jisoo->Jennie->Rosé->Lisa
    # Walls: level 45