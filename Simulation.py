from Server import Server
import os


class Simulation:

    def __init__(self, sim_time):
        self.sim_time = sim_time
        self.queue = []

    def create_servers(self, file_name, num_servers):
        for i in range(num_servers):
            server = Server()
            server.load_config(file_name, self.sim_time)
            for incident in server.queue:
                self.queue.append(incident)
        self.sort_queue()

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
            f.write(str(incident[2].name)+";"+str(incident[0])+";1\n")
            f.write(str(incident[2].name)+";"+str(incident[0]+incident[1])+";0\n")
            f.close()


def main():
    x = Simulation(100000)
    x.create_servers("config.txt", 3)
    x.write_output()


if __name__ == '__main__':
    main()
