import pygame

from rendering.stategraph import SingleStateGraph

class MrFlip(pygame.sprite.Sprite):
    def __init__(self, sheet, position):
        pygame.sprite.Sprite.__init__(self)

        self.graph = SingleStateGraph(sheet, [2, 0], 25)
        self.position = position
        self.interaction_count = 0

        self.image = self.graph.activeFrame
        self.rect = self.image.get_rect(bottomright=(0, 0))

    def update(self, state):
        self.graph.tick()

        self.image = self.graph.activeFrame
        self.rect = self.image.get_rect(center=self.position + state.camera)

        if self.interaction_count == 0:
            self.interact(state, True)

    def converse_script(self, state):
        script = "in_game_neutral"

        if state.win_condition():
            script = "on_win"
            state.winGame = True
        if self.interaction_count == 0:
            script = "startgame"
        if self.interaction_count == 1:
            script = "in_game_hint"

        state.text.begin_conversation(script)
        state.text.togglecapture()
        state.pause()
        self.interaction_count += 1

    def interact(self, state, shouldInteract):
        if shouldInteract:
            self.converse_script(state)
        return False