import pygame

projectilespeed = 8
hitdistsqr = 25**2

class Projectile(pygame.sprite.Sprite):
    def __init__(self, sprite, direction, position):
        pygame.sprite.Sprite.__init__(self)
        self.position: pygame.Vector2 = position.copy()
        
        self.image = sprite
        self.rect = sprite.get_rect(center=position)
        self.forward = direction
        

    def update(self, state):

        self.position += self.forward * projectilespeed

        if not state.map.get_collision_at_point(self.position):
            self.kill()

        if self.position.distance_squared_to(state.player.position) < hitdistsqr:
            state.player.kill()
            self.kill()


    def interact(self, state, _):
        pass