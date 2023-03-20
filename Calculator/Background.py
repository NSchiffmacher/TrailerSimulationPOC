import pygame
from pygame.locals import *

import random, time

class Background():
    def __init__(self,width, height):
        self.width, self.height = width, height

        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(60)

        N = 1000
        for _ in range(N):
            self.add_circle()
            # print(x, y, r)

        self.last = time.time()
        self.add_interval = float('inf')


    def update(self):
        now = time.time()
        if now - self.last > self.add_interval:
            self.add_circle()
            self.last = now

    def add_circle(self):
        R = random.randint(0,255)
        G = random.randint(0,255)
        B = random.randint(0,255)
        color = (R, G, B)

        r = random.randint(20,100)
        # x = random.randint(r * 2, width - 2 * r)
        # y = random.randint(r * 2, height - 2 * r)
        x = random.randint(-r, self.width+r)
        y = random.randint(-r, self.height+r)

        pygame.draw.circle(self.surface, color, (x, y), r)

    def draw(self, fenetre):
        fenetre.blit(self.surface, (0,0))