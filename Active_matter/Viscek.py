import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cProfile 

def main():
    SIDE = 1000
    X_MIN, X_MAX = 0, SIDE
    Y_MIN, Y_MAX = 0, SIDE
    N_line, N_column = 3, 3
    x_side = (X_MAX - X_MIN) / N_column
    y_side = (Y_MAX - Y_MIN) / N_line

    class Area:
        def __init__(self,x,y,ID,N_Line,N_Column) :
            self.ID = ID
            self.N_Line = N_Line
            self.N_Column = N_Column
            self.x = x
            self.y = y
            self.x_side = x_side
            self.y_side = y_side
            self.insider = []

        def learn_agent(self):
            for agent in agents_list :
                #Learn the agents of neighbor cells too
                if (self.x < agent.x < self.x + self.x_side 
                    and self.y < agent.y < self.y + self.y_side) :
                    self.insider.append(agent)
            return self.insider
        
        def total_insider(self):
            total_list = self.insider
            L,R,Dw,Up = False,False,False,False  
            if self.x > 0 :
                total_list += cell_list[self.ID - 1].insider
                L = True
            if self.x < X_MAX - self.x_side :
                total_list += cell_list[self.ID + 1].insider
                R = True
            if self.y > 0 :
                total_list += cell_list[self.ID - self.N_Column].insider
                Dw = True
            if self.y < Y_MAX - self.y_side :
                total_list += cell_list[self.ID + self.N_Column].insider
                Up = True
            if L and Dw == True :
                total_list += cell_list[self.ID - (self.N_Column + 1)].insider
            if L and Up == True :
                total_list += cell_list[self.ID + (self.N_Column - 1)].insider
            if R and Up == True : 
                total_list += cell_list[self.ID + (self.N_Column + 1)].insider
            if R and Dw == True :
                total_list += cell_list[self.ID - (self.N_Column - 1)].insider
            return total_list





    cell_list = []

    def create_grid(X_MIN,X_MAX,Y_MIN,Y_MAX):
        x_side = (X_MAX-X_MIN)/N_column
        y_side = (Y_MAX-Y_MIN)/N_line
        ID = 0
        for k in range(N_line):
            for j in range(N_column):
                ID += 1
                cell = Area(j*x_side,k*y_side,x_side,y_side,ID,N_line,N_column)
                cell_list.append(cell)

    create_grid(X_MIN,X_MAX,Y_MIN,Y_MAX,)
    count = 0
    for cell in cell_list:
        count += 1
        
    print("nombre de cell :", len(cell_list))

    class Agent:
        
        def __init__(self, ax, x, y, rot_speed, angle, color, length, blind_spot):
            self.ax = ax
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.rot_speed = rot_speed
            self.angle = angle
            self.length = length
            self.color = color
            self.blind_spot = blind_spot
            self.quiver = self.ax.quiver(self.x, self.y, self.length * np.cos(self.angle), self.length * np.sin(self.angle), color=self.color,scale = 100)
            self.patch = plt.Circle((self.x, self.y),repulsion_radius, fc='none', ec="y", lw=1)
            self.ax.add_patch(self.patch)
            self.patch1 = plt.Circle((self.x, self.y),orientation_radius, fc='none', ec="g", lw=1)
            self.ax.add_patch(self.patch1)

        def distance(self, target):
            dx = target.x - self.x
            dy = target.y - self.y
            return np.sqrt(dx*dx + dy*dy)
        
        def area_check(self):
            for cell in cell_list:
                if cell.x < self.x < cell.x + cell.x_side and cell.y < self.y < cell.y + cell.y_side :
                    return cell_list.index(cell)
                
        def compute_theta(self,agent,angle):
            A = np.array([self.x,self.y])
            B = A + np.array([self.length*np.cos(angle) , self.length*np.sin(angle)])
            C = np.array([agent.x, agent.y])
            AB = B - A
            AC = C - A
            scalar = np.dot(AB,AC)
            theta = np.arccos(scalar/(np.linalg.norm(AB)*np.linalg.norm(AC)))
            return theta
        
        def average_angle(self,area_index):
            sum_angles = 0
            count = 0
            cell = cell_list[area_index]
            near_agent = cell.total_insider()
            for agent in near_agent:
                if self.distance(agent) <= orientation_radius:
                    if agent != self :
                        angle = agent.angle
                        if self.distance(agent) < repulsion_radius:
                            return -self.angle
                    else :
                        angle = self.angle

                    theta = self.compute_theta(agent,angle) #angle between agent vector and origin of neighbor            
                    if  0 < theta <  np.pi - blind_spot or np.pi + blind_spot > theta > 2*np.pi*blind_spot :
                        sum_angles += angle
                        count += 1

            if count > 0:
                return sum_angles / count
            
            return self.angle

        def align_intrinsic(self,area_index):
            Xi= round(random.uniform(-np.pi,np.pi),2)
            self.angle = self.average_angle(area_index) + noise_intensity * Xi
            return self.angle
        
        def align_extrinsic(self,area_index):
            Xi= round(random.uniform(-np.pi, np.pi),2)
            self.angle = np.angle(np.exp(1j*self.average_angle(area_index))+noise_intensity*np.exp(1j*Xi))
            return self.angle
        
        def align_all_noises(self,area_index):
            self.angle = 0.8*self.align_extrinsic(area_index)  + 0.2*self.align_intrinsic(area_index)
            return self.angle
        
        def move(self, noise_type):

            area_index = self.area_check()

            if noise_type == 0 :
                self.angle = self.align_intrinsic(area_index)
            if noise_type == 1 :
                self.angle = self.align_extrinsic(area_index)    
            if noise_type == 2 :
                self.angle = self.align_all_noises(area_index)        
            
            self.vx = np.cos(self.angle)
            self.vy = np.sin(self.angle)
            if self.x <= X_MIN + orientation_radius or self.x >= X_MAX - orientation_radius :
                self.vx = -self.vx
            if self.y <= Y_MIN + orientation_radius or self.y >= Y_MAX - orientation_radius:
                self.vy = -self.vy
            self.x += self.vx
            self.y += self.vy
            new_positions = np.array([[self.x, self.y]])
            self.quiver.set_offsets(new_positions)
            self.patch.center = (self.x, self.y)
            self.patch1.center = (self.x, self.y)
            self.quiver.set_UVC(self.length * np.cos(self.angle), self.length * np.sin(self.angle))

    # rot_speed = d_angle/dt
    # For  a new dt the angle increase by rot_speed

    # Parameters
    noise_type = 2
    noise_intensity = 0.1
    orientation_radius = 40
    attraction_radius = 80
    repulsion_radius = 5
    vx = 0.00
    vy = 0.00
    rot_speed = 1
    blind_spot = 0.2778 # Avian binocular ref 50°
    NUM_AGENTS = 2
    spawn_zone = SIDE/5 #square of spawn on center
    length = 1

    fig, ax = plt.subplots()
    ax.set_xlim([X_MIN, X_MAX])
    ax.set_ylim([Y_MIN, Y_MAX])
    ax.set_facecolor("dimgray")


    agents_list = []
    for _ in range(NUM_AGENTS):
        agent = Agent(ax, x=random.uniform(X_MAX/2 - spawn_zone, X_MAX/2 + spawn_zone), y=random.uniform(Y_MAX/2 - spawn_zone, Y_MAX/2 + spawn_zone), rot_speed = rot_speed, angle=round(random.uniform(0, 2*np.pi),1), color='whitesmoke', length = length, blind_spot = blind_spot)
        agents_list.append(agent)
    for cell in cell_list:
        cell.learn_agent()

    def animate(frame):
        for agent in agents_list:
            agent.move(noise_type)
        return [agent.quiver for agent in agents_list]


    # Création de l'animation
    ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 2*np.pi, 0.1), interval=0.1)

    plt.show()

cProfile.run(main())