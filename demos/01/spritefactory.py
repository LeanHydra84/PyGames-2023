import pygame as pg
import os

_path_base = ""

class sprite_sheet:
    def __init__(self, sprite, x, y):
        self.image = sprite
        self.cellsWide = x
        self.cellsTall = y

        self.w = sprite.get_width() / x
        self.h = sprite.get_height() / y

    def get_rect(self, x, y):
        return pg.Rect(x * self.w, y * self.h, self.w, self.h)

    def frame(self, x, y):
        image = pg.Surface((self.w, self.h))
        image.blit(self.image, (0, 0), self.get_rect(x, y))
        return image.convert_alpha()
    
    def reframe(self, x, y, image):
        image.blit(self.image, (0, 0), self.get_rect(x, y))
        image.convert_alpha()
    
        
        


def set_resource_location(path):
    global _path_base
    _path_base = path

def import_sprite_static(name):
    path = os.path.join(_path_base, name)
    return pg.image.load(path).convert_alpha()

def import_sprite_sheet(name, x, y):
    print("Here is the path:", _path_base, "!")
    path = os.path.join(_path_base, name)
    return sprite_sheet(pg.image.load(path).convert_alpha(), x, y)
