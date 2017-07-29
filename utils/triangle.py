from utils.objects import *
import pygame


class Triangle(MoveRotate):
    def __init__(self, v1, v2, v3, *args, **kwargs):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        super().__init__(*args, **kwargs)
        self.vs = [self.v1, self.v2, self.v3]
        self.color = kwargs.get('color', (0, 0, 0))

    def draw(self, screen, transform):
        def nt(point):
            return transform(self.to_nonlocal(point))
        lst = [nt(p) for p in self.vs]
        pygame.draw.polygon(screen, self.color, lst)

    def tick(self):
        super(Triangle, self).tick()

    def sub(self, p1, p2):
        return (p1[0]-p2[0], p1[1]-p2[1])

    def add(self, p1, p2):
        return (p1[0]+p2[0], p1[1]+p2[1])

    def mul(self, p1, p2):
        return (p1[0]*p2[0], p1[1]*p2[1])

    def div(self, p1, p2):
        return (p1[0]/p2[0], p1[1]/p2[1])

    def dot(self, p1, p2):
        return p1[0]*p2[0]+p1[1]*p2[1]

    def collides(self, tri):
        if not issubclass(tri, Triangle):
            return False
        v0 = self.sub(self.v3, self.v1)
        v1 = self.sub(self.v2, self.v1)
        for p in tri.vs:
            v2 = self.sub(p, self.v1)
            dot00 = self.dot(v0, v0)
            dot01 = self.dot(v0, v1)
            dot02 = self.dot(v0, v2)
            dot11 = self.dot(v1, v1)
            dot12 = self.dot(v1, v2)
            invd = 1 / (dot00 * dot11 - dot01 * dot01)
            u = (dot11 * dot02 - dot01 * dot12) * invd
            v = (dot00 * dot12 - dot01 * dot02) * invd

            if u >= 0 and v >= 0 and u+v < 1:
                return True
        return False



class ColorBackground(BaseObject):
    def __init__(self, color):
        super().__init__(0, 0)
        self.color = color

    def draw(self, screen, transform):
        screen.fill(self.color)
