#!/usr/bin/env python3
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

def element_naprawialny(l, mi, t):							#l = lambda
	czas = 0.0
	stan = 0
	stanLista = [0]
	czasLista = [0.0]

	print("Czas: ", czas, " Stan: ", stan)

	while czas < t:
		s = stan;											# stan aktualny
		if stan == 0:										# element sprawny - wystąpi uszkodzenie
			czas = czas + np.random.exponential(l);			# losowanie chwili uszkodzenia
			czasLista.append(czas)
			stanLista.append(stan)
			stan = 1;										# zmiana stanu na 1 (element uszkodzony)
		else:
			czas = czas + np.random.exponential(mi);		# losowanie chwili zakończenia naprawy
			czasLista.append(czas)
			stanLista.append(stan)
			stan = 0;
		print("Czas: ", czas, " Stan: ", stan)
		stanLista.append(stan)
		czasLista.append(czas)

	plt.plot(czasLista, stanLista)
	plt.xlim(0, t)
	plt.show()

def main():
	element_naprawialny(1000, 100, 10000)
		
if __name__ == '__main__':
	main()
