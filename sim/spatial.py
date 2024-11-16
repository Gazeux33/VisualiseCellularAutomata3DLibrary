import numpy as np
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class AABB:
    min_point: np.ndarray
    max_point: np.ndarray

    def intersects(self, other: 'AABB') -> bool:
        return np.all(self.min_point <= other.max_point) and np.all(other.min_point <= self.max_point)


class SpatialGrid:
    def __init__(self, cell_size: float = 10.0):
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int, int], Set[int]] = defaultdict(set)

    def get_cell_coords(self, position: np.ndarray):
        return tuple(map(int, position // self.cell_size))

    def add_cube(self, cube_id: int, position: np.ndarray) -> None:
        cell = self.get_cell_coords(position)
        self.grid[cell].add(cube_id)

    def get_nearby_cubes(self, position: np.ndarray, radius: float = 2.0) -> Set[int]:
        center_cell = self.get_cell_coords(position)
        radius_cells = int(radius / self.cell_size) + 1
        nearby_cubes = set()

        for x in range(center_cell[0] - radius_cells, center_cell[0] + radius_cells + 1):
            for y in range(center_cell[1] - radius_cells, center_cell[1] + radius_cells + 1):
                for z in range(center_cell[2] - radius_cells, center_cell[2] + radius_cells + 1):
                    nearby_cubes.update(self.grid.get((x, y, z), set()))

        return nearby_cubes