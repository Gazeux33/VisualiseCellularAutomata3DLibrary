from abc import ABC, abstractmethod
from typing import Any

from OpenGL.GL import *
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
import glfw

from render.config import PLAYER_SPEED
from render.graphics import GraphicsEngine
from render.scene import Scene
from render.utils import WindowSize



class BaseApp(ABC):
    def __init__(self, window_name: str = "OpenGL", window_size=WindowSize(640, 480)) -> None:
        self.window_title = window_name
        self.window_size = window_size
        self.cursor_pos = None
        self.on_move = None
        self.window = self._init_glfw()

        self.renderer = GraphicsEngine(self.window_size)
        self.scene = Scene()

        self.lastTime = glfw.get_time()
        self.currentTime = 0
        self.nbFrames = 0
        self.frameTime = 0

        self.lastFrameTime = glfw.get_time()
        self.deltaTime = 0.0

        glfw.set_window_size_callback(self.window, self._on_window_size_change)
        glfw.set_key_callback(self.window, self._on_key_event)
        self.key_callbacks = {}

    def launch(self) -> None:
        running = True
        while running:
            if glfw.window_should_close(self.window) or glfw.get_key(self.window,
                                                                     GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                running = False
            self._handle_keys()
            self._handle_mouse()
            glfw.poll_events()
            self.update()
            self.scene.update(self.deltaTime)
            self.renderer.render(self.scene)
            glfw.swap_buffers(self.window)
            self._calculate_framerate()

    @abstractmethod
    def update(self) -> None:
        pass

    def _handle_keys(self) -> None:
        walk_offset_lookup = {
            1: 0, 2: 90, 3: 45, 4: 180, 6: 135, 7: 90, 8: 270, 9: 315, 11: 0, 12: 225, 13: 270, 14: 180,
        }
        keys = [GLFW_CONSTANTS.GLFW_KEY_W, GLFW_CONSTANTS.GLFW_KEY_A, GLFW_CONSTANTS.GLFW_KEY_S,
                GLFW_CONSTANTS.GLFW_KEY_D]
        combo = sum(1 << i for i, key in enumerate(keys) if
                    glfw.get_key(self.window, key) == GLFW_CONSTANTS.GLFW_PRESS)

        if combo in walk_offset_lookup:
            directionModifier = walk_offset_lookup[combo]
            speed = PLAYER_SPEED  # Vitesse du joueur (unités par seconde)
            d_pos = [
                speed * self.deltaTime * np.cos(
                    np.deg2rad(self.scene.player.theta + directionModifier)),
                speed * self.deltaTime * np.sin(
                    np.deg2rad(self.scene.player.theta + directionModifier)),
                0
            ]
            self.scene.move_player(d_pos)

        # Mouvement vertical
        vertical_speed = PLAYER_SPEED  # Vitesse verticale
        vertical_moves = {
            GLFW_CONSTANTS.GLFW_KEY_SPACE: [0, 0, vertical_speed * self.deltaTime],
            GLFW_CONSTANTS.GLFW_KEY_LEFT_SHIFT: [0, 0, -vertical_speed * self.deltaTime]
        }
        for key, move in vertical_moves.items():
            if glfw.get_key(self.window, key) == GLFW_CONSTANTS.GLFW_PRESS:
                self.scene.move_player(move)

    def _handle_mouse(self) -> None:
        current_button_state = glfw.get_mouse_button(self.window,
                                                     GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_RIGHT)

        if current_button_state == GLFW_CONSTANTS.GLFW_PRESS and not self.on_move:
            self.on_move = True
            self.cursor_pos = glfw.get_cursor_pos(self.window)

        if current_button_state == GLFW_CONSTANTS.GLFW_RELEASE:
            self.on_move = False
            self.cursor_pos = None

        if self.on_move:
            new_x, new_y = glfw.get_cursor_pos(self.window)
            old_x, old_y = self.cursor_pos

            sensitivity = 0.1
            theta_increment = (old_x - new_x) * sensitivity
            phi_increment = (old_y - new_y) * sensitivity

            self.scene.spin_player(theta_increment, phi_increment)
            glfw.set_cursor_pos(self.window, old_x, old_y)

    def _calculate_framerate(self) -> None:
        self.currentTime = glfw.get_time()
        self.deltaTime = self.currentTime - self.lastFrameTime
        self.lastFrameTime = self.currentTime

        self.nbFrames += 1
        delta = self.currentTime - self.lastTime
        if delta >= 1:
            framerate = max(1, int(self.nbFrames / delta))
            self.lastTime = self.currentTime
            self.nbFrames = 0
            glfw.set_window_title(self.window, f"{self.window_title} - {framerate} FPS")

    def quit(self) -> None:
        self.renderer.quit()

    def _init_glfw(self) -> Any:
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
            GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
        )
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT,
            GLFW_CONSTANTS.GLFW_TRUE
        )
        glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_TRUE)
        window = glfw.create_window(self.window_size[0], self.window_size[1], self.window_title, None, None)
        if not window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")
        glfw.make_context_current(window)
        glfw.set_input_mode(window, GLFW_CONSTANTS.GLFW_CURSOR, GLFW_CONSTANTS.GLFW_CURSOR_NORMAL)
        glfw.swap_interval(0)  # Désactiver V-Sync
        return window

    def set_window_title(self, title: str) -> None:
        self.window_title = title
        glfw.set_window_title(self.window, title)

    def get_window_size(self) -> WindowSize:
        return WindowSize(*glfw.get_window_size(self.window))

    def set_window_size(self, size: WindowSize) -> None:
        self.window_size = size
        glfw.set_window_size(self.window, size.width, size.height)
        monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(monitor)
        window_pos_x = (video_mode.size.width - size.width) // 2
        window_pos_y = (video_mode.size.height - size.height) // 2
        glfw.set_window_pos(self.window, window_pos_x, window_pos_y)
        self._on_window_size_change(self.window, size.width, size.height)

    def _on_window_size_change(self, window, width: int, height: int) -> None:
        self.window_size = WindowSize(width, height)
        glViewport(0, 0, width, height)
        self.renderer.update_projection_matrix(width, height)

    def add_event_key_callback(self, callback: callable, key: int) -> None:
        self.key_callbacks[key] = callback

    def _on_key_event(self, window, key, scancode, action, mods) -> None:
        if action == GLFW_CONSTANTS.GLFW_PRESS and key in self.key_callbacks:
            self.key_callbacks[key]()