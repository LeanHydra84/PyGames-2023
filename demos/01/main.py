import pygame
import random as rand
import guytest

def random_colorint():
    return rand.randrange(0, 255, 1)

def random_color():
    return pygame.Color(random_colorint(), random_colorint(), random_colorint(), 255)

pygame.init()
screen = pygame.display.set_mode((1280, 720))

running = True
render = True

screencolor = random_color()
clock = pygame.time.Clock()

guy = guytest.SheetGuy(pygame.image.load("assets\\sprite_sheet_test.png").convert_alpha(), 1, 0)
guy.scale = 10

group = pygame.sprite.Group()
guy.add(group)

#frame = sf.import_sprite_static("frame0.png")

keys = [False, False]

while running:

    # Check for events
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # On Screen Close
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN: # On Mouse Down
            screencolor = random_color()
            render = True

        elif event.type == pygame.KEYDOWN: # On Key Down

            if event.key == pygame.K_ESCAPE: # Escape -- Close game
                running = False

            if event.key == pygame.K_a:
                keys[0] = True
            elif event.key == pygame.K_d:
                keys[1] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                keys[0] = False
            elif event.key == pygame.K_d:
                keys[1] = False

    # Spritegroup update
    if keys[0] == keys[1]:
        pass
    elif keys[0]:
        guy.position.x -= 4
        guy.right = False
    elif keys[1]:
        guy.position.x += 4
        guy.right = True

    group.update()
    

    # Begin draw frame
    screen.fill(screencolor)
    group.draw(screen)

    # End of frame render
    pygame.display.flip()
    clock.tick(60)
    render = False

    

pygame.quit()