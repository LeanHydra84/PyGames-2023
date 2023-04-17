import pygame
import random

LIFESPAN = 600

class Unconscious(pygame.sprite.Sprite):
    def __init__(self, bodysprite, worldpos):
        pygame.sprite.Sprite.__init__(self)

        rotation = random.randrange(0, 360)

        self.image = pygame.transform.rotate(bodysprite, rotation)
        self.rect = self.image.get_rect(topleft=(-100, -100))
        self.position: pygame.Vector2 = worldpos

        self.framelife = 0
        

    def update(self, state):
        self.rect.center = self.position + state.camera

        self.framelife += 1
        if self.framelife > LIFESPAN:
            self.kill()

