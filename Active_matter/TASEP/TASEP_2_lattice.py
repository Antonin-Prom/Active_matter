import random as rnd 
import numpy as np
import matplotlib.pyplot as plt
# Generation de la lattice
N = 400
lattice1 = [0]*N
lattice2 = [0]*N



# Paramètre du système
p1 = 1
alpha1 = 0.2
beta1 = 0.6
wa1 = 3/(N-2)
wb1 = 1/(N-2)
s1 = 1/(N-2)

#Lattice 2 
p2 = 1
alpha2 = 0.2
beta2 = 0.6
wa2 = 3/(N-2)
wb2 = 1/(N-2)
s2 = 1/(N-2)

nb_ite = 5000

count1 = [0]*N
count2 = [0]*N

count_transi_1_2 = [0]*N

# Fonctions du système
def gene_rnd(x):
    if  rnd.uniform(0,1) <= x : 
        return True 
    
def entrance(alpha1):
    if gene_rnd(alpha1) == True and lattice1[0] == 0 :
        lattice1[0] = 1

def ex(beta1):
    if gene_rnd(beta1) == True and lattice1[N-1] == 1 :
        lattice1[N-1] = 0
        
def walk(p,n):
    if gene_rnd(p) == True and lattice1[n-1] == 1 and lattice1[n]==0 and moved[n-1] == False:
        lattice1[n] = 1
        lattice1[n-1] = 0
        moved[n] = True
        
def absorption(wa1,n):
    if gene_rnd(wa1) == True and  lattice1[n] == 0:
         lattice1[n] = 1

def desorption(wb1,n):
    if gene_rnd(wb1) == True and  lattice1[n] == 1:
         lattice1[n] = 0    
         
def counting(n,lattice,count) :
    if lattice[n] == 1 :
        count[n] = count[n]+1

def transition(n,lattice_1,lattice_2,s):
    if lattice_1[n] == 1 and lattice_2[n] == 0 and gene_rnd(s1) == True :
        lattice_1[n] = 0
        lattice_2[n] = 1

        

for i in range(nb_ite) :
    
    # Checking not already moved
    moved = [False]*N
    entrance(alpha1)
    entrance(alpha2)
    ex(beta1)
    ex(beta2)
    for n in range(N) :
        walk(p1,n)
        walk(p2,n)
        absorption(wa1,n)
        absorption(wa2,n)
        desorption(wb1,n)
        desorption(wb2,n)
        counting(n,lattice1,count1)
        counting(n,lattice2,count2)
        transition(n,lattice1,lattice2,s1)
        transition(n,lattice2,lattice1,s2)
    
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
plt.plot(2,1,2)
density_f_N(count1)
plt.show()