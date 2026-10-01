import math

class MathUtils:

    @staticmethod
    def distance(point1, point2):
        """
        Calculate 3D Euclidean distance between two MediaPipe landmarks.
        """
        x1, y1, z1 = point1.x, point1.y, point1.z
        x2, y2, z2 = point2.x, point2.y, point2.z

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)