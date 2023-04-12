import pygame

class Unconscious(pygame.sprite.Sprite):
    def __init__(self, bodysprite, worldpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = bodysprite
        self.rect = bodysprite.get_rect(topleft=(-100, -100))
        self.position: pygame.Vector2 = worldpos
        

    def update(self, state):
        self.rect.center = self.position + state.camera

