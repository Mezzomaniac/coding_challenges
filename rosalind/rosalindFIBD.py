import timeit
"""def fibd(n,m):
	# n=months, m=months before death, fibo[0]=newborns, fibo[1:m]=other ages, fibo[m]=total
	fibo = [[0,1]]
	for a in range(m-1):
		fibo.append([0,0])
	fibo.append([0,1])
	for t in range(n-1):
		fibo[0].append(sum(fibo[a][-1] for a in range(1,m)))
		for a in range(1,m):
			fibo[a].append(fibo[a-1][-2])
		fibo[m].append(sum(fibo[a][-1] for a in range(m)))
	return fibo[m][n]
print(fibd(88,18))"""
def fibd1(n,m):
	fibo = [0,1]
	for i in range(2,n+1):
		if i <= m:
			fibo.append(fibo[-1]+fibo[-2])
		else:
			fibo.append(sum(fibo[a] for a in range(-m,-1)))
	return fibo[n]
print(fibd1(88,18))
"""print(timeit.timeit("fibd(88,18)", number=5000, globals=globals()))
print(timeit.timeit("fibd1(88,18)", number=5000, globals=globals()))"""
