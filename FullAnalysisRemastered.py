import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

dostepny = 0
niedostepny = 0
iloscTestow = 100
failure_hours_total = []
totalServerUptime = []

for i in range(iloscTestow):

    # tu podac sciezku do pliku z ktorego checmy obliczyc procent sprawnosci dzialania systemu
    data = np.loadtxt("output/simulation_1/online_offline_simulation_" + str(i) + ".txt", delimiter=";")
    total_time = 100000*0.00365

    # Przeliczenie czasów na dni
    data[:, 0] = data[:, 0] * 0.00365

    # Obliczenie czasów działania i czasów awarii do histogramu
    working_hours = (data[:, 0][data[:, 1] == 1] - data[:, 0][data[:, 1] == 0]) * 24
    failure_hours = (data[:, 0][data[:, 1] == 0] - data[:, 0][data[:, 1] == 1]) * 24
    year = 365
    for i in range(len(failure_hours)):
        failure_hours_total.append(failure_hours[i])
        year = year - failure_hours[i] / 24

    totalServerUptime.append(year)
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

    #Sumowanie dostępności serwerów w n próbkach
    dostepny += active_percentage
    niedostepny += inactive_percentage

    workingTime = []
    lastDefect = 0
    stanLista = [0]
    czasLista = [0.0]

    for d in data[:,:]:
        czasLista.append(d[0])
        czasLista.append(d[0])
        if d[1] == 0:
            lastDefect = d[0]
            stanLista.append(1)
        else:
            workingTime.append(d[0] - lastDefect)
            stanLista.append(0)
        stanLista.append(d[1])
    workingTime.append(365 - lastDefect)
    stanLista.append(0)
    czasLista.append(365)


dostepny = dostepny / iloscTestow
niedostepny = niedostepny / iloscTestow
labels = ['Jest Sprawny', 'Nie Jest Sprawny']
sizes = [dostepny, niedostepny]
colors = ['#4CAF50', '#E53935']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Dostępność systemu w przeciągu roku')
plt.show()
#
# # Obliczenie statystyk punktowych
# mean = np.mean(uptime) * 1000
# mean_ci = np.percentile(uptime, [2.5, 97.5]) * 1000
# variance = np.var(uptime) * 1000
# min_val = np.min(uptime) * 1000
# max_val = np.max(uptime) * 1000
#
# # Obliczenie poziomu ryzyka
# lambda_ = len(uptime) / total_time
# risk = poisson.cdf(np.floor(0.99*total_time), lambda_)
#
# # Wyświetlenie wyników
# print(f"Średni czas działania: {mean:.2f} ({mean_ci[0]:.2f}, {mean_ci[1]:.2f})")
# print(f"Wariancja czasu działania: {variance:.2f}")
# print(f"Najkrótszy czas działania: {min_val:.2f}")
# print(f"Najdłuższy czas działania: {max_val:.2f}")
# print(f"Poziom ryzyka w %: {risk:.5f}")
#
# Ogólny stan serwerowni w trakcie roku
# plt.plot(czasLista, stanLista)
# plt.title("Linia czasu dostępności serwera")
# plt.xlabel("Czas (dni)")
# plt.ylabel("Stan")
# plt.xlim(0, total_time)
# plt.show()
#
# # Empiryczna funkcja dystrybucji
# n = len(uptime)
# x = np.sort(uptime)
# y = np.arange(1, n + 1) / n
# plt.step(x, y)
# plt.title("Empirical distribution function")
# plt.xlabel("Time (days)")
# plt.ylabel("Probability")
# plt.show()
#
# Histogram awarii
plt.hist(failure_hours_total, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii')
plt.show()

#Histogram czasu działania serwera
plt.hist(totalServerUptime, bins=100, range=(358, 365), color='green', alpha=0.7)
plt.xlabel('Ilość dni w ciągu roku')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu dostępności serwera')
plt.show()


# Histogram naprawy
# plt.hist(working_hours_total, bins=100, range=(0, 20), color='red', alpha=0.7)
# plt.xlabel('Czas przerwy (godzin)')
# plt.ylabel('Częstotliwość')
# plt.title('Dystrybucja czasu sprawności')
# plt.show()

# Histogram czasu działania
# plt.hist(working_hours_total, bins = 90)
# plt.title("Czas działania serwera")
# plt.xlabel("Czas (dni)")
# plt.ylabel("Częstotliwość")
# plt.show()