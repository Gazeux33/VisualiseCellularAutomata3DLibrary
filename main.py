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
        self.triangle = Triangle()
    
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
        self.verticles = (
            -0.5,-0.5,0.0,1.0,0.0,0.0,
            0.5,-0.5,0.0,0.0,1.0,0.0,
            0.0,0.5,0.0,0.0,0.0,1.0,
        )
        self.verticles = np.array(self.verticles, dtype=np.float32)
        self.vertex_count = 3
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1) # vertex buffer object
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.verticles.nbytes, self.verticles, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        
        
    def destroy(self):
        glDeleteVertexArrays(1, self.vao)
        glDeleteBuffers(1, self.vbo)
        
        
        
        

if __name__ == "__main__":
    r = Render()
    r.launch()