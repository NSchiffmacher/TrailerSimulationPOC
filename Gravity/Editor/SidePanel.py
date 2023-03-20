import pygame
from pygame.locals import *

from lib.Math.Vector import Vector2
from lib.Options import Container

from lib.HUD.Canvas import Canvas
from lib.HUD.Button import Button
from lib.HUD.RoundedRect import RoundedRect

from Gravity.Editor.ease import EaseInOut

import fontawesome as fa
import time


class SidePanel(Canvas):
    TRANSPARENT = Canvas.TRANSPARENT

    def __init__(self, parent, options, background_color: list or int or None = TRANSPARENT, position: Vector2 or None = None, size: Vector2 or None = None):
        super().__init__(parent, background_color, position, size)
        self.options = options

        self.panel_moving = False
        self.ease = None
        self.panel_state = 'left' # Next direction

        

    def load(self):
        options = self.options.side_panel
        # Canvas stuff
        self.set_size_from_ratio(Vector2(options.size.x,options.size.y)).center_vertically_ratio(0)
        super().load()

        # Background
        self.background = RoundedRect(self).set_position(Vector2(0,0)).set_size_from_ratio(Vector2(1,1))
        self.background.set_corners(RoundedRect.RIGHT).set_radius(self.options.side_panel.radius).set_color(self.options.side_panel.background_color).add_to_canvas(self)

        # Bouton
        font = pygame.font.Font(options.button.font, options.button.font_size)
        self.button = Button(self, button_font=font, button_text=fa.icons[options.button.icon_left]).set_size_from_ratio(Vector2(options.button.size_x, 1)).set_position_ratio(Vector2(1-options.button.size_x, 0))
        self.button.set_radius(options.radius).set_colors({
            "normal"    : options.button.colors.normal,
            "hover"     : options.button.colors.hover,
            "pressed"   : options.button.colors.pressed,
            "label"     :options.button.colors.label
        }).set_callbacks({
            'RELEASED'  : self.button_callback
        })
        self.button.set_corners(RoundedRect.RIGHT).add_to_canvas(self)

    def button_callback(self):
        options = self.options.side_panel
        if not self.panel_moving:
            self.panel_moving = True
            if self.panel_state == 'left':
                self.panel_state = 'right'
                self.button.change_text(fa.icons[options.button.icon_right])
                self.ease = EaseInOut(time.time(), options.anim_length, 0, -self.size.x + self.button.size.x)
            else:
                self.panel_state = 'left'
                self.button.change_text(fa.icons[options.button.icon_left])
                self.ease = EaseInOut(time.time(), options.anim_length, -self.size.x + self.button.size.x, 0)




    def update(self, events):
        self.button.update(events)

        if self.panel_moving:
            t = time.time()
            x = int(self.ease.eval(time.time()))
            self.center_vertically(x)
            if self.ease.done:
                self.panel_moving = False