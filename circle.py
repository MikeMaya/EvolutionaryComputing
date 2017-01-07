

from Tkinter import *
import math
import random
#Chromosomes are 4 bits long
points = [[5, 3], [5,7], [7,5]]

Nbits_r=Nbits_h=Nbits_k=8
L_chromosome=3*Nbits_r
N_chains=2**Nbits_r

#Lower and upper limits of search space

crossover_point=L_chromosome/2


def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random()<0.5:
            chromosome.append(0)
        else:
            chromosome.append(1)

    return chromosome

#Number of chromosomes
N_chromosomes=10
#probability of mutation
prob_m=0.5

F0=[]
fitness_values=[]

for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

def decode_float(lower, upper, bits):
    global N_chains
    Lbits=len(bits)
    value=0
    for p in range(Lbits):
        value+=(2**p)*bits[-1-p]
    return lower+(upper-lower)*float(value)/(N_chains-1)

#binary codification
def decode_chromosome(chromosome):
    h=decode_float(0, 10, chromosome[:Nbits_h])
    k=decode_float(0, 10, chromosome[Nbits_h:Nbits_h+Nbits_k])
    r=decode_float(0,5,  chromosome[Nbits_h+Nbits_k:Nbits_h+Nbits_k+Nbits_r])
    return (h, k, r)

def f(x): 
    global points
    (h,k,r)=x
    error=0
    for index in range (len(points)):
        raux2= (points[index][0]-h)**2 + (points[index][1]-k)**2
        error+=abs(raux2 - r**2)
    return error

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


suma=float(N_chromosomes*(N_chromosomes+1))/2.

Lwheel=N_chromosomes*10

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
        
F1=F0[:]

def nextgeneration():
    w.delete(ALL)
    F0.sort(cmp=compare_chromosomes)
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

    graph_population(F0,'red')
    graph_population(F1,'green')
    graph_f()
    #The generation replaces the old one
    F0[:]=F1[:]



#visualization
master = Tk()

xmax=200
ymax=200

xo=0
yo=200

s=20

w = Canvas(master, width=xmax, height=ymax)
w.pack()

            
button1 = Button(master, text="Next Generation", command=nextgeneration)
button1.pack()


def graph_f():
    for index in range (len(points)):
        w.create_oval(xo+points[index][0]*s, yo-points[index][1]*s, xo+(points[index][0]+.2 )*s, yo-(points[index][1]+.2)*s, fill="black")

def graph_population(F,color):
    for chromosome in F:
        h,k,r=decode_chromosome(chromosome)
        w.create_oval( (h-r)*s, (yo-(k+r)*s), (h+r)*s , (yo-(k-r)*s) ,outline=color)

graph_f()
graph_population(F0,'red')
F0.sort(cmp=compare_chromosomes)
evaluate_chromosomes()

mainloop()
