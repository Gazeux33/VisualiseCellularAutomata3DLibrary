from sim.render import BaseApp
from sim.utils import WindowSize,Color

from perlin_noise import PerlinNoise
import numpy as np

class LandScape(BaseApp):
    def __init__(self,seed:int=None) -> None:
        super().__init__()
        self.start_octave = 1.3
        self.seed = seed
        self.step = 3
        self.set_window_title("LandScape")
        self.set_window_size(WindowSize(1000,800))
        self.matrix_size = 20
        self.noise_map = self.generate_noise_map()
        # 40 -> 1.7
        # 20 -> 1.1

        self.create_cube_from_noise_map()
        self.add_event_key_callback(self.regenerate_matrix,82)





    def update(self) -> None:
        pass

    def regenerate_matrix(self) -> None:
        self.scene.delete_all_cubes()
        self.noise_map = self.generate_noise_map()
        self.create_cube_from_noise_map()


    def generate_noise_map(self) -> np.ndarray:
        noises = [PerlinNoise(octaves=octave, seed=self.seed) for octave in [pow(self.start_octave, i) for i in range(4)]]
        weights = np.array([1, 0.5, 0.25, 0.125])

        x = np.linspace(0, 1, self.matrix_size)
        y = np.linspace(0, 1, self.matrix_size)

        pic = np.zeros((self.matrix_size, self.matrix_size))
        for noise, weight in zip(noises, weights):
            pic += weight * np.array([[noise([i, j]) for j in y] for i in x])
        return pic

    def create_cube_from_noise_map(self) -> None:
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                self.scene.add_cube(i, j, self.noise_map[i, j] * self.matrix_size)




