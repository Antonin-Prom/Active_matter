import numpy as np
import matplotlib.pyplot as plt
# Nombre de cellules en x et y
nx = 200
ny = 200

class Fluid():
    def __init__(self, density, nbx, nby, h):
        self.density = density
        self.nbx = nbx + 2
        self.nby = nby + 2
        self.h = h
        self.nbCells = self.nbx * self.nby
        self.u = np.zeros(self.nbCells)
        self.v = np.zeros(self.nbCells)
        self.new_u = np.zeros(self.nbCells)
        self.new_v = np.zeros(self.nbCells)
        self.p = np.zeros(self.nbCells)
        self.s = np.zeros(self.nbCells)
        self.m = np.zeros(self.nbCells)
        self.newM = np.ones(self.nbCells)
        nb = nbx * nby

    def solveIncompressibility(self, nbIters, dt):
        n = self.nby
        cp = self.density * self.h / dt
        for _ in range(nbIters):
            for i in range(1, self.nbx - 1):
                for j in range(1, self.nby - 1):
                    if self.s[i * n + j] == 0.0:
                        continue
                    s = self.s
                    sx0 = self.s[(i - 1) * n + j]
                    sx1 = self.s[i + 1 * n + j]
                    sy0 = self.s[i * n + j - 1]
                    sy1 = self.s[i * n + j + 1]
                    s = sx0 + sx1 + sy0 + sy1
                    if s == 0.0:
                        continue

                    div = (
                        self.u[(i + 1) * n + j]
                        - self.u[i * n + j]
                        + self.v[i * n + j + 1]
                        - self.v[i * n + j]
                    )
                    p = -div / s
                    p *= 1.999
                    self.p[i * n + j] += cp * p

                    self.u[i * n + j] -= sx0 * p
                    self.u[(i + 1) * n + j] += sx1 * p
                    self.v[i * n + j] -= sy0 * p
                    self.v[i * n + j + 1] += sy1 * p

    def extrapolate(self):
        n = self.nby
        for i in range(0, self.nbx):
            self.u[i * n + 0] = self.u[i * n + 1]
            self.u[i * n + self.nby - 1] = self.u[i * n + self.nby - 2]

        for j in range(self.nby):
            self.v[n + j] = self.v[n + j]
            self.v[(self.nbx - 1) * n + j] = self.v[(self.nbx - 2) * n + j]

    def advect(self, field, field0, u, v, dt):
        n = self.nby
        dt0 = dt * max(self.nbx, self.nby)
        for i in range(1, self.nbx - 1):
            for j in range(1, self.nby - 1):
                x = i - dt0 * u[i * n + j]
                y = j - dt0 * v[i * n + j]
                x = max(0.5, min(self.nbx - 1.5, x))
                i0, i1 = int(x), int(x) + 1
                y = max(0.5, min(self.nby - 1.5, y))
                j0, j1 = int(y), int(y) + 1

                s1 = x - i0
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                field[i * n + j] = (
                    s0
                    * (t0 * field0[i0 * n + j0] + t1 * field0[i0 * n + j1])
                    + s1
                    * (t0 * field0[i1 * n + j0] + t1 * field0[i1 * n + j1])
                )

    def step(self, dt):
        self.solveIncompressibility(20, dt)
        self.extrapolate()
        self.advect(self.u, self.new_u, self.u, self.v, dt)
        self.advect(self.v, self.new_v, self.u, self.v, dt)
        self.extrapolate()

        # Update velocities
        self.u, self.new_u = self.new_u, self.u
        self.v, self.new_v = self.new_v, self.v


    def render(self):
        # Reshape velocity arrays to 2D grid
        u_grid = self.u[1:-1].reshape((nx, ny))
        v_grid = self.v[1:-1].reshape((nx, ny))

        # Create grid coordinates
        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 1, ny)
        X, Y = np.meshgrid(x, y)

        # Plot velocity vectors
        plt.figure()
        plt.quiver(X, Y, u_grid, v_grid)
        plt.show()

# Create a Fluid instance
fluid = Fluid(density=1.0, nbx=nx-2, nby=ny-2, h=1.0)

# Perform simulation steps
num_steps = 100
dt = 1
for step in range(num_steps):
    fluid.step(dt)

# Render the fluid simulation
fluid.render()

