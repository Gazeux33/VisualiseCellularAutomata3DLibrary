import numpy as np
from scipy.ndimage import convolve

from render.render import BaseApp
from render.utils import WindowSize

import glfw.GLFW as GLFW_CONSTANTS


class ConwayGame(BaseApp):
    def __init__(self, seed: int = None) -> None:
        super().__init__()
        self.matrix = None
        self.seed = seed
        self.set_window_title("Conway's Game of Life")
        self.set_window_size(WindowSize(1000, 800))
        self.add_event_key_callback(self.step, GLFW_CONSTANTS.GLFW_KEY_T)
        self.add_event_key_callback(self.reset, GLFW_CONSTANTS.GLFW_KEY_R)
        self.need_to_generate = True

        self.matrix_size = 10
        self.nb_birth = list(range(14, 20))
        self.nb_survive = list(range(13, 27))
        self.reset()

    def update(self) -> None:
        if self.need_to_generate:
            self.scene.delete_all_cubes()
            self.create_cube()
            self.renderer.update_instance_buffer(self.scene.cubes)
            self.renderer.prepare_instance_data()  # Assurez-vous d'appeler cette méthode
            self.need_to_generate = False

    def create_cube(self):
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                for z in range(self.matrix_size):
                    if self.matrix[x, y, z] == 1:
                        texture_name = "gray_bordure.png"
                        self.scene.add_cube(x, y, z, texture_name=texture_name)

    def reset(self):
        self.matrix = np.random.choice([0, 1], (self.matrix_size, self.matrix_size, self.matrix_size), p=[0.5, 0.5])
        self.need_to_generate = True

    def step(self):
        kernel = np.ones((3, 3, 3), dtype=int)
        kernel[1, 1, 1] = 0
        neighbor_count = convolve(self.matrix, kernel, mode='constant', cval=0)
        birth = (self.matrix == 0) & np.isin(neighbor_count, self.nb_birth)
        survive = (self.matrix == 1) & np.isin(neighbor_count, self.nb_survive)
        self.matrix[...] = 0
        self.matrix[birth | survive] = 1
        self.need_to_generate = True
