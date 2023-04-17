import pygame

projectilespeed = 8
hitdistsqr = 35**2
maxLife = 1000

class Projectile(pygame.sprite.Sprite):
    def __init__(self, sprite, direction, position):
        pygame.sprite.Sprite.__init__(self)
        self.position: pygame.Vector2 = position.copy()
        
        self.image = sprite
        self.rect = sprite.get_rect(topleft=(-100, -100))
        self.forward = direction

        self.lifecounter = 0
        

    def update(self, state):

        self.lifecounter += 1
        self.position += self.forward * projectilespeed
        self.rect.center = self.position + state.camera

        if not state.map.get_collision_at_point(self.position + state.camera):
            self.kill()

        if self.position.distance_squared_to(state.player.position) < hitdistsqr:
            self.kill()

            if state.player.hit_by_enemy_attack(self.forward, state):
                state.RESOURCES.SND_PUNCH.play()

        if self.lifecounter >= maxLife:
            self.kill()


    def interact(self, state, _):
        return True