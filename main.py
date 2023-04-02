import pygame
import room_creator
import player

from layerManager import LayerManager

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

    char = player.createplayer(5)

    layers = LayerManager()
    layers.add(map.group, "Map")
    layers.add_new("Character").add(char)
    layers.add_new("Legs").add(char.feet)

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

        # Update

        char.update(keys, pygame.Vector2(pygame.mouse.get_pos()))

        # Draw

        screen.fill(backgroundColor)

        layers.render(screen)        

        clock.tick(60)
        pygame.display.flip()



if __name__ == "__main__":
    main()