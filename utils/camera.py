import pygame
from utils.objects import *


class Camera(Mover):
    def __init__(self, screen, sceneobj, *args, **kwargs):
        self.screen = screen
        self.scene = sceneobj
        super().__init__(*args, **kwargs)
        self.w = kwargs.get('w',1920)
        self.h = kwargs.get('h',1080)
        self.ww, self.wh = screen.get_size()
        self.ox = self.x+2
        self.oy = self.y+2

    def transform(self, point):
        return ((point[0]-self.x) * self.ww / self.w,
                (point[1]-self.y) * self.wh / self.h)

    def draw(self, screen, transform=None):
        self.scene.draw(screen, self.transform)
        pygame.display.flip()
