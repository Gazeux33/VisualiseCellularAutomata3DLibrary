from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

from config import *
from sim.cube import Cube,CubeMesh
from sim.material import Material


class Render:
    def __init__(self):
        self.running = True
        self._setup_pygame()
        self._setup_gl()
        self._setup_shaders()
        
        
        # Initialisation du cube avec sa position et sa rotation
        self.cube = Cube(position=[0, 0, -2], eulers=[0, 0, 0])
        self.cube_mesh = CubeMesh()  # Création de la mesh du cube
        self.texture = Material(WAVE_TEXTURE_PATH)  # Chargement de la texture du cube

        # Crée une matrice de projection en perspective ( Transforme la 3d en 2d pour le rendu a l'ecran)
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WINDOW_SIZE[0] / WINDOW_SIZE[1],
            near=0.1, far=10, dtype=np.float32
        )

        # Télécharge la matrice de projection sur le GPU
        glUniformMatrix4fv(
            glGetUniformLocation(self.shaders, "projection"),
            1, GL_FALSE, projection_transform
        )

        # Localisation de la matrice modèle sur le GPU
        self.modelMatrixLocation = glGetUniformLocation(self.shaders, "model")

    

    def launch(self):
        while self.running:
            self._event_handler()

            # Rotation du cube
            self.cube.eulers[2] += 0.2
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360

            # Efface la fenêtre
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram(self.shaders)
            self.texture.use()

            # Crée une matrice d'identité pour le modèle
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            # Applique la rotation à la matrice du modèle
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )
            # Applique la translation à la matrice du modèle
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )

            # Télécharge la matrice du modèle sur le GPU
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glBindVertexArray(self.cube_mesh.vao)  # Lie le VAO du cube
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)  # Dessine le cube

            pg.display.flip()  # Échange les buffers
            self.clock.tick(FPS)  # Limite le framerate à 60 FPS

        self._quit()

    def _quit(self):
        self.cube_mesh.destroy()  # Détruit la mesh du cube
        self.texture.destroy()  # Détruit la texture
        glDeleteProgram(self.shaders)  # Supprime le programme de shaders
        pg.quit()  # Quitte Pygame

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
    
    def _event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False  # Sort de la boucle si on quitte la fenêtre
    
    def _setup_pygame(self):
        self.clock = pg.time.Clock()
        # Crée la fenêtre avec les flags OPENGL et DOUBLEBUF pour double buffering
        pg.display.set_mode(WINDOW_SIZE, pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(WINDOW_NAME)  # Définit le nom de la fenêtre
    
    @staticmethod
    def _setup_gl():
        glClearColor(*CLEAR_COLOR)  # Définit la couleur de fond
        glEnable(GL_BLEND)  # Active le blending pour les effets de transparence
        glEnable(GL_DEPTH_TEST)  # Active le test de profondeur pour un rendu correct des objets 3D
        
    def _setup_shaders(self):
        # Crée et utilise les shaders
        self.shaders = self._create_shaders("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shaders)

        # Charge le shader dans le GPU
        glUniform1i(glGetUniformLocation(self.shaders, "imageTexture"), 0)