from utils.objects import *
import pygame
import pygame.gfxdraw


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

        pygame.gfxdraw.filled_polygon(screen, lst, self.color)
        pygame.gfxdraw.aapolygon(screen, lst, self.color)

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

    def collides(self, tri, mt, ot):
        if not issubclass(Triangle, tri.__class__):
            return False
        nv1 = mt(self.v1)
        nv2 = mt(self.v2)
        nv3 = mt(self.v3)
        v0 = self.sub(nv3, nv1)
        v1 = self.sub(nv2, nv1)
        for p in tri.vs:
            print(self.vs, p)
            p = ot(p)
            v2 = self.sub(p, nv1)
            print([nv1, nv2, nv3], p)
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
    def __init__(self, color, width, height):
        super().__init__(0, 0)
        self.color = color
        self.w = width
        self.h = height

    def draw(self, screen, transform):
        screen.fill(self.color)
