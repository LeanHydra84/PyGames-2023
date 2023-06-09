import pygame

class Feet(pygame.sprite.Sprite):
    def __init__(self, parent, resource):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent

        base = resource.states[0]
        self.image_base = base.img
        self.image = self.image_base
        self.rect = self.image_base.get_rect()

        self.frametick = 0
        self.frametimer = base.speed
        self.layer_group = None

    def flip_base(self):
        self.image_base = pygame.transform.flip(self.image_base, True, False)

    def set_visible(self, toggle: bool):
        if toggle:
            self.layer_group.add(self)
        else:
            self.kill()

    def update(self, position):

        # Rotate
        self.image = pygame.transform.rotate(self.image_base, self.parent.rotation)
        self.rect = self.image.get_rect()

        # Set position
        self.rect.center = position

        # Animate feet motion
        if self.frametick >= self.frametimer:
            self.frametick = 0
            self.flip_base()
        else:
            self.frametick += 1

    def add(self, group):
        self.layer_group = group