from sim.cube import CubeMesh
from sim.material import Material

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import numpy as np


class GraphicsEngine:
    def __init__(self):
        self.cube_meshs = CubeMesh()
        self.wave_texture = Material("textures/wave.png")

        glClearColor(0.1,0.1,0.2,1) 
        self.shaders = self._create_shaders("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shaders)
        glUniform1i(glGetUniformLocation(self.shaders, "imageTexture"), 0)
        glEnable(GL_BLEND)  
        glEnable(GL_DEPTH_TEST)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=90, aspect=640/480,
            near=0.1, far=1000, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shaders, "projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shaders, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shaders, "view")
        
    def render(self,scene):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shaders)

        # Crée une matrice d'identité pour le modèle
        view_transform = pyrr.matrix44.create_look_at(
            eye = scene.player.position, 
            target=scene.player.position+scene.player.forwards,
            up = scene.player.up,
            dtype=np.float32)
        glUniformMatrix4fv(self.viewMatrixLocation,1,GL_FALSE,view_transform)

        self.wave_texture.use()
        glBindVertexArray(self.cube_meshs.vao)  # Lie le VAO du cube
        for cube in scene.cubes:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(cube.eulers),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=cube.position,
                    dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_meshs.vertex_count)  # Dessine le cube
        glFlush()

    def quit(self):
        self.cube_meshs.destroy()  # Détruit la mesh du cube
        self.wave_texture.destroy()  # Détruit la texture
        glDeleteProgram(self.shaders)  # Supprime le programme de shaders

        
        

    @staticmethod
    def _create_shaders(vertex_path, fragment_path):
        with open(vertex_path, 'r') as file:
            vertex_src = file.read()  # Lit le code source du vertex shader
    
        with open(fragment_path, 'r') as file:
            fragment_src = file.read()  # Lit le code source du fragment shader
    
        # Compile les shaders et les lie ensemble dans un programme
        shaders = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        return shaders