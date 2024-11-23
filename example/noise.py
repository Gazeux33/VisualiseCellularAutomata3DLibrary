import numpy as np
from perlin_noise import PerlinNoise
import glfw.GLFW as GLFW_CONSTANTS

from render.render import BaseApp
from render.utils import WindowSize


class PerlinNoiseVisualisation(BaseApp): # Inherit from BaseApp (3D visualisation library)
    def __init__(self) -> None:
        super().__init__()
        self.noise_map = None
        self.set_window_title("PerlinNoise") # Set window title
        self.set_window_size(WindowSize(1000, 800)) # Set window size
        self.matrix_size = 50 # Size of the matrix
        self.need_to_generate = True
        self.add_event_key_callback(self.regenerate_matrix, GLFW_CONSTANTS.GLFW_KEY_R) # Add key callback

    def update(self) -> None:
        if self.need_to_generate:
            self.noise_map = self.generate_noise_map()
            self.create_cube_from_noise_map()
            self.renderer.update_instance_buffer(self.scene.cubes)
            self.renderer.prepare_instance_data()
            self.need_to_generate = False

    def regenerate_matrix(self) -> None:
        self.scene.delete_all_cubes()
        self.noise_map = self.generate_noise_map()
        self.create_cube_from_noise_map()
        self.renderer.update_instance_buffer(self.scene.cubes)
        self.renderer.prepare_instance_data()

    def generate_noise_map(self) -> np.ndarray:
        noise = PerlinNoise(octaves=2.3)
        lin = np.linspace(0, 1, self.matrix_size, endpoint=False)
        x, y = np.meshgrid(lin, lin)
        pic = np.zeros((self.matrix_size, self.matrix_size))
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                pic[i][j] = noise([x[i][j], y[i][j]])
        return pic

    def create_cube_from_noise_map(self) -> None:
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
               # Add cube to the scene
                self.scene.add_cube(i, j, self.noise_map[i, j] * self.matrix_size,texture_name="pastel.png")

