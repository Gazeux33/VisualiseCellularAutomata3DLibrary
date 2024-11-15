from typing import List

from sim.cube import Cube
from sim.player import Player
from sim.utils import Position

import numpy as np


class Scene:
    def __init__(self) -> None:
        self.cubes : List[Cube] = []
        self.player : Player = Player(Position(-6,0,0))

    def add_cube(self,x:float,y:float,z:float) -> None:
        self.cubes.append(Cube(Position(x,y,z)))

    def set_player_position(self,x:float,y:float,z:float) -> None:
        self.player.position = np.array([x,y,z],dtype=np.float32)

    def update(self,rate:float) -> None:
        pass

                
    def move_player(self, d_pos:List[float | int]) -> None:
        d_pos = np.array(d_pos, dtype=np.float32)
        self.player.position += d_pos
        
    def spin_player(self,d_theta:float,d_phi:float) -> None:
        self.player.theta += d_theta
        if self.player.theta > 360:
            self.player.theta -= 360
        if self.player.theta < 0:
            self.player.theta += 360
            
        self.player.phi = min(
            89,max(-89,self.player.phi + d_phi)
        )
        self.player.update_vectors()