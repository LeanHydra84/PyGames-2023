import pygame
import room_creator

SCREENSIZE = (1280, 720)

backgroundColor = pygame.Color(100, 100, 100, 255)

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(SCREENSIZE)
    clock = pygame.time.Clock()

    room_creator.room_scale = 5
    map = room_creator.Map()
    map.create_rooms()

    running = True

    keys = [False, False, False, False]

    while running:
        
        for event in pygame.event.get():

            # Process Events
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_w:
                    keys[0] = True
                elif event.key == pygame.K_a:
                    keys[1] = True
                elif event.key == pygame.K_s:
                    keys[2] = True
                elif event.key == pygame.K_d:
                    keys[3] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False

        screen.fill(backgroundColor)
        map.group.draw(screen)
        

        clock.tick(60)
        pygame.display.flip()



if __name__ == "__main__":
    main()