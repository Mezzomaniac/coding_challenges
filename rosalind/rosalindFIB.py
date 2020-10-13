def fib(n,k):
	fibo = [1,1]
	for i in range(n-2):
		fibo.append(fibo[-1]+fibo[-2]*k)
	return fibo[n-1]
print(fib(5,3))
