import pygame
from capture.menu import OverlayMenu


def win_game_scene(screen: pygame.Surface, background):


    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                
        # Draw
        screen.blit(background, (0, 0))

        # End Frame
        pygame.display.flip()
        clock.tick(60)