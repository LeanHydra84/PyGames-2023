import pygame
import json
import random as rand

import numpy
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

from main import SCREENSIZE

room_scale = 1
json_path = "assets\\rooms\\rooms.json"

def dist(a: list, b: list):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return numpy.sqrt(x*x + y*y)

def get_points_mindist(n, mindist):
    plist = [[rand.randrange(0, SCREENSIZE[0], 25 * room_scale), rand.randrange(0, SCREENSIZE[1], 25 * room_scale)] for p in range(n)]
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
        
        self.image = pygame.transform.scale(low, (rect.w * room_scale, rect.h * room_scale))
        self.collider = pygame.transform.scale(col, (rect.w * room_scale, rect.h * room_scale))
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

        self.rect = self.image.get_rect(topleft=position.coord)



class Map:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.rooms = []

    def placeroom(self, room):
        
        pass

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
            newroom = RoomActual(required[0], pos)
            self.rooms.append(newroom)
            self.group.add(newroom)