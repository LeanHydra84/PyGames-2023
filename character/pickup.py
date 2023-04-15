import pygame
import math



# class Interactable(pygame.sprite.Sprite):
#     def __init__(self, sprite, type, position, oninteract):
#         self.type = type
#         self.image = sprite
#         self.position = position
#         self.rect = self.image.get_rect(center=position)
#         self.oninteract = oninteract

#     def update(self, state):
#         pass

#     def interact(self, state, isEpressed):
#         if isEpressed:
#             self.oninteract(state)

# class Pickup(Interactable):
#     def update(self, state):
#         newpos = self.position.copy()
#         newpos.y +=  + math.sin(pygame.time.get_ticks() * 0.1)
#         self.rect.center = newpos
        
#     def interact(self, state, _):
#         self.kill()
#         self.oninteract(state)

pickupSinScale = 5

itemHintMoveSpeed = 15

def lerp(f1, f2, frac):
    return f1 + (f2 - f1) * frac

class ItemHint(pygame.sprite.Sprite):
    def __init__(self, sprite, aliveframes):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.bottomright = (0, 0)

        self.stage = 0
        self.current = 0
        self.lifespan = aliveframes
    
    def update(self, state):
        if self.stage == 0:
            if self.current > itemHintMoveSpeed:
                self.stage = 1
                self.current = 0
                return
            newY = lerp(-self.rect.h, 0, self.current / itemHintMoveSpeed)
            self.rect.topright = (state.screensize[0], newY)
            self.current += 1
        elif self.stage == 1:
            self.current += 1
            if self.current > self.lifespan:
                self.stage = 2
                self.current = 0
                return
        elif self.stage == 2:
            if self.current > itemHintMoveSpeed:
                self.kill()
                return
            
            newY = lerp(0, -self.rect.h, self.current / itemHintMoveSpeed)
            self.rect.topright = (state.screensize[0], newY)
            self.current += 1


class Pickup(pygame.sprite.Sprite):
    def __init__(self, sprite, type, position, hint = None):
        pygame.sprite.Sprite.__init__(self)

        self.type = type
        self.position = pygame.Vector2(position)
        
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.bottomright = (0, 0) # shove that thing off screen until the camera's initialized, amirite?
        self.hint = hint

    def update(self, state):
        newpos = self.position.copy()
        newpos.y += pickupSinScale * math.sin(pygame.time.get_ticks() * 0.004)
        self.rect.center = newpos + state.camera

    def interact(self, state, _):
        state.player.pickup_item(self.type)
        self.kill()

        state.RESOURCES.SND_PICKUP_ITEM.play()

        if self.hint != None:
            hintobj = ItemHint(self.hint, 240)
            state.renderLayers.add_to("Character", hintobj) # Character layer on top, so why not right