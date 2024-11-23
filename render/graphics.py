from typing import List

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
import numpy as np
import pyrr

from render.cube import Cube
from render.cube_mesh import CubeMesh
from render.material import Material
from render.scene import Scene
from render.utils import Color, WindowSize
from render.config import *

class GraphicsEngine:
    def __init__(self, window_size: WindowSize, clear_color: Color = (0.1, 0.1, 0.2, 1)) -> None:
        self.instance_data_per_texture = None
        self.cubes_by_texture = None
        self.window_size = window_size
        self.cube_mesh: CubeMesh = CubeMesh()
        self.wave_texture: Material = Material("textures/gray_bordure.png")

        self.near = NEAR
        self.far = FAR
        self.fov = FOV

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

        self.viewMatrixLocation = glGetUniformLocation(self.shaders, "view")

        # Compteur d'instances
        self.instance_count = 0

        self.textures = {}

    def render(self, scene: Scene):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shaders)

        view_transform = pyrr.matrix44.create_look_at(
            eye=scene.player.position,
            target=scene.player.position + scene.player.forwards,
            up=scene.player.up,
            dtype=np.float32)
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        glBindVertexArray(self.cube_mesh.vao)

        for texture_name, instance_data in self.instance_data_per_texture.items():
            # Utiliser la texture appropriée
            texture = self.get_texture(texture_name)
            texture.use()

            # Mettre à jour les données d'instance
            self.cube_mesh.update_instance_data(instance_data)

            # Dessiner les cubes
            instance_count = len(instance_data)
            glDrawArraysInstanced(GL_TRIANGLES, 0, self.cube_mesh.vertex_count, instance_count)


    def get_texture(self, texture_name: str) -> 'Material':
        if texture_name not in self.textures:
            self.textures[texture_name] = Material(f"textures/{texture_name}")
        return self.textures[texture_name]

    def update_instance_buffer(self, cubes: List[Cube]) -> None:
        # Regrouper les cubes par texture
        self.cubes_by_texture = {}
        for cube in cubes:
            texture_name = cube.texture_name
            if texture_name not in self.cubes_by_texture:
                self.cubes_by_texture[texture_name] = []
            self.cubes_by_texture[texture_name].append(cube)

    def prepare_instance_data(self):
        self.instance_data_per_texture = {}
        for texture_name, cubes in self.cubes_by_texture.items():
            instance_data = []
            for cube in cubes:
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
                instance_data.append(model_transform)
            instance_data = np.array(instance_data, dtype=np.float32)
            self.instance_data_per_texture[texture_name] = instance_data

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