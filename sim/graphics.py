from typing import Tuple

from sim.cube import CubeMesh
from sim.material import Material
from sim.scene import Scene
from sim.utils import WindowSize,Color

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
import pyrr
import numpy as np


class GraphicsEngine:
    def __init__(self, window_size: WindowSize, clear_color: Color = (0.1, 0.1, 0.2, 1)) -> None:
        self.window_size = window_size
        self.cube_mesh: CubeMesh = CubeMesh()
        self.wave_texture: Material = Material("textures/pastel.png")

        self.near = 0.1
        self.far = 100
        self.fov = 90

        glClearColor(*clear_color)
        self.shaders = self._create_shaders("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shaders)
        glUniform1i(glGetUniformLocation(self.shaders, "imageTexture"), 0)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        # Stocker l'emplacement de la matrice de projection
        self.projectionMatrixLocation = glGetUniformLocation(self.shaders, "projection")

        # Initialiser la matrice de projection
        self._update_projection_matrix(window_size.width, window_size.height)

        self.modelMatrixLocation = glGetUniformLocation(self.shaders, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shaders, "view")

    def render(self,scene:Scene):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shaders)

        view_transform = pyrr.matrix44.create_look_at(
            eye = scene.player.position,
            target=scene.player.position+scene.player.forwards,
            up = scene.player.up,
            dtype=np.float32)
        glUniformMatrix4fv(self.viewMatrixLocation,1,GL_FALSE,view_transform)

        self.wave_texture.use()
        glBindVertexArray(self.cube_mesh.vao)  # Lie le VAO du cube
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
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)  # Dessine le cube
        glFlush()

    def quit(self) -> None:
        self.cube_mesh.destroy()  # Détruit la mesh du cube
        self.wave_texture.destroy()  # Détruit la texture
        glDeleteProgram(self.shaders)  # Supprime le programme de shaders

    @staticmethod
    def _create_shaders(vertex_path: str, fragment_path: str) -> ShaderProgram:
        def read_shader_source(path: str) -> str:
            with open(path, 'r') as file:
                return file.read()

        vertex_src = read_shader_source(vertex_path)
        fragment_src = read_shader_source(fragment_path)

        shaders = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        return shaders

    @staticmethod
    def set_clear_color(color:Color)->None:
        glClearColor(*color)


    def update_projection_matrix(self, width: int, height: int) -> None:
        glUseProgram(self.shaders)
        self._update_projection_matrix(width, height)

    def _update_projection_matrix(self, width: int, height: int) -> None:
        aspect_ratio = width / height
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=self.fov, aspect=aspect_ratio,
            near=self.near, far=self.far, dtype=np.float32
        )
        glUniformMatrix4fv(
            self.projectionMatrixLocation,
            1, GL_FALSE, projection_transform
        )

    def set_near(self,near:float)->None:
        self.near = near
        self._update_projection_matrix(self.window_size.width,self.window_size.height)

    def set_far(self,far:float)->None:
        self.far = far
        self._update_projection_matrix(self.window_size.width,self.window_size.height)

    def set_fov(self,fov:float)->None:
        self.fov = fov
        self._update_projection_matrix(self.window_size.width,self.window_size.height)


