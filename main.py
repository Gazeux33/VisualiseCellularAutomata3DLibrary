import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

# Couleur de fond de la fenêtre OpenGL
CLEAR_COLOR = (0.1, 0.1, 0.2, 1.0)
# Taille de la fenêtre
WINDOW_SIZE = (800, 600)
# Nom de la fenêtre
WINDOW_NAME = "OpenGL"

pg.init()

class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)  # Position du cube
        self.eulers = np.array(eulers, dtype=np.float32)  # Angles d'Euler du cube (rotation)

class Render:
    def __init__(self):
        self.clock = pg.time.Clock()
        # Crée la fenêtre avec les flags OPENGL et DOUBLEBUF pour double buffering
        pg.display.set_mode(WINDOW_SIZE, pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(WINDOW_NAME)  # Définit le nom de la fenêtre
        glClearColor(*CLEAR_COLOR)  # Définit la couleur de fond
        glEnable(GL_BLEND)  # Active le blending pour les effets de transparence
        glEnable(GL_DEPTH_TEST)  # Active le test de profondeur pour un rendu correct des objets 3D

        # Crée et utilise les shaders
        self.shaders = self.create_shader("shaders/vertex2.txt", "shaders/fragment2.txt")
        glUseProgram(self.shaders)

        # Charge le shader dans le GPU
        glUniform1i(glGetUniformLocation(self.shaders, "imageTexture"), 0)

        # Initialisation du cube avec sa position et sa rotation
        self.cube = Cube(position=[0, 0, -3], eulers=[0, 0, 0])
        self.cube_mesh = CubeMesh()  # Création de la mesh du cube
        self.texture = Material("wave.png")  # Chargement de la texture du cube

        # Crée une matrice de projection en perspective
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

    @staticmethod
    def create_shader(vertex_path, fragment_path):
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

    def launch(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False  # Sort de la boucle si on quitte la fenêtre

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
            self.clock.tick(60)  # Limite le framerate à 60 FPS

        self.quit()

    def quit(self):
        self.cube_mesh.destroy()  # Détruit la mesh du cube
        self.texture.destroy()  # Détruit la texture
        glDeleteProgram(self.shaders)  # Supprime le programme de shaders
        pg.quit()  # Quitte Pygame

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

class Material:
    def __init__(self, filepath):
        self.texture = glGenTextures(1)  # Génère un objet de texture
        glBindTexture(GL_TEXTURE_2D, self.texture)  # Lie la texture créée pour qu'elle soit utilisée pour les opérations suivantes
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Définit le mode de wrapping de la texture sur l'axe S
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Définit le mode de wrapping de la texture sur l'axe T
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  # Définit le filtre de minification de la texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Définit le filtre de magnification de la texture

        image = pg.image.load(filepath).convert()  # Charge l'image et la convertit en format compatible avec Pygame
        image_width, image_height = image.get_rect().size  # Obtient la taille de l'image
        image_data = pg.image.tostring(image, "RGBA")  # Convertit l'image en chaîne de bytes au format RGBA
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)  # Charge les données de l'image dans la texture
        glGenerateMipmap(GL_TEXTURE_2D)  # Génère les mipmaps pour la texture

    def use(self):
        glActiveTexture(GL_TEXTURE0)  # Active l'unité de texture 0
        glBindTexture(GL_TEXTURE_2D, self.texture)  # Lie la texture pour qu'elle soit utilisée dans les opérations de dessin

    def destroy(self):
        glDeleteTextures(1, self.texture)  # Supprime la texture

if __name__ == "__main__":
    r = Render()  # Crée une instance de la classe Render
    r.launch()  # Lance la boucle principale de rendu
