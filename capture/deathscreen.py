import pygame

from capture.menu import OverlayMenu
from capture.capturestate import CaptureState

def lerp(f1, f2, frac):
    return f1 + (f2 - f1) * frac

def saturate(val, low, high):
    if val < low:
        return low
    if val > high:
        return high
    return val

# This fully sucks!!!
# I should just use the OverlayMenu class I wrote
# and figure out how to make the text do that.
# because then there would be a super easy
# blinking text "Insert Another Coin To Play Again"

class DeathScreen(CaptureState):
    def __init__(self, state, sprite, startsize, endsize, time):
        super().__init__(state)

        self.group = pygame.sprite.GroupSingle()
        self.deathText = pygame.sprite.Sprite()

        self.centerScreen = state.centerScreen
        self.static_image = sprite
        self.deathText.image = sprite
        self.deathText.rect = sprite.get_rect(center=state.centerScreen)
        self.group.add(self.deathText)

        self.startsize = startsize
        self.endsize = endsize

        self.alphaTime = pygame.time.get_ticks()
        self.time = time

        state.RESOURCES.SND_DEATH_SOUND.play()

    def render(self, screen):
        self.group.draw(screen)

    def update(self):

        if pygame.time.get_ticks() - self.alphaTime <= self.time * 1000:
            percent = saturate((pygame.time.get_ticks() - self.alphaTime) / (self.time * 1000), 0, 1)
            scale = lerp(self.startsize, self.endsize, percent)

            self.deathText.image = pygame.transform.scale_by(self.static_image, scale)
            self.deathText.rect = self.deathText.image.get_rect(center=self.centerScreen)


def create_death_screen(state) -> OverlayMenu:
    death = OverlayMenu(state)
    death.multColor = pygame.Color(100, 100, 100)
    
    dtext = pygame.sprite.Sprite()
    dtext.image = pygame.transform.scale_by(state.RESOURCES.DEATH_TEXT, 3)
    dtext.rect = dtext.image.get_rect(center=state.centerScreen)
    death.add_static(dtext)
    
    font: pygame.font.Font = state.RESOURCES.FONT_25
    coinSpr = pygame.sprite.Sprite()
    coinSpr.image = font.render("Insert coin to continue... (Or press SPACE)", True, pygame.Color(255, 255, 255))
    coinSpr.rect = coinSpr.image.get_rect(bottomleft=(30, state.screensize[1] - 30))
    death.add_static(coinSpr, True)

    return death