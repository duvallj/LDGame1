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
    cam = Camera(screen, scene)

    ih = InputHandler()
    ih.bind_key(pygame.K_UP, cam.start_move_up, cam.stop_move_up)
    ih.bind_key(pygame.K_DOWN, cam.start_move_down, cam.stop_move_down)
    ih.bind_key(pygame.K_LEFT, cam.start_move_left, cam.stop_move_left)
    ih.bind_key(pygame.K_RIGHT, cam.start_move_right, cam.stop_move_right)

    scene.add(ColorBackground(BLACK))
    scene.add(Triangle((0,0),(500,500),(0,500),WHITE,500,0))
    scene.add(Triangle((0,0),(200,200),(100,300),GREEN,2000,100))

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