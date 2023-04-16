import pygame.time
from rendering.textobject import BasicTextObject
from math import floor

class FormattedCountdownTimer:
    def __init__(self, time, font):
        self.timeRenderer = BasicTextObject(font)

        self.alphaTime = pygame.time.get_ticks()
        self.betaTime = time * 1000 # to milliseconds

    def restart(self):
        self.alphaTime = pygame.time.get_ticks()
    
    def update(self):
        dT = pygame.time.get_ticks() - self.alphaTime
        remaining = floor((self.betaTime - dT) * 0.001) # convert to seconds
        textstr = f"{remaining // 60}:{(remaining % 60):02}"
        if textstr != self.timeRenderer.text:
            self.timeRenderer.set_text(textstr)
            self.timeRenderer.rect.topleft = (10, 10)