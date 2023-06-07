import numpy as np
import matplotlib.pyplot as plt

available = 0
unavailable = 0
numTests = 10000
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

# Contract options
total_Interruptions = 0
# 1. Standard 95%
chance_std = 0
total_interruptions_std = 0
max_interruptions_std = 0
avg_repair_time_std = 0

# 2. Premium 99%
chance_pr = 0
total_interruptions_pr = 0
max_interruptions_pr = 0
avg_repair_time_pr = 0

for i in range(numTests):

    # Enter the path to the file from which we want to calculate the percentage of system operation
    data = np.loadtxt("output/simulation_1/online_offline_simulation_" + str(i) + ".txt", delimiter=";")
    data_gen = np.loadtxt("output/gen_queue/general_queue_simulation_" + str(i) + ".txt", delimiter=";")
    total_time = 100000*0.00365

    # Time to days converter
    data[:, 0] = data[:, 0] * 0.00365
    data_gen[:, 2] = data_gen[:, 2] * 0.00365

    # Calculation of the sum of failure hours
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

    # Calculation of working & failure times for a histogram
    working_hours = (data[:, 0][data[:, 1] == 1] - data[:, 0][data[:, 1] == 0]) * 24
    failure_hours = (data[:, 0][data[:, 1] == 0] - data[:, 0][data[:, 1] == 1]) * 24
    year = 365

    total_Interruptions = 0
    isMoreStd = False
    isMorePr = False
    avg_repair_time = 0

    j = 0
    counter_type1 = 0
    counter_type2 = 0
    for i in range(len(failure_hours)):
        total_Interruptions += 1
        if data[j][2] == 2:
            failure_hours_total_type2.append(failure_hours[i])
            counter_type2 += 1
        if data[j][2] == 1:
            failure_hours_total_type1.append(failure_hours[i])
            counter_type1 += 1
        failure_hours_total.append(failure_hours[i])
        year = year - failure_hours[i] / 24

        # Calculation of the maximum failure period
        if failure_hours[i] > 24:
            isMoreStd = True
        if failure_hours[i] > 12:
            isMorePr = True

        # Calculation of the average repair time
        avg_repair_time += failure_hours[i]
        j += 2
    total_important_failures_type1 += counter_type1
    total_important_failures_type2 += counter_type2

    avg_repair_time = avg_repair_time / total_Interruptions
    if avg_repair_time < 5:
        avg_repair_time_std += 1
    if avg_repair_time < 3:
        avg_repair_time_pr += 1
    if not isMoreStd:
        max_interruptions_std += 1
    if not isMorePr:
        max_interruptions_pr += 1

    totalServerUptime.append(year)

    # Calculation of uptime and downtime
    downtime = data[:, 0][data[:, 1] == 1]
    uptime = data[:, 0][data[:, 1] == 0]

    downtime_downtime = uptime
    for x in range(len(downtime)):
        downtime_downtime[x] = uptime[x] - downtime[x]
    # Calculation of the overall availability
    downtime_sum = np.sum(downtime_downtime)
    active_percentage = 100 - (downtime_sum / total_time) * 100
    inactive_percentage = 100 - active_percentage

    # Calculation of the chance of achieving expected availability
    if active_percentage > 95:
        chance_std += 1
    if active_percentage > 99:
        chance_pr += 1

    # Calculation of the number of interruptions
    if total_Interruptions < 52:
        total_interruptions_std += 1
    if total_Interruptions < 22:
        total_interruptions_pr += 1

    # Sum of server availability in n samples
    available += active_percentage
    unavailable += inactive_percentage

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


available = available / numTests
unavailable = unavailable / numTests
labels = ['Jest Sprawny', 'Nie Jest Sprawny']
sizes = [available, unavailable]
colors = ['#4CAF50', '#E53935']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Dostępność systemu w przeciągu roku')
plt.show()

# failure hours histogram
plt.hist(failure_hours_total, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii')
plt.show()

# type 1 failures histogram
plt.hist(failure_hours_total_type1, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii dla typu 1')
plt.show()

# type 2 failures histogram
plt.hist(failure_hours_total_type2, bins=100, range=(0, 20), color='green', alpha=0.7)
plt.xlabel('Czas przerwy (godzin)')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu awarii dla typu 2')
plt.show()

# server uptime histogram
plt.hist(totalServerUptime, bins=100, range=(358, 365), color='green', alpha=0.7)
plt.xlabel('Ilość dni w ciągu roku')
plt.ylabel('Ilość')
plt.title('Dystrybucja czasu dostępności serwera')
plt.show()

chance_std = chance_std / numTests * 100
chance_pr = chance_pr / numTests * 100
print("Szansa na osiągnięcie dostępności > 95%: " + str(chance_std))
print("Szansa na osiągnięcie dostępności > 99%: " + str(chance_pr))
total_interruptions_std = total_interruptions_std / numTests * 100
total_interruptions_pr = total_interruptions_pr / numTests * 100
print("Szansa na osiągnięcie ilości przerw < 52: " + str(total_interruptions_std))
print("Szansa na osiągnięcie ilości przerw < 22: " + str(total_interruptions_pr))
maksPrzerwStd = max_interruptions_std / numTests * 100
max_interruptions_pr = max_interruptions_pr / numTests * 100
print("Szansa na osiągnięcie maksymalnej długości przerwy < 24: " + str(maksPrzerwStd))
print("Szansa na osiągnięcie maksymalnej długości przerwy < 12: " + str(max_interruptions_pr))
failure_hours_sum_type1 = failure_hours_sum_type1 / numTests * 24
failure_hours_sum_type2 = failure_hours_sum_type2 / numTests * 24
print("Średnia suma czasów napraw typu 1: " + str(failure_hours_sum_type1))
print("Średnia suma czasów napraw typu 2: " + str(failure_hours_sum_type2))
failure_hours_avg_type1 = failure_hours_avg_type1 / numTests * 24
failure_hours_avg_type2 = failure_hours_avg_type2 / numTests * 24
print("Średnia czasów napraw typu 1: " + str(failure_hours_avg_type1))
print("Średnia czasów napraw typu 2: " + str(failure_hours_avg_type2))
total_failures_count_type1 = total_failures_count_type1 / numTests
total_failures_count_type2 = total_failures_count_type2 / numTests
print("Średnia ilość wszystkich awarii typu 1: " + str(total_failures_count_type1))
print("Średnia ilość wszystkich awarii typu 2: " + str(total_failures_count_type2))
total_important_failures_type1 = total_important_failures_type1 / numTests
total_important_failures_type2 = total_important_failures_type2 / numTests
print("Średnia ilość wszystkich awarii typu 1 mających wpływ na przestuj serwerowni: " + str(total_important_failures_type1))
print("Średnia ilość wszystkich awarii typu 2 mających wpływ na przestuj serwerowni: " + str(total_important_failures_type2))
