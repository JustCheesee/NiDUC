import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm

# tu podac sciezku do pliku z ktorego checmy obliczyc procent sprawnosci dzialania systemu
data = np.loadtxt("output/simulation_3/online_offline_simulation_3.txt", delimiter=";")
total_time = 100000*0.00365

# Przeliczenie czasów na dni
data[:, 0] = data[:, 0] * 0.00365

# Obliczenie czasów działania i czasów awarii
downtime = data[:, 0][data[:, 1] == 1]
uptime = data[:, 0][data[:, 1] == 0]

downtime_downtime = uptime
for x in range(len(downtime)):
    downtime_downtime[x] = uptime[x] - downtime[x]
# Obliczenie dostępności
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

# Obliczenie statystyk punktowych
mean = np.mean(uptime) * 1000
mean_ci = np.percentile(uptime, [2.5, 97.5]) * 1000
variance = np.var(uptime) * 1000
min_val = np.min(uptime) * 1000
max_val = np.max(uptime) * 1000

# Obliczenie poziomu ryzyka
lambda_ = len(uptime) / total_time
risk = poisson.cdf(np.floor(0.99*total_time), lambda_)

# Wyświetlenie wyników
print(f"Średni czas działania: {mean:.2f} ({mean_ci[0]:.2f}, {mean_ci[1]:.2f})")
print(f"Wariancja czasu działania: {variance:.2f}")
print(f"Najkrótszy czas działania: {min_val:.2f}")
print(f"Najdłuższy czas działania: {max_val:.2f}")
print(f"Poziom ryzyka w %: {risk:.5f}")

# Wykres rozkładu czasów działania
plt.hist(uptime, bins=10)
plt.title("Uptime distribution")
plt.xlabel("Time (days)")
plt.ylabel("Frequency")
plt.show()

# Wykres rozkładu czasów awarii
plt.hist(downtime, bins=50)
plt.title("Downtime distribution")
plt.xlabel("Time (days)")
plt.ylabel("Frequency")
plt.show()

# Empiryczna funkcja dystrybucji
n = len(uptime)
x = np.sort(uptime)
y = np.arange(1, n + 1) / n
plt.step(x, y)
plt.title("Empirical distribution function")
plt.xlabel("Time (days)")
plt.ylabel("Probability")
plt.show()


