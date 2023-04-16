import pygame

from rendering.stategraph import StateGraph

class MrsFlips(pygame.sprite.Sprite):
    def __init__(self, animationset, position):
        pygame.sprite.Sprite.__init__(self)

        self.graph = StateGraph(animationset)
        self.position = position

    def update(self, state):

        self.graph.tick()

        self.image = self.graph.activeFrame
        self.rect = self.image.get_rect(center=self.position + state.camera)

    def interact(self, state, shouldInteract):
        if shouldInteract:
            state.text.begin_conversation(["Here is some\nepic text for you to read", "And here is some extra more\ntext for you to read like a big boy.", "Finally, here is last text"])
            state.text.togglecapture()
            state.pause()