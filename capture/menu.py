import pygame
import capture.capturestate as capturestate

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)

        self.imageBase = sprite
        self.rect = self.imageBase.get_rect()
        self.hoverColor = pygame.Color(0, 0, 0, 255)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.set_hover(False)

    def set_hover(self, isHover):
        self.image.blit(self.imageBase, (0, 0))
        if isHover:
            self.image.fill(self.hoverColor, None, pygame.BLEND_RGBA_MULT)


class OverlayMenu(capturestate.CaptureState):
    def __init__(self, state):
        capturestate.CaptureState.__init__(self, state)

        self.multColor = pygame.Color(100, 100, 100, 255)
        self.group = pygame.sprite.Group()
        self.buttons = []

    def get_onclick(self, pos):
        for sprite in self.buttons:
            if pygame.Rect.collidepoint(sprite[0].rect, pos):
                return sprite
        return None

    def render(self, screen: pygame.Surface):
        screen.fill(self.multColor, None, pygame.BLEND_MULT)

        for sprite in self.buttons:
            if pygame.Rect.collidepoint(sprite[0].rect, pygame.mouse.get_pos()):
                sprite[0].set_hover(True)
            else:
                sprite[0].set_hover(False)

        self.group.draw(screen)

    def register_click(self, position):
        clicked = self.get_onclick(position)
        if clicked == None:
            return
        clicked[1]()
        

    def add_static(self, sprite):
        self.group.add(sprite)

    def add_button(self, sprite, behavior):
        self.buttons.append((sprite, behavior))
        self.group.add(sprite)

def build_pause_menu(state_object) -> OverlayMenu:

    menu = OverlayMenu(state_object)
    menu.multColor = pygame.Color(100, 100, 200, 255)
    
    resume = MenuButton(pygame.image.load("assets\\menu_test\\resume_sprite.png").convert_alpha())
    resume.hoverColor = pygame.Color(50, 200, 100, 255)
    resume.rect.topleft = (100, 100)
    menu.add_button(resume, lambda: (menu.togglecapture(), state_object.unpause()))

    quit = MenuButton(pygame.image.load("assets\\menu_test\\quit_sprite.png").convert_alpha())
    quit.hoverColor = pygame.Color(200, 50, 100, 255)
    quit.rect.topleft = (100, 200)
    menu.add_button(quit, state_object.quit)

    return menu