import numpy as np
import math
import random

def initPopulasi(kl, interval, pops):
	return np.random.uniform(-interval, interval, (pops,kl))

def fitness(kr):
	return 1/( (((4 - (2.1 * (kr[0]*kr[0]) ) + (math.pow(kr[0], 4) / 3) )*(kr[0]*kr[0])) + (kr[0]*kr[1]) 
		+ ((-4 + (4 * (kr[1]*kr[1]) )) *kr[1]*kr[1])) + 243)

def selectIndParent(pop):
	total_fitness = 0
	par = 0
	for i in xrange(len(pop)):
		total_fitness += fitness(pop[i])
	
	dart = random.uniform(0,1)*total_fitness
	temp = 0
	for i in xrange(len(pop)):
		temp += fitness(pop[i])
		if dart < temp:
			par = i
			break
	return par

def rekombinasi(pop, indPar):
	child = np.zeros((2,2))
	for i in xrange(len(indPar)):
		parInd = i + 1
		if parInd > (2-1):
			parInd = 0
		for j in range(0,1):
			child[i][j] = pop[int(indPar[i])][j]
		for j in range(1,2):
			child[i][j] = pop[int(indPar[parInd])][j]
	return child

def mutasi(kr, kl, interval):
	mut = random.randint(0,kl-1)
	kr[mut] = (random.uniform(-interval,interval))
	return kr

def fitnessRank(pop):
	return np.array((  np.insert(pop, len(pop[0]), [(fitness(pop[i])) for i in xrange(len(pop))], axis=1)  ))

def selectSurvivor(pop, child):
	sort = fitnessRank(np.append(child,pop,axis=0))[np.argsort(fitnessRank(np.append(child,pop,axis=0))[:,-1])][::-1][:len(pop),:]
	return sort[:,:-1], sort[:,-1]


def evolusi(pop, kl, interval):
	ch = np.zeros((1,kl))
	indPar = np.zeros((2))
	while len(ch) < len(pop):
		for i in xrange(2):
			indPar[i] = selectIndParent(pop)
		rek = rekombinasi(pop, indPar)

		for i in xrange(2):
			rek[i] = mutasi(rek[i], kl, interval)
		ch = np.append(ch,rek,axis=0)
	ch = np.delete(ch,0,0)
	return ch

def ga(kl, interval, pops, gens):
	pop = initPopulasi(kl, interval, pops)
	gen = 1
	while gen <= gens:
		ch = evolusi(pop, kl, interval)
		pop, sortFitness = selectSurvivor(pop,ch)
		print gen,' : Individu Terbaik : ' ,pop[0], ' Fitness : ' ,sortFitness[0], ' Nilai Minimum : ', ((1/sortFitness[0]) - 243)
		gen += 1


ga(2, 3, 50, 2000)