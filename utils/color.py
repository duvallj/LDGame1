import random


WHITE = (255,255,255)
BLACK = (0,0,0)

GRAY = (127,127,127)
RED = (200,0,0)
GREEN = (0,150,0)
BLUE = (10,10,180)


def offset_random(color, diff=10):
    return tuple([color[i]+random.randint(-diff, diff) for i in range(3)])


def offset_constant(color, diff):
    return tuple([color[i] + diff for i in range(3)])
