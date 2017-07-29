import pygame


def add(dct, val, itm):
    d = dct.get(val, [])
    d.append(itm)
    dct[val] = d


class InputHandler:
    def __init__(self):
        self.assoc_down = dict()
        self.assoc_up = dict()
        self.mdown = []
        self.mup = []
        self.mmove = []
        self.stop = []

    def bind_key(self, key, down_action=None, up_action=None):
        if down_action is not None:
            add(self.assoc_down, key, down_action)
        if up_action is not None:
            add(self.assoc_up, key, up_action)

    def unbind_key(self, key):
        self.assoc_up[key] = []
        self.assoc_down[key] = []

    def bind_mouse(self, down_action=None, up_action=None, move_action=None):
        if down_action is not None:
            self.mdown.append(down_action)
        if up_action is not None:
            self.mup.append(up_action)
        if move_action is not None:
            self.mmove.append(move_action)

    def bind_stop(self, action=None):
        if action is not None:
            self.stop.append(action)

    def tick(self, evtlist):
        for evt in evtlist:
            if evt.type == pygame.KEYDOWN:
                if evt.key in self.assoc_down:
                    for func in self.assoc_down[evt.key]:
                        func(evt.mod)
            elif evt.type == pygame.KEYUP:
                if evt.key in self.assoc_up:
                    for func in self.assoc_up[evt.key]:
                        func(evt.mod)
            elif evt.type == pygame.MOUSEBUTTONDOWN:
                for func in self.mdown:
                    func(evt.pos, evt.button)
            elif evt.type == pygame.MOUSEBUTTONUP:
                for func in self.mup:
                    func(evt.pos, evt.button)
            elif evt.type == pygame.MOUSEMOTION:
                for func in self.mmove:
                    func(evt.pos, evt.rel, evt.buttons)
            elif evt.type == pygame.QUIT:
                for func in self.stop:
                    func()