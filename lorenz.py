import random
import pygame

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

    # Using equations dx/dt = a(y-x), dy/dt = x(b-z)-y, dz/dt = xy-cz where {a.b.c} will serve as the parameters
    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.a * (self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X * (self.b - self.Z) - self.Y)) 
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.c * self.Z))

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
        self.size = self.width, self.height = 1920, 1080 #Full Screen
        self.count = 0
        self.outputCount = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorenz Atractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        # Configure the attractor
        colors = []
        colors.append((51, 153, 255))
        colors.append((204, 204, 255))
        colors.append((0, 0, 255))

        for i in range(3):
            self.attractors.append(Lorenz())

            # Tiny perturbations with random
            self.attractors[i].X = random.uniform(0.1,0.101)
            self.attractors[i].pixelColor = colors[i]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        # Call the step method for the attractor
        for x in self.attractors:
            x.step()

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
            
            self.on_loop()
            self.on_render()

            self.fpsClock.tick()
            self.count += 1

        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()




