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

    def increment_frames(self):
        if(self.curframe[0] >= self.sheetdim[0]):
            if self.curframe[1] >= self.sheetdim[1]:
                self.curframe[0] = 0
                self.curframe[1] = 0
                # On animation complete
                # Check if state should recalc
                if self.transfergraph[self._state] != self._state:
                    self.force_state(self.transfergraph[self._state])
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
        
def check_collider(room, point: list[int]) -> bool:

    for col in room:
        collider = col.collider
        colrect = col.rect
        adjP = (point[0] - colrect.x, point[1] - colrect.y)
        if adjP[0] < colrect.w and adjP[0] >= 0 and adjP[1] < colrect.h and adjP[1] >= 0:
            if collider.get_at(adjP).r != 255:
                return False
    return True