import pygame
import json
import random as rand

import numpy
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

room_scale = 1
json_path = "assets\\rooms\\rooms.json"

def dist(a: list, b: list):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return numpy.sqrt(x*x + y*y)

def get_points_mindist(n, mindist):
    plist = [[rand.randrange(0, 1280, 25 * room_scale), rand.randrange(0, 720, 25 * room_scale)] for p in range(n)]
    return numpy.array([p for p in plist if all(dist(p, x) > mindist for x in plist if x != p)])

def delauneytest(n, nmin, mindist):
    array = get_points_mindist(n, mindist)
    while len(array) < nmin:
        array = get_points_mindist(n, mindist)
    
    tri = Delaunay(array)
    plt.triplot(array[:,0], array[:,1], tri.simplices)
    plt.plot(array[:,0], array[:,1], 'o')
    plt.show()

# json structure:
'''
image: path to visible image
collider: path to collider image
doors: [] Array of door positions -- coordinate on image where the door pivot exists
items: [] Array of item objects, with positions, types, and chance of showing up. Chances of 1 will always show up
'''

def read_json(jsonpath):
    decoder = json.decoder.JSONDecoder()
    file = open(jsonpath)
    text = file.read()
    file.close()
    return decoder.decode(text)

class RoomArchetype:
    def __init__(self, roomdetails):
        low = pygame.image.load(roomdetails["image"]).convert()
        col = pygame.image.load(roomdetails["collider"]).convert()
        rect = low.get_rect()
        
        self.image = pygame.transform.scale_by(low, room_scale)
        self.collider = pygame.transform.scale_by(col, room_scale)
        self.rect = self.image.get_rect()

        
class PositioningInfo:
    def __init__(self, coord: tuple[float], rotationState) -> None:
        self.coord = coord
        self.rotationState = rotationState
        

class RoomActual(pygame.sprite.Sprite):
    def __init__(self, archetype: RoomArchetype, position: PositioningInfo):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.rotate(archetype.image, 90 * position.rotationState)
        self.collider = pygame.transform.rotate(archetype.collider, 90 * position.rotationState)
        
        # Doors, pickups, etc.

        self.position: pygame.Vector2 = position.coord
        self.rect = self.image.get_rect(topleft=position.coord)

    def update(self, state):
        self.rect.topleft = self.position + state.camera
        pass
        #self.rect.topleft = self.position - state.camPos


class Map:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.rooms = []

    def placeroom(self, room):
        
        pass

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

    def create_rooms(self):
        roomCollection = read_json(json_path)
        required = [RoomArchetype(p) for p in roomCollection["requiredrooms"]]
        hallways = [RoomArchetype(p) for p in roomCollection["connector_rooms"]]

        plist = get_points_mindist(5, 25)
        #delaunay = Delaunay(plist)
        #print(delaunay.simplices)

        cur = None
        for p in plist:
            pos = PositioningInfo((p[0], p[1]), rand.randrange(0, 4, 1))
            newroom = RoomActual(rand.choice(required), pos)
            self.rooms.append(newroom)
            self.group.add(newroom)