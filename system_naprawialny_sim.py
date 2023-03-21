#!/usr/bin/env python3
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

class Element_naprawialny:
	def __init__(self, lam, mi, t):
		self.lam = lam
		self.mi = mi
		self.t = t

	def symulacja(self):											#l = lambda
		czas = 0.0
		stan = 0
		stanLista = [0]
		czasLista = [0.0]
		gotowosc = 0.0

		print("Czas: ", czas, " Stan: ", stan)

		while czas < self.t:
			s = stan;												# stan aktualny
			if stan == 0:											# element sprawny - wystąpi uszkodzenie
				r = np.random.exponential(self.lam)
				czas = czas + r										# losowanie chwili uszkodzenia
				gotowosc = gotowosc + r
				czasLista.append(czas)
				stanLista.append(stan)
				stan = 1;											# zmiana stanu na 1 (element uszkodzony)
			else:
				czas = czas + np.random.exponential(self.mi);		# losowanie chwili zakończenia naprawy
				czasLista.append(czas)
				stanLista.append(stan)
				stan = 0;
			print("Czas: ", czas, " Stan: ", stan)
			stanLista.append(stan)
			czasLista.append(czas)

		print(gotowosc/czas)

		plt.plot(czasLista, stanLista)
		plt.xlim(0, self.t)
		plt.show()
	

def main():
	e1 = Element_naprawialny(20000, 24, 100000)
	e1.symulacja()
		
if __name__ == '__main__':
	main()