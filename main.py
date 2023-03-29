import pygame
import random as rand

print("Hello World!")

def random_colorint():
    return rand.randrange(0, 255, 1)

def random_color():
    return pygame.Color(random_colorint(), random_colorint(), random_colorint(), 255)

pygame.init()
screen = pygame.display.set_mode((1280, 720))

running = True
render = True

screencolor = random_color()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            screencolor = random_color()
            render = True
    
    if render == True:
        screen.fill(screencolor)

        pygame.display.flip()
        render = False

    pass

print("End")
pygame.quit()