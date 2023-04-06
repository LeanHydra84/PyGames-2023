from rendering.animation_set import AnimationGraph

class GlobalResources:
    def __init__(self, scale):
        self.scale = scale

    def load(self):

        self.PLAYER = AnimationGraph("assets\\player.json", self.scale)
        self.HALLMONITOR = AnimationGraph("assets\\hallmonitor.json", self.scale)
        self.FEET = AnimationGraph("assets\\feet.json", self.scale)

    def release(self):
        del self.PLAYER
        del self.HALLMONITOR
        del self.FEET