import capture.capturestate as capturestate
import rendering.textobject as to
import pygame

from rendering.conversations import ConversationPartner

class Textbox(capturestate.CaptureState):
    def __init__(self, state):
        capturestate.CaptureState.__init__(self, state)

        self.convoManger = state.RESOURCES.CONVERSATION

        self.textObject = None
        self.font = state.RESOURCES.FONT_40
        self.group = pygame.sprite.Group()

        self.background = pygame.transform.scale_by(pygame.image.load("assets\\menu\\textbox_border1.png").convert_alpha(), 5)
        self.brRect = self.background.get_rect()
        self.brRect.centerx = state.centerScreen[0]
        self.brRect.bottom = state.screensize[1]

        self.nameBox = to.BasicTextObject(self.font)
        self.group.add(self.nameBox)

        self.headBox = pygame.sprite.Sprite()
        self.group.add(self.headBox)

        self.conversation = None

    def begin_conversation(self, conversation_id):
        convo = self.convoManger.get_conversation(conversation_id)
        self.conversation = iter(convo)
        self.read(next(self.conversation))

    def read(self, line): # INITIALIZES MLWTO FOR DISPLAY. In future: will take a tuple of data: sprite for head, string for text, and color for shading the textbox background
        person: ConversationPartner = self.convoManger.get_partner(line[0])

        # sprite, name, color
        self.nameBox.color = person.color
        self.nameBox.set_text(person.name)


        self.textObject = to.MultilineWritingTextObject(line[1].split('\n'), self.font, 3, person.color)
        self.textObject.rect.center = self.brRect.center
        
        self.headBox.image = person.sprite
        self.headBox.rect = person.sprite.get_rect(centery=self.brRect.centery, right=(self.brRect.left - 10))
        
        self.nameBox.rect.bottom = self.headBox.rect.top
        self.nameBox.rect.centerx = self.headBox.rect.centerx

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
            self.textObject.kill()
            self.get_next()