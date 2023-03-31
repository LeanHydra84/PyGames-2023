import pygame

def create_character():
    img = pygame.image.load("assets\\sprite_sheet_test.png")
    return Character(img, (2, 1))

class Character(pygame.sprite.Sprite):
    def __init__(self, image, sheetDim):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.image_base = image
        self.right = False

        rect = image.get_rect()
        self.rect = pygame.Rect(0, 0, rect.w / (x + 1), rect.h / (y + 1))

        self.scale = 1
        self.rotation = 0
        self.position = pygame.Vector2(500, 500)
        self.frametick = 0
        self.curframe = [0, 0]
        self.activeframe = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.set_active_frame()

        self.sheetDim = sheetDim

    def set_active_frame(self):
        self.activeframe.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.rect)
        newRect.x = self.curframe[0] * self.rect.w
        newRect.y = self.curframe[1] * self.rect.h
        self.activeframe.blit(self.image_base, (0, 0), newRect)
        

    def increment_frames(self):
        if(self.curframe[0] >= self.sheetDim[0]):
            if self.curframe[1] >= self.sheetDim[1]:
                self.curframe[0] = 0
                self.curframe[1] = 0
            else:
                self.curframe[0] = 0
                self.curframe[1] += 1
        else:
            self.curframe[0] += 1

    def update(self):
        self.frametick += 1
        if self.frametick > 25:
            self.frametick = 0
            self.increment_frames()
            self.set_active_frame()

        if self.right:
            self.image = pygame.transform.flip(self.activeframe, True, False)
        else:
            self.image = self.activeframe
            
        self.image = pygame.transform.scale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))

        # Positioning
        self.rect.x = self.position.x
        self.rect.y = self.position.y