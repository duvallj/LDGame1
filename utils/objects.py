from math import sqrt, sin, cos, pi
from itertools import product


class BaseObject:
    def __init__(self, *args, **kwargs):
        if args:
            self.x = args[0]
            self.y = args[1]
        else:
            self.x = kwargs.get('x', 0)
            self.y = kwargs.get('y', 0)

    def draw(self, screen, transform):
        pass

    def tick(self):
        pass

    def to_nonlocal(self, point):
        return (point[0]+self.x, point[1]+self.y)

    def move(self, x, y):
        self.x += x
        self.y += y

    def collides(self, other, my_transform, other_transform):
        return False

    def off_screen(self):
        return False


class Mover(BaseObject):
    def __init__(self, *args, **kwargs):
        super(Mover, self).__init__(*args, **kwargs)
        self.xv = 0
        self.yv = 0
        self.xaccl = kwargs.get('xaccl', 1)
        self.yaccl = kwargs.get('yaccl', 1)
        self.xdccl = kwargs.get('xdccl', 0)
        self.ydccl = kwargs.get('ydccl', 0)
        self.maxv = kwargs.get('maxv', 1)
        self.xgrav = kwargs.get('xgrav', 0)
        self.ygrav = kwargs.get('ygrav', 0)

        self.mdirs = set()

    def move_dir(self, dire):
        self.xv += cos(dire*pi/180) * self.xaccl
        self.yv -= sin(dire*pi/180) * self.yaccl

    def start_move_dir(self, dire):
        def f(*args):
            self.mdirs.add(dire)
        return f

    def stop_move_dir(self, dire):
        def f(*args):
            self.mdirs.discard(dire)
        return f

    def limit_v(self):
        speed = sqrt(self.xv*self.xv+self.yv*self.yv)

        if speed > self.maxv:
            self.xv = self.maxv * self.xv / speed
            self.yv = self.maxv * self.yv / speed

    def apply_velocity(self):
        self.limit_v()
        self.move(self.xv, self.yv)

    def tick(self):
        self.xv *= self.xdccl
        self.yv *= self.ydccl
        for dire in self.mdirs:
            self.move_dir(dire)
        self.xv += self.xgrav
        self.yv += self.ygrav
        self.apply_velocity()
        super(Mover, self).tick()

class Rotator(BaseObject):
    def __init__(self, *args, **kwargs):
        super(Rotator, self).__init__(*args, **kwargs)
        self.rv = 0
        self.raccl = kwargs.get('raccl', 1)
        self.maxrv = kwargs.get('maxrv', 1)
        self.rdccl = kwargs.get('rdccl', 0.5)
        self.angle = 0
        self.cw = False
        self.cc = False

    def to_nonlocal(self, point):
        s = sin(self.angle*pi/180)
        c = cos(self.angle*pi/180)
        px = point[0]
        py = point[1]
        return super().to_nonlocal((px*c-py*s, px*s+py*c))

    def start_clockwise(self,*args):
        self.cw = True

    def stop_clockwise(self,*args):
        self.cw = False

    def start_counterclock(self,*args):
        self.cc = True

    def stop_counterclock(self,*args):
        self.cc = False

    def tick(self):
        self.rv *= self.rdccl
        if self.cw:
            self.rv += self.raccl
        if self.cc:
            self.rv -= self.raccl
        if abs(self.rv) > self.maxrv:
            self.rv = self.maxrv * ((self.rv>0)-(self.rv<0))
        self.angle += self.rv
        super(Rotator, self).tick()

class MoveRotate(Mover, Rotator):
    def __init__(self, *args, **kwargs):
        super(MoveRotate, self).__init__(*args, **kwargs)

    def move_dir(self, dire):
        dire = dire - self.angle
        self.xv += cos(dire*pi/180) * self.xaccl
        self.yv -= sin(dire*pi/180) * self.yaccl

    def tick(self):
        super(MoveRotate, self).tick()

class ContainerObject(Mover):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = []

    def add(self, obj):
        self.children.append(obj)

    def remove(self, obj):
        self.children.remove(obj)

    def draw(self, screen, transform):
        def new_transform(point):
            return transform(self.to_nonlocal(point))
        for child in self.children:
            child.draw(screen, new_transform)

    def tick(self):
        for child in self.children:
            child.tick()
        super(ContainerObject, self).tick()

    def collides(self, other, my_transform, other_transform):
        def new_mt(point):
            return my_transform(self.to_nonlocal(point))
        def new_ot(point):
            return other_transform(other.to_nonlocal(point))
        if issubclass(ContainerObject, other.__class__):
            for c1, c2 in product(self.children, other.children):
                if c1.collides(c2, new_ot, new_mt):
                    return True
            return False
        else:
            for c in self.children:
                if c.collides(other, new_ot, new_mt) or \
                        other.collides(c, new_ot, new_mt):
                    return True
            return False

