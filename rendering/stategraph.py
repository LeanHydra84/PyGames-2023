import pygame
import rendering.animation_set
from rendering.animation_set import ImageBase

# Consider optimizing the frames using SubSurfaces instead of blit copies

class StateGraph:
    def __init__(self, animationset: rendering.animation_set.AnimationCollection):

        self.states:  list[ImageBase] = animationset.states
        self.transfergraph: list[int] = animationset.transitions

        self._state = 0
        self.curframe = [0, 0]
        self.frametick = 0
        self.idle = 0
        self.setup_surface()
        self.calculate_active_frame()

    def setup_surface(self):
        dim = self.states[self._state].dimension
        rect = self.states[self._state].img.get_rect()

        self.sheetdim = dim
        self.frametickspeed = self.states[self._state].speed
        self.rect = pygame.Rect(0, 0, rect.w / (dim[0] + 1), rect.h / (dim[1] + 1))

        self.activeFrame = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def state(self):
        return self._state

    # Change state, recalculate size of activeFrame surface, etc
    def force_state(self, state: int):
        self._state = state

        self.curframe = [0, 0]
        self.frametick = 0
        
        self.setup_surface()
        self.calculate_active_frame()
        

    def calculate_active_frame(self):
        self.activeFrame.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.rect)
        newRect.x = self.curframe[0] * self.rect.w
        newRect.y = self.curframe[1] * self.rect.h
        self.activeFrame.blit(self.states[self._state].img, (0, 0), newRect)

    def set_idle(self, val):
        self.idle = val

    def is_idle(self) -> bool:
        return self._state == self.idle

    def increment_frames(self):
        if(self.curframe[0] >= self.sheetdim[0]):
            if self.curframe[1] >= self.sheetdim[1]:
                self.curframe[0] = 0
                self.curframe[1] = 0
                # On animation complete
                # Check if state should recalc
                if self.transfergraph[self._state] != self._state:
                    transferstate = self.transfergraph[self._state]
                    if transferstate == "Idle":
                        transferstate = self.idle
                    self.force_state(transferstate)
            else:
                self.curframe[0] = 0
                self.curframe[1] += 1
        else:
            self.curframe[0] += 1

    def tick(self):
        self.frametick += 1
        if self.frametick > self.frametickspeed:
            self.frametick = 0
            self.increment_frames()
            self.calculate_active_frame()


class SingleStateGraph:
    def __init__(self, image, dimensions, speed):
        self.sheet = image
        self.dimensions = dimensions
        
        self.frameTimer = speed
        self.curframe = [0, 0]
        self.frametick = 0

        sheetrect = self.sheet.get_rect()
        self.rect = pygame.Rect((0, 0), (sheetrect.w / (self.dimensions[0] + 1), sheetrect.h / (self.dimensions[1] + 1)))

        self.activeFrame = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.calculate_active_frame()


    def calculate_active_frame(self):
        self.activeFrame.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.rect)
        newRect.x = self.curframe[0] * self.rect.w
        newRect.y = self.curframe[1] * self.rect.h
        self.activeFrame.blit(self.sheet, (0, 0), newRect)

    def increment_frame(self):
        if(self.curframe[0] >= self.dimensions[0]):
            if self.curframe[1] >= self.dimensions[1]:
                self.curframe[0] = 0
                self.curframe[1] = 0
            else:
                self.curframe[0] = 0
                self.curframe[1] += 1
        else:
            self.curframe[0] += 1

    def tick(self):
        self.frametick += 1
        if self.frametick > self.frameTimer:
            self.frametick = 0
            self.increment_frame()
            self.calculate_active_frame()