# подключаем необходимые библиотеки:

import numpy as np # библиотека для работы с массивами
import math # библиотека, добавляющая математические функции
import matplotlib.pyplot as plt # библиотека для построения графиков
from mpl_toolkits.mplot3d import Axes3D # библиотека для работы с 3D-графиками 

# исходные данные:

while True:

    try:
        h = 1000*float(input("Введите высоту орбиты, км: ")) # высота орбиты, м
        alpha = float(input("Введите угол наклона траектории, °: ")) # угол наклона траектории в градусах
        alpha = (alpha*math.pi)/180 # угол наклона траектории в радианах
        dt = float(input("Введите шаг разбиения по времени, с: ")) # шаг разбиения по времени
        break
    except ValueError:
        print('\nПерепроверьте введенные данные и повторите попытку!\n')
    
R = 6371000 # радиус Земли, м
mu = 3.986004415e+14 # гравитационный параметр Земли, м^3*c^-2
v0 = (mu/(R + h))**0.5; # начальная скорость, м/с
t0 = 0 # начальный момент времени
tk = 2*math.pi*(R + h)/v0 # время совершения полного оборота
n = tk/dt # количество разбиений для заданного шага
n = round(n) # округляем до целого числа

print("Выполняется построение траектории...")

# создаем массивы для координат и скоростей (изначально заполняем их нулями):

xarr = np.zeros(n)
yarr = np.zeros(n)
zarr = np.zeros(n)
Vxarr = np.zeros(n)
Vyarr = np.zeros(n)
Vzarr = np.zeros(n)

# присваиваем параметрам состояния начальные значения:

x = R + h
y = 0
z = 0
Vx = 0
Vy = v0
Vz = 0

# заполняем первые ячейки массивов начальными значениями, 
# переходя из повернутой системы координат в основную:

xarr[0] = x
yarr[0] = y*math.cos(alpha) - z*math.sin(alpha) 
zarr[0] = y*math.sin(alpha) + z*math.cos(alpha) 
Vxarr[0] = Vx
Vyarr[0] = Vy*math.cos(alpha) - Vz*math.sin(alpha) 
Vzarr[0] = Vy*math.sin(alpha) + Vz*math.cos(alpha) 

# цикл интегрирования:

t = t0 # присваиваем переменной времени начальное значение

for i in range(n):
    
    # радиус-вектор:
    r = (x*x + y*y + z*z)**0.5 
    
    # производные по координатам (скорости):
    dxdt = Vx 
    dydt = Vy
    dzdt = Vz
    
    # производные по скоростям (ускорения):
    dVxdt = - (mu*x)/(r*r*r) 
    dVydt = - (mu*y)/(r*r*r)
    dVzdt = - (mu*z)/(r*r*r)
    
    # интегрируем по методу Эйлера:            
    x = x + dxdt*dt
    y = y + dydt*dt
    z = z + dzdt*dt
    Vx = Vx + dVxdt*dt
    Vy = Vy + dVydt*dt
    Vz = Vz + dVzdt*dt
    
    # заполняем созданные ранее массивы, переходя из повернутой системы координат в основную:           
    xarr[i] = x       
    yarr[i] = y*math.cos(alpha) - z*math.sin(alpha)
    zarr[i] = y*math.sin(alpha) + z*math.cos(alpha)
    Vxarr[i] = Vx
    Vyarr[i] = Vy*math.cos(alpha) - Vz*math.sin(alpha) 
    Vzarr[i] = Vy*math.sin(alpha) + Vz*math.cos(alpha) 
    
    t += dt 

# визуализируем полученные массивы координат (строим траекторию):

fig = plt.figure(figsize=(10,10)) # размер графика
ax = fig.add_subplot(111, projection='3d') # создание сетки
ax.plot(xarr, yarr, zarr, label='parametric curve') # построение графика
ax.set_xlabel('x') # обозначение оси x
ax.set_ylabel('y') # обозначение оси y
ax.set_zlabel('z') # обозначение оси z
plt.show()

input()
