import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene
from lib.Math.Vector import Vector2

from Gravity.Simulation.Body import Body
from Gravity.Simulation.body_load import load_bodies

from Gravity.Editor.PathDrawer import PathDrawer

import time
import json

BODIES_FILE = "Gravity/Simulation/bodies.json"


class Scene(BaseScene):
    def load(self):
        self.bodies = load_bodies(BODIES_FILE, self.app.options.window)
        self.last = time.time()


    def update(self, dt, events):
        if events.mouse.left.double_click:
            print('Double Click')

    def on_swap_scene(self):
        self.swap_scene("Gravity/Editor")


    def physics_update(self, dt):
        for body1 in self.bodies:
            for body2 in self.bodies:
                if body1 != body2:
                    # Body 1 "recoit" l'attraction de body2
                    distance = (body2.position - body1.position)
                    # print(distance)
                    r2 = distance.mag_squared()

                    force = distance.to_mag(self.app.options.GravitationalConstant * body1.mass * body2.mass / r2)
                    body1.apply_force(force)

        for body in self.bodies:
            body.update(dt)

    
    def draw(self, fenetre):
        for body in self.bodies:
            body.draw(fenetre)
