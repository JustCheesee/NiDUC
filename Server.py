from ServerComponent import ServerComponent

class Server:
    def __init__(self):
        self.queue = []

    def load_config(self, file_name, sim_time):
        with open(file_name, 'r') as file:
            config = file.readlines()
        for l in config:
            line = l.split(";")
            for i in range(int(line[1])):
                component = ServerComponent(int(line[2]), int(line[3]), self, line[0])
                for x in component.create_life_time(sim_time):
                    self.queue.append(x)
        self.shift_queue(sim_time)

    #Przesuniecie komponentow w czasie o czas naprawy poprzednich elementow (zakladamy ze podczas naprawy serwer jest wylaczony)
    def shift_queue(self, sim_time):
        shift = 0
        for incident in self.queue:
            # jeœli incident to niesamonaprawialny
            #if incident[3] > 1:
                # sprawdzenie czy dostepny serwis
                # find_repair_team()
                        
                # jesli dostepny, oblicz czas naprawy
            if incident[0] + shift + incident[1] < sim_time:                               
                incident[0] = incident[0] + shift
                shift += incident[1]
            else:
                self.queue.remove(incident)

def main():
    x = Server()
    x.load_config("config.txt", 10000)
    print(x.queue)


if __name__ == '__main__':
    main()
