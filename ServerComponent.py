import numpy as np


class ServerComponent:

    def __init__(self, ld, mi, server, name):
        # lambda
        self.ld = ld
        # mi
        self.mi = mi
        self.server = server
        self.name = name

    # returns [[downtime, repair_time, object], [...]]
    def create_life_time(self, sim_time) -> list:

        res = []
        current_time = 0
        while current_time < sim_time:
            ld_time = np.random.exponential(self.ld)
            # randomization of the moment of failure
            current_time = current_time + ld_time
            # randomization of the failure type
            if np.random.random() < 0.3:
            # randomization of the repair time
                mi_time = np.random.exponential(self.mi)
                fault_type = 1
            else:
                mi_time = np.random.exponential(self.mi)
                fault_type = 2
            res.append([current_time, mi_time, self, fault_type])
            current_time = current_time + mi_time
        return res


def main():
    x = ServerComponent(2000, 24, 100000)
    x.create_life_time()


if __name__ == '__main__':
    main()
