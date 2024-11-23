from render.render import BaseApp
from render.utils import WindowSize

import numpy as np
from scipy.ndimage import convolve
import glfw.GLFW as GLFW_CONSTANTS


class BriansBrainGame(BaseApp):
    def __init__(self, seed: int = None) -> None:
        super().__init__()
        self.matrix = None
        self.seed = seed
        self.set_window_title("Brian's Brain")
        self.set_window_size(WindowSize(800, 600))
        self.add_event_key_callback(self.step, GLFW_CONSTANTS.GLFW_KEY_T)
        self.add_event_key_callback(self.reset, GLFW_CONSTANTS.GLFW_KEY_R)
        self.need_to_generate = True

        self.matrix_size = 50  # Adjust size as needed
        self.reset()

    def update(self) -> None:
        if self.need_to_generate:
            self.scene.delete_all_cubes()
            self.create_cubes()
            self.renderer.update_instance_buffer(self.scene.cubes)
            self.renderer.prepare_instance_data()
            self.need_to_generate = False

    def create_cubes(self):
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                for z in range(self.matrix_size):
                    state = self.matrix[x, y, z]
                    if state == 1:  # On
                        texture_name = "gray.png"  # Ensure this texture exists
                    elif state == 2:  # Dying
                        texture_name = "wave.png"  # Ensure this texture exists
                    else:
                        continue  # Skip Off cells
                    self.scene.add_cube(x, y, z, texture_name=texture_name)

    def reset(self):
        self.matrix = np.random.choice([0, 1], size=(self.matrix_size, self.matrix_size, self.matrix_size), p=[0.8, 0.2])
        self.need_to_generate = True

    def step(self):
        kernel = np.ones((3, 3, 3), dtype=int)
        kernel[1, 1, 1] = 0
        neighbor_count = convolve((self.matrix == 1).astype(int), kernel, mode='constant', cval=0)

        new_matrix = np.zeros_like(self.matrix)

        new_matrix[self.matrix == 1] = 2
        new_matrix[self.matrix == 2] = 0
        new_matrix[(self.matrix == 0) & (neighbor_count == 2)] = 1

        self.matrix = new_matrix
        self.need_to_generate = True