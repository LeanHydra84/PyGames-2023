import pygame
from rendering.animation_set import AnimationCollection

class GlobalResources:
    def __init__(self, scale):
        self.scale = scale

    def load(self):

        self.PLAYER = AnimationCollection("assets\\player.json", self.scale)
        self.HALLMONITOR = AnimationCollection("assets\\hallmonitor.json", self.scale)
        self.FEET = AnimationCollection("assets\\feet.json", self.scale)
        self.DEADBODY_TESTSPRITE = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\DEBUG_X.png").convert_alpha(), self.scale ) 

        self.SND_PUNCH = pygame.mixer.Sound("assets\\audio\\punch_test.wav")
        self.SND_WHIFF = pygame.mixer.Sound("assets\\audio\\whiff_test.mp3")

        self.SND_PUNCH.set_volume(0.5)
        self.SND_WHIFF.set_volume(0.5)

    def release(self):
        del self.PLAYER
        del self.HALLMONITOR
        del self.FEET