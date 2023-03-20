import pygame
from pygame.locals import *

from lib.Math.Vector import Vector2

class PathDrawer:
    def __init__(self, color, width):
        self.color = color
        self.width = width
        self.nodes = []

    def add_node(self, position):
        self.nodes.append(position)

    def clear(self):
        self.nodes = []

    def draw(self, window):
        if len(self.nodes) <= 1:
            return
        
        pointA = self.nodes[0]
        for pointB in self.nodes[1:]:
            pygame.draw.line(window, self.color, pointA.to_pygame(), pointB.to_pygame(), self.width)          
            pointA = pointB
