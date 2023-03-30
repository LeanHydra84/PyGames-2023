import pygame
import json

# json structure:
'''
image: path to visible image
collider: path to collider image
doors: [] Array of door positions -- coordinate on image where the door pivot exists
'''

room_scale = 1

class Room(pygame.sprite.Sprite):
    def __init__(self, path: str, colliderpath: str):
        low = pygame.image.load(path).convert()
        col = pygame.image.load(colliderpath).convert()
        rect = self.image.get_rect()
        
        self.image = pygame.transform.scale(low, (rect.w * room_scale, rect.h * room_scale))
        self.collider = pygame.transform.scale(col, (rect.w * room_scale, rect.h * room_scale))
        self.rect = self.image.get_rect()


class Map:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.create_rooms()


    def create_rooms(self):
        pass


