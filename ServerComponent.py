import numpy as np


class ServerComponent:

    def __init__(self, ld, mi, server, name):
        # lambda
        self.ld = ld
        # mi
        self.mi = mi
        self.server = server
        self.name = name

    # zwraca [[czas_zepsucia, czas_naprawy, obiekt], [...]]
    def create_life_time(self, sim_time) -> list:
        res = []
        current_time = 0
        while current_time < sim_time:
            ld_time = np.random.exponential(self.ld)
            # losowanie chwili uszkodzenia
            current_time = current_time + ld_time
            # losowanie czasu naprawy
            mi_time = np.random.exponential(self.mi)
            res.append([current_time, mi_time, self])
            current_time = current_time + mi_time
        return res


def main():
    x = ServerComponent(2000, 24, 100000)
    x.create_life_time()


if __name__ == '__main__':
    main()
