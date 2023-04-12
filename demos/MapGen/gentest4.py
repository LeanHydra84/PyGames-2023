import pygame
import json

import random
#from random import choice

rooms = []
hallways = []

SCALE = 5

def readalltext(fpath):
    file = open(fpath)
    text = file.read()
    file.close()
    return text

class HALLWAY:
    def __init__(self, obj):
        self.name = obj['name']
        
        self.image = pygame.transform.scale_by(pygame.image.load(obj['path']).convert_alpha(), SCALE)
        self.collider = pygame.transform.scale_by(pygame.image.load(obj['collider']).convert(), SCALE)
        self.exits = obj['exits']

class ROOMGEN:
    def __init__(self):
        decoder = json.decoder.JSONDecoder()
        
        hwJSON = readalltext("assets\\R2\\hallways.json")
        hallwaysobject = decoder.decode(hwJSON)

        self.hallways = [HALLWAY(p) for p in hallwaysobject if "disabled" not in p]

        rmJSON = readalltext("assets\\R2\\rooms.json")
        roomsObject = decoder.decode(rmJSON)

        self.rooms = [HALLWAY(p) for p in roomsObject]

    def find_hallway(self, name) -> HALLWAY:
        return [p for p in self.hallways if p.name == name][0]
    
    def get_hallway(self) -> HALLWAY:
        return random.choice(self.hallways)
    
    def get_room(self):
        pass

    def find_room(self, name):
        return [p for p in self.rooms if p.name == name][0]
    
    def get_end_cap(self):
        return self.find_room("Dead End")

class HallwayActual(pygame.sprite.Sprite):
    def __init__(self, image, collider, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.collider = collider

        self.position = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=pos)

    def update(self, state):
        self.rect.center = self.position + state.camera

        
class BuildDetails:
    def __init__(self, group):
        self.uncappedEnds = 0
        self.deadEndPos = []
        self.group = group

def rotate_90(coord: list):
    # Clockwise rotation: [x, y] ==> [y, -x]
    temp = coord[0]
    coord[0] = coord[1]
    coord[1] = -temp


def tuple_multiply(t1, t2):
    return tuple(t1[i] * t2[i] for i in range(len(t1)))

def tuple_sum(t1, t2):
    return tuple(t1[i] + t2[i] for i in range(len(t1)))

def multipy_tuple_then_sum(t1, t2):
    return sum(tuple_multiply(t1, t2))

# SOOOOOO MUCH DUPLICATE AND DISGUSTING CODE HERE!!!!!!! I NEED TO FIX THAT!!!

def place_dead_end(details: BuildDetails, resource, pos, direction):
    nextr = resource.get_end_cap()

    chosenExit = nextr.exits[0].copy()
    revDirection = [-direction[0], -direction[1]]

    orientationCounter = 0
    while orientationCounter < 4:
        
        if chosenExit == revDirection:
            break
        else:
            orientationCounter += 1
            rotate_90(chosenExit)

    IMAGE = pygame.transform.rotate(nextr.image, orientationCounter * 90)
    COLLIDER = pygame.transform.rotate(nextr.collider, orientationCounter * 90)

    scalar = abs(multipy_tuple_then_sum(IMAGE.get_rect().size, direction))
    posDelta = pygame.Vector2(direction) * scalar * 0.5
    hw = HallwayActual(IMAGE, COLLIDER, posDelta + pos)

    details.group.add(hw)
    details.deadEndPos.append(hw.rect.center)
    details.uncappedEnds -= 1


def _recurse_add_room(details: BuildDetails, resource, pos, direction, depth):
    if depth <= 0:
        place_dead_end(details, resource, pos, direction)
        return

    nextr: HALLWAY = resource.get_hallway()

    _exits: list = [p.copy() for p in nextr.exits]
    chosenexit = random.choice(_exits)
    _exits.remove(chosenexit)
    

    revDirection = [-direction[0], -direction[1]]

    # Rotate Room To Correct Orientation ==> [chosenexit == revDirection]

    orientationCounter = 0
    while orientationCounter < 4:
        
        if chosenexit == revDirection:
            break
        else:
            orientationCounter += 1
            rotate_90(chosenexit)
        
    assert(orientationCounter < 4)

    IMAGE = pygame.transform.rotate(nextr.image, orientationCounter * 90)
    COLLIDER = pygame.transform.rotate(nextr.collider, orientationCounter * 90)

    # ALIGN NEW ROOM (x, y) ENTRANCE WITH CURRENT EXIT

    scalar = abs(multipy_tuple_then_sum(IMAGE.get_rect().size, direction))
    posDelta = pygame.Vector2(direction) * scalar * 0.5

    hw = HallwayActual(IMAGE, COLLIDER, posDelta + pos)

    if len(pygame.sprite.spritecollide(hw, details.group, False)) > 0:
        place_dead_end(details, resource, pos, direction)
        return

    details.group.add(hw)

    # Rotate each exit from _exits to match orientation,
    for d in _exits:
        for i in range(orientationCounter):
            rotate_90(d)

        add = tuple_multiply(hw.rect.size, d)
        add = tuple(p * 0.5 for p in add)
        newPos = tuple_sum(hw.rect.center, add)

        #pygame.draw.circle(main.DEBUGSCREEN, pygame.Color(255, 0, 0), newPos, 25)
        
        details.uncappedEnds += 1
        _recurse_add_room(details, resource, newPos, d, depth - 1)

class Mapv2:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.details = BuildDetails(self.group)
        #self.rooms = []

    def get_collision_at_point(self, point) -> bool:
        for x in self.group:
            if x.rect.collidepoint(point):
                col: pygame.Surface = x.collider
                color = col.get_at( (int(point.x - x.rect.x), int(point.y - x.rect.y)) )
                if color.r == 255:
                    return True
                return False
        return True

    def get_inside(self, sprite : pygame.sprite.Sprite):
        collist = pygame.sprite.spritecollide(sprite, self.group, False)
        if len(collist) > 0:
            return collist
        return None


def createmap(depth):
    #random.seed(50)
    resource = ROOMGEN()
    nmap = Mapv2()

    _recurse_add_room(nmap.details, resource, (1280/2, 720/2), (-1, 0), depth)

    return nmap

