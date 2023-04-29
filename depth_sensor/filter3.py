import serial
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time

# Configurar la conexión serial
ser = serial.Serial('COM7', baudrate=115200)
ser.reset_input_buffer()

# Parámetros iniciales
tiempo_total = float(input("Ingresa el tiempo de medición (s) : "))
i = 0
windowSize = 2
fs = 0.5

# Crear las listas para almacenar los datos
t = []
distancia = []
no_sporious = []
moving_average = deque(maxlen=windowSize)
sigma = []

# Configurar la gráfica
plt.figure()
line1, = plt.plot(t, distancia, 'r', label='Distancia')
line2, = plt.plot(t, no_sporious, 'g', label='No Spurious')
line3, = plt.plot(t, sigma, 'b', label='Sigma')
plt.xlabel("Tiempo [seg]")
plt.ylabel("Distancia [cm]")
plt.legend()
plt.title("Grafica en Tiempo Real")
plt.show(block=False)

# Bucle para leer y plotear los datos en tiempo real
start_time = time.time()
while (time.time() - start_time) < tiempo_total:
    t.append(time.time() - start_time)
    # Leer los datos del puerto serie
    distancia.append(int(ser.readline().decode().strip()))
    moving_average.append(np.mean(distancia))
    sigma.append(distancia[-1] - moving_average[-1])

    # Calcular no_sporious
    if len(distancia) > 1:
        if (distancia[-1] >= moving_average[-1] + np.ptp(sigma)) or (distancia[-1] <= moving_average[-1] - np.ptp(sigma)):
            no_sporious.append(no_sporious[-1])
        else:
            no_sporious.append(distancia[-1])
    else:
        no_sporious.append(distancia[-1])

    # Actualizar los datos de la gráfica en tiempo real
    line1.set_data(t, distancia)
    line2.set_data(t, no_sporious)
    line3.set_data(t, sigma)
    plt.xlim(min(t), max(t))
    plt.ylim(min(distancia), max(distancia))
    plt.pause(0.01)

ser.close()