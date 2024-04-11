import numpy as np
import matplotlib.pyplot as plt

# # range1 = np.arange(15)
# # print(range1)
# # #размерность
# # print(range1.ndim)
# # print(range1.size)


# # #преобразование в матрицу 3 строки и 5 столбцов
# # arr1 = range1.reshape(3,5)

# # print(arr1)
# # print(arr1.ndim)
# # print(arr1.size)


# # #из обычного массива в numpy массив:
# # list1  = [1,3,5,6,7]
# # print(list1)
# # range2 = np.array(list1)
# # print(range2)



# # arr2 = np.array([1,2,7],[3,4,8], dtype=complex)
# # print(arr2[0,1].real)


# # range3 = np.pi * np.ones((2,3), dtype=np.float64)
# # print(range3)

# #от до  количество элементов тип
# # range4 = np.linspace(0,2,11,dtype=complex)
# # print(range4)

# #доступ к элементам
# # t = np.linspace(0,99, 100)
# # print(t)


# t1 = np.linspace(0,10,6).reshape(6,1)
# t2 = np.linspace(10,20,5).reshape(1,5)

# #произведение векторов
# prod1 = t1@t2
# print(prod1)

# #dot - векторное произведение
# np.dot(t1,t2)
# print(prod1[1:3,0:4])

chartLen = 100
maxTime = 1e-3
step = maxTime/(chartLen-1)


t = np.linspace(0, maxTime-step, chartLen)

w1 = 2e3*2*np.pi
w2 = 1e3*2*np.pi

A1 = 6
ph1 = 50
s1 = A1*np.cos(w1*t+ph1*np.pi/180)


A1 = 10
ph2 = 30
s2 = A1*np.cos(w2*t+ph2*np.pi/180)

C = 5

s_sum = s1+s2+C

# plt.plot(t,s1)
# plt.plot(t,s2)
# plt.plot(t,s_sum)

fig, ax = plt.subplots()
# line1 = ax.plot(t,s1, label='line1', linestyle='--', linewidth=2, color='r')[0]
# line2 = ax.plot(t,s2, label='line2', linestyle=':', marker='+')[0]
# line3 = ax.plot(t,s_sum, label='line3', linestyle=':', marker='^')[0]

ax.grid()



#исключительно для дискретных
spectr = np.fft.fftshift(np.fft.fft(s_sum))/chartLen

freq = [ftemp/maxTime for ftemp in range(int(-chartLen/2), int(chartLen/2))]



plt.stem(freq, np.abs(spectr))
plt.show()


spectr0 = spectr
#проходим по спектру и все значения,которые меньше 1e3 приравниваем к 0
#исправляем математитческую ошибку
spectr0[np.abs(spectr) < 1e3 ] = 0

plt.stem(freq, np.angle(spectr0)*180/np.pi)
plt.show()
