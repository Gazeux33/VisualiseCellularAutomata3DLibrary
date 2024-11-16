import numpy as np

from sim.spatial import AABB


class Frustum:
    def __init__(self):
        self.planes = np.zeros((6, 4))  # 6 plans: Near, Far, Left, Right, Top, Bottom
        self.dirty = True

    def update(self, projection_view_matrix: np.ndarray) -> None:
        if not self.dirty:
            return

        # Extract frustum planes from projection-view matrix
        self.planes[0] = projection_view_matrix[3] + projection_view_matrix[2]  # Near
        self.planes[1] = projection_view_matrix[3] - projection_view_matrix[2]  # Far
        self.planes[2] = projection_view_matrix[3] + projection_view_matrix[0]  # Left
        self.planes[3] = projection_view_matrix[3] - projection_view_matrix[0]  # Right
        self.planes[4] = projection_view_matrix[3] - projection_view_matrix[1]  # Top
        self.planes[5] = projection_view_matrix[3] + projection_view_matrix[1]  # Bottom

        # Normalize planes
        for i in range(6):
            self.planes[i] /= np.linalg.norm(self.planes[i][:3])

        self.dirty = False

    def is_visible(self, aabb: AABB) -> bool:
        for plane in self.planes:
            # Find the positive vertex
            p_vertex = aabb.min_point.copy()
            if plane[0] >= 0:
                p_vertex[0] = aabb.max_point[0]
            if plane[1] >= 0:
                p_vertex[1] = aabb.max_point[1]
            if plane[2] >= 0:
                p_vertex[2] = aabb.max_point[2]

            # If positive vertex is outside, whole AABB is outside
            if np.dot(plane[:3], p_vertex) + plane[3] < 0:
                return False
        return True