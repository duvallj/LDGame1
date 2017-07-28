from utils.objects import *
import pygame


class Triangle(Mover):
    def __init__(self, v1, v2, v3, color, x=0, y=0,
                 xaccl=1, yaccl=1, xdccl=0.5, ydccl=0.5, maxv=1, xgrav=0, ygrav=0):
        super().__init__(x, y, xaccl, yaccl, xdccl, ydccl, maxv, xgrav, ygrav)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.vs = [v1, v2, v3]
        self.color = color

    def draw(self, screen, transform):
        def nt(point):
            return transform((point[0]+self.x, point[1]+self.y))
        pygame.draw.polygon(screen, self.color, [nt(p) for p in self.vs])


class ColorBackground(BaseObject):
    def __init__(self, color):
        super().__init__(0, 0)
        self.color = color

    def draw(self, screen, transform):
        screen.fill(self.color)
