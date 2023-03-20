import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

from lib.Math.Vector import Vector2 as V
import math

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

def draw_rotated_rectangle(fenetre, reference_point: V, theta: float, size: V, offset: V):
    """
        reference_point: Vector2 -> The position of the reference point in the global frame
        theta: float -> The angle between the rectangles frame and the global frame (x axis is theta = 0, in degrees)
        size: Vector2 -> The size of the rectangle, in the rectangles frame (if it means something)
        offset: The position of the reference point in the rectangles frame ()
    """
    origin_global_frame = V(
        reference_point.x - offset.x * size.x * math.cos(math.radians(theta)),
        reference_point.y - offset.y * size.y * math.cos(math.radians(theta)),
    )

class Scene(BaseScene):
    def load(self):
        self.window_size = V(self.app.options.window.width, self.app.options.window.height)

    def global_frame_to_draw_frame(self, vector: V):
        """
        Takes a vector in the global frame as input, and returns the vector in the drawing frame
        """
        # res.x = vector.x * scale_factor + window_width / 2
        # res.y = -vector.y * scale_factor + window_height / 2

        u = self.options.unit_vector_size_in_px
        return V(vector) * V(u, -u) + self.window_size / 2

    def draw_point(self, point: V, color: tuple, radius=5):
        """
        Draws a point on the window

        Arguments:
            point: Vector2 -> The point's position in the global frame
            color: tuple -> color in rgb
            radius: int -> Radius in px
        """
        pygame.draw.circle(self.window, color, self.global_frame_to_draw_frame(point).to_pygame(), radius)
    
    def draw_line(self, pointA: V, pointB: V, color: tuple, width: int):
        """
        Draws a line on the window

        Arguments:
            pointA: Vector2 -> One of the endpoints in the global frame
            pointB: Vector2 -> The second endpoint in the global frame
            color: tuple -> color in rgb
            width: int -> width of the line
        """
        pygame.draw.line(self.window, color, self.global_frame_to_draw_frame(pointA).to_pygame(), self.global_frame_to_draw_frame(pointB).to_pygame(), width)

    def draw_reference_frame(self, position: V, theta: float, scale_factor: float=1):
        """
        Draws a custom reference frame (x is red, y is green)

        Arguments:
            position: Vector2 -> The reference frame's position in the global frame
            theta: float -> The angle between the global x axis and it's x axis (degrees)
            scale_factor: float -> shrink the size of the unit vectors 
        """

        rotated_x_axis = V(math.cos(math.radians(theta)), math.sin(math.radians(theta)))
        rotated_y_axis = V(-math.sin(math.radians(theta)), math.cos(math.radians(theta)))

        self.draw_line(position, position + rotated_x_axis, RED, 2)
        self.draw_line(position, position + rotated_y_axis, GREEN, 2)



    def update(self, dt, events):
        pass

    def physics_update(self, dt):
        pass


    def draw(self, fenetre):
        # self.draw_point(V(10,5), (0, 255, 255))
        self.draw_reference_frame(V(0,0), 0, 0.5)
        self.draw_reference_frame(V(3,2), 45)
