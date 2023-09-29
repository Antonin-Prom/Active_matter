from Nodes import Nodes
import time
from tkinter import *
import numpy as np


# Canvas parameters
fen = Tk()
fen.geometry('2000x2000')
canvas = Canvas(fen, width=2000, height=2000, highlightthickness=0)
canvas.pack()
canvas.place(x=0, y=0)
canvas.configure(bg='Gray26')

class mRNA():
    def __init__(self,canvas,x,y,vx,vy):
        self.id = canvas.create_rectangle()