# skończone

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def turning_direction(p1, p2, p3):
    return (p2.get_y() - p1.get_y())*(p3.get_x() - p2.get_x()) - (p3.get_y() - p2.get_y())*(p2.get_x() - p1.get_x())


def Jarvis(list_of_points):
    p = list_of_points[0]
    for point in list_of_points:
        if p == point:
            continue
        if point.get_x() <= p.get_x():
            if point.get_x() == p.get_x() and point.get_y() >= p.get_y():
                pass
            else:
                p = point
    convex_hull = [p]
    q = None
    first_ite = True
    while p != convex_hull[0] or first_ite:
        if first_ite:
            first_ite = False
        for i in range(len(list_of_points)):
            if list_of_points[i] == p:
                q = list_of_points[(i+1) % len(list_of_points)]
                break
        for point in list_of_points:
            r = point
            if turning_direction(p, q, r) > 0:
                q = r
        if not q == convex_hull[0]:
            convex_hull.append(q)
        p = q
    return convex_hull


def Jarvis_corrected(list_of_points):
    p = list_of_points[0]
    for point in list_of_points:
        if p == point:
            continue
        if point.get_x() <= p.get_x():
            if point.get_x() == p.get_x() and point.get_y() >= p.get_y():
                pass
            else:
                p = point
    convex_hull = [p]
    q = None
    first_ite = True
    while p != convex_hull[0] or first_ite:
        if first_ite:
            first_ite = False
        for i in range(len(list_of_points)):
            if list_of_points[i] == p:
                q = list_of_points[(i+1) % len(list_of_points)]
                break
        for point in list_of_points:
            r = point
            if turning_direction(p, q, r) > 0:
                q = r
            elif turning_direction(p, r, q) == 0 and (min(p.get_x(), r.get_x()) < q.get_x() < max(p.get_x(), r.get_x())
                                                      or max(p.get_y(), r.get_y()) > q.get_y() > min(p.get_y(), r.get_y())):
                q = r
        if not q == convex_hull[0]:
            convex_hull.append(q)
        p = q
    return convex_hull


def main():
    list_of_points1 = []
    list_of_coords1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
    for coords in list_of_coords1:
        list_of_points1.append(Point(coords[0], coords[1]))

    print(Jarvis(list_of_points1))

    list_of_points2 = []
    list_of_coords2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
    for coords in list_of_coords2:
        list_of_points2.append(Point(coords[0], coords[1]))

    print(Jarvis(list_of_points2))

    print(Jarvis_corrected(list_of_points1))
    print(Jarvis_corrected(list_of_points2))

    list_of_points3 = []
    list_of_coords3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    for coords in list_of_coords3:
        list_of_points3.append(Point(coords[0], coords[1]))

    print(Jarvis(list_of_points3))
    print(Jarvis_corrected(list_of_points3))


if __name__ == "__main__":
    main()
