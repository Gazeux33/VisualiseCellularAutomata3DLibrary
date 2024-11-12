import pygame as pg
from OpenGL.GL import *

import numpy as np

from OpenGL.GL.shaders import compileProgram, compileShader


CLEAR_COLOR = (0.1, 0.2, 0.2, 1.0)
WINDOW_SIZE = (800, 600)
WINDOW_NAME = "OpenGL"

pg.init()


class Render:
    def __init__(self):
        self.clock = pg.time.Clock()
        pg.display.set_mode(WINDOW_SIZE, pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(WINDOW_NAME)
        glClearColor(*CLEAR_COLOR)

        self.shaders = self.create_shader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shaders)
        glUniform1i(glGetUniformLocation(self.shaders, "imageTexture"), 0)
        
        
        self.triangle = Triangle()
        self.texture = Material("wave.png")
    
    @staticmethod
    def create_shader(vertex_path, fragment_path):
        with open(vertex_path, 'r') as file:
            vertex_src = file.read()
            
        with open(fragment_path, 'r') as file:
            fragment_src = file.read()
            
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
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shaders)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)
            
            pg.display.flip()
            self.clock.tick(60)
            
        self.quit()
        
    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shaders)
        pg.quit()
        
        
class Triangle:
    def __init__(self):
        
        # x,y,z,r,g,b , s,t 
        self.verticles = (
            -0.5,-0.5,0.0,1.0,0.0,0.0,0.0,1.0,
            0.5,-0.5,0.0,0.0,1.0,0.0,1.0,1.0,
            0.0,0.5,0.0,0.0,0.0,1.0,0.5,0.0,
        )
        self.verticles = np.array(self.verticles, dtype=np.float32)
        self.vertex_count = 3  # Définit le nombre de sommets du triangle (3 sommets)
        
        self.vao = glGenVertexArrays(1) # Génère un objet Vertex Array Object
        glBindVertexArray(self.vao) # Lie le VAO créé pour qu'il soit utilisé pour les opérations suivantes
        self.vbo = glGenBuffers(1) # Génère un objet Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) # Lie le VBO créé pour qu'il soit utilisé pour les opérations suivantes
        glBufferData(GL_ARRAY_BUFFER, self.verticles.nbytes, self.verticles, GL_STATIC_DRAW) # Remplit le VBO avec les données des sommets
        
        glEnableVertexAttribArray(0) # Active l'attribut de sommet à l'emplacement 0 (les positions des sommets)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        """Définit la manière dont les données de couleur des sommets sont organisées 
        dans le VBO. Ici, l'emplacement 1 utilise 3 composantes de type float, 
        sans normalisation, avec un décalage de 24 octets entre chaque sommet, 
        et commence à l'offset 12
        """
        
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        
        
    def destroy(self):
        glDeleteVertexArrays(1, self.vao)
        glDeleteBuffers(1, self.vbo)

class Material:
    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pg.image.load(filepath).convert()
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, self.texture)
        
        
        
        
        

        
        
        

if __name__ == "__main__":
    r = Render()
    r.launch()