from tkinter import *

class Segment :
    def __init__(self,canvas,x,y,length,color):
        self.length=length
        self.x = x
        self.y = y 
        self.canvas = canvas
        self.image = canvas.create_rectangle(x,y,x+length,y+15,fill=color)      
        
class Ball :
    
    def __init__(self,canvas,x,y,diameter,v_x,v_y,color):
        self.x = y
        self.y = y
        self.canvas = canvas
        #    id = C.create_oval(x0, y0, x1, y1, option, ...)
        #    id = C.create_oval(0, 1, 10, 10, option, ...)
        self.image = canvas.create_oval(x,y,x+diameter,diameter+y,fill=color)
        self.v_x = v_x
        self.v_y = v_y
        
    def move(self):
        coordinates = self.canvas.coords(self.image)
        #if(coordinates[2] >= (self.canvas.winfo_width()) or coordinates [0]<0):
        #   self.v_x = - self.v_x
        #if(coordinates[3] >= (self.canvas.winfo_height()) or coordinates [1]<0):
        #    self.v_y = - self.v_y
            
        self.canvas.move(self.image,self.v_x,self.v_y)
           
      