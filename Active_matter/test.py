import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.text import Text 
import time

def main():
    SIDE = 1500
    X_MIN, X_MAX = 0, SIDE
    Y_MIN, Y_MAX = 0, SIDE

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
        
        def compute_theta(self,agent,angle):
            A = np.array([self.x,self.y])
            B = A + np.array([self.length*np.cos(angle) , self.length*np.sin(angle)])
            C = np.array([agent.x, agent.y])
            AB = B - A
            AC = C - A
            scalar = np.dot(AB,AC)
            theta = np.arccos(scalar/(np.linalg.norm(AB)*np.linalg.norm(AC)))
            return theta
        
        def average_angle(self):
            sum_angles = 0
            count = 0
            for agent in agents_set:
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

        def align_intrinsic(self):
            Xi= round(random.uniform(-np.pi,np.pi),2)
            self.angle = self.average_angle() + noise_intensity * Xi
            return self.angle
        
        def align_extrinsic(self):
            Xi= round(random.uniform(-np.pi, np.pi),2)
            self.angle = np.angle(np.exp(1j*self.average_angle())+noise_intensity*np.exp(1j*Xi))
            return self.angle
        
        def align_all_noises(self):
            self.angle = 0.8*self.align_extrinsic()  + 0.2*self.align_intrinsic()
            return self.angle
        
        def move(self, noise_type):
            
            if noise_type == 0 :
                self.angle = self.align_intrinsic()
            if noise_type == 1 :
                self.angle = self.align_extrinsic()    
            if noise_type == 2 :
                self.angle = self.align_all_noises()        
            
            self.vx = np.cos(self.angle)
            self.vy = np.sin(self.angle)
            self.x += self.vx
            self.y += self.vy
            new_positions = np.array([[self.x, self.y]])
            self.quiver.set_offsets(new_positions)
            self.patch.center = (self.x, self.y)
            self.patch1.center = (self.x, self.y)
            self.quiver.set_UVC(self.length * np.cos(self.angle), self.length * np.sin(self.angle))
    
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
    NUM_AGENTS = 100
    spawn_zone = 250 #square of spawn on center
    length = 1

    fig, ax = plt.subplots()
    ax.set_xlim([X_MIN, X_MAX])
    ax.set_ylim([Y_MIN, Y_MAX])
    ax.set_facecolor("dimgray")

    agents_set = set()  # Use a set to store agents
    fps_text = ax.text(10, 10, '', color='white', fontsize=12)  # Create a Text object for displaying FPS
    

    for _ in range(NUM_AGENTS):
        agent = Agent(ax, x=random.uniform(X_MAX/2 - spawn_zone, X_MAX/2 + spawn_zone), y=random.uniform(Y_MAX/2 - spawn_zone, Y_MAX/2 + spawn_zone), rot_speed=rot_speed, angle=round(random.uniform(0, 2*np.pi), 1), color='whitesmoke', length=length, blind_spot=blind_spot)
        agents_set.add(agent)  # Add agents to the set

    def init_fps():
        fps_text.set_text('')
        return [fps_text]
    
    point = ax.scatter(0, 0, color='red', marker='o', s=20)
    
    def mass_center():
        A = np.array([0,0])
        for bird in agents_set:
            A[0] += bird.x
            A[1] += bird.y
        mass_c = [A[0]/len(agents_set),A[1]/len(agents_set)]
        return mass_c    
    
    last_time = 0

    def animate(frame):
        mass_c = mass_center()
        nonlocal last_time
        for agent in agents_set:
            agent.move(noise_type)

        current_time = time.time()  # Get the current time
        elapsed_time = current_time - last_time
        last_time = current_time  # Update last_time
        
        if elapsed_time != 0:
            fps = 1 / elapsed_time
        else:
            fps = 0

        fps_text.set_text(f'FPS: {int(fps)}')

        point.set_offsets(np.array([[mass_c[0], mass_c[1]]]))

        return [agent.quiver for agent in agents_set] + [fps_text] + [point]



    # Création de l'animation
    ani = animation.FuncAnimation(fig, animate, init_func=init_fps, frames=np.arange(0, 2*np.pi, 0.1), interval=1)
    plt.show()

main()

