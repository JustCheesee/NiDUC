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

    def load_repair(self, file_name):
        with open(file_name, 'r') as file:
            config = file.readlines()
        for l in config:
            line = l.split(";")
            service = Service(int(line[0]), int(line[1]), int(line[2]))
            self.repair.append(service)

    # Set up server-to-server connections
    def set_relations(self, file_name):
        with open(file_name, 'r') as file:
            config = file.readlines()
        for l in config:
            self.relations = l

    # Sorting the queue by time
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

    # non-self repair on the whole queue
    def service_repair(self, sim_time, availability_level):
        shift = 0
        repair_time = 0
        next_crew_up = sim_time

        for incident in self.queue:
            # freeing the crew
            for crew in self.repair:
                if not crew.free:
                    if crew.time_free < incident[0]:
                        crew.free = True
                        crew.time_free = 0
                        next_crew_up = incident[0]

            if incident[3] > 1:
                # check if the team is available
                for crew in self.repair:
                    if crew.free:
                        # if yes, change its state and retrieve repair time
                        repair_time = crew.services[availability_level]
                        crew.free = False
                        crew.time_free = repair_time + incident[0] + incident[1]  # adding repair time
                        break
                    else:
                        if crew.time_free < next_crew_up:
                            next_crew_up = crew.time_free
                # if every crew is busy
                if repair_time == 0:
                    for crew in self.repair:
                        # found the team
                        if crew.time_free == next_crew_up:
                            repair_time = crew.services[availability_level] + next_crew_up - incident[0]
                            shift = next_crew_up - incident[0]
                            crew.free = False
                            crew.time_free += repair_time
                            break
                if incident[0] + incident[1] + repair_time + shift < sim_time:
                    incident[1] += repair_time
                else:
                    self.queue.remove(incident)
            else:
                if incident[0] + shift + incident[1] < sim_time:
                    pass
                else:
                    self.queue.remove(incident)
            repair_time = 0

    # Creating a folder and saving the results to files (one file is one server)
    def write_output(self, counter: int, folder: str):
        path = "./output/" + str(folder)

        # general queue
        f = open("./output/gen_queue/general_queue_simulation_" + str(counter) + ".txt", "a")
        for incident in self.queue:
            f.write(str(incident[2].server.id) + ";" + "2137" + ";" + str(incident[0]) + ";" + str(
                incident[3]) + "\n")
            f.write(str(incident[2].server.id) + ";" + "2137" + ";" + str(
                incident[0] + incident[1]) + ";0\n")
        f.close()

        # online/offline server room
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
            # freeing the crew
            for crew in self.repair:
                if not crew.free:
                    if crew.time_free < incident[0]:
                        crew.free = True
                        crew.time_free = 0

            # server status update
            for i in range(len(status_table)):
                if status_table[i] <= incident[0] + shift:
                    status_table[i] = 0

            txt = self.relations
            for i in range(1, Simulation.counter_id + 1):
                temp = 0
                if status_table[i - 1] == 0:
                    temp = 1
                txt = txt.replace(str(i), str(temp))

            # server room is not working
            if eval(txt) != 1:
                shift += potential_shift
                # server status update
                for i in range(len(status_table)):
                    if status_table[i] <= incident[0] + shift:
                        status_table[i] = 0

            # self repair incidents
            if incident[3] < 2:
                status_table[incident[2].server.id - 1] = incident[0] + incident[1] + shift

            # non self repair incidents
            else:
                # check the crew
                lowest_time = 0
                for crew in self.repair:
                    if crew.free:
                        crew.free = False
                        crew.time_free = incident[0] + incident[1] + shift
                        lowest_time = 0
                        break
                    else:
                        if lowest_time > crew.time_free:
                            lowest_time = crew.time_free
                # available crew
                if lowest_time == 0:
                    status_table[incident[2].server.id - 1] = incident[0] + incident[1] + shift

                # the need to wait for the next crew
                else:
                    incident[1] += lowest_time - (incident[0] + shift)
                    for crew in self.repair:
                        if crew.time_free == lowest_time:
                            crew.free = False
                            crew.time_free = incident[0] + incident[1] + shift
                            break
                    status_table[incident[2].server.id - 1] = incident + incident[1] + shift
            # needed in that version
            potential_shift = incident[1]

            # check the current status of the server
            txt = self.relations
            for i in range(1, Simulation.counter_id + 1):
                temp = 0
                if status_table[i - 1] == 0:
                    temp = 1
                txt = txt.replace(str(i), str(temp))

            if eval(txt) != 1:
                f.write(str(incident[0] + shift) + ";1;" + str(incident[3]) + "\n")
                f.write(str(incident[0] + incident[1] + shift) + ";0;" + str(incident[3]) + "\n")

        f.close()


def timesrunning(times: int, folder: str):
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
    timesrunning(10000, "simulation_1")


if __name__ == '__main__':
    main()
