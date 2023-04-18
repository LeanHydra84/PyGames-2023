import pygame

from rendering.stategraph import SingleStateGraph

LIFESPAN = 60
class OverlayAnswer(pygame.sprite.Sprite):
    def __init__(self, state, str):
        pygame.sprite.Sprite.__init__(self)
        
        self.image: pygame.Surface = state.RESOURCES.ON_ANSWER.copy()
        
        nameimage = None
        match str:
            case "Hist":
                nameimage = state.RESOURCES.HISTORY
            case "Sci":
                nameimage = state.RESOURCES.SCIENCE
            case "Math":
                nameimage = state.RESOURCES.MATH
        
        if nameimage == None:
            return
        
        self.image.blit(nameimage, (0, 0))
        self.rect = self.image.get_rect(center=state.centerScreen)

        self.framecounter = 0

    def update(self, state):
        self.framecounter += 1
        if self.framecounter > LIFESPAN:
            self.kill()

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

        convo = None
        wincounter = state.answer_count()
        match wincounter:
            case 1:
                convo = "first_answer_get"
            case 2:
                convo = "second_answer_get"
            case 3:
                convo = "third_answer_get"

        state.renderLayers.add_to("Character", OverlayAnswer(state, self.answerType))

        if convo == None:
            return
        
        state.text.begin_conversation(convo)
        state.text.togglecapture()
        state.pause()

    def interact(self, state, ePress):
        if ePress and not self.used:
            self.finish_minigame(state)
            self.used = True
            return True
        return self.used