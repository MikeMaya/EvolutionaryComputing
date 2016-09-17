#File ejemploag.py
#Example of GA
#Dr. Jorge Luis Rosas Trigueros
#Last change: 21sep15

from Tkinter import *
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
    value=0
    for p in range(L_chromosome):
        value+=(2**p)*chromosome[-1-p]
    return a+(b-a)*float(value)/(N_chains-1)

def f(x):
    return 0.05*x*x-4*math.cos(x)

def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        v=decode_chromosome(F0[p])
        fitness_values[p]=f(v)
        

def compare_chromosomes(chromosome1,chromosome2):
    vc1=decode_chromosome(chromosome1)
    vc2=decode_chromosome(chromosome2)
    fvc1=f(vc1)
    fvc2=f(vc2)
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
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
    w.delete(ALL)
    F0.sort(cmp=compare_chromosomes)
    n_generation+=1
    print "Generation: ",n_generation
    print "Best solution so far:"
    print "f(",decode_chromosome(F0[0]),")= ", f(decode_chromosome(F0[0]))
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

    graph_f()
    graph_population(F0,w,s,s,xo,yo,'red')
    graph_population(F1,w,s,s*0.5,xo,yo,'green')
    #The generation replaces the old one
    F0[:]=F1[:]

#visualization
master = Tk()

xmax=400
ymax=400

xo=200
yo=200

s=10

w = Canvas(master, width=xmax, height=ymax)
w.pack()

            
button1 = Button(master, text="Next Generation", command=nextgeneration)
button1.pack()

N=100


def graph_f():
    xini=-20.
    xfin=20.

    dx=(xfin-xini)/N

    xold=xini
    yold=f(xold)
    for i in range(1,N):
        xnew=xini+i*dx
        ynew=f(xnew)
        w.create_line(xo+xold*s,yo-yold*s,xo+xnew*s,yo-ynew*s)
        xold=xnew
        yold=ynew

def graph_population(F,mycanvas,escalax,escalay,xcentro,ycentro,color):
    for chromosome in F:
        x=decode_chromosome(chromosome)
        mycanvas.create_line(xcentro+x*escalax,ycentro-10*escalay,xcentro+x*escalax, ycentro+10*escalay,fill=color)

#Chromosomes are 4 bits long  
L_chromosome=2
#Lower and upper limits of search space
a=-20
b=20
for j in range (0, 6):
    L_chromosome*=2;
    prob_m=-0.1
    for k in range (0,5):
        prob_m+=0.2
        N_chains=2**L_chromosome
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
