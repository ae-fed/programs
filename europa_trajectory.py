# Подключаем необходимые библиотеки:
import numpy as np # библиотека для работы с массивами
import matplotlib.pyplot as plt # библиотека для построения графиков
from matplotlib.patches import * # библиотека для построения геометрических фигур


def main():
    # Задаем исходные данные:
    Europa = Body(name = 'Europa', 
                  mu = 3.20356e12,
                  R = 1560.8e3,
                  color = 'goldenrod') # экземпляр класса Body с параметрами спутника
    h = 150e3 # высота орбиты, м
    x0 = Europa.R + h # начальное положение по оси x, м
    y0 = 0 # начальное положение по оси y, м
    vx0 = 0 # начальная скорость по оси x, м/с
    vy0 = (Europa.mu/(Europa.R+h))**0.5 # начальная скорость по оси y, м/с
    pm = 0.8 # удельная тяга тормозных двигателей, Н/м
    tbr = 60 # время работы тормозных двигателей, с
    step = 0.01 # шаг разбиения по времени, c

    # Получаем массивы координат и проекций скорости:
    trajectory = integration(x0, y0, vx0, vy0, pm, tbr, step, Europa)

    # Определяем проекцию полной скорости на радиальное направление:
    vr = vector_rad(trajectory[4], trajectory[5], trajectory[6], trajectory[7])

    # Определяем проекцию полного ускорения на радиальное направление:
    ar = vector_rad(trajectory[4], trajectory[5], trajectory[8], trajectory[9])

    # Выводим результаты (проекции скорости/ускорения в момент посадки):
    print(f'Координаты (x, y): {trajectory[4]}, {trajectory[5]}')
    print(f'Проекции скорости (vx, vy): {trajectory[6]}, {trajectory[7]}')
    print(f'Проекции ускорения (ax, ay): {trajectory[8]}, {trajectory[9]}')
    print(f'Радиальная составляющая скорости (vr): {vr}')
    print(f'Радиальная составляющая ускорения (ar): {ar}')

    # Визуализируем полученные массивы координат:
    visualization(trajectory[0], trajectory[1], Europa)


# Создаем класс для генерации небесных тел:
class Body:

    def __init__(self, name, mu, R, color):
        self.name = name # название небесного тела
        self.mu = mu # гравитационный параметр небесного тела, м^3*c^-2
        self.R = R # радиус небесного тела, м
        self.color = color # цвет поверхности небесного тела


# Функция для интегрирования по методу Эйлера:
def integration(x, y, vx, vy, p, tb, dt, object):
    # Задаем массивы координат и проекций скорости,
    # заполняя их начальными значениями:
    xarr, yarr, vxarr, vyarr = [x], [y], [vx], [vy]

    # Задаем начальные значения для проекций тяги тормозных двигателей:
    px, py = 0, -p

    # Вводим начальный момент времени:
    t = 0

    # Выполняем интегрирование:
    while (x**2 + y**2)**0.5 > object.R:
        # Проверяем, включены ли тормозные двигатели,
        # и вычисляем ускорение:
        if t <= tb:
            ax = -(object.mu*x)/((x**2 + y**2)**(3/2)) + px
            ay = -(object.mu*y)/((x**2 + y**2)**(3/2)) + py
        else:
            ax = -(object.mu*x)/((x**2 + y**2)**(3/2))
            ay = -(object.mu*y)/((x**2 + y**2)**(3/2))

        # Интегрируем:
        x = x + vx*dt
        y = y + vy*dt
        vx = vx + ax*dt
        vy = vy + ay*dt
        t += dt

        # Заполняем массивы новыми значениями:
        xarr.append(x)
        yarr.append(y)
        vxarr.append(vx)
        vyarr.append(vy)
        
        # Переопределяем значения для проекций тормозящей силы:
        px = -p*np.sin(np.arctan(abs(vx)/abs(vy)))*vx/abs(vx)
        py = -p*np.cos(np.arctan(abs(vx)/abs(vy)))*vy/abs(vy)

    # Возвращаем результаты:
    return [xarr, yarr, vxarr, vyarr, x, y, vx, vy, ax, ay]


# Функция для определения радиальной составляющей вектора (a, b):
def vector_rad(x, y, a, b):
    # Косинус угла между векторами:
    cos_alpha = ((x*a) + (y*b))/((x**2 + y**2)**0.5 * (a**2 + b**2)**0.5)

    # Проекция вектора на радиальное направление:
    return ((a**2 + b**2)**0.5) * cos_alpha


# Функция для построения траектории полета:
def visualization(x, y, object):
    fig = plt.figure(figsize=(5,5)) # создаем окно для графика
    ax = fig.add_subplot() # добавляем оси
    c = Circle((0, 0), object.R, facecolor=object.color, label=object.name) # создаем эскиз небесного тела
    ax.add_patch(c) # добавляем созданный эскиз на график
    ax.plot(x, y, label='trajectory') # чертим траекторию полета по координатам x, y
    ax.legend() # добавляем на график легенду
    plt.xlim([-3e6, 3e6]) # задаем ограничения по оси x
    plt.ylim([-3e6, 3e6]) # задаем ограничения по оси y
    plt.grid() # рисуем сетку
    plt.show() # отображаем график


if __name__ == '__main__':
    main()
