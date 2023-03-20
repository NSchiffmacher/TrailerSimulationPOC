import pygame
from pygame.locals import *

from lib.Math.Vector import Vector2



class Body:
    def __init__(self, pos, vel, radius, mass, color):
        self.position       = pos
        self.velocity       = vel
        self.acceleration   = Vector2()

        self.radius         = radius
        self.mass           = mass
        self.color          = color

        self.forces         = Vector2()

    def apply_force(self, force):
        self.forces += force

    def update(self, dt):
        self.acceleration   =  self.forces / self.mass
        self.velocity       += self.acceleration * dt
        self.position       += self.velocity * dt
        
        # Reset forces for next physics frame
        self.forces = Vector2()
    
    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )