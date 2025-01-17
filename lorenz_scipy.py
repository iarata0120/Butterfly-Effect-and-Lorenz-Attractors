import random
import pygame
import numpy as np

# Integrating scipy into program in order to use odeint (exact solutions)
from scipy.integrate import odeint


class Lorenz:
    def __init__(self):
        self.xMin, self.xMax = -35, 35
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = 0, 50
        self.X, self.Y, self.Z = 0.1, 0.0, 10.0
        self.oX, self.oY, self.Z = self.X, self.Y, self.Z
        self.dt = 0.01
        self.a, self.b, self.c = 10, 28, 8/3
        self.pixelColor = (51, 153, 255)

        # For values given by scipy odeint
        self.initX, self.initY, self.initZ = self.X, self.Y, self.Z
        self.states = None
        self.count = 0
        self.numFrames = 0

    # Using equations dx/dt = a(y-x), dy/dt = x(b-z)-y, dz/dt = xy-cz where {a.b.c} will serve as the parameters
    # a = sigma, b = rho, c = beta from wikipedia Lorenz equations
    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.a * (self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X * (self.b - self.Z) - self.Y)) 
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.c * self.Z))

    # Using scipy odeint (ODE solver)
    def F(self, inputX, tempT, a, b, c):
        tx, ty, tz = inputX
        dXdt = [a * (ty - tx), tx * (b - tz) - ty, tx * ty - c * tz]
        return dXdt

    # Use newly defined F function for odeint. tempT represents domain of inputs t to feed into odeint.
    def solve(self):
        state0 = [self.initX, self.initY, self.initZ]
        tempT = np.arange(0.0, 80.0, self.dt)
        self.states = odeint(self.F, state0, tempT, args=(self.a, self.b, self.c))
        self.numFrames = self.states.shape

    def step3(self):
        if self.count < self.numFrames[0]:
            self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
            self.X = self.states[self.count, 0]
            self.Y = self.states[self.count, 1]
            self.Z = self.states[self.count, 2]
            self.count += 1

    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oZ, self.xMin, self.xMax, self.zMin, self.zMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Z, self.xMin, self.xMax, self.zMin, self.zMax, width, height)

        # Draw the current line segment
        newRect = pygame.draw.line(displaySurface, self.pixelColor, oldPos, newPos, 1)

        # Return the bounding rectangle
        return newRect

    # Method to convert values to coordinates that fit screen
    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x - xMin) / (xMax - xMin))
        newY = height * ((yMax - y) / (yMax - yMin))
        return round(newX), round(newY)


class Application:
    def __init__(self):
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        #self.size = self.width, self.height = 960, 540 #Screen size
        self.size = self.width, self.height = 1920, 1080 #Full Screen
        self.count = 0
        self.outputCount = 1
        self.pause = False
        self.restart = False

    def on_init(self):
        pygame.init()
        rgbTextFont = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.display.set_caption("Lorenz Atractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        # Configure the attractor
        colors = []

        # Personal Favorite
        #colors.append((51, 153, 255))
        #colors.append((204, 204, 255))
        #colors.append((0, 0, 255))

        # Green
        #colors.append((50, 205, 50))
        #colors.append((152, 251, 152))
        #colors.append((0, 255, 255))

        # Random
        colors.append((random.uniform(0,255), random.uniform(0,255), random.uniform(0,255)))
        colors.append((random.uniform(0,255), random.uniform(0,255), random.uniform(0,255)))
        colors.append((random.uniform(0,255), random.uniform(0,255), random.uniform(0,255)))


        for i in range(3):
            self.attractors.append(Lorenz())

            #self.attractors[i].X = random.uniform(0.1,0.101)

            # Tiny perturbations with random
            self.attractors[i].initX = random.uniform(0.1, 0.101)
            self.attractors[i].pixelColor = colors[i]

            # Solve for each attractor with respectively varying inital states (initX is randomized)
            self.attractors[i].solve()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

        # Implementing pause (key p/space), restart (key r) and quit (keys/Esc) user interactions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                self.pause = not self.pause
            if event.key == pygame.K_r:
                self.restart = True
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.isRunning = False

    def on_loop(self):
        # Call the step method for the attractor
        for x in self.attractors:
            #x.step()
            x.step3()

    def on_render(self):
        #Draw the attractor
        for x in self.attractors:
            newRect = x.draw(self.displaySurface)
            pygame.display.update(newRect)

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)
            
            if self.pause == False:
                self.on_loop()
                self.on_render()

            if self.restart == True:
                self = Application()
                self.on_execute()
                self.restart = False
                self.isRunning = False

            self.fpsClock.tick()
            self.count += 1

        # Uncomment block below to save a screenshot of finished drawing
        #pygame.image.save(self.displaySurface,"screenshot.jpg")
        
        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()



