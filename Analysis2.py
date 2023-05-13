import numpy as np
import matplotlib.pyplot as plt

# Tu nazwa plika
data = np.loadtxt("output/simulation_0/online_offline_simulation_0.txt", delimiter=";")

# Przeliczenie czasów na dni
data[:, 0] = data[:, 0] * 0.00365

# Obliczenie czasów działania i czasów awarii
uptime = data[:, 0][data[:, 1] == 0]
downtime = data[:, 0][data[:, 1] == 1]

# Obliczenie całkowitego czasu i dostępności
total_time = np.sum(data[:, 0])
availability = np.sum(uptime) / total_time

# Obliczenie statystyk punktowych
mean = np.mean(uptime)
mean_ci = np.percentile(uptime, [2.5, 97.5])
variance = np.var(uptime)
min_val = np.min(uptime)
max_val = np.max(uptime)

# Wyświetlenie wyników
print(f"Dostępność: {availability:.2%}")
print(f"Średni czas działania: {mean:.2f} ({mean_ci[0]:.2f}, {mean_ci[1]:.2f})")
print(f"Wariancja czasu działania: {variance:.2f}")
print(f"Najkrótszy czas działania: {min_val:.2f}")
print(f"Najdłuższy czas działania: {max_val:.2f}")

# Wykres rozkładu czasów działania
plt.hist(uptime, bins=50)
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

# Empirical distribution function
n = len(uptime)
x = np.sort(uptime)
y = np.arange(1, n+1) / n
plt.step(x, y)
plt.title("Empirical distribution function")
plt.xlabel("Time (days)")
plt.ylabel("Probability")
plt.show()

# Obliczenie prawdopodobieństwa dostępności poniżej 99% w ciągu roku (365 dni)
n_obs = len(data)
lambda_ = n_obs / total_time
prob_below_99 = 1 - np.exp(-lambda_ * (1 - 0.99) * 365 * 24 * 60 * 60)

# Wyświetlenie wyników
print(f"Prawdopodobieństwo rocznej dostępności poniżej 99%: {prob_below_99:.2%}")
