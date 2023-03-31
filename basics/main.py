import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        dx = pow(point.x - self.x, 2)
        dy = pow(point.y - self.y, 2)
        return math.sqrt(dx + dy)

    def __str__(self):
        return f"(x = {self.x}; y = {self.y})"


# tutaj dorobić te metody distance i area
class Points:
    def __init__(self, *points):
        self.points = list(points)[:]

    def append(self, x, y):
        point = Point(x, y)
        self.points.append(point)

    def distance(self):
        suma = 0
        for index, element in enumerate(self.points):
            if index + 1 < len(self.points):
                suma += self.points[index + 1].dist(self.points[index])
        return suma

    def area(self):
        suma = 0
        for index, element in enumerate(self.points):
            if index + 1 < len(self.points):
                suma += self.points[index].x * self.points[index + 1].y - self.points[index + 1].x * self.points[
                    index].y

        return abs(2 * suma)

    def __str__(self):
        text = ""
        for point in self.points:
            text += point.__str__() + "\n"

        return text


poly = Points()
poly.append(5, 5)
poly.append(10, 15)
poly.append(15, 20)
poly.append(25, 30)
print(poly)
print("Odległość między punktami:", poly.distance())
print("Pole polygonu:", poly.area())
