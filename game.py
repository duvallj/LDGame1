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
TODO:
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

        self.mom = 0
        self.launched = False

    def start(self, sm, sv):
        def func(*args):
            self.ygrav  = 0.01
            self.mom = sm
            self.xv = sv
            self.launched = True
        return func

    def move_dir(self, dire):
        dire = dire - self.angle
        self.xv += cos(dire*pi/180) * self.xaccl
        self.yv -= sin(dire*pi/180) * self.yaccl

    def move_dir_force(self, dire, force):
        dire = dire - self.angle
        self.xv += cos(dire * pi / 180) * force
        self.yv -= sin(dire * pi / 180) * force

    def calc_speed(self, cx, cy, ca):
        # Calculates new speed based off change in height
        # and angle from previous frame

        # We can change the speed by changing the acceleration.
        # Player has complete control over direction, so not
        # realistic to change direction really.
        # Although, still need to make sure being straight up is not a strat
        # plane should still be able to fall backwards
        heading = atan2(self.yv, self.xv)
        aot = heading - self.angle
        vel = self.xv*self.xv+self.yv*self.yv
        self.v = sqrt(vel)
        area = 0.01
        fps = 100

        lc = 2 * pi * aot / 180 * pi
        lf = vel*1.225*area*lc
        self.move_dir_force(90, lf/fps)

        dc = .0039 * aot * aot + .025
        if vel != 0:
            ldf = (lf*lf) / (55.125 * area * vel * pi)
        else:
            ldf = 0
        fd = 0.6125 * area * vel * dc
        df = ldf + fd
        if cy > 0:
            self.move_dir_force(0, df / fps)
        else:
            self.move_dir_force(180, df / fps)

        self.move_dir_force(0, self.mom)
        self.mom *= 0.95

        self.xv += self.xgrav
        self.yv += self.ygrav

    def tick(self):
        self.rv *= self.rdccl
        if self.cw:
            self.rv += self.raccl
        if self.cc:
            self.rv -= self.raccl
        if abs(self.rv) > self.maxrv:
            self.rv = self.maxrv * ((self.rv > 0) - (self.rv < 0))
        self.angle += self.rv

        self.apply_velocity()

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


class HideableImage(ImageThing):
    def __init__(self, *args, **kwargs):
        super(HideableImage, self).__init__(*args, **kwargs)
        self.hidden = False

    def draw(self, screen, transform):
        if not (self.off_screen() or self.hidden):
            screen.blit(self.image, transform((self.x, self.y)))


class ButtonImage(HideableImage):
    def __init__(self, callback, xo, yo, *args, **kwargs):
        super(ButtonImage, self).__init__(*args, **kwargs)
        self.smaller = self.image
        self.bigger = pygame.transform.scale(self.image, (int(self.w*1.1), int(self.h*1.1)))
        self.mon = False
        self._cb = callback
        self.xo = xo
        self.yo = yo

    def callback(self, *args):
        if self.mon and not self.hidden:
            self._cb(*args)

    def mouseover(self, pos, rel, buttons):
        if self.off_screen():
            self.mon = False
        x = self.x - self.cam.x
        y = self.y - self.cam.y
        x1 = x - self.w/2
        y1 = y - self.h/2
        x2 = x1 + self.w
        y2 = y1 + self.h
        if x1 < pos[0]+self.xo < x2 and y1 < pos[1]+self.yo < y2:
            self.mon = True
            self.image = self.bigger
        else:
            self.mon = False
            self.image = self.smaller


class TextDisplay(BaseObject):
    def __init__(self, color, tsize, *args, **kwargs):
        super(TextDisplay, self).__init__(*args, **kwargs)
        self.font = pygame.font.SysFont(None, tsize)
        self.text = ''
        self.color = color

    def draw(self, screen, transform):
        def nt(point):
            pt = self.to_nonlocal(point)
            return transform(pt)

        words = [word.split(' ') for word in self.text.splitlines()]
        space = self.font.size(' ')[0]
        max_width, max_height = screen.get_size()
        x, y = 0, 0
        word_width, word_height = 0, 0
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = 0
                    y += word_height
                screen.blit(word_surface, nt((x*2, y*2)))
                x += word_width + space
            x = 0
            y += word_height


class Statistics:
    def __init__(self):
        self.max_height = 0
        self.max_dist = 0
        self.max_speed = 0


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.going = True
        self.scene = ContainerObject()
        self.cam = Camera(self.screen, self.scene, xaccl=0.007, yaccl=0.007,
                          maxv=2, xdccl=0.994, ydccl=0.994)
        self.ih = InputHandler()
        self.ih.bind_key(pygame.K_ESCAPE, self.noreallystop)
        self.ih.bind_stop(self.noreallystop)
        self.actuallystop = False
        self.clock = pygame.time.Clock()
        self.stats = Statistics()

    def stop(self, *args):
        self.going = False

    def noreallystop(self, *args):
        self.going = False
        self.actuallystop = True

    def tick(self):
        evtlist = pygame.event.get()
        self.ih.tick(evtlist)
        self.scene.tick()
        self.cam.tick()
        self.clock.tick(100)

    def draw(self):
        self.cam.draw(self.screen)
        #pygame.display.flip()


def update_bgitems(g, iset, fname, mi, isp, xo, yo, yro):
    irem = set()
    for grs in iset:
        if grs.off_area():
            irem.add(grs)
            #g.scene.remove(grs)
    iset.difference_update(irem)
    if len(iset) == 0 or (len(iset) < mi and random.random() < isp):
        grs = ImageThing(fname, g.cam,
                         x=g.cam.x + g.cam.w + xo,
                         y=yo + random.randint(-yro, yro))
        iset.add(grs)
        g.scene.add(grs)

def play_game(g, td, startmom, startvel):
    g.scene.children = []

    pl = PaperPlane(x=100, y=560,
                    raccl=0.05, maxrv=1, rdccl=0.994,
                    maxv=10000, xaccl=3, yaccl=3)
    gr = Ground(y=1080)
    bg = ColorBackground((45, 244, 255), 960, 540)
    g.scene.add(bg)
    g.scene.add(td)
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

    tx = 100
    ty = 540

    g.ih.bind_key(pygame.K_SPACE, up_action=pl.start(startmom, startvel))

    while g.going:
        if pl.launched:
            update_bgitems(g, grass, 'imgs/grass.png', max_grass, gspawn, -25, 865, 20)
            for x in range(400, 2000, 200):
                update_bgitems(g, cloud1s, 'imgs/cloud1.png', max_cloud1s, c1spawn, -25, -x, 100)
            for x in range(2000, 5000, 400):
                update_bgitems(g, cloud2s, 'imgs/cloud2.png', max_cloud2s, c2spawn, -25, -x, 200)
            for x in range(5000, 8000, 400):
                update_bgitems(g, stars, 'imgs/star.png', max_stars, sspawn, -25, -x, 200)
        pc = g.cam.to_nonlocal((tx, ty))
        pp = g.scene.to_nonlocal((pl.x, pl.y))
        g.cam.x += (pp[0] - pc[0]) / 10
        g.cam.y += (pp[1] - pc[1]) / 10

        oa = pl.angle
        oy = pl.y
        ox = pl.x

        g.tick()
        if g.cam.y > 0:
            g.cam.y = 0
        gr.x = g.cam.x

        td.x = g.cam.x
        td.y = g.cam.y

        if pl.angle > 180:
            pl.angle = 360 - pl.angle
        if pl.angle < -180:
            pl.angle = 360 + pl.angle
        pl.angle *= 0.997
        na = pl.angle
        ny = pl.y
        nx = pl.x

        pl.calc_speed(nx - ox, ny - oy, na - oa)
        dist = (pl.x - 100) / 100
        hght = -(pl.y - 860) / 100

        if dist > g.stats.max_dist:
            g.stats.max_dist = dist
        if hght > g.stats.max_height:
            g.stats.max_height = hght
        if pl.v > g.stats.max_speed:
            g.stats.max_speed = pl.v

        txt = f'Height: {round(hght,2)} ({round(g.stats.max_height,2)})\n'
        txt += f'Distance: {round(dist,2)} ({round(g.stats.max_dist,2)})\n'
        txt += f'Speed: {round(pl.v,2)} ({round(g.stats.max_speed,2)})'
        td.text = txt

        color = tuple([
            (max(g.cam.y, ye) - ys) * (bge[i] - bgs[i]) / (ye - ys) + bgs[i]
            for i in range(3)
        ])
        bg.color = color

        if pl.y > 860:
            g.stop()

        g.draw()

    g.going = True
    g.ih.unbind_key(pygame.K_a)
    g.ih.unbind_key(pygame.K_d)
    pl.xv = 0
    pl.yv = 0
    pl.rv = 0
    pl.stop_counterclock()
    pl.stop_clockwise()

def main():
    pygame.init()
    screen = pygame.display.set_mode((960, 540), pygame.HWSURFACE | pygame.DOUBLEBUF)
    g = Game(screen)

    sb = ButtonImage(g.stop, 80, 170, 'imgs/playbutton.png', g.cam)
    sb.x = g.cam.x + g.cam.w / 2 - sb.w
    sb.y = g.cam.y + g.cam.h / 2
    ts = ImageThing('imgs/pps2k7.png', g.cam)
    ts.x = g.cam.x + g.cam.w / 2 - ts.w
    ts.y = g.cam.y + g.cam.h / 2 - ts.h * 1.5

    g.scene.add(ColorBackground((255, 255, 255), 960, 540))
    g.scene.add(ts)
    g.scene.add(sb)

    g.ih.bind_mouse(down_action=sb.callback, move_action=sb.mouseover)

    while g.going:
        g.tick()
        g.draw()

    g.going = True
    g.scene.children = []

    rb = ButtonImage(g.stop, 80, -30, 'imgs/retrybutton.png', g.cam)
    g.ih.bind_mouse(down_action=rb.callback, move_action=rb.mouseover)

    td = TextDisplay(BLACK, 30)

    while not g.actuallystop:

        play_game(g, td, 0.1, 10)

        g.scene.add(rb)
        rb.x = g.cam.x + g.cam.w / 2 - rb.w
        rb.y = g.cam.y + g.cam.h / 2 - rb.h * 2

        while g.going and not g.actuallystop:
            g.tick()
            g.draw()

        g.going = True

    pygame.quit()

if __name__=="__main__":
    main()
