import pygame
import feet
import math

from character import ImageBase

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet: tuple[ImageBase]):
        pygame.sprite.Sprite.__init__(self)

        # Persistent Data (Sprites that do not change)
        self.sheet = sheet

        # Semi-persistent data (Sprites that may change, but are not drawn and are not unrecoverable)
        self.image_base : pygame.Surface = sheet[0].img
        self.feet = feet.Feet(self, sheet[1])

        # Draw Sprites
        self.sheetdim = sheet[0].dimension
        rect : pygame.Rect = sheet[0].img.get_rect()
        self.trueRect = pygame.Rect(0, 0, rect.w / (self.sheetdim[0] + 1), rect.h / (self.sheetdim[1] + 1))
        self.rect = self.trueRect

        self.activeFrame = pygame.Surface(self.trueRect.size, pygame.SRCALPHA)
        self.image = self.activeFrame

        # Movement
        self.position = pygame.Vector2()
        self.rotation = 0
        self.speed = 1
        self.moving = False

        # Sprite sheet rendering
        self.frametickspeed = sheet[0].speed
        self.frametick = 0
        self.curframe = [0, 0]

        self.set_active_frame()
    

    def set_active_frame(self):
        self.activeFrame.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.trueRect)
        newRect.x = self.curframe[0] * self.trueRect.w
        newRect.y = self.curframe[1] * self.trueRect.h
        self.activeFrame.blit(self.image_base, (0, 0), newRect)
        
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

    def update(self, keys, mousepos : pygame.Vector2):
        
        self.rotation = -(mousepos - self.position).as_polar()[1]
        self.image = pygame.transform.rotate(self.activeFrame, self.rotation)
        self.rect = self.image.get_rect()

        # Animation
        self.frametick += 1
        if self.frametick > self.frametickspeed:
            self.frametick = 0
            self.increment_frames()
            self.set_active_frame()

        # Movement
        mx = 1 if keys[3] else -1 if keys[1] else 0
        my = 1 if keys[2] else -1 if keys[0] else 0

        if mx != 0 or my != 0:
            mv = pygame.Vector2(mx, my).normalize() * self.speed
            self.position += mv

            if self.moving == False:
                #self.feet.add(self.groups()[0])
                self.feet.visible = True
            self.moving = True
        else:
            if self.moving == True:
                #self.feet.kill()
                self.feet.visible = False
            self.moving = False

        # Positioning
        self.rect.center = self.position
        self.feet.update()
        


        
def createplayer(scale) -> Player:
    img = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\girl1.png").convert_alpha(), scale)
    feet = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\leg2.png").convert_alpha(), scale / 1.5)

    sheet = ( ImageBase(img, (2, 0), 25), ImageBase(feet, (0, 0), 21) )
    char = Player(sheet)
    char.speed = 1

    return char