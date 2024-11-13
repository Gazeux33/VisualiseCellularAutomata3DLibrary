import numpy as np
from OpenGL.GL import *

class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)  # Position du cube
        self.eulers = np.array(eulers, dtype=np.float32)  # Angles d'Euler du cube (rotation)

class CubeMesh:
    def __init__(self):

        # Coordonnées des sommets du cube (x, y, z) et coordonnées de texture (s, t)
        vertices = (-0.5, -0.5, -0.5, 0, 0,
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
        self.vertex_count = len(vertices) // 5  # Compte le nombre de sommets
        self.verticles = np.array(vertices, dtype=np.float32)  # Convertit les sommets en array numpy

        self.vao = glGenVertexArrays(1)  # Génère un objet Vertex Array Object
        glBindVertexArray(self.vao)  # Lie le VAO créé pour qu'il soit utilisé pour les opérations suivantes
        self.vbo = glGenBuffers(1)  # Génère un objet Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)  # Lie le VBO créé pour qu'il soit utilisé pour les opérations suivantes
        glBufferData(GL_ARRAY_BUFFER, self.verticles.nbytes, self.verticles, GL_STATIC_DRAW)  # Remplit le VBO avec les données des sommets

        glEnableVertexAttribArray(0)  # Active l'attribut de sommet à l'emplacement 0 (les positions des sommets)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))  # Spécifie la disposition des coordonnées des sommets

        glEnableVertexAttribArray(1)  # Active l'attribut de sommet à l'emplacement 1 (les coordonnées de texture)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))  # Spécifie la disposition des coordonnées de texture

    def destroy(self):
        glDeleteVertexArrays(1, self.vao)  # Supprime le VAO
        glDeleteBuffers(1, self.vbo)  # Supprime le VBO