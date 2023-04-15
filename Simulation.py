from Server import Server
from Service import Service
import os
import numpy as np

class Simulation:

    def __init__(self, sim_time):
        self.sim_time = sim_time
        self.queue = []
        self.repair = []

    def create_servers(self, file_name, num_servers):
        for i in range(num_servers):
            server = Server()
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

    #Sortowanie kolejki według czasow
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
                if crew.free == False:
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
                       crew.time_free = repair_time + incident[0]
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
                           shift += next_crew_up - incident[0]
                           crew.free = False
                           crew.time_free += repair_time
                           break
                if incident[0] + incident[1] + repair_time + shift < sim_time:
                    incident[0] += shift
                    incident[1] = repair_time
                else:
                    self.queue.remove(incident)
            else:
                if incident[0] + shift + incident[1] < sim_time:
                    incident[0] += shift
                else:    
                    self.queue.remove(incident)
            repair_time = 0

    #Tworzenie folderu i zapisywanie wynikow do plikow (jeden plik to jeden serwer)
    def write_output(self):
        folders = 0
        for dir_names in os.walk("./output"):
            folders += 1
        folders = folders-1
        path = "./output/simulation_"+str(folders)
        os.mkdir(path)
        for incident in self.queue:
            file_name = str(incident[2].server).replace("<", "")
            file_name = file_name.replace(">", "")
            f = open(path+"/"+file_name+".txt", "a")
            f.write(str(incident[2].name)+";"+str(incident[0])+";"+str(incident[3])+"\n")
            f.write(str(incident[2].name)+";"+str(incident[0]+incident[1])+";0\n")
            f.close()

            # generalna kolejka
            file_name = file_name.replace("Server.Server object at ", "")
            f = open(path+"/general_queue_simulation_" + str(folders) +".txt", "a")
            f.write(file_name+";"+str(incident[2].name)+";"+str(incident[0])+";"+str(incident[3])+"\n")
            f.write(file_name+";"+str(incident[2].name)+";"+str(incident[0]+incident[1])+";0\n")
            f.close()


def main():
    x = Simulation(100000)
    x.load_repair("repair.txt")
    x.create_servers("config.txt", 3)
    x.service_repair(x.sim_time, 0)
    x.write_output()
    for incident in x.queue:
        print(incident[0], " ", incident[1], " ", incident[3])


if __name__ == '__main__':
    main()
