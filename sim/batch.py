import numpy as np
from OpenGL.GL import *
import pyrr

from sim.frustrum import Frustum
from sim.player import Player
from sim.spatial import SpatialGrid
from sim.utils import Position


class InstanceBatch:
    def __init__(self, max_instances: int = 1000):
        self.max_instances = max_instances
        self.instance_count = 0
        self.transform_matrices = np.zeros((max_instances, 16), dtype=np.float32)
        self.visible_instances = np.zeros(max_instances, dtype=np.int32)
        self.dirty = True

        # Instance buffer for transform matrices
        self.instance_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.instance_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.transform_matrices.nbytes, None, GL_DYNAMIC_DRAW)

        # Configure instance attributes (4 vec4s for matrix)
        for i in range(4):
            glEnableVertexAttribArray(2 + i)
            glVertexAttribPointer(2 + i, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(i * 16))
            glVertexAttribDivisor(2 + i, 1)

    def update_instance(self, index: int, position: np.ndarray, rotation: np.ndarray) -> None:
        model_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        model_matrix = pyrr.matrix44.multiply(
            model_matrix,
            pyrr.matrix44.create_from_eulers(rotation, dtype=np.float32)
        )
        model_matrix = pyrr.matrix44.multiply(
            model_matrix,
            pyrr.matrix44.create_from_translation(position, dtype=np.float32)
        )

        self.transform_matrices[index] = model_matrix.flatten()
        self.dirty = True

    def upload_data(self) -> None:
        if not self.dirty:
            return

        glBindBuffer(GL_ARRAY_BUFFER, self.instance_buffer)
        glBufferSubData(GL_ARRAY_BUFFER, 0,
                        self.transform_matrices[:self.instance_count].nbytes,
                        self.transform_matrices[:self.instance_count])
        self.dirty = False


# Modifications to Scene class
class Scene:
    def __init__(self, position_player=Position(-6, 0, 0)) -> None:
        self.spatial_grid = SpatialGrid()
        self.instance_batch = InstanceBatch()
        self.frustum = Frustum()
        self.player = Player(position_player)
        self.cube_positions = []
        self.cube_rotations = []

    def add_cube(self, x: float, y: float, z: float) -> None:
        position = np.array([x, y, z], dtype=np.float32)
        rotation = np.zeros(3, dtype=np.float32)

        cube_id = len(self.cube_positions)
        self.cube_positions.append(position)
        self.cube_rotations.append(rotation)
        self.spatial_grid.add_cube(cube_id, position)
        self.instance_batch.update_instance(cube_id, position, rotation)
        self.instance_batch.instance_count += 1