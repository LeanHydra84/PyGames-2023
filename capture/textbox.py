import capture.capturestate as capturestate
import capture.textobject as to
import pygame

class Textbox(capturestate.CaptureState):
    def __init__(self, state):
        capturestate.CaptureState.__init__(self, state)
        self.textObject = None
        self.font = pygame.font.SysFont("Arial", 40) # Import font
        self.group = pygame.sprite.GroupSingle()

        self.background = pygame.transform.scale_by(pygame.image.load("assets\\menu_test\\textbox_border.png").convert_alpha(), 15)
        self.brRect = self.background.get_rect()
        self.brRect.centerx = state.centerScreen[0]
        self.brRect.bottom = state.screensize[1]

        self.conversation = None

    def begin_conversation(self, conversation):
        self.conversation = iter(conversation)
        self.read(next(self.conversation))

    def read(self, string): # INITIALIZES MLWTO FOR DISPLAY. In future: will take a tuple of data: sprite for head, string for text, and color for shading the textbox background
        self.textObject = to.MultilineWritingTextObject(string.split('\n'), self.font, 3, pygame.Color(0, 0, 0))
        self.textObject.rect.center = self.brRect.center
        self.group.add(self.textObject)

    def render(self, screen: pygame.Surface):
        screen.blit(self.background, self.brRect.topleft)
        self.group.draw(screen)

    def update(self):
        self.textObject.update()

    def end_text(self):
        self.conversation = None
        self.togglecapture()
        self.reference_state.unpause()
        self.textObject.kill()
        self.textObject = None

    def get_next(self):
        if self.conversation == None:
            self.end_text()
            return
        
        try:
            nxt = next(self.conversation)
            self.read(nxt)
        except StopIteration:
            self.end_text()
            

    def register_click(self, _):
        if not self.textObject.is_complete():
            self.textObject.force_complete()
        else:
            self.get_next()