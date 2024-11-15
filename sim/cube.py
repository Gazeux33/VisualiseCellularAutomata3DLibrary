from typing import List, Tuple

import numpy as np
from OpenGL.GL import *

from sim.utils import Position

class Cube:
    def __init__(self, position:Position, eulers:Position=(0,0,0)) -> None:
        self.position: np.ndarray  = np.array(position, dtype=np.float32)
        self.eulers: np.ndarray  = np.array(eulers, dtype=np.float32)

class CubeMesh:
    def __init__(self) -> None:
        vertices:Tuple= (-0.5, -0.5, -0.5, 0, 0,
                    0.5, -0.5, -0.5, 1, 0,
                    0.5,  0.5, -0.5, 1, 1,
                    0.5,  0.5, -0.5, 1, 1,
                    -0.5,  0.5, -0.5, 0, 1,
                    -0.5, -0.5, -0.5, 0, 0,
                    -0.5, -0.5,  0.5, 0, 0,
                    0.5, -0.5,  0.5, 1, 0,
                    0.5,  0.5,  0.5, 1, 1,
                    0.5,  0.5,  0.5, 1, 1,
                    -0.5,  0.5,  0.5, 0, 1,
                    -0.5, -0.5,  0.5, 0, 0,
                    -0.5,  0.5,  0.5, 1, 0,
                    -0.5,  0.5, -0.5, 1, 1,
                    -0.5, -0.5, -0.5, 0, 1,
                    -0.5, -0.5, -0.5, 0, 1,
                    -0.5, -0.5,  0.5, 0, 0,
                    -0.5,  0.5,  0.5, 1, 0,
                    0.5,  0.5,  0.5, 1, 0,
                    0.5,  0.5, -0.5, 1, 1,
                    0.5, -0.5, -0.5, 0, 1,
                    0.5, -0.5, -0.5, 0, 1,
                    0.5, -0.5,  0.5, 0, 0,
                    0.5,  0.5,  0.5, 1, 0,
                    -0.5, -0.5, -0.5, 0, 1,
                    0.5, -0.5, -0.5, 1, 1,
                    0.5, -0.5,  0.5, 1, 0,
                    0.5, -0.5,  0.5, 1, 0,
                    -0.5, -0.5,  0.5, 0, 0,
                    -0.5, -0.5, -0.5, 0, 1,
                    -0.5,  0.5, -0.5, 0, 1,
                    0.5,  0.5, -0.5, 1, 1,
                    0.5,  0.5,  0.5, 1, 0,
                    0.5,  0.5,  0.5, 1, 0,
                    -0.5,  0.5,  0.5, 0, 0,
                    -0.5,  0.5, -0.5, 0, 1)
        self.vertex_count:int = len(vertices) // 5
        self.vertices: np.ndarray = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1) 
        glBindVertexArray(self.vao)  
        self.vbo = glGenBuffers(1)  
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)  
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)  

        glEnableVertexAttribArray(0)  
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))  

        glEnableVertexAttribArray(1) 
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))  

    def destroy(self) -> None:
        glDeleteVertexArrays(1, self.vao)  
        glDeleteBuffers(1, self.vbo)  