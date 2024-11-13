import pygame as pg
from OpenGL.GL import *

import numpy as np

from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

CLEAR_COLOR = (0.1, 0.1, 0.2, 1.0)
WINDOW_SIZE = (800, 600)
WINDOW_NAME = "OpenGL"

pg.init()


class Cube:
    def __init__(self,position,eulers):
        self.position = np.array(position,dtype=np.float32)
        self.eulers = np.array(eulers,dtype=np.float32)




class Render:
    def __init__(self):
        self.clock = pg.time.Clock()
        pg.display.set_mode(WINDOW_SIZE, pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(WINDOW_NAME)
        glClearColor(*CLEAR_COLOR)
        glEnable(GL_BLEND) # pour les effets de transparences
        glEnable(GL_DEPTH_TEST) # permet de rendre les pixels dans le bonne ordre

        self.shaders = self.create_shader("shaders/vertex2.txt", "shaders/fragment2.txt")
        glUseProgram(self.shaders)
        
        # charge le shader dans le GPU
        glUniform1i(glGetUniformLocation(self.shaders, "imageTexture"), 0)
        
        
        self.cube = Cube(
            position = [0,0,-3],
            eulers= [0,0,0]
        )
        self.cube_mesh = CubeMesh()
        self.texture = Material("wave.png")
        
        # creer une matrice de projection en perspective (transforme les coord 3d et 2d pour rendu a l'ecran)
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45,aspect=WINDOW_SIZE[0]/WINDOW_SIZE[1],
            near = 0.1,far=10,dtype=np.float32
        )
        
        # telecharge la matrice sur le GPU 
        glUniformMatrix4fv(
            glGetUniformLocation(self.shaders,"projection"),
            1,GL_FALSE,projection_transform
        )
        
        
        self.modelMatrixLocation = glGetUniformLocation(self.shaders,"model")
        
    
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
                    
            # rotation of the cube
            self.cube.eulers[2] += 0.2
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360
                    
                    
            # clear the window  
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram(self.shaders)
            self.texture.use()
            
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1 = model_transform,
                m2 = pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype = np.float32
                )
            )

            model_transform = pyrr.matrix44.multiply(
                m1 = model_transform,
                m2 = pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype = np.float32
                )
            )
            
            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
            
            pg.display.flip()
            self.clock.tick(60)
            
        self.quit()
        
    def quit(self):
        self.cube_mesh.destroy()
        self.texture.destroy()
        glDeleteProgram(self.shaders)
        pg.quit()
               
class CubeMesh:
    def __init__(self):
        
        # x,y,z , s,t 
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
        self.vertex_count = len(vertices)//5
        self.verticles = np.array(vertices, dtype=np.float32)
        
        self.vao = glGenVertexArrays(1) # Génère un objet Vertex Array Object
        glBindVertexArray(self.vao) # Lie le VAO créé pour qu'il soit utilisé pour les opérations suivantes
        self.vbo = glGenBuffers(1) # Génère un objet Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) # Lie le VBO créé pour qu'il soit utilisé pour les opérations suivantes
        glBufferData(GL_ARRAY_BUFFER, self.verticles.nbytes, self.verticles, GL_STATIC_DRAW) # Remplit le VBO avec les données des sommets
        
        glEnableVertexAttribArray(0) # Active l'attribut de sommet à l'emplacement 0 (les positions des sommets)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        
        
        
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