import os
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

print("Serwerownia jest sprawna: {:.2f}%".format(active_percentage))
print("Serwierownia nie jest sprawna: {:.2f}%".format(inactive_percentage))