from collections import namedtuple
import os

import pygame as pg

pg.init()

# Couleur de fond de la fenêtre OpenGL
CLEAR_COLOR = (0.1, 0.1, 0.2, 1.0)
# Taille de la fenêtre
WINDOW_SIZE = (800, 600)
# Nom de la fenêtre
WINDOW_NAME = "OpenGL"
FPS = 100

SHADERS_DIR = "shaders"
TEXTURES_DIR = "textures"

WAVE_TEXTURE_PATH = os.path.join(TEXTURES_DIR,"wave.png")

# named tuple Coord
Coord = namedtuple('Coord', ['x', 'y', 'z'])

MATRIX_SIZE = 200
TILE_SIZE = 10
STEP = MATRIX_SIZE//TILE_SIZE