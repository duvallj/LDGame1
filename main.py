import pygame
from utils.camera import Camera
from utils.triangle import *
from utils.color import *
from utils.input import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    scene = ContainerObject()
    going = True
    cam = Camera(screen, scene, xaccl=0.01, yaccl=0.01, maxv=2, xdccl=0.994, ydccl=0.994)

    ih = InputHandler()
    ih.bind_key(pygame.K_UP, cam.start_move_dir(90), cam.stop_move_dir(90))
    ih.bind_key(pygame.K_DOWN, cam.start_move_dir(270), cam.stop_move_dir(270))
    ih.bind_key(pygame.K_LEFT, cam.start_move_dir(180), cam.stop_move_dir(180))
    ih.bind_key(pygame.K_RIGHT, cam.start_move_dir(0), cam.stop_move_dir(0))

    gt = Triangle((0,0),(200,200),(100,300),2000,100,color=GREEN)
    ih.bind_key(pygame.K_q, gt.start_counterclock, gt.stop_counterclock)
    ih.bind_key(pygame.K_e, gt.start_clockwise, gt.stop_clockwise)

    scene.add(ColorBackground(BLACK))
    scene.add(Triangle((0,0),(500,500),(0,500),500,0,color=WHITE))
    scene.add(gt)

    while going:
        evtlist = pygame.event.get()
        for evt in evtlist:
            if evt.type == pygame.QUIT:
                going = False
        ih.tick(evtlist)

        scene.tick()
        cam.tick()
        cam.draw(screen)

if __name__=='__main__':
    main()