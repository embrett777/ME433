from ulab import numpy as np
import board

dt = 1.0/1024
t = np.arange(0.0, 1.0, dt)

s = np.sin(2 * np.pi * 2 * t)
r = np.sin(2 * np.pi * 20 * t)
q = np.sin(2 * np.pi * 200 * t)

total = s + r + q

y = total
Y = np.fft.fft(y)

Y = Y[:int(len(y)/2)]

for i in range(len(Y[0])):
    print(np.sqrt((Y[0][i])**2+(Y[1][i])**2))

