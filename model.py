import random
import math
import numpy as np
import matplotlib.pyplot as plt

def age_infested(yard_age):
	for square_index in range(len(yard_age)):
		if yard_age[square_index] > 0:
			yard_age[square_index] += 1

def ruin_old_infested(yard, yard_age):
	for square_index in range(len(yard)):
		if yard[square_index] == 1 and yard_age[square_index] > 14:
			yard[square_index] = 2

def gen_spread(reproduction_rate, cross_contamination_rate):
	yard = [0] * 10000
	yard_age = [0] * 10000
	weeds = 10
	suspectible = len(yard) - weeds

	for i in range(weeds):
		r = random.randint(0, len(yard)/2)
		yard_age[r] = 1
		yard[r] = 1

	day = 0
	day_cases = []
	while yard.count(1) != 0 or yard.count(2) != len(yard):
		# print(f'infested = {yard.count(1)}, susceptible = {yard.count(0)}')
		i_to = reproduction_rate * min(yard.count(1) * cross_contamination_rate, yard.count(0))
		new_exposures = min(yard.count(1) * cross_contamination_rate, yard.count(0))

		infested = 0
		sus = 0

		for _ in range(round(new_exposures)):
			r = random.uniform(0,1)

			if r > reproduction_rate:
				infested += 1
			else:
				sus += 1

		day_count = 0
		for _ in range(infested):
			day_count += 1

			r = random.randint(0, len(yard)-1)
			
			while(yard[r] != 0):
				r = random.randint(0, len(yard)-1)

			yard_age[r] = 1
			yard[r] = 1

		day_cases.append(day_count)
		ruin_old_infested(yard, yard_age)
		age_infested(yard_age)
		day += 1

	return day_cases

def main():
	for x in [0.9, 0.6, 0.4, 0.3, 0.2]:
		day_cases = gen_spread(x, 1.0)
		plt.plot(list(range(len(day_cases))), day_cases)
		pt = max(day_cases)
		plt.annotate(f'r0={x}, c=1.0', (day_cases.index(pt), pt))

	plt.title('weed spread per day')
	plt.xlabel('days')
	plt.ylabel('infections per day')
	plt.show()

if __name__ == '__main__':
	main()
