from rendering.animation_set import AnimationCollection

class GlobalResources:
    def __init__(self, scale):
        self.scale = scale

    def load(self):

        self.PLAYER = AnimationCollection("assets\\player.json", self.scale)
        self.HALLMONITOR = AnimationCollection("assets\\hallmonitor.json", self.scale)
        self.FEET = AnimationCollection("assets\\feet.json", self.scale)

    def release(self):
        del self.PLAYER
        del self.HALLMONITOR
        del self.FEET