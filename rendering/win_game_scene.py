import pygame
from capture.menu import OverlayMenu
from capture.menu import BounceText


def win_game_scene(screen: pygame.Surface, state):
    resources = state.RESOURCES

    clock = pygame.time.Clock()

    menu = OverlayMenu(None)
    menu.multColor = pygame.Color(255, 255, 255)


    wintext = BounceText(resources.YOUWON, (200, 0), 2)
    menu.add_static(wintext)

    keyspr = pygame.sprite.Sprite()
    keyspr.image = state.RESOURCES.FONT_25.render("Press space to continue...", True, pygame.Color(255, 255, 255))
    keyspr.rect = keyspr.image.get_rect(bottomright=pygame.Vector2(state.screensize) - (30, 30))
    menu.add_static(keyspr, True)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        
        menu.update()

        # Draw
        screen.blit(resources.WINNINGSCREEN, (0, 0))

        menu.render(screen)

        # End Frame
        pygame.display.flip()
        clock.tick(60)