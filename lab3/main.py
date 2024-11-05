import pygame
import sys
import time
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_GRAY = (30, 30, 30)
BLUE = (0, 100, 255)

SIDE_PANEL_WIDTH = 200

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rasterization Algorithms")
font = pygame.font.SysFont('Courier New', 18)
def draw_grid():
    for x in range(0, WIDTH - SIDE_PANEL_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y))

    pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH - SIDE_PANEL_WIDTH, HEIGHT // 2), 2)
    pygame.draw.line(screen, WHITE, ((WIDTH - SIDE_PANEL_WIDTH) // 2, 0), ((WIDTH - SIDE_PANEL_WIDTH) // 2, HEIGHT), 2)
    
def draw_pixel(x, y, color=RED):
    pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def step_by_step(x0, y0, x1, y1):
    if x0 == x1:  
        return [(x0, y) for y in range(min(y0, y1), max(y0, y1) + 1)]

    points = []
    dx = x1 - x0
    dy = y1 - y0
    k = dy / dx
    b = y0 - k * x0
    step = 1 / max(abs(dx), abs(dy))  
    x = x0
    if dx > 0:  
        while x <= x1:
            y = k * x + b
            points.append((round(x), round(y)))
            x += step
    else:
        while x >= x1:
            y = k * x + b
            points.append((round(x), round(y)))
            x -= step

    return points
def dda_algorithm(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    points = []
    x, y = x0, y0
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment
    return points

def bresenham_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    points = []
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

def bresenham_circle(xc, yc, r):
    points = []
    x = r
    y = 0
    d = 1 - r

    while x >= y:
        for xi, yi in [(x, y), (y, x), (-x, y), (-y, x), (x, -y), (-x, -y), (y, -x), (-y, -x)]:
            points.append((xc + xi, yc + yi))
        y += 1
        if d < 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * y - 2 * x + 1
    return points

class RasterizationApp:
    def __init__(self):
        self.algorithm = "Bresenham"
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.drawing = False
        self.radius = 0
        self.input_active = False
        self.input_radius = ""
        self.drawn_points = []
        self.execution_time = 0.0

    def draw_algorithm(self):
        x0, y0 = self.start_point
        start_time = time.time()
        
        if self.algorithm == "Circle":
            r = self.radius
            points = bresenham_circle(x0, y0, r)
        else:
            x1, y1 = self.end_point
            if self.algorithm == "Step by Step":
                points = step_by_step(x0, y0, x1, y1)
            elif self.algorithm == "DDA":
                points = dda_algorithm(x0, y0, x1, y1)
            elif self.algorithm == "Bresenham":
                points = bresenham_line(x0, y0, x1, y1)

        self.execution_time = time.time() - start_time
        self.drawn_points.extend(points)

    def draw_sidebar(self):
        pygame.draw.rect(screen, BLUE, (WIDTH - SIDE_PANEL_WIDTH, 0, SIDE_PANEL_WIDTH, HEIGHT))
        text = font.render(f'Алгоритм: {self.algorithm}', True, WHITE)
        screen.blit(text, (WIDTH - SIDE_PANEL_WIDTH + 10, 10))

        input_box = pygame.Rect(WIDTH - SIDE_PANEL_WIDTH + 10, 50, 180, 30)
        pygame.draw.rect(screen, WHITE if self.input_active else DARK_GRAY, input_box, 2)
        radius_text = font.render(self.input_radius, True, WHITE)
        screen.blit(radius_text, (input_box.x + 5, input_box.y + 5))

        time_text = font.render(f'Время: {self.execution_time:.6f} с', True, WHITE)
        screen.blit(time_text, (WIDTH - SIDE_PANEL_WIDTH + 10, 90))

        algorithms = ["Step by Step", "DDA", "Bresenham", "Circle", "Clear"]
        for i, algo in enumerate(algorithms):
            button_color = WHITE if self.algorithm == algo else BLACK
            label = font.render(algo, True, button_color)
            screen.blit(label, (WIDTH - SIDE_PANEL_WIDTH + 10, 120 + i * 30))

    def redraw_all(self):
        for x, y in self.drawn_points:
            draw_pixel(x, y)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            screen.fill(BLACK)
            draw_grid()
            self.draw_sidebar()
            self.redraw_all()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if WIDTH - SIDE_PANEL_WIDTH < event.pos[0] < WIDTH:
                            if 50 <= event.pos[1] <= 80:
                                self.input_active = not self.input_active
                            else:
                                self.input_active = False
                        else:
                            if self.algorithm == "Circle":
                                self.start_point = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                                if self.input_radius.isdigit():
                                    self.radius = int(self.input_radius)
                                    self.draw_algorithm()
                            else:
                                if not self.drawing:
                                    self.start_point = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                                    self.drawing = True
                                else:
                                    self.end_point = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                                    self.draw_algorithm()
                                    self.drawing = False
                elif event.type == KEYDOWN:
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            if self.input_radius.isdigit():
                                self.radius = int(self.input_radius)
                            self.input_radius = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_radius = self.input_radius[:-1]
                        else:
                            if event.unicode.isdigit():
                                self.input_radius += event.unicode

            mouse_pos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if mouse_pos[0] > WIDTH - SIDE_PANEL_WIDTH:
                    for i, algo in enumerate(["Step by Step", "DDA", "Bresenham", "Circle", "Clear"]):
                        if 120 + i * 30 <= mouse_pos[1] <= 120 + (i + 1) * 30:
                            if algo == "Clear":
                                self.start_point = (0, 0)
                                self.end_point = (0, 0)
                                self.drawn_points.clear()
                                screen.fill(BLACK)
                            else:
                                self.algorithm = algo

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    app = RasterizationApp()
    app.run()
