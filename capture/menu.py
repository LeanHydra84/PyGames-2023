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

        self.blinkstate = False
        self.static_blink_frame = 0
        self.static_blink_time = 40

        self.buttons = []
        self.blink = []

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
        

    def add_static(self, sprite, doesblink = False):
        self.group.add(sprite)
        if doesblink:
            self.blink.append(sprite)

    def add_button(self, sprite, behavior):
        self.buttons.append((sprite, behavior))
        self.group.add(sprite)

    def invert_blink_state(self):
        self.blinkstate = not self.blinkstate
        for x in self.blink:
            if self.blinkstate:
                x.kill()
            else:
                self.group.add(x)

    def update(self):
        self.static_blink_frame += 1
        if self.static_blink_frame >= self.static_blink_time:
            self.static_blink_frame = 0
            self.invert_blink_state()

def build_pause_menu(state_object, btnScale) -> OverlayMenu:

    menu = OverlayMenu(state_object)
    menu.multColor = pygame.Color(100, 100, 200, 255)

    headerIMG = pygame.transform.scale_by(pygame.image.load("assets\\menu\\header.png").convert_alpha(), btnScale)
    header = pygame.sprite.Sprite()
    header.image = headerIMG
    header.rect = headerIMG.get_rect()
    header.rect.centerx = 640
    header.rect.y = 25
    menu.add_static(header, True)
    
    resumeIMG = pygame.transform.scale_by(pygame.image.load("assets\\menu\\play.png").convert_alpha(), btnScale)
    resume = MenuButton(resumeIMG)
    resume.hoverColor = pygame.Color(50, 200, 100, 255)
    resume.rect.topleft = (100, 300)
    menu.add_button(resume, lambda: (menu.togglecapture(), state_object.unpause()))

    quitIMG = pygame.transform.scale_by(pygame.image.load("assets\\menu\\stop.png").convert_alpha(), btnScale)
    quit = MenuButton(quitIMG)
    quit.hoverColor = pygame.Color(200, 50, 100, 255)
    quit.rect.topleft = (100, 450)
    menu.add_button(quit, state_object.quit)

    return menu