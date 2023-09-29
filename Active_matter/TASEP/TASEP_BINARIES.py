import random as rnd 
import numpy as np
import matplotlib.pyplot as plt
# Generation de la latice 
N = 800
latice = [0]*N



# Paramètre du système
p = 1
alpha = 0.2
beta = 0.6
wa = 3/(N-2)
wb = 1/(N-2)
nb_ite = 5000

count = [0]*N


# Fonctions du système
def gene_rnd(x):
    if  rnd.uniform(0,1) <= x : 
        return True 
    
def entrance(alpha):
    if gene_rnd(alpha) == True and latice[0] == 0 :
        latice[0] = 1

def ex(beta):
    if gene_rnd(beta) == True and latice[N-1] == 1 :
        latice[N-1] = 0
        
def walk(p,n):
    if gene_rnd(p) == True and latice[n-1] == 1 and latice[n]==0 and moved[n-1] == False:
        latice[n] = 1
        latice[n-1] = 0
        moved[n] = True
        
def absorption(wa,n):
    if gene_rnd(wa) == True and  latice[n] == 0:
         latice[n] = 1

def desorption(wb,n):
    if gene_rnd(wb) == True and  latice[n] == 1:
         latice[n] = 0    
         
def counting(n) :
    if latice[n] == 1 :
        count[n] = count[n]+1

for i in range(nb_ite) :
    
    # Checking not already moved
    moved = [False]*N
    entrance(alpha)
    ex(beta)
    for n in range(N) :
        walk(p,n)
        absorption(wa,n)
        desorption(wb,n)
        counting(n)
    
def density_f_N(count):       
    density = [0]*N
    for i in range(N):
        density[i] = count[i]/nb_ite
    plt.plot(density)

fig = plt.figure()
fig.set_figwidth(N)
fig.set_figheight(1.1)
plt.xlim(0,N)
plt.ylim(0,1)
density_f_N(count)
plt.show()