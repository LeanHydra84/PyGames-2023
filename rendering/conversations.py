import pygame.image
import json

from collections import namedtuple

ConversationPartner = namedtuple("ConversationPartner", "sprite name color")

class ConversationManager:
    def __init__(self, jsonpath):
        decoder = json.decoder.JSONDecoder()

        file = open(jsonpath)
        jsontext = file.read()
        file.close()

        obj = decoder.decode(jsontext)

        self.manifest = {}
        for man in obj['manifest']:
            handle = man['handle']
            path = man['path']

            name = man['name']
            color = pygame.Color(man['color'])
            sprite = pygame.image.load(path).convert()

            self.manifest[handle] = ConversationPartner(sprite, name, color)

        self.conversations = obj['conversations']

    def get_conversation(self, convHandle):
        return self.conversations[convHandle]
    
    def get_partner(self, partnerHandle):
        return self.manifest[partnerHandle]

        