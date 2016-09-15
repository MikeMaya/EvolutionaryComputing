#Matrix global de la DP
matrix = []

def knapsack (E, W, values, weights): #elementos, peso maximo, ganancias, pesos
	global matrix
	matrix=[[0 for j in range(W+1)] for i in range(E+1)]
	for i in xrange(1, E+1):
		for j in xrange(0, W+1):
			if weights[i-1] > j:
				matrix[i][j] = matrix[i-1][j]
			else: 
				matrix[i][j] = max( matrix[i-1][j] , matrix[i-1][j - weights[i-1]] + values[i-1])
	return matrix[E][W]

def reconstruir (E, W, weights):
	respuesta = []
	print "Items utilizados :"
	for i in range(E, 0 ,-1):
		if matrix[i][W] != matrix[i-1][W] :
			respuesta.append(i)
			W= W- weights[i-1]
	for i in reversed(respuesta):
		print i

def lectura():
	elementos=peso=0
	ws=[]
	vs=[]
	elementos = input("Ingrese numero de elementos :")
	peso= input("Ingrese el peso de la bolsa :")
	print "Ingrese cada peso"
	for i in range(0, elementos):
		ws.append(input())
	print "Ingrese cada valor"
	for i in range(0, elementos):
		vs.append(input())
	maximo = knapsack(elementos, peso, vs, ws)
	print "El maximo valor obtenido es: ", maximo
	reconstruir(elementos, peso, ws)

lectura()
