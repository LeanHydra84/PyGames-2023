import pygame
from collections import namedtuple

layertype = namedtuple("Layer", "layer name doupdate")

# Add support for update() function
"""
This seems super easy, right?
Just iterate over the layers and call update().
Problem: Some layers dont need to update (Map),
but much more pressingly some layers have to be updated in a different order
than they're drawn.

Mainly, the feet have to be drawn behind the playermodel.
However, the feet position depends on the position of the character,
which is set in update(). So the feet have to update() after the character,
but be drawn before. Mehhhhh. Damn.
"""

class LayerManager:
    def __init__(self):
        self.layers : list[layertype] = []

    def add(self, group: pygame.sprite.Group, name: str, doUpdate: bool = False):
        self.layers.append( layertype(group, name, doUpdate) )
        return group

    def add_new(self, name: str, doUpdate: bool = False):
        newgroup = pygame.sprite.Group()
        self.layers.append( layertype( newgroup, name, doUpdate ) )
        return newgroup

    def add_to(self, name: str, obj: pygame.sprite.Sprite):
        group = self.find(name)
        if group == None:
            group = self.add_new(name)
        obj.add(group.layer)

    def remove(self, groupname: str):
        self.layers = list(filter(lambda x: x[1] != groupname, self.layers))

    def remove(self, group: pygame.sprite.Group):
        self.layers = list(filter(lambda x: x[0] != group, self.layers))

    def find(self, name: str):
        for x in self.layers:
            if x.name == name:
                return x
        return None

    def render(self, screen):
        for l in self.layers:
            l.layer.draw(screen)

    def update(self, state):
        for layer in self.layers:
            if layer.doupdate:
                layer.layer.update(state)