# -*- coding: cp1252 -*-
#File: pso_wikipedia.py
#Example of PSO based on the wikipedia entry
#Jorge Luis Rosas Trigueros, Ph.D.
#Last modification: 18 oct 2016

from Tkinter import *
from numpy import *
#import random

lower_limit=-20
upper_limit=20
itera=1
n_particles=10
n_dimensions=2


def f(dupla):
    x1=1*dupla[0]
    x2=1*dupla[1]
    res = 0
    res = 20; 
    res += x1*x1 - 10* math.cos(2 * math.pi * x1)
    res += x2*x2 - 10* math.cos(2 * math.pi * x2)
    return res


# Initialize the particle positions and their velocities
X = lower_limit + (upper_limit - lower_limit) * random.rand(n_particles, n_dimensions) 
assert X.shape == (n_particles, n_dimensions)
V = zeros(X.shape)

# Initialize the global and local fitness to the worst possible
fitness_gbest = inf
fitness_lbest = fitness_gbest * ones(n_particles)

X_lbest= 1*X
X_gbest= 1*X_lbest[0]

fitness_X = zeros(X.shape)

for I in range(0, n_particles):
    if f(X_lbest[I])<f(X_gbest):
        X_gbest=1*X_lbest[I]

def iteracion():
    global itera,X,X_lbest,X_gbest,V
# Loop until convergence, in this example a finite number of iterations chosen
    w.delete(ALL)
    weight=.03
    C1=0.3
    C2=0.6
 
    print "Best particle in:",X_gbest," gbest: ",f(X_gbest), " iteracion: ",itera
    itera+=1
    # Update the particle velocity and position
    for I in range(0, n_particles):
        for J in range(0, n_dimensions):
          R1 = random.rand()#uniform_random_number()
          R2 = random.rand()#uniform_random_number()
          V[I][J] = (weight*V[I][J]
                    + C1*R1*(X_lbest[I][J] - X[I][J]) 
                    + C2*R2*(X_gbest[J] - X[I][J]))
          X[I][J] = X[I][J] + V[I][J]
        if f(X[I])<f(X_lbest[I]):
            X_lbest[I]=1*X[I]
            if f(X_lbest[I])<f(X_gbest):
                X_gbest=1*X_lbest[I]
          
    #graph_f()
    #graph_population(X,V,w,s,s,xo,yo,'blue',0.2)
    #graph_population([X_gbest],V,w,s,s,xo,yo,'red',0.4)
    w.update()
    



#código para la graficación
master = Tk()

xmax=400
ymax=400

xo=200
yo=200

s=10

w = Canvas(master, width=xmax, height=ymax)
w.pack()

            
b = Button(master, text="Iniciar", command=iteracion)
b.pack()


N=100


def graph_f():
    xini=-20.
    xfin=20.

    dx=(xfin-xini)/N

    xold=xini
    yold=f(xold) #evaluate_fitness([xold])
    for i in range(1,N):
        xnew=xini+i*dx
        ynew=f(xnew) #evaluate_fitness([xnew])
        w.create_line(xo+xold*s,yo-yold*s,xo+xnew*s,yo-ynew*s)
#        w.create_line(xo+xold*s,yo-yold[0]*s,xo+xnew*s,yo-ynew[0]*s)
        xold=xnew
        yold=ynew

def graph_population(F,V,mycanvas,escalax,escalay,xcentro,ycentro,color,r):
    n_p=len(F)
    for I in range(0, n_p):
        p=F[I][0]
        y=f(p) #evaluate_fitness(p)

        mycanvas.create_oval(xcentro+(p-r)*escalax,ycentro-(y-r)*escalay,
                             xcentro+(p+r)*escalax, ycentro-(y+r)*escalay,
                             fill=color)
        mycanvas.create_line(xcentro+p*escalax,ycentro-y*escalay,
                             xcentro+(p+V[I][0]*escalax)*escalax,ycentro-y*escalay,fill=color)




#graph_f()
#graph_population(X,V,w,s,s,xo,yo,'blue',0.2)

mainloop()



