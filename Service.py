
class Service:
    # team_nr - number of service technicians, service_types - normal, premium, etc. packages with repair time
    def __init__(self, standard, premium, extra_premium):
        self.free = True
        self.services = [standard, premium, extra_premium]
        self.time_free = 0


def main():
    Service()


if __name__ == '__main__':
    main()
