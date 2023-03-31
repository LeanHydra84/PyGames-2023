import pygame
from collections import namedtuple

ImageBase = namedtuple('ImageBase', 'img dimension speed')

class Character(pygame.sprite.Sprite):
    def __init__(self, sheets: tuple[ImageBase]):
        pygame.sprite.Sprite.__init__(self)

        image = sheets[0].img
        self.sheetDim = sheets[0].dimension
        self.frametickspeed = sheets[0].speed

        self.image = image
        self.sheet = sheets
        self.image_base = image
        self.right = False

        rect = image.get_rect()
        self.rect = pygame.Rect(0, 0, rect.w / (self.sheetDim[0] + 1), rect.h / (self.sheetDim[1] + 1))

        self.speed = 1
        self.moving = False
        self.position = pygame.Vector2(500, 500)
        self.frametick = 0
        self.curframe = [0, 0]
        self.activeframe = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        self.set_active_frame()


    def set_active_frame(self):
        self.activeframe.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.rect)
        newRect.x = self.curframe[0] * self.rect.w
        newRect.y = self.curframe[1] * self.rect.h
        self.activeframe.blit(self.image_base, (0, 0), newRect)
        
    def recalculate_imagebase(self):
        newimgbase = self.sheet[1 if self.moving else 0]
        self.image_base = newimgbase.img
        self.sheetDim = newimgbase.dimension
        self.frametickspeed = newimgbase.speed
        self.frametick = 0
        self.set_active_frame()

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

    def update(self, movement, room):

        # Animation
        self.frametick += 1
        if self.frametick > self.frametickspeed:
            self.frametick = 0
            self.increment_frames()
            self.set_active_frame()

        # Direction
        if self.right:
            self.image = pygame.transform.flip(self.activeframe, True, False)
        else:
            self.image = self.activeframe

        #self.image = pygame.transform.scale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))

        # Movement

        mx = 1 if movement[3] else -1 if movement[1] else 0
        my = 1 if movement[2] else -1 if movement[0] else 0

        if mx != 0 or my != 0:
            mv = pygame.Vector2(mx, my).normalize() * self.speed
            self.position += mv
            if self.moving != True:
                self.moving = True
                self.recalculate_imagebase()
        else:
            if self.moving != False:
                self.moving = False
                self.recalculate_imagebase()
            
        if mx > 0:
            self.right = True
        elif mx < 0:
            self.right = False

        # Positioning
        self.rect.x = self.position.x
        self.rect.y = self.position.y

def create_character(scale: float) -> Character:
    idle = pygame.transform.scale_by(pygame.image.load("assets\\sprite_sheet_test.png").convert_alpha(), scale)
    walk = pygame.transform.scale_by(pygame.image.load("assets\\walking_sprite.png").convert_alpha(), scale)

    sheets = ( ImageBase(idle, (1, 0), 25), ImageBase(walk, (1, 0), 15) )

    character = Character(sheets)
    character.speed = 4

    return character