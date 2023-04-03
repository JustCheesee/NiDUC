import numpy as np

class Service:
	# teams_nr - liczba serwisantów, service_types - pakiety normal, premium itd z czasem naprawy
	def __init__(self, standard, premium, extra_premium):
		self.free = True
		self.services = [standard, premium, extra_premium]
		self.time_free = 0

def main():
    s = Service()

if __name__ == '__main__':
    main()