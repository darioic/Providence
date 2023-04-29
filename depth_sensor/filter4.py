import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
moving_average = []
sigma = []

# Configurar la gráfica
fig, ax = plt.subplots()
line1, = ax.plot(t, distancia, 'r', label='Distancia')
line2, = ax.plot(t, no_sporious, 'g', label='No Spurious')
line3, = ax.plot(t, sigma, 'b', label='Sigma')
ax.set_xlabel("Tiempo [seg]")
ax.set_ylabel("Distancia [cm]")
ax.legend()
ax.set_title("Grafica en Tiempo Real")

# Función de animación para actualizar los datos en tiempo real
def update(frame):
    t.append(frame * 0.01)  # Intervalo de tiempo para la animación
    distancia.append(int(ser.readline().decode().strip()))
    moving_average.append(sum(distancia[-windowSize:]) / len(distancia[-windowSize:]))
    sigma.append(distancia[-1] - moving_average[-1])

    if len(distancia) > 1:
        if (distancia[-1] >= moving_average[-1] + max(sigma)) or (distancia[-1] <= moving_average[-1] - max(sigma)):
            no_sporious.append(no_sporious[-1])
        else:
            no_sporious.append(distancia[-1])
    else:
        no_sporious.append(distancia[-1])

    line1.set_data(t, distancia)
    line2.set_data(t, no_sporious)
    line3.set_data(t, sigma)
    ax.relim()
    ax.autoscale_view()
    return line1, line2, line3

# Crear la animación
ani = FuncAnimation(fig, update, frames=range(int(tiempo_total / 0.01)), interval=10, blit=True)

# Mostrar la gráfica en tiempo real
plt.show()

ser.close()