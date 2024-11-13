from OpenGL.GL import *
import pygame as pg

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