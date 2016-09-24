#File knapsackAG.py
#Algoritmo para resolver coin Change Genetic Algorithm
#Miguel Angel Maya Hernandez
#Last change: 23 de Septiembre 2016

import math
import random

def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random()<0.1:
            chromosome.append(0)
        else:
            chromosome.append(1)
    return chromosome

#binary codification
def decode_chromosome(chromosome):
    global L_chromosome,Di,tam
    amount=0
    tcant=0
    cantidad=0
    i=0
    j=0
    #print chromosome
    for p in range(0,L_chromosome):
        cantidad += 2**i * chromosome[-1-p]
        i+=1
        if i % tam == 0 and p > 0:
            amount+=Di[j]*cantidad
            tcant+=cantidad
            #print cantidad, " cant ",amount, " amo"
            cantidad = 0
            i = 0
            j += 1
    return (amount, tcant)

def f (amount): 
    global conversion
    res = 0
    if amount > conversion:
        res-= amount-conversion
    else:
        res=amount
    return res

def evaluate_chromosomes():
    global F0
    for p in range(N_chromosomes):
        #print F0[p]
        (am, cant)=decode_chromosome(F0[p])
        #print pe," ",ga
        fitness_values[p]=f(am)

def compare_chromosomes(chromosome1,chromosome2):
    (am1, cant1)=decode_chromosome(chromosome1)
    (am2, cant2)=decode_chromosome(chromosome2)
    fvc1=f(am1)
    fvc2=f(am2)
    if fvc1 > fvc2:
        return -1
    elif fvc1 == fvc2:
        if cant1 > cant2:
            return 1
        elif cant1 == cant2:
            return 0
        else: 
            return -1
    else: #fvg1<fvg2
        return 1

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
    (v1,am)=decode_chromosome(F0[0])
    print "f(",v1,") = ", f(v1)," # con ", am," monedas -",F0[0]
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
            o1[int(round(random.random()*(L_chromosome-1)))]^=1
        if random.random() < prob_m:
            o2[int(round(random.random()*(L_chromosome-1)))]^=1
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2
    #The generation replaces the old one
    F0[:]=F1[:]



print "Coin Change with GA \n"
Di = map(int, raw_input("Denominaciones de moneda (iniciar con 1)\n").split())
conversion = int(raw_input("Dinero a cambiar\n"))
tam = int(math.ceil(math.log(conversion, 2)))
print tam, " tam"
L_chromosome = len(Di)*tam
prob_m=0.7
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
for i in range(0,100):
    nextgeneration()
    print "\n"
