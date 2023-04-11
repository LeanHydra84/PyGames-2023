import pygame.color as col

class HueShift:
    def __init__(self, startColor = col.Color(255, 0, 0), shiftspeed = 10):
        self.clr = startColor
        self.shiftspeed = shiftspeed

    def update(self):
        listify = list(self.clr.hsva)
        listify[0] += self.shiftspeed
        self.clr.hsva = tuple(listify)

    def color(self):
        return self.clr