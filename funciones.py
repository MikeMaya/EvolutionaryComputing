import math

def Rastrigin (x1, x2): 
	res = 0
	res = 20; 
	res+ = x1*x1 - 10* math.cos(2 * math.pi * x1)
	res+ = x2*x2 - 10* math.cos(2 * math.pi * x2)
	return res

def Ackley (x1, x2):
	res = 0
	a = 0
	b = 0
	c = 0
	res = -a*math.exp(-b*math.sqrt((1/2)*(x1*x1 + x2*x2))) 
		-1*math.exp((1/2)*( math.cos(c*x1) + math.cos(c*x2))
		+ a + math.exp(1) 
	return res