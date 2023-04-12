import pygame
import gentest2

def main():
    pygame.init()


    screen = pygame.display.set_mode( (1280, 720) )
    clock = pygame.time.Clock()
    group = pygame.sprite.Group()

    gentest2.createmap(group)

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