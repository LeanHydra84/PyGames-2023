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

    # Check for events
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # On Screen Close
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: # On Mouse Down
            screencolor = random_color()
            render = True

        if event.type == pygame.KEYDOWN: # On Key Down

            if event.key == pygame.K_ESCAPE:
                running = False

    
    # Draw Screen
    if render == True:

        # Begin draw frame
        screen.fill(screencolor)


        # End of frame render
        pygame.display.flip()
        render = False

pygame.quit()