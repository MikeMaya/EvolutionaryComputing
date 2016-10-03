#File 3JugsGA.py
#Algoritmo para resolver el problema de las 3 jarras
#Miguel Angel Maya Hernandez
#Last change: 23 de Septiembre 2016

#Este algoritmo considera a todo el cromosoma como la mejor solucion posible
#, considerando el que tenga menor numero de operaciones no vacias


# -- Tabla de movimientos validos -- 
# 0  Llenar Jarra 8L
# 1  Llenar Jarra 5L
# 2  Llenar Jarra 3L
# 3  Tirar Jarra 8L
# 4  Tirar Jarra 5L
# 5  Tirar Jarra 3L
# 6  Mover 8L a 5L
# 7  Mover 8L a 3L
# 8  Mover 5L a 8L
# 9  Mover 5L a 3L 
# 10 Mover 3L a 8L
# 11 Mover 3L a 5L
# 12 Hacer nada.

import math 
import random

#Genera un cromosoma random con movimientos de la tabla
def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        chromosome.append(random.randint(0,12))
    return chromosome

#Regresa el valor de las tres jarras al final de los movimientos
#Regresa el valor de las tres jarras en su mejor momento 
def decode_chromosome(chromosome):
    global L_chromosome
    j8=0
    j5=0
    j3=0
    j1=0
    j2=0
    for p in range(0,L_chromosome):
        if chromosome[p] == 0:
            j8=8
        elif chromosome[p] == 1:
            j5=5
        elif chromosome[p] == 2:
            j3=3
        elif chromosome[p] == 3:
            j8=0
        elif chromosome[p] == 4:
            j5=0
        elif chromosome[p] == 5:
            j3=0
        elif chromosome[p] == 6:
            j1=j8 #a mover
            j2=5-j5 #disponible
            if j1 <= j2 : 
                j5+=j1
                j8-=j1
            else :
                j5+=j2
                j8-=j2
        elif chromosome[p] == 7:
            j1=j8 #a mover
            j2=3-j3 #disponible
            if j1 <= j2 : 
                j3+=j1
                j8-=j1
            else :
                j3+=j2
                j8-=j2
        elif chromosome[p] == 8:
            j1=j5 #a mover
            j2=8-j8 #disponible
            if j1 <= j2 : 
                j8+=j1
                j5-=j1
            else :
                j8+=j2
                j5-=j2
        elif chromosome[p] == 9:
            j1=j5 #a mover
            j2=3-j3 #disponible
            if j1 <= j2 : 
                j3+=j1
                j5-=j1
            else :
                j3+=j2
                j5-=j2
        elif chromosome[p] == 10:
            j1=j3 #a mover
            j2=8-j8 #disponible
            if j1 <= j2 : 
                j8+=j1
                j3-=j1
            else :
                j8+=j2
                j3-=j2
        elif chromosome[p] == 11:
            j1=j3 #a mover
            j2=5-j5 #disponible
            if j1 <= j2 : 
                j5+=j1
                j3-=j1
            else :
                j5+=j2
                j3-=j2
    return (j8, j5, j3)

def f (j8, j5, j3): 
    res=0
    res = min(math.fabs(buscado - j8), math.fabs(buscado - j5))
    return res

def evaluate_chromosomes():
    global F0
    for p in range(N_chromosomes):
        (j8, j5, j3)=decode_chromosome(F0[p])
        fitness_values[p]=f(j8, j5, j3)

def cont_nulos(chromosome):
    contador=0
    for p in range(L_chromosome):
        if chromosome[p]==12:
            contador+=1
    return contador

def compare_chromosomes(chromosome1,chromosome2):
    (j8, j5, j3)=decode_chromosome(chromosome1)
    fvc1=f(j8, j5, j3)
    (j8, j5, j3)=decode_chromosome(chromosome2)
    fvc2=f(j8, j5, j3)
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
        n1= cont_nulos(chromosome1)
        n2= cont_nulos(chromosome2)
        if n2 > n1 :
            return 1
        elif n2 == n1:
            return 0
        else :
            return -1
        return 0
    else: #fvg1<fvg2
        return -1

def create_wheel():
    global F0,fitness_values

    maxv=max(fitness_values)
    acc=0
    for p in range(N_chromosomes):
        acc+=maxv-fitness_values[p]
    fraction=[]
    for p in range(N_chromosomes):
        fraction.append( float(maxv-fitness_values[p])/acc)
        if fraction[-1]<=1.0/Lwheel:
            fraction[-1]=1.0/Lwheel
##    print fraction
    fraction[0]-=(sum(fraction)-1.0)/2
    fraction[1]-=(sum(fraction)-1.0)/2
##    print fraction

    wheel=[]

    pc=0

    for f in fraction:
        Np=int(f*Lwheel)
        for i in range(Np):
            wheel.append(pc)
        pc+=1

    return wheel

def nextgeneration():
    global n_generation    
    F0.sort(cmp=compare_chromosomes)
    n_generation+=1
    print "Generation: ",n_generation
    print "Best solution so far:"
    (j8, j5, j3)=decode_chromosome(F0[0])
    print "f(",j8, j5, j3,") = ", f(j8, j5, j3)," \n Chromosome- ",F0[0]
    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    for i in range(0,(N_chromosomes-2)/2):
        roulette=create_wheel()
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)
        #Two descendants are generated
        o1=F0[p1][0:crossover_point]
        o1.extend(F0[p2][crossover_point:L_chromosome])
        o2=F0[p2][0:crossover_point]
        o2.extend(F0[p1][crossover_point:L_chromosome])
        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o1[int(round(random.random()*(L_chromosome-1)))]=random.randint(0,12);
        if random.random() < prob_m:
            o2[int(round(random.random()*(L_chromosome-1)))]=random.randint(0,12)
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2
    #The generation replaces the old one
    F0[:]=F1[:]
    #print F0


print "3 Jugs with GA \n"
buscado=4
L_chromosome = 50
prob_m=0.5
crossover_point=L_chromosome/2
N_chromosomes=10
F0=[]
F1=[]
fitness_values=[]
for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)
Lwheel=N_chromosomes*10
F1=F0[:]
F0.sort(cmp=compare_chromosomes)
evaluate_chromosomes()
n_generation=0
print "\n" 
for i in range(0,500):
    nextgeneration()
    print 

