import matplotlib.pyplot as plt
import math

class Shapes:
    def __init__(self, n_angles, angles, sides):
        self.n_angles = n_angles
        self.angles = angles
        self.sides = sides
        self.checking()

    def get_perimetr(self):
        return sum(self.sides)

    def get_info(self):
        return f"Количество углов: {self.n_angles} \n  Значения углов в градусах: {self.angles} \n  Количество сторон: {len(self.sides)} \n  Длины сторон: {self.sides} \n  Периметр фигуры: {self.get_perimetr()}"

    def checking(self):

        for angle in self.angles:
            if angle is not None and (angle <= 0 or angle >= 360):
                raise ValueError("Углы должны быть положительны и меньше 360.")

        for side in self.sides:
            if side is None or side <= 0:
                raise ValueError("Длины сторон должны быть заданы и быть положительными.")

        if self.n_angles > 2:
            missing_angles = self.angles.count(None)
            if missing_angles == 1:
                total_sum = 180 * (self.n_angles - 2)
                known_sum = sum(angle for angle in self.angles if angle is not None)
                missing_angle = total_sum - known_sum
                if missing_angle <= 0 or missing_angle >= 360:
                    raise ValueError("Фигура с такими углами невозможна.")
                self.angles[self.angles.index(None)] = missing_angle
            elif missing_angles > 1:
                raise ValueError("Не хватает данных для восстановления углов.")

        if self.n_angles > 2:
            filtered_angles = list(filter(None, self.angles))
            total_sum = sum(filtered_angles)
            expected_sum = 180 * (self.n_angles - 2)
            if total_sum != expected_sum:
                raise ValueError("Сумма углов не соответствует количеству углов фигуры.")

    def draw(self):

        x, y = 0, 0
        angle = 0
        vertices = [(x, y)]

        for i in range(self.n_angles - 1):
            angle += self.angles[i]
            x += self.sides[i] * math.cos(math.radians(angle))
            y += self.sides[i] * math.sin(math.radians(angle))
            vertices.append((x, y))

        vertices.append((0, 0))
        x_coords, y_coords = zip(*vertices)
        plt.figure()
        plt.plot(x_coords, y_coords, marker='o', color='blue')
        plt.fill(x_coords, y_coords, color='lightblue', alpha=0.5)
        plt.title(f"Фигура с {self.n_angles} углами")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()



class Circle(Shapes):
    def __init__(self, radius):
        if radius is None or radius <= 0:
            raise ValueError("Радиус должен быть задан положительным числом.")
        super().__init__(0, [], [radius])
        self.name = "Circle"
        self.radius = radius

    def set_sides(self, sides):
        if len(sides) != 1 or sides[0] <= 0:
            raise ValueError("Радиус должен быть положительным числом.")
        self.sides = sides
        self.radius = sides[0]

    def get_sq(self):
        return str(round(math.pi * self.radius ** 2, 3)) + "\n"

    def get_info(self):
        info = f"Фигура: {self.name} \n  Количество углов: {self.n_angles} \n  Длина радиуса: {self.sides} \n  Площадь фигуры: {self.get_sq()}"
        return info

    def draw(self):
        fig, ax = plt.subplots()
        circle = plt.Circle((0, 0), self.sides[0], fill=False, color='blue', linewidth=2)
        ax.add_patch(circle)
        ax.set_xlim(-self.sides[0] - 1, self.sides[0] + 1)
        ax.set_ylim(-self.sides[0] - 1, self.sides[0] + 1)
        ax.set_aspect('equal', 'box')
        plt.title(f"Круг с радиусом {self.sides[0]}")
        plt.grid()
        plt.show()


class Triangle(Shapes):
    def __init__(self, angles, sides):
        super().__init__(3, angles, sides)
        self.name = "Triangle"

    def checking(self):
        super().checking()
        if len(self.sides) != 3:
            raise ValueError("Треугольник должен иметь 3 стороны. \n")
        if not (self.sides[0] + self.sides[1] > self.sides[2] and
                self.sides[0] + self.sides[2] > self.sides[1] and
                self.sides[1] + self.sides[2] > self.sides[0]):
            raise ValueError("Треугольник с такими сторонами не существует. \n")

        tolerance = 0.1
        ratio1 = math.sin(math.radians(self.angles[0])) / self.sides[0]
        ratio2 = math.sin(math.radians(self.angles[1])) / self.sides[1]
        ratio3 = math.sin(math.radians(self.angles[2])) / self.sides[2]

        if not (abs(ratio1 - ratio2) < tolerance and abs(ratio1 - ratio3) < tolerance and abs(ratio2 - ratio3) < tolerance):
            raise ValueError("Такой треугольник не может существовать. Некорректный ввод сторон или углов. \n")


    def set_angles(self, angles):
        if len(angles) != 3:
            raise ValueError("Треугольник должен иметь 3 угла. \n")
        self.angles = angles
        self.checking()

    def set_sides(self, sides):
        if len(sides) != 3:
            raise ValueError("Треугольник должен иметь 3 стороны. \n")
        self.sides = sides
        self.checking()

    def get_sq(self):
        pol_per = self.get_perimetr() / 2
        a, b, c = self.angles
        x, y, z = self.sides
        square = []
        try:
            square.append(("Формула Герона", round(math.sqrt(pol_per * (pol_per - self.sides[0]) * (pol_per - self.sides[1]) * (pol_per - self.sides[2])), 3)))
            square.append(("Через две стороны и угол между ними", round(self.sides[0] * self.sides[2] * math.sin(math.radians(self.angles[1])) / 2, 3)))
            h = self.sides[0] * math.sin(math.radians(self.angles[1]))
            square.append(("Через высоту и основание", round(self.sides[2] * h / 2, 3)))
            return square
        except ValueError as e:
            return "Ошибка при находжении площади."

    def get_info(self):
        return f"Название: {self.name} \n  {super().get_info()} \n  Площадь фигуры: {self.get_sq()} \n"



class Quadrangle(Shapes):
    def __init__(self, angles, sides):
        super().__init__(4, angles, sides)
        self.name = "Quadrangle"

    def checking(self):
        super().checking()
        if len(self.angles) not in [3, 4] or len(self.sides) != 4:
            raise ValueError("Информации не достаточно для нахождения площади.")


    def set_angles(self, angles):
        if len(angles) not in [3, 4]:
            raise ValueError("Четырёхугольник должен иметь 3 или 4 угла.")
        self.angles = angles
        self.checking()

    def set_sides(self, sides):
        if len(sides) != 4:
            raise ValueError("Четырёхугольник должен иметь 4 стороны.")
        self.sides = sides
        self.checking()

    def get_sq(self):
        a, b, c, d = self.angles
        w, x, y, z = self.sides
        if a == b == c == d == 90:
            if w == x == y == z:
                return str(w * x) + " - квадрат"
            else:
                return str(w * x) + " - прямоугольник"
        elif a == c and b == d and a + b == c + d == 180:
            if w == x == y == z:
                return str(round(z * w * math.sin(math.radians(a)), 3)) + " - ромб"
            else:
                return str(round(z * w * math.sin(math.radians(a)), 3)) + " - параллелограмм"
        elif (w != y or x != z) and (a + b == c + d == 180):
            return str(round((x + z) * w * math.sin(math.radians(a)) / 2, 3)) + " - трапеция"

        else:
            s = self.get_perimetr() / 2
            try:
                # через диагонали не получилось, я воспользовалась формулой Бретшнайдера
                squ = round(math.sqrt((s - w) * (s - x) * (s - y) * (s - z) - (w * x * y * z) * (math.cos(math.radians((a + c) / 2)) * 2)), 3)
                return str(squ) + " - произвольный 4х-угольник"
            except ValueError:
                return "Некорректный ввод, площадь не может быть найдена"

    def get_info(self):
        return f"Название: {self.name} \n  {super().get_info()} \n  Площадь фигуры: {self.get_sq()} \n"



class Nangle(Shapes):
    def __init__(self, n_angles, angles=None, sides=None):
        super().__init__(n_angles, angles, sides)
        self.name = f"{n_angles}-угольник"
        self.vertices = []


    def checking(self):
        super().checking()
        if not (len(self.angles) == self.n_angles or len(self.sides) == self.n_angles):
            raise ValueError("Многоугольник должен иметь все стороны или все углы.")

    def get_sq(self):
        if not (len(self.angles) == self.n_angles and len(self.sides) == self.n_angles):
            return "Для вычисления площади необходимо задать все углы и стороны"
        vertices = [(0, 0)]
        x, y = 0, 0
        angle = 0
        for i in range(self.n_angles):
            x += self.sides[i] * math.cos(math.radians(angle))
            y += self.sides[i] * math.sin(math.radians(angle))
            vertices.append((x, y))
            angle += self.angles[i]

        square = 0
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            square += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
        square = round(abs(square) / 2, 3)
        return square

    def get_info(self):
        return f"Название: {self.name} \n  {super().get_info()}  \n  Площадь фигуры: {self.get_sq()} \n"


try:
    fig_1 = Shapes(4, [90, 90, None, 90], [10, 10, 10, 10])
    print(fig_1.get_info())
    fig_1.draw()
except ValueError as e:
    print("Фигура не может быть создана:", e)

try:
    c_1 = Circle(3)
    print(c_1.get_info())
    c_1.draw()
except ValueError as e:
    print("Фигура не может быть создана:", e)

try:
    t_1 = Triangle([90, None, 53.13], [5, 3, 4])
    print(t_1.get_info())
    t_1.draw()
except ValueError as e:
    print("Фигура не может быть создана:", e)

try:
    print("___Проверка несуществующего треугольника___")
    t_2 = Triangle([60, 70, 50], [4, 4, 6])
    print(t_2.get_info())
except ValueError as e:
    print("Фигура не может быть создана:", e)

try:
    q_3 = Quadrangle([60, 120, 150, 30], [2, 3, 3.5, 2.5]) #Пример, стороны и углы могут быть разные
    print(q_3.get_info())
    q_3.set_sides([4, 7, 2, 7])
    print(q_3.get_info())

except ValueError as e:
    print("Фигура не может быть создана:", e)

try:
    q_3 = Quadrangle([63, 12, 148, 137], [2, 3, 7, 2.5]) #Пример, стороны и углы могут быть разные
    print(q_3.get_info())
except ValueError as e:
    print("Фигура не может быть создана:", e)

try:
    n_1 = Nangle(5,[None, 77, 127, 111, 72], [4, 2.5, 3, 3, 3.5])
    print(n_1.get_info())
except ValueError as e:
    print("Фигура не может быть создана:", e)
