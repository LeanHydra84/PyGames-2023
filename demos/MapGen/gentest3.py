import pygame

decreasedHallwayMapSize = (50, 50)

def segment(surf, pos, dir):

    pygame.draw.line(surf, pygame.Color(255, 255, 255), pos)

    pass

def createmap(group):
    
    dhLeft = (20, 25)
    dhRight = (30, 25)

    onepixelsegment = pygame.Surface(decreasedHallwayMapSize)
    onepixelsegment.fill(pygame.Color(0, 0, 0))
    segment(onepixelsegment, dhLeft, (-1, 0))
    segment(onepixelsegment, dhRight, (1, 0))


    return onepixelsegment