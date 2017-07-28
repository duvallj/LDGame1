from math import sqrt


class BaseObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def draw(self, screen, transform):
        pass

    def tick(self):
        pass

    def move(self, x, y):
        self.x += x
        self.y += y


class Mover(BaseObject):
    def __init__(self, x=0, y=0, xaccl=1, yaccl=1, xdccl=0.5, ydccl=0.5, maxv=1, xgrav=0, ygrav=0):
        super().__init__(x, y)
        self.xv = 0
        self.yv = 0
        self.xaccl = xaccl
        self.yaccl = yaccl
        self.xdccl = xdccl
        self.ydccl = ydccl
        self.maxv = maxv
        self.xgrav = xgrav
        self.ygrav = ygrav

        self.mr = False
        self.ml = False
        self.md = False
        self.mu = False

    def move_right(self):
        self.xv += self.xaccl
        self.apply_velocity()

    def start_move_right(self,*args):
        self.mr = True
    def stop_move_right(self,*args):
        self.mr = False

    def move_left(self):
        self.xv -= self.xaccl
        self.apply_velocity()

    def start_move_left(self,*args):
        self.ml = True
    def stop_move_left(self,*args):
        self.ml = False

    def move_down(self):
        self.yv += self.yaccl
        self.apply_velocity()

    def start_move_down(self,*args):
        self.md = True
    def stop_move_down(self,*args):
        self.md = False

    def move_up(self):
        self.yv -= self.yaccl
        self.apply_velocity()

    def start_move_up(self,*args):
        self.mu = True
    def stop_move_up(self,*args):
        self.mu = False

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
        if self.mr:
            self.move_right()
        if self.ml:
            self.move_left()
        if self.md:
            self.move_down()
        if self.mu:
            self.move_up()

class ContainerObject(Mover):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.children = set()

    def add(self, obj):
        self.children.add(obj)

    def remove(self, obj):
        self.children.discard(obj)

    def draw(self, screen, transform):
        def new_transform(point):
            return transform((point[0]+self.x, point[1]+self.y))
        for child in self.children:
            child.draw(screen, new_transform)

    def tick(self):
        for child in self.children:
            child.tick()
