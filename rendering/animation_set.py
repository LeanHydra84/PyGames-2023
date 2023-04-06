import pygame
import json
from collections import namedtuple

ImageBase = namedtuple('ImageBase', 'img dimension speed')

class AnimationGraph:
    def __init__(self, jsonPath: str, scale: float):
        decoder = json.decoder.JSONDecoder()

        file = open(jsonPath)
        jdata = file.read()
        file.close()

        obj = decoder.decode(jdata)

        self.states: list[ImageBase] = []
        self.transitions: list[int] = []

        for i in obj:
            img = pygame.transform.scale_by(pygame.image.load(i['path']).convert_alpha(), scale)
            dim = i['dim']
            speed = i['frames']

            self.states.append(ImageBase(img, dim, speed))
            self.transitions.append(i['transition'])
