from sim.render import BaseApp
from sim.utils import WindowSize,Color


class LandScape(BaseApp):
    def __init__(self) -> None:
        super().__init__()
        self.renderer.set_clear_color(Color(1, 1, 1, 1))
        self.set_window_title("LandScape")
        self.set_window_size(WindowSize(1000,800))
        self.scene.add_cube(0 ,0 ,0)
        self.scene.add_cube(0 ,1 ,0)
        self.scene.add_cube(0, 2, 0)
        self.scene.add_cube(1, 0, 0)
        self.scene.add_cube(-1, 0, 0)
        self.scene.add_cube(0, 0, 1)
        self.scene.add_cube(0, 0, 2)
        self.scene.add_cube(0, 0, 3)


    def update(self) -> None:
        pass
