#File ackley.py
#Algoritmo para obtener minimo de la funcion de ackley
#Miguel Angel Maya Hernandez
#Last change: 14 de Septiembre 2016

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
    global L_chromosome,N_chains,a,b
    v1=0
    v2=0
    for p in range(L_chromosome):
        if(p<L_chromosome/2): 
            v2+=(2**p)*chromosome[-1-p]
        else:
            v1+=(2**(p-L_chromosome/2))*chromosome[-1-p]
    return (a+(b-a)*float(v1)/(N_chains-1) , a+(b-a)*float(v2)/(N_chains-1))

def f (x1, x2): 
    res = 0
    a1 = 20.0
    b1 = 0.2
    c1 = 2.0 * math.pi
    res = (-a1)*math.exp((-b1)*math.sqrt((0.5)*(x1**2 + x2**2))) 
    res-= math.exp((0.5)*( math.cos(c1*x1) + math.cos(c1*x2))) + a1 + math.exp(1.0) 
    return res

def evaluate_chromosomes():
    global F0
    for p in range(N_chromosomes):
        (v,v1)=decode_chromosome(F0[p])
        fitness_values[p]=f(v, v1)

def compare_chromosomes(chromosome1,chromosome2):
    (vc11,vc12)=decode_chromosome(chromosome1)
    (vc21,vc22)=decode_chromosome(chromosome2)
    fvc1=f(vc11, vc12)
    fvc2=f(vc21, vc22)
    if fvc1 > fvc2:
        return 0
    elif fvc1 == fvc2:
        return 1
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
    (v1,v2)=decode_chromosome(F0[0])
    print "f(",decode_chromosome(F0[0]),")= ", f(v1,v2)
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


a=-32.768
b= 32.768
L_chromosome=2
print "Ackley \n\n"
for j in range (0, 6):
    L_chromosome*=2;
    prob_m=-0.1
    for k in range (0,5):
        prob_m+=0.2
        N_chains=2**(L_chromosome/2)
        crossover_point=L_chromosome/2
        #Number of chromosomes
        N_chromosomes=10
        #probability of mutation
        #Nomenclatura de primera poblacion
        F0=[]
        F1=[]
        fitness_values=[]
        for i in range(0,N_chromosomes):
            F0.append(random_chromosome())
            fitness_values.append(0)
        suma=float(N_chromosomes*(N_chromosomes+1))/2.
        Lwheel=N_chromosomes*10
        F1=F0[:]
        F0.sort(cmp=compare_chromosomes)
        evaluate_chromosomes()
        n_generation=0
        print "Chromosomes "
        print L_chromosome
        print " mutation "
        print prob_m
        print "\n\n" 
        for i in range(0,100):
            nextgeneration()
        print "\n\n"
