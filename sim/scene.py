from sim.cube import Cube
from sim.player import Player

import numpy as np


class Scene:
    def __init__(self):
        self.cubes = [Cube(position=[6,0,0],eulers=[0,0,0]),]
        
        self.player = Player(position=[0,0,2])
        
    def update(self,rate):
        """
        
        for cube in self.cubes:
            cube.eulers[1] += 0.25*rate
            if cube.eulers[1] > 360:
                cube.eulers[1] -= 360
        """
        
                
    def move_player(self,dpos):
        dpos = np.array(dpos,dtype=np.float32)
        self.player.position += dpos
        
    def spin_player(self,dtheta,dphi):
        self.player.theta += dtheta
        if self.player.theta > 360:
            self.player.theta -= 360
        if self.player.theta < 0:
            self.player.theta += 360
            
        self.player.phi = min(
            89,max(-89,self.player.phi + dphi)
        )
        self.player.update_vectors()