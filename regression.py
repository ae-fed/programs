# импорт необходимых библиотек:

import numpy as np
import scipy as sc

# Матрица значений факторов:

X = (np.array([[0.4,   2.6,   0.4,   2.6,   0.4,    2.6,    0.4,    2.6 ],
               [40,    40,    320,   320,   40,     40,     320,    320 ],
               [300,   300,   300,   300,   2700,   2700,   2700,   2700]])).T
               
print('Матрица значений факторов X: \n')
print(X)

# Значения отклика y:

Y = (np.array([[22.95, 26.23, 95.72, 99.21, 118.94, 122.38, 191.84, 195.12]])).T

print('\nВектор значений отклика Y: \n')
print(Y)

# Массив значений отклика y в специальной серии опытов:

Y_SP = (np.array([[109.00, 108.98, 108.97, 109.16, 108.99, 109.13, 109.09, 109.07]])).T

print('\nВектор значений отклика в специальной серии опытов Y_SP: \n')
print(Y_SP)

# Матрица значений базисных функций:

F = np.hstack([np.full((X.shape[0], 1), 1), X])

print('\nМатрица значений базисных функций F: \n')
print(F)

# Точечные оценки коэффициентов регрессии с применением МНК:

C = np.linalg.inv(np.dot(F.T, F))
B = np.dot(C, np.dot(F.T, Y))

print('\nТочечные оценки коэффициентов регрессии с применением МНК: \n\n   - матрица C:\n')
print(C, '\n\n   - вектор коэффициентов регрессии B: \n')
print(B)

# Точечная оценка дисперсии с использованием результатов специальной серии опытов:

y_sp_av = 0 # Среднее значение отклика в специальной серии опытов
s_e_2 = 0 # Точечная оценка дисперсии для специальной серии опытов

for i in range(Y_SP.shape[0]):
    y_sp_av += (1/Y_SP.shape[0]) * Y_SP[i]
    
for i in range(Y_SP.shape[0]):
    s_e_2 += (1/(Y_SP.shape[0] - 1))*((Y_SP[i] - y_sp_av)**2)
    
print('\nТочечная оценка дисперсии с использованием результатов специальной серии опытов: \n')
print('   - среднее значение отклика y_sp_av: \n')
print(y_sp_av)
print('\n   - точечная оценка дисперсии s_e_2: \n')
print(s_e_2)
    
# Вычисление статистик t для проверки значимости полученных коэффициентов регрессии:

T = np.zeros(F.shape[1])

for i in range(F.shape[1]):
    T[i] = B[i]/((s_e_2*C[i][i])**0.5)
    
print('\nВектор статистик t: \n')
print(T)
    
# Определение критического значения t:

alpha = 0.05 # уровень значимости
    
t_cr = sc.stats.t.ppf(1 - alpha/2, Y_SP.shape[0] - 1)

print('\nКритическое значение t: \n')
print(t_cr)

# Исключение незначимых коэффициентов из модели:

for i in range(F.shape[1]):
    if abs(T[i]) <= t_cr:
        B[i] = 0
        
print('\nВектор коэффициентов регрессии после исключения незначимых факторов: \n')
print(B)

# Составление новой матрицы значений базисных функций:

FF = np.zeros((Y.shape[0], 0))
H = np.zeros((Y.shape[0], 1)) # вспомогательная матрица

for i in range(F.shape[1]):
    if B[i] != 0:
        for j in range(Y.shape[0]):
            H[j] = F[j][i]
        FF = np.hstack([FF, H])
        
print('\nНовая матрица значений базисных функций F: \n')
print(FF)

# Повторное определение точечных оценок коэффициентов регрессии:

CC = np.linalg.inv(np.dot(FF.T, FF))
BB = np.dot(CC, np.dot(FF.T, Y))

print('\nНовая матрица C: \n')
print(CC)

BBB = np.zeros((B.shape[0], 1))

j = 0
for i in range(B.shape[0]):
    if B[i] != 0:
        BBB[i] = BB[j]
        j += 1
        
print('\nНовый вектор коэффициентов регрессии B: \n')
print(BBB)

# Прогнозирование значений отклика с помощью полученных коэффициентов:

Y_pr = np.zeros((Y.shape[0], 1))

for i in range(Y.shape[0]):
    for j in range(BBB.shape[0]):
        Y_pr[i] += BBB[j]*F[i][j]
    
# Определение оценки остаточной дисперсии:
    
s_rem_2 = 0
    
for i in range(Y.shape[0]):
    s_rem_2 += (1/(Y.shape[0] - BB.shape[0]))*((Y[i] - Y_pr[i])**2)

# Проверка адекватности модели:

print('\nПроверка адекватности модели: \n')

print('   - оценка остаточной дисперсии s_rem_2: \n')
print(s_rem_2)
        
f = s_rem_2/s_e_2

print('\n   - nараметр f: \n')
print(f)

f_cr = sc.stats.f.ppf(1 - alpha, Y.shape[0] - BB.shape[0], Y_SP.shape[0] - 1)

print('\n   - критическое значение параметра f: \n')
print(f_cr)

if f <= f_cr:
    print('\n   таким образом, модель адекватна! \n')
else:
    print('\n   таким образрм, модель неадекватна! \n')
    
# Проверка работоспособности модели с помощью коэффициента детерминации:

print('Проверка работоспособности модели:  \n')

y_av = 0 # Среднее значение отклика
s_y_2 = 0 # Точечная оценка дисперсии

for i in range(Y.shape[0]):
    y_av += (1/Y.shape[0]) * Y[i]
    
for i in range(Y.shape[0]):
    s_y_2 += (1/(Y.shape[0] - 1))*((Y[i] - y_av)**2)


r_2 = 1 - ((Y.shape[0] - BB.shape[0])/(Y.shape[0] - 1))*(s_rem_2/s_y_2)

print('   - среднее значение отклика y_av: \n')
print(y_av)
print('\n   - точечная оценка дисперсии s_y_2: \n')
print(s_y_2)
print('\n   - коэффициент детерминации (если близок к 1, значит модель работоспособна): \n')
print(r_2)

input()


       
    

    