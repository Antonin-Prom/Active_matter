from tkinter import *

class Segment :
    def __init__(self,canvas,x,y,length,color):
        self.length=length
        self.x = x
        self.y = y 
        self.canvas = canvas
        self.image = canvas.create_rectangle(x,y,x+length,y,fill=color)      
        
class Ball :
    
    def __init__(self,canvas,x,y,diameter,v_x,color):
        self.x = y
        self.y = y
        self.canvas = canvas
        #    id = C.create_oval(x0, y0, x1, y1, option, ...)
        #    id = C.create_oval(0, 1, 10, 10, option, ...)
        self.image = canvas.create_oval(x,y,x+diameter,diameter+y,fill=color)
        self.v_x = v_x
      
        

    def move(self, v_x, v_y):
        self.canvas.move(self.circle, v_x, v_y)
        self.x += v_x
        self.y += v_y
        
           
      