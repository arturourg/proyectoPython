import random,math

def hola(t):
	if i[-1] in "aeiou":
		return i.upper()  
	else:
		return i[::-1]

def funcion(r):
	return r %2 ==0

def arreglo_aleatorio(n):
	'''
	a = []
	for i in range(n):
		a.append(random.randint(20,60))
	'''
	#devuelve los numeros pares del arrreglo ar
	ar = [2,4,6,7,9,120,43]
	
	ar1 = [i for i in ar if i%2==0]
	ar1_filter = list(filter(lambda x: x%2==0, ar))

	print(f"arreglo principal: {ar}")
	print(f"pares comprension: {ar1}")
	print(f"pares filter: {ar1_filter}")
	
	#transforma todos las cadenas 
	#del arreglo a mayuscula
	ar_v = ["hola","soy","un","arreglito"]
	ar_v1 = [i.upper() if i[-1] in "aeiou" else i[::-1] for i in ar_v]
	#ar_v1_map = list(map(lambda t:t.upper() if t[-1] in "aeiou" else t[::-1],))
	
	tabla_siete = [i*7 for i in range(1,12)]
	#a = [random.randint(20,60) for i in range(n)]
	a_map = list(map(lambda i:random.randint(20,60),range(n)))
	tabla_siete = [i*7 for i in range(1,12)]
	tabla_siete_map = list(map(lambda x:x*7,range(1,12)))
	return ar
	
def maximo(arreglo):
	return max(arreglo)

def minimo(arreglo):
	return min(arreglo)

def promedio(arreglo):
	return sum(arreglo)/len(arreglo)

def moda(arreglo):
	d = {}
	m = [-1,-1]
	for i in arreglo:
		if i in d:
			d[i]+=1
		else:
			d[i] = 1
		if m[1]<d[i]:
			m[1] = d[i]
			m[0] = i
	print(m) 

def desv_estd(arreglo):
	avg = promedio(arreglo)
	s = 0
	for i in arreglo:
		s+=(i-avg)**2
	return math.sqrt(s/len(arreglo))

n = int(input("Ingrese N: "))
arr = arreglo_aleatorio(n)