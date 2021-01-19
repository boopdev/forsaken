import pygame
from mcm import MovingCameraManager

class GameSurface(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.SURFACE = pygame.Surface(
            size = self.game.screen.get_size()
        )

        self.mcm = MovingCameraManager(self.game, self.SURFACE)
        
    def draw_surface(self):
        self.SURFACE.fill(
            'red'
        )

        sur = self.game.LARGE_FONT.render(
            "FUCK YOU",
            True,
            'black'
        )

        self.SURFACE.blit(
            sur,
            (
                (self.SURFACE.get_width() - sur.get_width()) / 2,
                (self.SURFACE.get_height() - sur.get_height()) / 2,
            )
        )

        self.game.screen.blit(self.SURFACE, (0, 0))