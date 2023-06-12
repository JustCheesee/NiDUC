import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

# enter the path to the file from which we want to calculate the percentage of system operation
data = np.loadtxt("output/simulation_1/online_offline_simulation_1.txt", delimiter=";")
total_time = 100000 * 0.00365

# time convertion to days
data[:, 0] = data[:, 0] * 0.00365

# calculation of the working & failure hours
working_hours = data[:, 0][data[:, 1] == 1] % 24
failure_hours = data[:, 0][data[:, 1] == 0] % 24
downtime = data[:, 0][data[:, 1] == 1]
uptime = data[:, 0][data[:, 1] == 0]

downtime_downtime = uptime
for x in range(len(downtime)):
    downtime_downtime[x] = uptime[x] - downtime[x]
# calculation of the availability
downtime_sum = np.sum(downtime_downtime)
active_percentage = 100 - (downtime_sum / total_time) * 100
inactive_percentage = 100 - active_percentage

workingTime = []
lastDefect = 0
statusList = [0]
timeList = [0.0]

for d in data[:, :]:
    timeList.append(d[0])
    timeList.append(d[0])
    if d[1] == 0:
        lastDefect = d[0]
        statusList.append(1)
    else:
        workingTime.append(d[0] - lastDefect)
        statusList.append(0)
    statusList.append(d[1])
workingTime.append(365 - lastDefect)
statusList.append(0)
timeList.append(365)

labels = ['Jest Sprawny', 'Nie Jest Sprawny']
sizes = [active_percentage, inactive_percentage]
colors = ['#4CAF50', '#E53935']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Dostępność systemu w przeciągu roku')
plt.show()

# Point stats calculations
mean = np.mean(uptime) * 1000
mean_ci = np.percentile(uptime, [2.5, 97.5]) * 1000
variance = np.var(uptime) * 1000
min_val = np.min(uptime) * 1000
max_val = np.max(uptime) * 1000

# Risk level calculation
lambda_ = len(uptime) / total_time
risk = poisson.cdf(np.floor(0.99 * total_time), lambda_)

# Displaying the results
print(f"Średni czas działania: {mean:.2f} ({mean_ci[0]:.2f}, {mean_ci[1]:.2f})")
print(f"Wariancja czasu działania: {variance:.2f}")
print(f"Najkrótszy czas działania: {min_val:.2f}")
print(f"Najdłuższy czas działania: {max_val:.2f}")
print(f"Poziom ryzyka w %: {risk:.5f}")

# General status of the server room during the year
plt.plot(timeList, statusList)
plt.title("Linia czasu dostępności serwera")
plt.xlabel("Czas (dni)")
plt.ylabel("Stan")
plt.xlim(0, total_time)
plt.show()

# Empirical distribution function
n = len(uptime)
x = np.sort(uptime)
y = np.arange(1, n + 1) / n
plt.step(x, y)
plt.title("Empirical distribution function")
plt.xlabel("Time (days)")
plt.ylabel("Probability")
plt.show()

# Failure histogram
plt.hist(failure_hours, bins=24, range=(0, 24), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Częstotliwość')
plt.title('Dystrybucja czasu awarii')
plt.show()

# working time histogram
plt.hist(workingTime, bins=90)
plt.title("Czas działania serwera")
plt.xlabel("Czas (dni)")
plt.ylabel("Częstotliwość")
plt.show()
