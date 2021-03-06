import pygame
import math
import random
import classes as forsakenclasses
import json
import enums
from utility import bsp, boop

# I really don't know how well my dungeon generator will work

# We're making this it's own class

class DungeonGenerator(object):
    def __init__(self, game, width, height, *args, **kwargs):
        self.game = game
        self.priority = kwargs.pop('priority', 100)
        self.HALLWAY_GENERATOR = None
        self.DUNGEON_MAPPING = self.generate_void_dungeon_map(width, height)

    def generate_void_dungeon_map(self, width, height):
        x = []
        for i in range(height):
            x.append([enums.DungeonTiles.DUNGEON_VOID] * width)
        return x

class DungeonRoomMap(object):
    def __init__(self, array : list = [], *args, **kwargs):
        self._mapping = array
        self.overlapping_rooms = []

        self.offset_x = None
        self.offset_y = None
        
        self.CACHED_WIDTH = 0
        self.CACHED_HEIGHT = 0

    def fetch_tile(self, x : int, y : int):
        return enums.DungeonTiles(self._mapping[y][x])

    def print_map(self):
        for i in self._mapping:
            print(''.join(str(i)))
                
    def old_draw_at(self, x, y, screen):
        w, h = len(self._mapping[0]), len(self._mapping)
        self.offset_x, self.offset_y = x, y
        sur = pygame.Surface((w * 16, h * 16))
        sur.fill('black')

        for colnum, colcont in enumerate(self._mapping):
            for rownum, num in enumerate(colcont):
                part = pygame.Surface((16, 16))
                if num == enums.DungeonTiles.wall.value:
                    part.fill('grey')
                elif num == enums.DungeonTiles.empty.value:
                    continue
                elif num == enums.DungeonTiles.door.value:
                    part.fill('brown')

                sur.blit(part, (rownum * 16, colnum * 16))


        screen.blit(sur, (x * 16, y * 16))

    # X and Y are the offsets for the screen
    # This function takes those offsets and only renders the pixels on the screen
    def new_draw_at(self, x, y, screen):
        self.offset_x, self.offset_y = x, y # NOTE: I don't know why, but you need this

        # The amount of pixels to render for each width and height
        screenPixelWidth = screen.get_width() / 16
        screenPixelHeight = screen.get_height() / 16

        sur = pygame.Surface(screen.get_size())
        sur.fill('black')

        for colNum, colCont, in enumerate(self._mapping):
            for rowNum, rowCont in enumerate(colCont):

                if colNum >= y * -1 and colNum <= screenPixelHeight + (y * -1):
                    if rowNum >= x * -1 and rowNum <= screenPixelWidth + (x * -1):


                        part = pygame.Surface((16, 16))

                        if rowCont == enums.DungeonTiles.wall.value:
                            part.fill('grey')
                            
                        elif rowCont == enums.DungeonTiles.empty.value:
                            continue

                        elif rowCont == enums.DungeonTiles.door.value:
                            part.fill('brown')

                        sur.blit(part, ((rowNum + x) * 16, (colNum + y) * 16))

        screen.blit(sur, (0, 0))

    @property
    def map_width(self):
        if len(self._mapping) == 0:
            return 0

        return len(self._mapping[0]) # Grabs the length of the first width

    @property
    def map_height(self):
        return len(self._mapping)

    @property
    def map_area(self):
        if self.map_width != 0:
            return sum([len(c) for c in self._mapping])
        raise ValueError("Map is Empty")


    def check_for_interference(self, other):
        interference_value = 0
        for ri, row in enumerate(other.map._mapping, start=other.pos_x):
            for ci, col in enumerate(other.map_mapping, start=other.pos_y):
                if self._mapping[ri][ci] != enums.DungeonTiles.DUNGEON_VOID:
                    interference_value += 1
        return interference_value

class FileDungeonGenerator(DungeonGenerator):
    def __init__(self, game, *args, **kwargs):
        ##super().__init__(
        ##    game, *args, **kwargs
        ##)
        self.RAW_MAP_DATA = {}

    @property
    def DUNGEON_MAPPING(self):
        if 'mapping' in self.RAW_MAP_DATA.keys():
            return self.RAW_MAP_DATA['mapping']
        else:
            return None

    def load_from_file(self, path : str):
        with open(path, 'r') as dfile:
            self.RAW_MAP_DATA = json.load(dfile)
        return DungeonRoomMap(self.DUNGEON_MAPPING)

class boopDungeonGenerator(DungeonGenerator):
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self.dungeon_size = self.game.DUNGEON_SIZE
        self.w, self.h = self.dungeon_size.get_size()
        super().__init__(self.game, width=self.w, height=self.h, *args, **kwargs)
        #self.game = game

        self.bspTree = bsp.boopTree
        self.DUNGEON_MAPPING = self.generate(lazy = True)

    def sex(self):
        return DungeonRoomMap(self.DUNGEON_MAPPING)

    def generate(self, lazy : bool = True):
        t = self.bspTree(self.w, self.h)
        t.createChildrenIteration(2)
        leaves = t.fetchAllLeafs()

        mapping = self.generate_void_dungeon_map(self.w, self.h)

        if not lazy:
            raise NotImplementedError("Efficient Loading doesn't exist yet")

        else:
            # This is an extremely slow method of generating dungeons.
            # TODO: Fucking change this you lazy prick.

            for leaf in leaves:

                for ri, row in enumerate(mapping):
                    for ci, column in enumerate(row):
                        
                        if ri == leaf.y1 or ri == leaf.y2:
                            mapping[ri][ci] = 2

                        elif ci == leaf.x1 or ci == leaf.x2:
                            mapping[ri][ci] = 2

        return mapping

                        
            

