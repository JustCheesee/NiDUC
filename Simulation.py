from Server import Server
from Service import Service
import os


class Simulation:
    counter_id = 0

    def __init__(self, sim_time):
        self.sim_time = sim_time
        self.queue = []
        self.repair = []
        self.relations = ""

    def create_servers(self, file_name, num_servers):
        for i in range(num_servers):
            Simulation.counter_id += 1
            server = Server(Simulation.counter_id)
            server.load_config(file_name, self.sim_time)
            for incident in server.queue:
                self.queue.append(incident)
        self.sort_queue()
        # repair crew ? w tym miejscu

    def load_repair(self, file_name):
        with open(file_name, 'r') as file:
            config = file.readlines()
        for l in config:
            line = l.split(";")
            service = Service(int(line[0]), int(line[1]), int(line[2]))
            self.repair.append(service)
        # for service in self.repair:
        #   print(service.services)

    # Ustaw połączenia między serwerami
    def set_relations(self, file_name):
        with open(file_name, 'r') as file:
            config = file.readlines()
        for l in config:
            self.relations = l

    # Sortowanie kolejki według czasow
    def sort_queue(self):
        n = len(self.queue)
        swapped = False
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.queue[j][0] > self.queue[j + 1][0]:
                    swapped = True
                    self.queue[j], self.queue[j + 1] = self.queue[j + 1], self.queue[j]
            if not swapped:
                return

    # naprawa niesamodzielna na całym queue
    def service_repair(self, sim_time, availability_level):
        shift = 0
        repair_time = 0
        next_crew_up = sim_time

        for incident in self.queue:
            # uwolnij crew tutaj
            # ... 
            for crew in self.repair:
                if not crew.free:
                    if crew.time_free < incident[0]:
                        crew.free = True
                        crew.time_free = 0
                        next_crew_up = incident[0]

            if incident[3] > 1:
                # sprawdz czy dostepna ekipa
                for crew in self.repair:
                    if crew.free:
                        # jesli dostepna, zmien jej stan i pobierz czas naprawy
                        repair_time = crew.services[availability_level]
                        crew.free = False
                        crew.time_free = repair_time + incident[0] + incident[1]  # dodanie czasu naprawy
                        break
                    else:
                        if crew.time_free < next_crew_up:
                            next_crew_up = crew.time_free
                # kazda ekipa zajeta
                if repair_time == 0:
                    for crew in self.repair:
                        # znaleziono odpowiednia ekipe
                        if crew.time_free == next_crew_up:
                            repair_time = crew.services[availability_level] + next_crew_up - incident[0]
                            # shift += next_crew_up - incident[0]
                            shift = next_crew_up - incident[0]
                            crew.free = False
                            crew.time_free += repair_time
                            break
                if incident[0] + incident[1] + repair_time + shift < sim_time:
                    # incident[0] += shift
                    incident[1] += repair_time
                else:
                    self.queue.remove(incident)
            else:
                if incident[0] + shift + incident[1] < sim_time:
                    o = 0
                    # incident[0] += shift
                else:
                    self.queue.remove(incident)
            repair_time = 0

    # Tworzenie folderu i zapisywanie wynikow do plikow (jeden plik to jeden serwer)
    def write_output(self, counter: int, folder: str):
        # folders = 0
        # for dir_names in os.walk("./output"):
        #     folders += 1
        # folders = folders - 1
        # path = "./output/simulation_" + str(folder)
        path = "./output/" + str(folder)
        # os.mkdir(path)
        # for incident in self.queue:
        #     file_name = str(incident[2].server).replace("<", "")
        #     file_name = file_name.replace(">", "")
        #     f = open(path + "/" + file_name + ".txt", "a")
        #     f.write(str(incident[2].name) + ";" + str(incident[0]) + ";" + str(incident[3]) + "\n")
        #     f.write(str(incident[2].name) + ";" + str(incident[0] + incident[1]) + ";0\n")
        #     f.close()

        # generalna kolejka
        f = open("./output/gen_queue/general_queue_simulation_" + str(counter) + ".txt", "a")
        for incident in self.queue:
            f.write(str(incident[2].server.id) + ";" + "2137" + ";" + str(incident[0]) + ";" + str(
                incident[3]) + "\n")
            f.write(str(incident[2].server.id) + ";" + "2137" + ";" + str(
                incident[0] + incident[1]) + ";0\n")
        f.close()

        # serwerownia online/offline
        # self.relations.count()
        f = open(path + "/online_offline_simulation_" + str(counter) + ".txt", "a")
        shift = 0
        potential_shift = 0
        status_table = []
        for i in range(Simulation.counter_id):
            status_table.append(0)

        for crew in self.repair:
            crew.free = True
            crew.time_free = 0

        for incident in self.queue:
            # uwolnij crew tutaj
            # ... 
            for crew in self.repair:
                if not crew.free:
                    if crew.time_free < incident[0]:
                        crew.free = True
                        crew.time_free = 0

            # aktualizacja stanów serwerów
            for i in range(len(status_table)):
                if status_table[i] <= incident[0] + shift:
                    status_table[i] = 0

            ### 
            txt = self.relations
            for i in range(1, Simulation.counter_id + 1):
                temp = 0
                if status_table[i - 1] == 0:
                    temp = 1
                txt = txt.replace(str(i), str(temp))

            # serwerownia działa
            # if eval(txt) == 1:

            # serwerownia nie działa
            if eval(txt) != 1:
                shift += potential_shift
                # aktualizacja stanów serwerów
                for i in range(len(status_table)):
                    if status_table[i] <= incident[0] + shift:
                        status_table[i] = 0

            # samonaprawialne    
            if incident[3] < 2:
                status_table[incident[2].server.id - 1] = incident[0] + incident[1] + shift
                # wypisz do pliku
                # 
            # niesamonaprawialne
            else:
                # sprawdz pracownikow
                lowest_time = 0
                for crew in self.repair:
                    if crew.free == True:
                        crew.free = False
                        crew.time_free = incident[0] + incident[1] + shift
                        lowest_time = 0
                        break
                    else:
                        if lowest_time > crew.time_free:
                            lowest_time = crew.time_free
                # dostepny pracownik
                if lowest_time == 0:
                    status_table[incident[2].server.id - 1] = incident[0] + incident[1] + shift

                # potrzeba poczekania na następne crew
                else:
                    incident[1] += lowest_time - (incident[0] + shift)
                    for crew in self.repair:
                        if crew.time_free == lowest_time:
                            crew.free = False
                            crew.time_free = incident[0] + incident[1] + shift
                            break
                    status_table[incident[2].server.id - 1] = incident + incident[1] + shift
            # potrzebne w tej wersji
            potential_shift = incident[1]

            # sprawdzenie obecnego stanu serwera
            txt = self.relations
            for i in range(1, Simulation.counter_id + 1):
                temp = 0
                if status_table[i - 1] == 0:
                    temp = 1
                txt = txt.replace(str(i), str(temp))

            if eval(txt) != 1:
                f.write(str(incident[0] + shift) + ";1;" + str(incident[3]) + "\n")
                f.write(str(incident[0] + incident[1] + shift) + ";0;" + str(incident[3]) + "\n")


            # jesli potrzebny debug, można odkomentować
            # print(txt)
            # print(incident[2].server.id, " ", incident[0] + shift, " ", incident[1], " ", incident[3], " ", eval(txt))
        f.close()


def timesRunning(times: int, folder: str):
    path = "./output/" + str(folder)
    os.mkdir(path)
    path = "./output/gen_queue"
    os.mkdir(path)
    for i in range(times):
        x = Simulation(100000)
        x.load_repair("repair.txt")
        x.create_servers("config.txt", 9)
        x.service_repair(x.sim_time, 0)
        x.set_relations("server_relations.txt")
        x.write_output(i, folder)
        Simulation.counter_id = 0

def main():
    timesRunning(10000, "simulation_1")


if __name__ == '__main__':
    main()
