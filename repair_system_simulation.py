#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

class ServerRoom:
	def __init__(self, t):
		self.t = t
		self.element = self.Repairable_element(20000, 24, t)

	class Repairable_element:
		def __init__(self, lam, mi, t):
			self.lam = lam
			self.mi = mi
			self.t = t

		def simulation(self):								# l = lambda
			time = 0.0
			status = 0
			statusList = [0]
			timeList = [0.0]
			readiness = 0.0

			print("Czas: ", time, " Stan: ", status)

			while time < self.t:
				statusList.append(status)
				if status == 0:										# functional element - damage will occur
					r = np.random.exponential(self.lam)
					time = time + r									# randomization of the moment of failure
					readiness = readiness + r
					timeList.append(time)
					status = 1										# status change to 1 (failed item)
				else:
					time = time + np.random.exponential(self.mi)	 # randomization of the moment of completion of repairs
					timeList.append(time)
					status = 0
				print("Czas: ", time, " Stan: ", status)
				statusList.append(status)
				timeList.append(time)

			print(readiness / time)

			plt.plot(timeList, statusList)
			plt.xlim(0, self.t)
			plt.show()
	
	class Repair:
		pass	

def main():

	s1 = ServerRoom(100000)
	s1.element.simulation()

if __name__ == '__main__':
	main()