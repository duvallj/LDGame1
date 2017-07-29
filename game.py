import pygame
from utils.objects import *
from utils.triangle import *
from utils.color import *
from utils.camera import *
from utils.input import *
from math import atan2, pi

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
    def __init__(self, image, *args, **kwargs):
        super(ImageThing, self).__init__(*args, **kwargs)
        self.image = image

    def draw(self, screen, transform):
        screen.blit(self.image, transform((self.x, self.y)))

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
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))#, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    g = Game(screen)
    pl = PaperPlane(x=100, y=780, raccl=0.01, maxrv=0.5, rdccl=0.994, ygrav=0.1)
    gr = Ground(y=1080)
    bg = ColorBackground((45,244,255))
    g.scene.add(bg)
    g.scene.add(gr)
    g.scene.add(pl)

    bgs = (45, 244, 255)
    bge = (0, 13, 51)
    ys = 0
    ye = -5000

    clouds = {}
    grass = {}

    g.ih.bind_key(pygame.K_a, pl.start_counterclock, pl.stop_counterclock)
    g.ih.bind_key(pygame.K_d, pl.start_clockwise, pl.stop_clockwise)
    #g.ih.bind_key(pygame.K_w, pl.start_move_dir(0), pl.stop_move_dir(0))

    tx = 100
    ty = 540

    # will adjust speed by changing max_v and [x,y]accl in tandem
    pl.start_move_dir(0)()

    while g.going:
        pc = g.cam.to_nonlocal((tx, ty))
        pp = g.scene.to_nonlocal((pl.x, pl.y))
        angle = atan2(pc[1]-pp[1], pp[0]-pc[0])
        g.cam.move_dir(angle*180/pi)
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
