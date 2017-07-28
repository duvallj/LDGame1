import pygame
from utils.objects import *

class Camera(Mover):
    def __init__(self, screen, sceneobj, x=0, y=0, w=1920, h=1080,
                 xaccl=1, yaccl=1, xdccl=0.5, ydccl=0.5, maxv=1, xgrav=0, ygrav=0):
        self.screen = screen
        self.scene = sceneobj
        super().__init__(x, y, xaccl, yaccl, xdccl, ydccl, maxv, xgrav, ygrav)
        self.w = w
        self.h = h
        self.ww, self.wh = screen.get_size()

    def transform(self, point):
        return ((point[0]-self.x) * self.ww / self.w,
                (point[1]-self.y) * self.wh / self.h)

    def draw(self, screen, transform=None):
        self.scene.draw(screen, self.transform)
        pygame.display.flip()
