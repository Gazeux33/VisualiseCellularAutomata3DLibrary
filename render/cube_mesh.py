from typing import Tuple

import numpy as np
from OpenGL.GL import *


class CubeMesh:
    def __init__(self) -> None:
        vertices: Tuple = (-0.5, -0.5, -0.5, 0, 0,
                           0.5, -0.5, -0.5, 1, 0,
                           0.5, 0.5, -0.5, 1, 1,
                           0.5, 0.5, -0.5, 1, 1,
                           -0.5, 0.5, -0.5, 0, 1,
                           -0.5, -0.5, -0.5, 0, 0,
                           -0.5, -0.5, 0.5, 0, 0,
                           0.5, -0.5, 0.5, 1, 0,
                           0.5, 0.5, 0.5, 1, 1,
                           0.5, 0.5, 0.5, 1, 1,
                           -0.5, 0.5, 0.5, 0, 1,
                           -0.5, -0.5, 0.5, 0, 0,
                           -0.5, 0.5, 0.5, 1, 0,
                           -0.5, 0.5, -0.5, 1, 1,
                           -0.5, -0.5, -0.5, 0, 1,
                           -0.5, -0.5, -0.5, 0, 1,
                           -0.5, -0.5, 0.5, 0, 0,
                           -0.5, 0.5, 0.5, 1, 0,
                           0.5, 0.5, 0.5, 1, 0,
                           0.5, 0.5, -0.5, 1, 1,
                           0.5, -0.5, -0.5, 0, 1,
                           0.5, -0.5, -0.5, 0, 1,
                           0.5, -0.5, 0.5, 0, 0,
                           0.5, 0.5, 0.5, 1, 0,
                           -0.5, -0.5, -0.5, 0, 1,
                           0.5, -0.5, -0.5, 1, 1,
                           0.5, -0.5, 0.5, 1, 0,
                           0.5, -0.5, 0.5, 1, 0,
                           -0.5, -0.5, 0.5, 0, 0,
                           -0.5, -0.5, -0.5, 0, 1,
                           -0.5, 0.5, -0.5, 0, 1,
                           0.5, 0.5, -0.5, 1, 1,
                           0.5, 0.5, 0.5, 1, 0,
                           0.5, 0.5, 0.5, 1, 0,
                           -0.5, 0.5, 0.5, 0, 0,
                           -0.5, 0.5, -0.5, 0, 1)

        self.vertex_count: int = len(vertices) // 5
        self.vertices: np.ndarray = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # VBO pour les données de vertex
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Attributs des vertex
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

        # VBO pour les données d'instance (matrices de modèle)
        self.instanceVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.instanceVBO)
        # Nous initialiserons les données plus tard

        # Attributs par instance (matrices de modèle)
        stride = 64  # 4 matrices de 4 floats (16 floats * 4 bytes)
        for i in range(4):
            glEnableVertexAttribArray(2 + i)
            glVertexAttribPointer(2 + i, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(16 * i))
            glVertexAttribDivisor(2 + i, 1)

    def update_instance_data(self, instance_data: np.ndarray) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.instanceVBO)
        glBufferData(GL_ARRAY_BUFFER, instance_data.nbytes, instance_data, GL_STATIC_DRAW)

    def destroy(self) -> None:
        glDeleteBuffers(1, [self.vbo, self.instanceVBO])
        glDeleteVertexArrays(1, [self.vao])