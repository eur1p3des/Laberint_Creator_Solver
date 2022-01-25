import pygame
import time
import random

# Finestra de Pygame
WIDTH = 500
HEIGHT = 600
FPS = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (46, 54, 88)
YELLOW = (255 ,255 ,0)

#Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberint Python")
clock = pygame.time.Clock()

# Variable pel laberint
x = 0
y = 0
w = 20
grid = []
visited = []
stack = []
solution = {}


# Fer la graella
def build_grid(x, y, w):
    for i in range(1,21):
        x = 20                                                            #  posa la coordenada x com a posició inicial
        y = y + 20                                                        # nova fila
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # part de dalt de la cel·la
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # part dreta de la cel·la
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # part de baix de la cel·la
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # part esquerra de la cel·la
            grid.append((x,y))                                            # afegir la cel·la a la llista
            x = x + 20                                                    # moure la cel·la a una nova posició


def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # dibuixa un rectangle el doble de l'amplada de la cel·la
    pygame.display.update()                                              # eliminar la paret


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w +1, y +1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 39, 19), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1, y +1, 18, 18), 0)          # dibuixa una cel·la d’amplada única
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 18, 18), 0)        # s'utilitza per tornar a acolorir el camí després de single_cell
    pygame.display.update()                                        # ha pasat per la casella


def solution_cell(x,y):
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             # mostra la solució
    pygame.display.update()                                        # ha pasat per la casella


def carve_out_maze(x,y):
    single_cell(x, y)
    stack.append((x,y))
    visited.append((x,y))
    while len(stack) > 0:
        time.sleep(.07)
        cell = []
        if (x + w, y) not in visited and (x + w, y) in grid:
            cell.append("right")

        if (x - w, y) not in visited and (x - w, y) in grid:
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:
            cell.append("up")

        if len(cell) > 0:
            cell_chosen = (random.choice(cell))

            if cell_chosen == "right":
                push_right(x, y)
                solution[(x + w, y)] = x, y
                x = x + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()
            single_cell(x, y)
            time.sleep(.05)
            backtracking_cell(x, y)


def plot_route_back(x,y):
    solution_cell(x, y)
    while (x, y) != (20,20):
        x, y = solution[x, y]
        solution_cell(x, y)
        time.sleep(.1)


x, y = 20, 20
build_grid(40, 0, 20)
carve_out_maze(x,y)
plot_route_back(400, 400)



running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False