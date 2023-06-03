import numpy as np
import matplotlib.pyplot as plt

dostepny = 0
niedostepny = 0
iloscTestow = 10000
failure_hours_total = []
failure_hours_total_type1 = []
failure_hours_total_type2 = []
totalServerUptime = []
failure_hours_sum_type1 = 0
failure_hours_sum_type2 = 0
failure_hours_avg_type1 = 0
failure_hours_avg_type2 = 0
total_failures_count_type1 = 0
total_failures_count_type2 = 0
total_important_failures_type1 = 0
total_important_failures_type2 = 0

#Warianty umowy
lacznaIloscPrzerw = 0
#1. Standard 95%
szansaStd = 0
iloscPrzerwStd = 0
maksPrzerwStd = 0
srCzasNaprawyStd = 0

#2. Premium 99%
szansaPr = 0
iloscPrzerwPr = 0
maksPrzerwPr = 0
srCzasNaprawyPr = 0

for i in range(iloscTestow):

    # tu podac sciezku do pliku z ktorego checmy obliczyc procent sprawnosci dzialania systemu
    data = np.loadtxt("output/simulation_1/online_offline_simulation_" + str(i) + ".txt", delimiter=";")
    data_gen = np.loadtxt("output/gen_queue/general_queue_simulation_" + str(i) + ".txt", delimiter=";")
    total_time = 100000*0.00365



    # Przeliczenie czasów na dni
    data[:, 0] = data[:, 0] * 0.00365
    data_gen[:, 2] = data_gen[:, 2] * 0.00365


    # Liczenie sumy czasów awarii
    failure_hours_type1 = 0
    failure_hours_type2 = 0
    k = 0
    y = 0
    s = 0
    for j in range(int((len(data_gen) - 1)/2)):
        time = data_gen[k + 1][2] - data_gen[k][2]
        if data_gen[k][3] == 1:
            failure_hours_type1 += time
            y += 1
        else:
            failure_hours_type2 += time
            s += 1
        k += 2
    total_failures_count_type1 += y
    total_failures_count_type2 += s

    failure_hours_sum_type1 += failure_hours_type1
    failure_hours_sum_type2 += failure_hours_type2
    failure_hours_avg_type1 += failure_hours_type1 / y
    failure_hours_avg_type2 += failure_hours_type2 / s


    # Obliczenie czasów działania i czasów awarii do histogramu
    working_hours = (data[:, 0][data[:, 1] == 1] - data[:, 0][data[:, 1] == 0]) * 24
    failure_hours = (data[:, 0][data[:, 1] == 0] - data[:, 0][data[:, 1] == 1]) * 24
    year = 365

    lacznaIloscPrzerw = 0
    isMoreStd = False
    isMorePr = False
    sredniCzasPrzerwy = 0

    j = 0
    counter_type1 = 0
    counter_type2 = 0
    for i in range(len(failure_hours)):
        lacznaIloscPrzerw += 1
        if data[j][2] == 2:
            failure_hours_total_type2.append(failure_hours[i])
            counter_type2 += 1
        if data[j][2] == 1:
            failure_hours_total_type1.append(failure_hours[i])
            counter_type1 += 1
        failure_hours_total.append(failure_hours[i])
        year = year - failure_hours[i] / 24
        #liczenie maksymalnej dlugosci przerwy
        if failure_hours[i] > 24:
            isMoreStd = True
        if failure_hours[i] > 12:
            isMorePr = True
        #liczenie sredniego czasu naprawy
        sredniCzasPrzerwy += failure_hours[i]
        j += 2
    total_important_failures_type1 += counter_type1
    total_important_failures_type2 += counter_type2

    sredniCzasPrzerwy = sredniCzasPrzerwy / lacznaIloscPrzerw
    if sredniCzasPrzerwy < 5:
        srCzasNaprawyStd += 1
    if sredniCzasPrzerwy < 3:
        srCzasNaprawyPr += 1
    if isMoreStd == False:
        maksPrzerwStd += 1
    if isMorePr == False:
        maksPrzerwPr += 1

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

    #liczenie szansy na osiągniecie dostępności
    if active_percentage > 95:
        szansaStd += 1
    if active_percentage > 99:
        szansaPr += 1

    #liczenie ilosci przerw
    if lacznaIloscPrzerw < 52:
        iloscPrzerwStd += 1
    if lacznaIloscPrzerw < 22:
        iloscPrzerwPr += 1

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

# Histogram awarii
plt.hist(failure_hours_total, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii')
plt.show()

# Histogram awarii dla osobnego typu 1
plt.hist(failure_hours_total_type1, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii dla typu 1')
plt.show()

# Histogram awarii dla osobnego typu 2
plt.hist(failure_hours_total_type2, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii dla typu 2')
plt.show()

#Histogram czasu działania serwera
plt.hist(totalServerUptime, bins=100, range=(358, 365), color='green', alpha=0.7)
plt.xlabel('Ilość dni w ciągu roku')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu dostępności serwera')
plt.show()

szansaStd = szansaStd / iloscTestow * 100
szansaPr = szansaPr / iloscTestow * 100
print("Szansa na osiągnięcie dostępności > 95%: " + str(szansaStd))
print("Szansa na osiągnięcie dostępności > 99%: " + str(szansaPr))
iloscPrzerwStd = iloscPrzerwStd / iloscTestow * 100
iloscPrzerwPr = iloscPrzerwPr / iloscTestow * 100
print("Szansa na osiągnięcie ilości przerw < 52: " + str(iloscPrzerwStd))
print("Szansa na osiągnięcie ilości przerw < 22: " + str(iloscPrzerwPr))
maksPrzerwStd = maksPrzerwStd / iloscTestow * 100
maksPrzerwPr = maksPrzerwPr / iloscTestow * 100
print("Szansa na osiągnięcie maksymalnej długości przerwy < 24: " + str(maksPrzerwStd))
print("Szansa na osiągnięcie maksymalnej długości przerwy < 12: " + str(maksPrzerwPr))
failure_hours_sum_type1 = failure_hours_sum_type1 / iloscTestow * 24
failure_hours_sum_type2 = failure_hours_sum_type2 / iloscTestow * 24
print("Średnia suma czasów napraw typu 1: " + str(failure_hours_sum_type1))
print("Średnia suma czasów napraw typu 2: " + str(failure_hours_sum_type2))
failure_hours_avg_type1 = failure_hours_avg_type1 / iloscTestow * 24
failure_hours_avg_type2 = failure_hours_avg_type2 / iloscTestow * 24
print("Średnia czasów napraw typu 1: " + str(failure_hours_avg_type1))
print("Średnia czasów napraw typu 2: " + str(failure_hours_avg_type2))
total_failures_count_type1 = total_failures_count_type1 / iloscTestow
total_failures_count_type2 = total_failures_count_type2 / iloscTestow
print("Średnia ilość wszystkich awarii typu 1: " + str(total_failures_count_type1))
print("Średnia ilość wszystkich awarii typu 2: " + str(total_failures_count_type2))
total_important_failures_type1 = total_important_failures_type1 / iloscTestow
total_important_failures_type2 = total_important_failures_type2 / iloscTestow
print("Średnia ilość wszystkich awarii typu 1 mających wpływ na przestuj serwerowni: " + str(total_important_failures_type1))
print("Średnia ilość wszystkich awarii typu 2 mających wpływ na przestuj serwerowni: " + str(total_important_failures_type2))


