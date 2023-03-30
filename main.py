import pygame

SCREENX = 1280
SCREENY = 720

backgroundColor = pygame.Color(100, 100, 100, 255)

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREENX, SCREENY))
    clock = pygame.time.Clock()

    running = True

    while running:
        
        for event in pygame.event.get():

            # Process Events
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            

        screen.fill(backgroundColor)

        clock.tick(60)
        pygame.display.flip()



if __name__ == "__main__":
    main()