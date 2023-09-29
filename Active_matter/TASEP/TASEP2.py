import random
import time
from tkinter import Tk, Canvas

class Segment:
    def __init__(self, canvas, x, y, length, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.length = length
        self.color = color
        self.rectangle = canvas.create_rectangle(x, y, x + length, y + 10, fill=color)


class Ball:
    def __init__(self, canvas, x, y, size, v_x, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.v_x = v_x
        self.color = color
        self.circle = canvas.create_oval(x, y, x + size, y + size, fill=color)

    def move(self, v_x, v_y):
        self.canvas.move(self.circle, v_x, v_y)
        self.x += v_x
        self.y += v_y


# Create window and canvas
window = Tk()
HEIGHT = 1000
WIDTH = 1500
canvas = Canvas(window, height=HEIGHT, width=WIDTH)
canvas.pack()


# Define the event handler function
def on_closing():
    window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

    
# Initialize variables
y_cell = 500
color_cell = "royal blue"
nbr_cell = 8
length = 50
gap = 20
cell = [0] * nbr_cell
balls_list = []
diameter = 50
alpha = 0.7
beta = 0.5
p = 0.5
dt = 1

def build_cell_segment(nbr_cell, length, gap):
    for i in range(nbr_cell):
        pos_x = i * (length + gap)
        Segment(canvas, pos_x, y_cell, length, color_cell)

def entrance(alpha, cell):
    result_a = random.uniform(0, 1)
    if result_a <= alpha and cell[0] == 0:
        cell[0] = 1
        balls_list.append(Ball(canvas, 0, y_cell - diameter, diameter, 0, "red"))

def sortie():

     if cell[nbr_cell-1] == 1:
        cell[nbr_cell-1] = 0
        for ball in reversed(balls_list):
            if ball.x >= ((nbr_cell-1) * (length + gap)):
                print("balls_list",balls_list)
                balls_list.pop()
                canvas.delete(ball.circle)
                print("sortie")
                print("balls_list",balls_list)
            

            
            
                
moved = [0] * nbr_cell
def move_array(p, cell):
    for i in range( nbr_cell):
        result_p = random.uniform(0, 1)
        if moved[i] == 0:
            if i == 0 and cell[0]==1 and cell[1]==0 and result_p < p :
                cell[0] = 0
                cell[1] = 1
                i = +1
            if cell[i] == 0 and cell[i - 1] == 1 and result_p < p and i < nbr_cell  :
            
                cell[i] = 1
                cell[i - 1] = 0
                
                # Find the ball that is being moved
                for j, ball in enumerate(balls_list):
                    if ball.x >= i * (length + gap) - length and ball.x < i * (length + gap):
                        # Update the ball's position
                        ball.x += length + gap
                        ball.v_x = (length+gap+5)/dt
                        ball.move(ball.v_x, 0)

                
                if i < nbr_cell-1 :
                    moved[i+1] = 1


def turn_binaries_in_coord(old_cell, new_cell, length):
    differences = []
    for i in range(len(old_cell)):
        if old_cell[i] == 0 and new_cell[i] == 1:
            differences.append(i * (length+gap))
    return differences


def move_balls(differences):
    for j in range(len(differences)):
        for i, ball in enumerate(balls_list):
            if ball.x >= (differences[j]- length+gap) and ball.x < differences[j] + length  :
                ball.v_x = (length+gap)/dt
                ball.move(ball.v_x, 0)
                
            

            
def update_ball_count():
    # Calculate the x and y coordinates for the text
    x = WIDTH - 300
    y = 50
    # Delete the previous text element
    if hasattr(update_ball_count, "text"):
        canvas.delete(update_ball_count.text)
    # Create the text on the canvas
    update_ball_count.text = canvas.create_text(x, y, text=f"Number of balls: {len(balls_list)}", font=("Arial", 20), fill="black") 

def update_new_cell_array():
    # Calculate the x and y coordinates for the text
    x = WIDTH - 500
    y = 200
    # Delete the previous text element
    if hasattr(update_new_cell_array, "text"):
        canvas.delete(update_new_cell_array.text)
    # Create the text on the canvas
    update_new_cell_array.text = canvas.create_text(x, y, text=f"Array: {cell}", font=("Arial", 20), fill="black") 


while True:
    old_cell = cell.copy()
    
    moved = [0] * nbr_cell 
    
    build_cell_segment(nbr_cell, length, gap)
    entrance(alpha, cell)
    move_array(p,cell)
    cell_differences = turn_binaries_in_coord(old_cell, cell, length)
    move_balls(cell_differences)
 
    
    result_b = random.uniform(0, 1)
    if result_b <= beta:
         sortie()
         
    update_ball_count()
    update_new_cell_array()   

     
    window.update()
    time.sleep(dt)

