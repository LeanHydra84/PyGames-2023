import pygame
import random as rand


scale = 5
sqrsize = 25
static_color = pygame.Color(200, 35, 10)

grid = (1280, 720)

test_room_wh = [
    (1, 1),
    (2, 2),
    (1, 2),
    (2, 1),
    (2, 3),
]

edgedamp = 0.6

class Room(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)

        #size = (dim[0] * scale * sqrsize, dim[1] * scale * sqrsize)

        center = rect.center
        adjwh = tuple(p * edgedamp for p in rect.size)
        self.rect = pygame.Rect((0, 0), adjwh)
        self.rect.center = center

        self.image = pygame.Surface(self.rect.size)
        self.image.fill(static_color)



def scuffed_tuple_mult(t1: tuple, t2: tuple):
    return tuple(t1[i] * t2[i] for i in range(t1.count()))
        
def placeroom(group, rect):
    newr = Room(rect)
    group.add(newr)

def binarypartition(group, rect: pygame.Rect, depth, draw = False):
    #partition = tuple(p * rand.normalvariate(0.5, 0.1) for p in rand.choice([(0, 1), (1, 0)]))

    if depth > 4:
        print("SIZE REACHED")
        if draw:
            placeroom(group, rect)
        return
    
    drawbit = bool(rand.getrandbits(1))
    percentage = max(min(rand.normalvariate(0.5, 0.15), 1), 0) 
    if rect.w > rect.h: # X
        newWa = rect.w * percentage
        newWb = rect.w - newWa

        newXb = rect.x + newWa

        rectA = pygame.Rect(rect.topleft, (newWa, rect.h))
        rectB = pygame.Rect((newXb, rect.y), (newWa, rect.h))
        
        binarypartition(group, rectA, depth + 1, drawbit)
        binarypartition(group, rectB, depth + 1, not drawbit)

        pass
    else:
        newHa = rect.h * percentage
        newHb = rect.h - newHa

        newYb = rect.y + newHa

        rectA = pygame.Rect(rect.topleft, (rect.w, newHa))
        rectB = pygame.Rect((rect.x, newYb), (rect.w, newHb))

        binarypartition(group, rectA, depth + 1, drawbit)
        binarypartition(group, rectB, depth + 1, not drawbit)


def createmap(spritegroup):

    binarypartition(spritegroup, pygame.Rect((0, 0), grid), 0)

    pass