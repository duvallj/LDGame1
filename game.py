import pygame
from utils.objects import *
from utils.triangle import *
from utils.color import *
from utils.camera import *
from utils.input import *
from math import atan2, pi
import pygame.image
import random

'''
Idea:
You are a paper airplane
You fly along, slowly running out of power as you do
Going down fast gets you more speed, going up decreases it
Updrafts push you up
Tail winds give you a boost of speed
Head winds decrease your speed even faster
If you hit the ground, you stop, game ends
'''

class PaperPlane(ContainerObject, MoveRotate):
    def __init__(self, *args, **kwargs):
        super(PaperPlane, self).__init__(*args, **kwargs)
        self.add(Triangle((-20,0),(-30,-15),(60,0),color=(255,245,145)))
        self.add(Triangle((-20,0),(-20,20),(60,0),color=(255,249,183)))

    def calc_speed(self, cy, ca):
        # Calculates new speed based off change in height
        # and angle from previous frame

        # We can change the speed by changing the acceleration.
        # Player has complete control over direction, so not
        # realistic to change direction really.
        # Although, still need to make sure being straight up is not a strat
        # plane should still be able to fall backwards



        pass

class Ground(ContainerObject):
    def __init__(self, *args, **kwargs):
        super(Ground, self).__init__(*args, **kwargs)
        self.add(Triangle((0,0),(0,-200),(1920,-200),color=(0,140,14)))
        self.add(Triangle((0,0),(1920,0),(1920,-200),color=(0,140,14)))

class ImageThing(BaseObject):
    def __init__(self, image, cam, *args, **kwargs):
        super(ImageThing, self).__init__(*args, **kwargs)
        self.cam = cam
        self.image = pygame.image.load(image).convert_alpha()
        self.w, self.h = self.image.get_size()

    def draw(self, screen, transform):
        if not self.off_screen():
            screen.blit(self.image, transform((self.x, self.y)))

    def off_screen(self):
        return (self.x > self.cam.x + self.cam.w or self.cam.x > self.x + self.w or
                self.y > self.cam.y + self.cam.h or self.cam.y > self.y + self.h)

    def off_area(self):
        return self.x > self.cam.x + self.cam.w or self.cam.x > self.x + self.w


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.going = True
        self.scene = ContainerObject()
        self.cam = Camera(self.screen, self.scene, xaccl=0.007, yaccl=0.007,
                          maxv=2, xdccl=0.994, ydccl=0.994)
        self.ih = InputHandler()
        self.ih.bind_key(pygame.K_ESCAPE, self.stop)
        self.ih.bind_stop(self.stop)

    def stop(self, *args):
        self.going = False

    def tick(self):
        evtlist = pygame.event.get()
        self.ih.tick(evtlist)
        self.scene.tick()
        self.cam.tick()

    def draw(self):
        self.cam.draw(self.screen)
        #pygame.display.flip()


def update_bgitems(g, iset, fname, mi, isp, xo, yo, yro):
    irem = set()
    for grs in iset:
        if grs.off_area():
            irem.add(grs)
            g.scene.remove(grs)
    iset.difference_update(irem)
    if len(iset) == 0 or (len(iset) < mi and random.random() < isp):
        grs = ImageThing(fname, g.cam,
                         x=g.cam.x + g.cam.w + xo,
                         y=yo + random.randint(-yro, yro))
        iset.add(grs)
        g.scene.add(grs)

def main():
    pygame.init()
    screen = pygame.display.set_mode((960,540), pygame.HWSURFACE | pygame.DOUBLEBUF)
    g = Game(screen)
    pl = PaperPlane(x=100, y=780,
                    raccl=0.01, maxrv=0.5, rdccl=0.994,
                    maxv=30, xaccl=3, yaccl=3,
                    ygrav=0.1)
    gr = Ground(y=1080)
    bg = ColorBackground((45, 244, 255), 960, 540)
    g.scene.add(bg)
    g.scene.add(gr)
    g.scene.add(pl)

    bgs = (45, 244, 255)
    bge = (0, 13, 51)
    ys = 0
    ye = -5000

    cloud1s = set()
    max_cloud1s = 5
    c1spawn = 0.0005

    cloud2s = set()
    max_cloud2s = 6
    c2spawn = 0.0006

    stars = set()
    max_stars = 100
    sspawn = 0.007

    grass = set()
    max_grass = 10
    gspawn = 0.002

    g.ih.bind_key(pygame.K_a, pl.start_counterclock, pl.stop_counterclock)
    g.ih.bind_key(pygame.K_d, pl.start_clockwise, pl.stop_clockwise)
    #g.ih.bind_key(pygame.K_w, pl.start_move_dir(0), pl.stop_move_dir(0))

    tx = 100
    ty = 540

    # will adjust speed by changing max_v and [x,y]accl in tandem
    pl.start_move_dir(0)()

    while g.going:
        update_bgitems(g, grass, 'imgs/grass.png', max_grass, gspawn, -25, 865, 20)
        for x in range(400, 2000, 200):
            update_bgitems(g, cloud1s, 'imgs/cloud1.png', max_cloud1s, c1spawn, -25, -x, 100)
        for x in range(2000, 5000, 400):
            update_bgitems(g, cloud2s, 'imgs/cloud2.png', max_cloud2s, c2spawn, -25, -x, 200)
        for x in range(5000, 8000, 400):
            update_bgitems(g, stars, 'imgs/star.png', max_stars, sspawn, -25, -x, 200)
        pc = g.cam.to_nonlocal((tx, ty))
        pp = g.scene.to_nonlocal((pl.x, pl.y))
        g.cam.x += (pp[0]-pc[0])/100
        g.cam.y += (pp[1]-pc[1])/100

        oa = pl.angle
        oy = pl.y

        g.tick()
        if g.cam.y > 0:
            g.cam.y = 0
        gr.x = g.cam.x

        pl.angle *= pl.rdccl
        na = pl.angle
        ny = pl.y
        pl.calc_speed(ny-oy, na-oa)

        color = tuple([
            (max(g.cam.y, ye) - ys) * (bge[i] - bgs[i]) / (ye - ys) + bgs[i]
            for i in range(3)
        ])
        bg.color = color

        g.draw()

    pygame.quit()

if __name__=="__main__":
    main()
