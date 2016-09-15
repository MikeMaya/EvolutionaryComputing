#Matrix global de la DP
matrix = []

def coinChange (cambio, monedas): 
	global matrix
	M=len(monedas)
	matrix=[[0 for j in range(cambio+1)] for i in range(M+1)]
	for i in xrange(1, cambio+1):
		matrix[1][i]=i
	for i in xrange(2, M+1):
		for j in xrange(0, cambio+1):
			if monedas[i-1] > j:
				matrix[i][j] = matrix[i-1][j]
			else: 
				matrix[i][j] = min(matrix[i-1][j] , matrix[i][j-monedas[i-1]] +1)
	return matrix[M][cambio]

def reconstruir (cambio, monedas):
	M=len(monedas)
	respuesta = []
	print "Monedas utilizadas :"
	while cambio > 0:
		if matrix[M][cambio] != matrix[M-1][cambio] :
			respuesta.append(monedas[M-1])
			cambio = cambio - monedas[M-1]
		else : 
			M= M-1
	for i in respuesta:
		print i

def lectura():
	cambio=0
	cantidad=0
	monedas=[]
	cambio = input("Ingrese el monto a cambiar: ")
	cantidad= input("Ingrese el numero de denominaciones :")
	print "Ingrese cada denominacion"
	for i in range(0, cantidad):
		monedas.append(input())
	maximo = coinChange(cambio, monedas)
	print "El minimo numero de monedas requeridas es: ", maximo
	reconstruir(cambio, monedas)

lectura()
