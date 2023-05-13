import os
import matplotlib.pyplot as plt
import numpy as np

# tu podac sciezku do pliku z ktorego checmy obliczyc procent sprawnosci dzialania systemu
data = np.loadtxt("output/simulation_0/online_offline_simulation_0.txt", delimiter=";")
total_time = 100000*0.00365

# Przeliczenie czasów na dni
data[:, 0] = data[:, 0] * 0.00365

# Obliczenie czasów działania i czasów awarii
downtime = data[:, 0][data[:, 1] == 1]
uptime = data[:, 0][data[:, 1] == 0]

downtime_downtime = uptime
for x in range(len(downtime)):
    downtime_downtime[x] = uptime[x] - downtime[x]
# Obliczenie całkowitego czasu i dostępności
downtime_sum = np.sum(downtime_downtime)

active_percentage = 100 - (downtime_sum / total_time) * 100
inactive_percentage = 100 - active_percentage

labels = ['Jest Sprawny', 'Nie Jest Sprawny']
sizes = [active_percentage, inactive_percentage]
colors = ['#4CAF50', '#E53935']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Dostępność systemu w przeciągu roku')
plt.show()

