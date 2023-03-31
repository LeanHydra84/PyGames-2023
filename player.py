import pygame
from character import ImageBase

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet: tuple[ImageBase]):
        pygame.sprite.Sprite.__init__(self)

        # Persistent Data (Sprites that do not change)
        self.sheet = sheet

        # Semi-persistent data (Sprites that may change, but are not drawn and are not unrecoverable)
        self.image_base : pygame.Surface = sheet[0].img

        # Draw Sprites
        self.sheetdim = sheet[0].dimension
        rect : pygame.Rect = sheet[0].img.get_rect()
        self.rect = pygame.Rect(0, 0, rect.w / (self.sheetdim[0] + 1), rect.h / (self.sheetdim[1] + 1))

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)


        # Movement
        self.position = pygame.Vector2()
        self.speed = 1

        # Sprite sheet rendering
        self.frametickspeed = sheet[0].speed
        self.frametick = 0
        self.curframe = [0, 0]

        self.set_active_frame()
    

    def set_active_frame(self):
        self.image.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.rect)
        newRect.x = self.curframe[0] * self.rect.w
        newRect.y = self.curframe[1] * self.rect.h
        self.image.blit(self.image_base, (0, 0), newRect)
        
    def recalculate_imagebase(self, index):
        newimgbase = self.sheet[index]
        self.image_base = newimgbase.img
        self.sheetdim = newimgbase.dimension
        self.frametickspeed = newimgbase.speed
        self.frametick = 0
        self.set_active_frame()

    def increment_frames(self):
        if(self.curframe[0] >= self.sheetdim[0]):
            if self.curframe[1] >= self.sheetdim[1]:
                self.curframe[0] = 0
                self.curframe[1] = 0
            else:
                self.curframe[0] = 0
                self.curframe[1] += 1
        else:
            self.curframe[0] += 1

    def update(self, keys):
        
        group = self.groups()[0]
        if group != None:
            pass
            

        # Animation
        self.frametick += 1
        if self.frametick > self.frametickspeed:
            print("tick")
            self.frametick = 0
            self.increment_frames()
            self.set_active_frame()

        # Movement
        mx = 1 if keys[3] else -1 if keys[1] else 0
        my = 1 if keys[2] else -1 if keys[0] else 0

        if mx != 0 or my != 0:
            mv = pygame.Vector2(mx, my).normalize() * self.speed
            self.position += mv

        # Positioning
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        


        
def createplayer(scale) -> Player:
    img = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\girl1.png").convert_alpha(), scale)
    feet = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\leg1.png").convert_alpha(), scale)

    sheet = ( ImageBase(img, (2, 0), 25), ImageBase(feet, (0, 0), -1) )
    char = Player(sheet)
    char.speed = 1

    return char