import numpy as np
from matplotlib import pyplot as plt
import random 
from tkinter import *
import time 
from Class_for_TASEP import *

window = Tk()
HEIGHT = 1000
WIDTH = 1500

canvas = Canvas(window, height = HEIGHT, width = WIDTH )
# c'est quoi la méthode pack ?
canvas.pack()

#créer 2 boites 
#Particules dans boite = 1 vide = 0
N = 10
prob_a = 0.5
prob_b = 0.5
iteration = 100
cases = np.zeros((N,),int)
first = cases[0] 
last = cases[N-1]

# Coefficients d'absorption et desorption
wa = 0.22
wd = 0.23

#Liste des segments
segment_list = []
xstart = 10
ystart = 800
length = 1000/N
color_rect = "royal blue"

#Liste des balles
balls_list = []
diameter = length
color_ball = "light salmon"
v_x = 0
v_y = 0

#tuple (case,coordonnée x)
tple_cases = []
while True :
    for ite in range (iteration) :
        
        result_a= random.uniform(0,1)
        result_b= random.uniform(0,1)

        if result_a <= prob_a :
            cases[0]= 1
            balls_list.append((Ball(canvas, xstart ,ystart - diameter - 20,diameter,color_ball,v_x,v_y),Ball.x))

        for i in range(N):
            pos_x = xstart +i*length +i*length/5
            
            tple_cases.append(cases[i],pos_x)
            # On génère des segments en range de N
            # (canvas,xstart +i*length +i*10  == espacement entre les segments)
            segment_list.append(Segment(canvas,pos_x,ystart, length, color_rect))  
            
            ball_tuple = balls_list.index((Ball(canvas, xstart ,ystart - diameter - 20,diameter,color_ball,v_x,v_y),Ball.x))
            #génération des proba de désorbtion et absorption
            p_abs= random.uniform(0,1)
            p_dsb= random.uniform(0,1)
            
            # On applique la désorbtion puis l'absorption mais comme c'est dans la boucle 
            # elles s'appliquent l'une après l'autre et non en meme temps sur toute l'array
            if cases[i] == 1 and p_dsb <= wd:
                cases[i] = 0
                if pos_x == ball_tuple[1]:
                     balls_list.remove(((Ball(canvas, xstart ,ystart - diameter - 20,diameter,color_ball,v_x,v_y),Ball.x)))
            # et donc la meme case peut désorber et absorber sur la meme iteration 
            
            if cases[i] == 0 and p_abs <= wa:
                cases[i] = 1
                balls_list.append((Ball(canvas, pos_x ,ystart - diameter - 20,diameter,color_ball,v_x,v_y),Ball.x))

            if cases[N-1] == 1 :
                if result_b <= prob_b :
                    cases[N-1] = 0
                    
            #progression
            if cases[i] == 0 and cases[i-1] == 1 :
                cases[i] = 1
                # Choper le bon indice dans la liste à la case i-1 correspond 
                # la boule d'une abscisse  "xstart +i*length +i*length/5":
              
               
    window.update()
    #la seule methode qu'on importe de time, sleep (intervalle )
    time.sleep(0.01)


