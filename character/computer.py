import pygame

from rendering.stategraph import SingleStateGraph

class Computer(pygame.sprite.Sprite):
    def __init__(self, sprite, offsprite, pos, answerType):
        pygame.sprite.Sprite.__init__(self)
        
        self.graph = SingleStateGraph(sprite, [2, 0], 20)
        self.offsprite = offsprite

        self.position = pos
        self.answerType = answerType

        self.used = False

        self.image = self.graph.activeFrame
        self.rect = self.image.get_rect(bottomright=(0, 0))

        
        
    def update(self, state):
        if not self.used:
            self.graph.tick()
            self.image = self.graph.activeFrame
        else:
            self.image = self.offsprite
        self.rect = self.image.get_rect(center=(self.position + state.camera))

    def finish_minigame(self, state):
        state.get_answer(self.answerType)
        layer: pygame.sprite.Group = state.renderLayers.find("Enemies").layer
        layer.empty()

        state.map.details.spawnIndex += 1
        state.map.spawn_all(state, True)

    def interact(self, state, ePress):
        if ePress and not self.used:
            self.finish_minigame(state)
            self.used = True