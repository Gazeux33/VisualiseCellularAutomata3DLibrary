from sim.render import BaseApp
from sim.utils import WindowSize,Color

from perlin_noise import PerlinNoise
import numpy as np

class LandScape(BaseApp):
    def __init__(self) -> None:
        super().__init__()
        self.step = 3
        self.set_window_title("LandScape")
        self.set_window_size(WindowSize(1000,800))
        self.matrix_size = 10
        self.noise_map = self.noise_map()

        self.create_cube_from_noise_map()





    def update(self) -> None:
        pass

    def noise_map(self) -> np.ndarray:
        noises = [PerlinNoise(octaves=octave) for octave in [3, 6, 12, 24]]
        weights = np.array([1, 0.5, 0.25, 0.125])

        x = np.linspace(0, 1, self.matrix_size)
        y = np.linspace(0, 1, self.matrix_size)

        pic = np.zeros((self.matrix_size, self.matrix_size))
        for noise, weight in zip(noises, weights):
            pic += weight * np.array([[noise([i, j]) for j in y] for i in x])
        return pic

    def create_cube_from_noise_map(self):
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                self.scene.add_cube(i, j, self.noise_map[i, j]*self.step)

