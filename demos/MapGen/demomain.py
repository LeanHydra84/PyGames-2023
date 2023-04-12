import pygame
import gentest2
import gentest3
import gentest4

global DEBUGSCREEN

def main():
    global DEBUGSCREEN
    pygame.init()


    screen = pygame.display.set_mode( (1280, 720) )
    DEBUGSCREEN = screen
    clock = pygame.time.Clock()

    group = pygame.sprite.Group()
    gentest4.createmap(group, 15)

    running = True
    while running:

        # Events Handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif e.key == pygame.K_j:
                    group.empty()
                    gentest4.createmap(group, 15)

        # Update

        # Draw
        screen.fill(pygame.Color(40, 40, 40))
        group.draw(screen)

        
        # End frame
        pygame.display.flip()
        clock.tick(60)


    pass

if __name__ == "__main__":
    main()