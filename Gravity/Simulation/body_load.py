import pygame
from pygame.locals import *

from lib.Math.Vector import Vector2

from Gravity.Simulation.Body import Body

import json

def load_bodies(filename, window_info):
    with open(filename, 'r') as file:
        data = json.loads(file.read())

    bodies = []
    for body_json in data:
        pos = Vector2(body_json['position']['x'] * window_info.width, body_json['position']['y'] * window_info.height)
        vel = Vector2(body_json['velocity']['x'], body_json['velocity']['y'])
        
        rad = body_json['radius']
        mass = body_json['mass']

        color = body_json['color']

        bodies.append(Body(pos, vel, rad, mass, color))

    return bodies