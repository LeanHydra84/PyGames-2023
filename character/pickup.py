import pygame
import math

class Pickup(pygame.sprite.Sprite):
    def __init__(self, sprite, type, position, onpickup):
        self.type = type
        self.image = sprite
        self.position = position
        self.rect = self.image.get_rect(center=position)
        self.onpickup = onpickup

    def update(self, state):
        newpos = self.position.copy()
        newpos.y +=  + math.sin(pygame.time.get_ticks() * 0.1)
        self.rect.center = newpos
        
    def interact(self, state, interactKeyPressed):
        self.kill()
        self.onpickup(state)