# Pygame imports
import pygame
from pygame.locals import *

# Other imports
import threading

# Library imports
from lib.BaseScene import BaseScene
from lib.Math.Vector import Vector2

# Gravity imports
from Gravity.Simulation.Body import Body
from Gravity.Simulation.body_load import load_bodies
from Gravity.Editor.SimuBody import SimuBody
from Gravity.Editor.SidePanel import SidePanel



import time

BODIES_FILE = "Gravity/Simulation/bodies.json"

class Scene(BaseScene):
    def load(self):
        self.bodies = load_bodies(BODIES_FILE, self.app.options.window)

        # Simu bodies contains a copy of the initial bodies, they
        # Will be used to compute the path of the differents bodies without actually moving them


        # HUD Components
        self.side_panel = SidePanel(self.window, self.options)
        self.side_panel.load_all()


        # Simulation Bodies
        self.current_steps_no = 0
        self.redraw_steps = True
        self.current_body_dragged = None
        self.dragged_offset = None

        self.simu_bodies = []
        for body in self.bodies:
            self.simu_bodies.append(SimuBody(body.position, body.velocity, body.radius, body.mass, body.color, int(body.radius * self.options.path_width_ratio)))


        # Threading stuff'
        threading.Thread(target=self.draw_path_thread).start()


        # App options
        self.last = time.time()

    def update(self, dt, events):
        t = time.time()

        
        if events.mouse.left.double_click:
            self.redraw_steps = True
        
        if events.mouse.left.down_rn:
            mouse_pos = events.mouse.pos()
            for body in self.simu_bodies:
                if body.distance_to_point_squared(mouse_pos) < body.radius ** 2:
                    self.current_body_dragged = body
                    self.last_mouse_pos = self.events.mouse.pos()

                    self.dragged_offset = body.render_body.position - mouse_pos

        elif events.mouse.left.up:
            # On le fait dès qu'on relache la souris,
            # Mais je pense que c'est quand même plus rapide
            self.current_body_dragged = None

        
        if self.current_body_dragged:
            mouse_pos = events.mouse.pos()
            if not (mouse_pos + self.dragged_offset).equals(self.current_body_dragged.start_pos):
                self.current_body_dragged.move_to(mouse_pos + self.dragged_offset)
                self.redraw_steps = True
            self.last_mouse_pos = mouse_pos
        
        self.side_panel.update(events)
        # print(time.time() - t)
        

    def on_swap_scene(self):
        self.swap_scene("Gravity/Simulation")


    def physics_update(self, dt):
        pass

    
    def draw_path_thread(self):
        while self.continuer:
            if self.current_steps_no < self.options.path_draw_steps:
                self.step()

            if self.redraw_steps:
                self.redraw_steps = False
                self.current_steps_no = 0

                for body in self.simu_bodies:
                    body.clear()

    def step(self):
        for body1 in self.simu_bodies:
            for body2 in self.simu_bodies:
                if body1 != body2:
                    # Body 1 "recoit" l'attraction de body2
                    distance = (body2.position - body1.position)
                    # print(distance)
                    r2 = distance.mag_squared()

                    force = distance.to_mag(self.app.options.GravitationalConstant * body1.mass * body2.mass / r2)
                    body1.apply_force(force)
        

        for body in self.simu_bodies:
            body.update(self.options.path_draw_dt)
            if self.current_steps_no % self.options.path_draw_interval == 0:
                body.update_nodes()

        self.current_steps_no += 1

    def draw(self, fenetre):
        # for body in self.simu_bodies:
        #     body.draw(fenetre)
            
        self.side_panel.draw()
