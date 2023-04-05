import capture.capturestate as capturestate
import capture.textobject as to
import pygame

class Textbox(capturestate.CaptureState):
    def __init__(self, state):
        capturestate.CaptureState.__init__(self, state)
        self.textObject = None
        self.font = pygame.font.SysFont("Arial", 25) # Import font
        self.group = pygame.sprite.GroupSingle()

    def read(self, string): # INITIALIZES MLWTO FOR DISPLAY. In future: will take a tuple of data: sprite for head, string for text, and color for shading the textbox background
        self.textObject = to.MultilineWritingTextObject(string.split('\n'), self.font, 3)
        self.group.add(self.textObject)

    def render(self, screen):
        self.group.draw(screen)

    def update(self):
        self.textObject.update()

    def register_click(self, position):
        if not self.textObject.is_complete():
            self.textObject.force_complete()
        else:
            self.togglecapture()
            self.reference_state.unpause()
            self.textObject.kill()
            self.textObject = None