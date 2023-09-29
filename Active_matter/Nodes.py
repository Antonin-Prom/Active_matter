import time 
from tkinter import *
import numpy as np
"""
fen = Tk()
fen.geometry('2000x2000')
canvas = Canvas(fen,width=2000,height=2000,highlightthickness=0)
canvas.pack()
canvas.place(x=0,y=0)
canvas.configure(bg='Gray26')
"""
#Paramètres :
seg_width = 10
dist_neighbor = 150
radius_nodes = 50
t = 0

class Nodes :
    def __init__(self,canvas,x,y,vx,vy):
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x+radius_nodes, y+radius_nodes, fill= "Turquoise3", outline = "Gray26")
        self.x = x
        self.y = y 
        self.vx = vx
        self.vy = vy
        self.m = 1
        self.b = 0.1
        self.ax = 0
        self.ay = 0
        self.neighbors = []
        self.dist_neighbor_box = []
        self.not_neighbor = []
        self.line_box = []

    #Each node has a list of its neighbors. if Bool is False the node is not a neighbor 
    #but we still prevent this one from coliding
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor) 

    def add_not_neighbor(self,nodes_list):
        for node in nodes_list :
            if node not in self.neighbors and node != self :
                self.not_neighbor.append(node)

    
    def distance(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        return np.sqrt(dx*dx + dy*dy)
    
    def angle(self,neighbor):
        dx = neighbor.x - self.x
        dy = neighbor.y - self.y
        dist = np.sqrt(dx*dx + dy*dy) 
        phi = np.arccos(dx/dist)
        return(phi)       

    def compute_line(self,neighbor):       
        phi = self.angle(neighbor)
        self.coin1_x = self.x + radius_nodes/2
        self.coin1_y = self.y + radius_nodes/2
        self.coin2_x = neighbor.x + radius_nodes/2
        self.coin2_y = neighbor.y + radius_nodes/2
        self.seg_coord = [self.coin1_x, self.coin1_y, self.coin2_x, self.coin2_y]
        return self.seg_coord 
        
        
    def create_line(self):
        for neighbor in self.neighbors :
            seg_coord = self.compute_line(neighbor)
            self.rect = self.canvas.create_line(seg_coord[0],seg_coord[1],seg_coord[2],seg_coord[3],fill = "LightSkyBlue3", width = 10)
            self.line_box.append([self.rect,neighbor])

    def update_line(self):
        for seg in self.line_box:
            seg_coord = self.compute_line(seg[1])
            self.canvas.coords(seg[0],seg_coord[0],seg_coord[1],seg_coord[2],seg_coord[3])
            self.canvas.tag_lower(seg[0])

    def tension(self):
        Tx = 0
        Ty = 0
        for neighbor in self.neighbors:
            dist = self.distance(neighbor)
            dx = neighbor.x - self.x
            dy = neighbor.y - self.y
            phi = np.arccos(dx/dist)
            if dist == 0:
                dist = 1
            if self.y > neighbor.y:  
                Tx += (dist - dist_neighbor)*np.cos(phi)
                Ty += - (dist - dist_neighbor)*np.sin(phi)
            elif self.y < neighbor.y:
                Tx += (dist - dist_neighbor)*np.cos(phi)
                Ty += (dist - dist_neighbor)*np.sin(phi)                               
        return (Tx, Ty)

    def collide(self):
        cx = 0
        cy = 0
        for node in self.not_neighbor :  
            if self.distance(node) < radius_nodes :
                L = self.distance(node)
                dx = abs(node.x - self.x)
                phi = np.arccos(dx/L)
                if self.y < node.y:  
                    cy += -(radius_nodes - L)*np.sin(phi)/2 
                elif self.y > node.y :
                    cy += (radius_nodes - L)*np.sin(phi)/2 
                if self.x < node.x :
                    cx += -(radius_nodes - L)*np.cos(phi) /2
                elif self.x > node.x :
                    cx += (radius_nodes - L)*np.cos(phi)/2
            else :
                cx = 0
                cy = 0                         
        return (2*cx,2*cy)    
      
    def resize_seg(self):
        self.canvas.itemconfig(self.rect)
        
    
    def move(self,add_force,propulsion):             
        # Maintain distance between nodes
        T = self.tension()
        
        tx = T[0]
        ty = T[1]
        Fx = self.vx + tx
        Fy = self.vy + ty   
        
        # Avoid collision
        cx = self.collide()[0]
        cy = self.collide()[1]
        
        # Calculate acceleration with damping term
        self.ax = Fx/self.m - self.b*self.vx/self.m + cx + add_force[0] + propulsion[0]
        self.ay = Fy/self.m - self.b*self.vy/self.m + cy + add_force[1] + propulsion[1]
        # Update velocity and position

        self.x += self.ax
        self.y += self.ay   
            
        self.canvas.coords(self.id, self.x, self.y, self.x+radius_nodes, self.y+radius_nodes)
        self.update_line()
        


#defining v(t)
def mvt_angle(t):
    return t
def XY(t):
    return (np.pi/8)*np.cos(mvt_angle(t)),(np.pi/8)*np.sin(mvt_angle(t))
""""
A = 1     
n1 = Nodes(canvas,500-np.sqrt(dist_neighbor*dist_neighbor+dist_neighbor*dist_neighbor/4),500+dist_neighbor/2,-9,0.2,'Turquoise3')
n2 = Nodes(canvas,500,500,0,0,'Turquoise3')
n3 = Nodes(canvas,500-np.sqrt(dist_neighbor*dist_neighbor+dist_neighbor*dist_neighbor/4),500-dist_neighbor/2,0.1,0.2,'Turquoise3')
n1.add_neighbor(n2)
n2.add_neighbor(n1)
n3.add_neighbor(n2)
n2.add_neighbor(n3)

nodes_list = [n1,n2,n3] 

for node in nodes_list :
    node.add_not_neighbor(nodes_list)
    node.create_line()


dt = 0.01    
while True: 
    time.sleep(dt)
    t += dt
    n1.move()
    n2.move()
    n3.move()
    fen.update()      
Tk.mainloop()   """