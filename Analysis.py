import os
import matplotlib.pyplot as plt
import numpy as np

# tu podac sciezku do pliku z ktorego checmy obliczyc procent sprawnosci dzialania systemu
filename = "output/simulation_0/online_offline_simulation_0.txt"
active_time = 0
total_time = 0

with open(filename, "r") as file:
    for line in file:
        time, status = line.strip().split(";")
        if int(status) == 1:
            active_time += 1
        total_time += 1

active_percentage = active_time / total_time * 100
inactive_percentage = 100 - active_percentage

labels = ['Jest Sprawny', 'Nie Jest Sprawny']
sizes = [active_percentage, inactive_percentage]
colors = ['#4CAF50', '#E53935']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Dostępność systemu w przeciągu roku')
plt.show()

