import pygame
import inventory
import math
import random
import enums

PLAYER_SIZE = (16, 16)

class EquipmentManager(object):
    def __init__(self, player):
        self.PLAYER = player

        self.EQUIPS = {}

    def get_health_benefits(self):
        return 0 # TODO: Implement Later

    # COMMON EQUIPS BELOW

    @property
    def helmet(self):
        self.EQUIPS.get(
            'helmet', None
        )

    @property
    def chestplate(self):
        self.EQUIPS.get(
            'chestplate', None
        )

    @property
    def leggings(self):
        self.EQUIPS.get(
            "leggings", None
        )

    @property
    def boots(self):
        self.EQUIPS.get(
            "boots", None
        )

class PlayerObject(pygame.sprite.Sprite):
    def __init__(self, game, *args, **kwargs):
        # Init base class
        self.GAME = game # No idea why you'd ever need this but here it is
        pygame.sprite.Sprite.__init__(self)

        self.height, self.width = PLAYER_SIZE

        self.image = self.fetch_character_icon()
        self.rect = self.image.get_rect()

        self.experience = 0
        self.damage_taken = 0

        self.SPECIES = random.choice(list(enums.PlayerSpecies.__members__.values()))
        self.CLASS = random.choice(list(enums.PlayerClasses.__members__.values()))
        self.PERK = random.choice(list(enums.PlayerBoosts.__members__.values()))

        self.BASE_CARRY_WEIGHT = 175

        self.INVENTORY = inventory.InventoryHandler(self)
        self.EQUIPS = EquipmentManager(self)

        # Things the player can't walk through
        self.COLLIDES_WITH = (
            enums.DungeonTiles.wall,
        )

    def draw_entity(self, screen):
        screen.blit(self.image, (self.location))


    def fetch_character_icon(self):
        i = pygame.Surface((self.height, self.width))
        i.fill('red')
        self.image = i
        return i

    def add_experience(self, c):
        self.experience += round(c)
        return round(c)

    def heal(self, a):
        h2h = round(a) if round(a) + self.health <= self.total_health else self.total_health - self.health
        self.health += h2h
        return h2h

    @property
    def free_carry_weight(self):
        return self.BASE_CARRY_WEIGHT - self.INVENTORY.fetch_storage_weight()

    @property
    def dead(self):
        return self.damage_taken == self.total_health

    @property
    def health(self):
        return self.total_health - self.damage_taken

    @property
    def total_health(self):
        return 20 * (5 * self.level) + self.EQUIPS.get_health_benefits()

    @property
    def level(self): # Ensure this works... because it probably doesn't
        return self.experience / 75 * math.floor(self.experience / 75)

    def draw(self, screen):
        screen.blit(self.image, self.location)

    @property
    def location(self):
        return (self.x, self.y)

    @property
    def x(self): return self.rect.x

    @property
    def y(self): return self.rect.y

    def check_tile(self, dungeon_mapping, x : int = None, y : int = None):
        if x is None and y is None:
            tX = (self.x / 16)
            tY = (self.y / 16)
        else:
            tX, tY = x, y

        print(dungeon_mapping.map_width)
        if tX >= dungeon_mapping.offset_x and tX <= (dungeon_mapping.offset_x + dungeon_mapping.map_width) - 1:
            if tY >= dungeon_mapping.offset_y and tY <= dungeon_mapping.offset_y + dungeon_mapping.map_height - 1:

                tXAO = tX - dungeon_mapping.offset_x
                tYAO = tY - dungeon_mapping.offset_y

                print(tXAO, tYAO, sep='\t')

                return dungeon_mapping.fetch_tile(int(tXAO), int(tYAO))
        return enums.DungeonTiles.DUNGEON_VOID # User probably isn't on a tile

    def can_move(self, dungeon_mapping, x, y):
        tile = self.check_tile(dungeon_mapping, x / 16, y / 16)
        return tile not in self.COLLIDES_WITH


    def move(self, x : int, y : int, *args, **kwargs):
        new_pos = self.rect.move(x, y)
        self.rect.x, self.rect.y = new_pos.x, new_pos.y
        return self.rect