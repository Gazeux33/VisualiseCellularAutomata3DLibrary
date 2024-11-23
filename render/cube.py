from render.utils import Position

import numpy as np

class Cube:
    def __init__(self, position: Position, eulers: Position = (0, 0, 0), texture_name: str = None) -> None:
        self.position: np.ndarray = np.array(position, dtype=np.float32)
        self.eulers: np.ndarray = np.array(eulers, dtype=np.float32)
        self.texture_name = texture_name if texture_name is not None else "default_texture.png"