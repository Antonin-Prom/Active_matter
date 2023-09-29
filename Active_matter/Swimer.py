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

# Nodes parameters
seg_width = 10
dist_neighbor = 150
radius_nodes = 50


def distance(node1, node2):
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    return np.sqrt(dx*dx + dy*dy)


class Swimmer:
    def __init__(self):
        # Generate upcoming nodes
        self.nA = Nodes(canvas, 500, 499 + dist_neighbor, 0, 0)
        self.nB = Nodes(canvas, 500, 500, 0, 0)
        self.nC = Nodes(canvas, 500, 499 - dist_neighbor / 2, 0, 0)
        self.rho = 1
        self.nA.add_neighbor(self.nB)
        self.nC.add_neighbor(self.nB)

        nodes_list = [self.nA, self.nB, self.nC]

        for node in nodes_list:
            node.add_not_neighbor(nodes_list)
            node.create_line()

    def angle_function(self, t):
        # Calculate angle based on time
        return (np.pi / 2) * np.cos(90 * t) + (np.arccos(2 * radius_nodes / dist_neighbor))

    def middle_node(self, node1, node2):
        Mx = (node1.x + node2.x) / 2
        My = (node1.y + node2.y) / 2
        return Mx, My

    def angular_movement(self, static_node, C2, C3, phi):
        A = 10
        M = self.middle_node(C2, C3)
        Mx, My = M
        theta = np.arctan((abs(My - static_node.y) + 0.01) / (abs(Mx - static_node.x) + 0.01))

        # Set the movement of C2 and C3 based on the desired angular movement
        x2 = np.cos(theta + phi / 2) * distance(static_node, C2) / A
        y2 = np.sin(theta + phi / 2) * distance(static_node, C2) / A
        x3 = np.cos(theta - phi / 2) * distance(static_node, C2) / A
        y3 = np.sin(theta - phi / 2) * distance(static_node, C2) / A

        # Update the velocities of C2 and C3
        wA = [x2, y2]
        wC = [x3, y3]

        # Set the velocity of the static node (B) to zero
        wB = [0, 0]

        return wA, wB, wC

    def propulsion(self, t):
        angle_avant = self.angle_function(t - dt)
        angle_apres = self.angle_function(t)
        d_angle = abs(angle_avant - angle_apres)
        aire = d_angle * dist_neighbor * dist_neighbor
        masse_expu = self.rho * aire
        v = np.cos(angle_apres) * dist_neighbor * d_angle

        if angle_apres < angle_avant:
            propulsion = masse_expu * v / 10000
            prop_x = -propulsion * np.cos(angle_apres)
            prop_y = -propulsion * np.sin(angle_apres)
            propulsion = [prop_x, prop_y]
            print("angle:", angle_apres, "aire =", aire, "propulsion =", propulsion)
            return propulsion
        else:
            return [0, 0]

    def move_swimmer(self, t):
        wA, wB, wC = self.angular_movement(self.nB, self.nA, self.nC, self.angle_function(t))
        self.nA.move(wA, [0, 0])
        self.nB.move(wB, self.propulsion(t))
        self.nC.move(wC, [0, 0])


swimmer1 = Swimmer()

# Simulation parameters
dt = 0.001
t = 0

while True:
    time.sleep(dt)
    t += dt
    swimmer1.move_swimmer(t)
    fen.update()

Tk.mainloop()
