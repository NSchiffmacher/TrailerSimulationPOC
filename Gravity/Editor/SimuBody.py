import pygame
from pygame.locals import *

from lib.Math.Vector import Vector2

from Gravity.Simulation.Body import Body
from Gravity.Editor.PathDrawer import PathDrawer

class SimuBody(Body):
    def __init__(self, pos, vel, radius, mass, color, pathdrawer_width):
        super().__init__(pos, vel, radius, mass, color)
        self.render_body = Body(pos, vel, radius, mass, color)
        self.path = PathDrawer(color, pathdrawer_width)

        self.start_pos = Vector2(pos.x, pos.y)
        self.start_vel = Vector2(vel.x, vel.y)

    def move_to(self, pos):
        self.start_pos = pos

    def clear(self):
        self.position = Vector2(self.start_pos.x, self.start_pos.y)
        self.velocity = Vector2(self.start_vel.x, self.start_vel.y)

        self.render_body.position = Vector2(self.start_pos.x, self.start_pos.y)
        self.render_body.velocity = Vector2(self.start_vel.x, self.start_vel.y)

        self.path.clear()

    
    def distance_to_point_squared(self, point):
        return (point - self.render_body.position).mag_sqr()

    def update(self, dt):
        super().update(dt)

    def update_nodes(self):
        self.path.add_node(self.position)

    def draw(self, window):
        self.path.draw(window)
        self.render_body.draw(window)