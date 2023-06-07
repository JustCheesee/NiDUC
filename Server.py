from ServerComponent import ServerComponent


class Server:
    def __init__(self, id):
        self.queue = []
        self.id = id

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

    # Moving components in time by the time of repairing previous elements (assuming that the server is turned off during the repair)
    def shift_queue(self, sim_time):
        shift = 0
        for incident in self.queue:
            if incident[0] + shift < sim_time:
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
