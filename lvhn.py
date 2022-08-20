import numpy as np
import cv2

class geometry:
    def __init__(self, max=10000):
        # Define Infinite (Using INT_MAX 
        # caused overflow problems)
        self.INT_MAX = max

    # Given three collinear points p, q, r, 
    # the function checks if point q lies
    # on line segment 'pr'
    def onSegment(self, p: tuple, q: tuple, r: tuple) -> bool:

        if ((q[0] <= max(p[0], r[0])) &
                (q[0] >= min(p[0], r[0])) &
                (q[1] <= max(p[1], r[1])) &
                (q[1] >= min(p[1], r[1]))):
            return True

        return False

    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are collinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise
    def orientation(self, p: tuple, q: tuple, r: tuple) -> int:

        val = (((q[1] - p[1]) *
                (r[0] - q[0])) -
               ((q[0] - p[0]) *
                (r[1] - q[1])))

        if val == 0:
            return 0
        if val > 0:
            return 1  # Collinear
        else:
            return 2  # Clock or counterclock

    def doIntersect(self, p1, q1, p2, q2):

        # Find the four orientations needed for 
        # general and special cases
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        # General case
        if (o1 != o2) and (o3 != o4):
            return True

        # Special Cases
        # p1, q1 and p2 are collinear and
        # p2 lies on segment p1q1
        if (o1 == 0) and (self.onSegment(p1, p2, q1)):
            return True

        # p1, q1 and p2 are collinear and
        # q2 lies on segment p1q1
        if (o2 == 0) and (self.onSegment(p1, q2, q1)):
            return True

        # p2, q2 and p1 are collinear and
        # p1 lies on segment p2q2
        if (o3 == 0) and (self.onSegment(p2, p1, q2)):
            return True

        # p2, q2 and q1 are collinear and
        # q1 lies on segment p2q2
        if (o4 == 0) and (self.onSegment(p2, q1, q2)):
            return True

        return False

    # Returns true if the point p lies 
    # inside the polygon[] with n vertices
    def is_inside_polygon(self, points: list, p: tuple) -> bool:

        n = len(points)

        # There must be at least 3 vertices
        # in polygon
        if n < 3:
            return False

        # Create a point for line segment
        # from p to infinite
        extreme = (self.INT_MAX, p[1])
        count = i = 0

        while True:
            next = (i + 1) % n

            # Check if the line segment from 'p' to 
            # 'extreme' intersects with the line 
            # segment from 'polygon[i]' to 'polygon[next]'
            if (self.doIntersect(points[i],
                                 points[next],
                                 p, extreme)):

                # If the point 'p' is collinear with line 
                # segment 'i-next', then check if it lies 
                # on segment. If it lies, return true, otherwise false
                if self.orientation(points[i], p,
                                    points[next]) == 0:
                    return self.onSegment(points[i], p,
                                          points[next])

                count += 1

            i = next

            if (i == 0):
                break

        # Return true if count is odd, false otherwise
        return (count % 2 == 1)


def read_pts(filename):
    # Polygon corner points coordinates
    with open(filename, mode='r') as f:
        pts = [line.split() for line in f]
        return np.array(pts, np.int32)


def get_mouse_pos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #  Write waring_pos
        with open('warning/location.txt', mode='a') as f:
            f.write(f'{x} {y}\n')
