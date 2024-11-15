from typing import List

import numpy as np

from sim.utils import Position


class Player:
    def  __init__(self,position:Position):
        self.up = None
        self.up : np.ndarray
        self.right = None
        self.forwards = None
        self.position = np.array(position,dtype=np.float32)
        self.theta = 0
        self.phi = 0
        self.update_vectors()
        
    def update_vectors(self) -> None:
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )
        globalUp = np.array([0,0,1],dtype=np.float32)
        self.right = np.cross(self.forwards,globalUp)
        self.up = np.cross(self.right,self.forwards)
        
        