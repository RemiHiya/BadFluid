import numpy as np

class Fluid:
    def __init__(self, width, height, diffusion, viscosity, dt):
        self.width = width
        self.height = height
        self.dt = dt
        self.diffusion = diffusion
        self.viscosity = viscosity

        self.s = np.zeros((width, height))
        self.density = np.zeros((width, height))

        self.Vx = np.zeros((width, height))
        self.Vy = np.zeros((width, height))
        
        self.Vx0 = np.zeros((width, height))
        self.Vy0 = np.zeros((width, height))
        self.obstacles = np.zeros((width, height), dtype=bool)

    def step(self):
        self.diffuse(1, self.Vx0, self.Vx, self.viscosity)
        self.diffuse(2, self.Vy0, self.Vy, self.viscosity)

        self.project(self.Vx0, self.Vy0, self.Vx, self.Vy)

        self.advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0)
        self.advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0)

        self.project(self.Vx, self.Vy, self.Vx0, self.Vy0)

        self.diffuse(0, self.s, self.density, self.diffusion)
        self.advect(0, self.density, self.s, self.Vx, self.Vy)

    def add_density(self, x, y, amount):
        self.density[x, y] += amount

    def add_velocity(self, x, y, amountX, amountY):
        self.Vx[x, y] += amountX
        self.Vy[x, y] += amountY
    
    def fade_velocity(self, x, y):
        self.Vx[x, y] -= 7
        self.Vy[x, y] -= 7
        self.Vx[x, y] = max(self.Vx[x, y], 0)
        self.Vy[x, y] = max(self.Vy[x, y], 0)

    def fade_density(self, x, y):
        self.density[x, y] -= 7
        self.density[x, y] = max(self.density[x, y], 0)

    def diffuse(self, b, x, x0, diff):
        a = self.dt * diff * self.width * self.height
        self.lin_solve(b, x, x0, a, 1 + 4 * a)

    def lin_solve(self, b, x, x0, a, c):
        c_recip = 1.0 / c
        for k in range(4):
            for i in range(1, self.width - 1):
                for j in range(1, self.height - 1):
                    if not self.obstacles[i, j]:
                        x[i, j] = (x0[i, j] + a * (x[i+1, j] + x[i-1, j] + x[i, j+1] + x[i, j-1])) * c_recip
            self.set_bnd(b, x)

    def project(self, velocX, velocY, p, div):
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                if not self.obstacles[i, j]:
                    div[i, j] = -0.5 * (velocX[i+1, j] - velocX[i-1, j] + velocY[i, j+1] - velocY[i, j-1]) / self.width
                    p[i, j] = 0

        self.set_bnd(0, div)
        self.set_bnd(0, p)
        self.lin_solve(0, p, div, 1, 4)

        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                if not self.obstacles[i, j]:
                    velocX[i, j] -= 0.5 * (p[i+1, j] - p[i-1, j]) * self.width
                    velocY[i, j] -= 0.5 * (p[i, j+1] - p[i, j-1]) * self.height

        self.set_bnd(1, velocX)
        self.set_bnd(2, velocY)

    def advect(self, b, d, d0, velocX, velocY):
        dt0 = self.dt * self.width
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                if not self.obstacles[i, j]:
                    tmp1 = dt0 * velocX[i, j]
                    tmp2 = dt0 * velocY[i, j]
                    x = i - tmp1
                    y = j - tmp2
                    if x < 0.5:
                        x = 0.5
                    if x > self.width + 0.5:
                        x = self.width + 0.5
                    i0 = int(x)
                    i1 = i0 + 1
                    if y < 0.5:
                        y = 0.5
                    if y > self.height + 0.5:
                        y = self.height + 0.5
                    j0 = int(y)
                    j1 = j0 + 1
                    s1 = x - i0
                    s0 = 1 - s1
                    t1 = y - j0
                    t0 = 1 - t1
                    try:
                        d[i, j] = s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) + s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1])
                    except: pass
        self.set_bnd(b, d)

    def set_bnd(self, b, x):
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                if self.obstacles[i, j]:
                    x[i, j] = 0
                else:
                    if i == 1 or i == self.width - 2 or self.obstacles[i-1, j] or self.obstacles[i+1, j]:
                        x[i, 0] = x[i, 1] if b == 2 else -x[i, 1]
                        x[i, self.height - 1] = x[i, self.height - 2] if b == 2 else -x[i, self.height - 2]
                    if j == 1 or j == self.height - 2 or self.obstacles[i, j-1] or self.obstacles[i, j+1]:
                        x[0, j] = x[1, j] if b == 1 else -x[1, j]
                        x[self.width - 1, j] = x[self.width - 2, j] if b == 1 else -x[self.width - 2, j]
        x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
        x[0, self.height - 1] = 0.5 * (x[1, self.height - 1] + x[0, self.height - 2])
        x[self.width - 1, 0] = 0.5 * (x[self.width - 2, 0] + x[self.width - 1, 1])
        x[self.width - 1, self.height - 1] = 0.5 * (x[self.width - 2, self.height - 1] + x[self.width - 1, self.height - 2])