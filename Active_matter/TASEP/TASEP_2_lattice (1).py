import random as rnd 
import numpy as np
import matplotlib.pyplot as plt
# Generation de la lattice
N = 400
l=[0,1]

lattice1 = [0]*N
lattice2 = [0]*N
for i in range (N) :
    lattice1[i] = rnd.choice(l)
    lattice2[i] = rnd.choice(l)
    

# Paramètre du système
p1 = 1
alpha1 = 0.5
beta1 = 0.5
wa1 = 0.9/(N-2)
wb1 = 0.3/(N-2)
s1 = 0

#Lattice 2 
p2 = 1
alpha2 = 0.0
beta2 = 0.6
wa2 = 0.3/(N-2)
wb2 = 0.1/(N-2)
s2 = 0

nb_ite = 5000

count1 = [0]*N
count2 = [0]*N
count_move = [0]*N
moved = [False]*N
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
        count_move[n] = count_move[n] + 1
        
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
    if lattice_1[n] == 1 and lattice_2[n] == 0 and gene_rnd(s) == True :
        lattice_1[n] = 0
        lattice_2[n] = 1

        
def loop_lattice():
    for i in range(nb_ite) :
        
        # Checking not already moved
        moved = [False]*N
        entrance(alpha1)
        entrance(alpha2)
        ex(beta1)
        ex(beta2)
        for n in range(N) :
            walk(p1,n)
            #walk(p2,n)
            absorption(wa1,n)
            #absorption(wa2,n)
            desorption(wb1,n)
            #desorption(wb2,n)
            counting(n,lattice1,count1)
            #counting(n,lattice2,count2)
            #transition(n,lattice1,lattice2,s1)
            #transition(n,lattice2,lattice1,s2)
    
def density_f_N(count):       
    density = [0]*N
    for i in range(N-1):
        density[i] = count[i]/10
    
    return density
    
k = 5
d = []
c = []
alpha1 = 0
alpha2 = 0
for i in range(k): 
    loop_lattice()
    alpha1 = alpha1 + 0.1
    beta1 = beta1 + 0.1
    d.append(np.mean(density_f_N(count1)))
    c.append(np.mean(density_f_N(count_move)))

fig = plt.figure()
fig.set_figwidth(k)
fig.set_figheight(1.1)
plt.xlim(0,k)
plt.plot(d,c)
plt.show()