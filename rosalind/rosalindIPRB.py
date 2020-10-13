from itertools import combinations as comb
def iprb(k,m,n):
	#Given 3 positive integers k, m, and n, representing a population containing k+m+n organisms, 
	#k individuals are homozygous dominant for a factor, m are heterozygous, and n are homozygous 
	#recessive. Function iprb returns the probability that two randomly selected mating organisms will
	#produce an individual possessing a dominant allele (and thus displaying the dominant phenotype),
	#assuming that any two organisms can mate.
	pop = []
	for i in range(k):
		pop.append("AA")
	for i in range(m):
		pop.append("Aa")
	for i in range(n):
		pop.append("aa")
	print(pop)
	pairs = tuple(comb(pop, 2))
	#print(pairs)
	print(len(pairs))
	doms = 0.0
	for x,y in pairs:
		if x == "AA" or y == "AA":
			doms += 1.0
		elif x == "Aa" and y == "Aa":
			doms += 0.75
		elif x == "aa" and y != "aa" or y == "aa" and x != "aa":
			doms += 0.5
		elif x == "aa" and y == "aa":
			doms += 0
		else:
			raise Exception
	print(doms)
	print(doms/len(pairs))
	return doms/len(pairs)
iprb(20,24,25)
