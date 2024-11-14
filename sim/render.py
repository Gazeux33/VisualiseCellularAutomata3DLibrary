import glfw 
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
from OpenGL.GL import *

from sim.graphics import GraphicsEngine
from sim.scene import Scene

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RETURN_ACTION_CONTINUE = 0
RETURN_ACTION_END = 1

def init_glfw():
    glfw.init()
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR,3)
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR,3)
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
        GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
    )
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT,
        GLFW_CONSTANTS.GLFW_TRUE
    )
    glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER,GL_FALSE)
    window = glfw.create_window(SCREEN_WIDTH,SCREEN_HEIGHT,"OpenGL Window",None,None)
    glfw.make_context_current(window)
    glfw.set_input_mode(window,GLFW_CONSTANTS.GLFW_CURSOR,GLFW_CONSTANTS.GLFW_CURSOR_NORMAL)
    return window


class App:
    def __init__(self,window):
        self.cursor_pos = None
        self.on_mouve = None
        self.window = window
        self.renderer = GraphicsEngine()
        self.scene = Scene()
        
        self.lastTime = glfw.get_time()
        self.currentTime = 0
        self.nbFrames = 0
        self.frameTime = 0



    def launch(self):
        running = True
        while running:
            if glfw.window_should_close(self.window) or glfw.get_key(self.window,GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                running = False
            self.handle_keys()
            self.handle_mouse()
            glfw.poll_events()
            
            self.scene.update(self.frameTime/16.7)
            self.renderer.render(self.scene)
            self.calculate_framerate()

    def handle_keys(self):
        self.walk_offset_lookup = {
            1:0,
            2:90,
            3:45,
            4:180,
            6:135,
            7:90,
            8:270,
            9:315,
            11:0,
            12:225,
            13:270,
            14:180,
        }
        combo = 0
        directionModifier = 0

        if glfw.get_key(self.window,GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 1
        if glfw.get_key(self.window,GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 2
        if glfw.get_key(self.window,GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 4
        if glfw.get_key(self.window,GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 8

        if combo in self.walk_offset_lookup:
            directionModifier = self.walk_offset_lookup[combo]
            dpos = [
                0.1*self.frameTime/16.7 * np.cos(np.deg2rad(self.scene.player.theta + directionModifier)),
                0.1*self.frameTime/16.7 * np.sin(np.deg2rad(self.scene.player.theta + directionModifier)),
                0
            ]
            self.scene.move_player(dpos)

        # Handle vertical movement
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_SPACE) == GLFW_CONSTANTS.GLFW_PRESS:
            self.scene.move_player([0, 0, 0.1 * self.frameTime / 16.7])
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_LEFT_SHIFT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.scene.move_player([0, 0, -0.1 * self.frameTime / 16.7])

    def handle_mouse(self):
    # Détecte si le bouton vient juste d'être pressé
        current_button_state = glfw.get_mouse_button(self.window, GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_RIGHT)
    
        # Si on vient juste d'appuyer sur le bouton (transition de relâché à pressé)
        if current_button_state == GLFW_CONSTANTS.GLFW_PRESS and not self.on_mouve:
            self.on_mouve = True
            self.cursor_pos = glfw.get_cursor_pos(self.window)
            print("update cursor pos")
    
        # Si on relâche le bouton
        if current_button_state == GLFW_CONSTANTS.GLFW_RELEASE:
            self.on_mouve = False
            self.cursor_pos = None
    
        # Gestion du mouvement
        if self.on_mouve:
            new_x, new_y = glfw.get_cursor_pos(self.window)
            old_x, old_y = self.cursor_pos
    
            sensitivity = 0.1
            theta_increment = (old_x - new_x) * sensitivity
            phi_increment = (old_y - new_y) * sensitivity
    
            self.scene.spin_player(theta_increment, phi_increment)
            glfw.set_cursor_pos(self.window, old_x, old_y)
            
            
    def calculate_framerate(self):
        self.currentTime = glfw.get_time()
        delta = self.currentTime - self.lastTime
        if delta >= 1:
            framerate = max(1,int(self.nbFrames/delta))
            glfw.set_window_title(self.window, f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.nbFrames = -1
            self.frameTime = float(1000.0 / max(1,framerate))
        self.nbFrames += 1
        
    def quit(self):
        self.renderer.quit()
        
    

    
    
