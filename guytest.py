import pygame

class Guy(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.image_base = image
        self.rect = image.get_rect()



        self.scale = 1
        self.rotation = 0
        self.position = pygame.Vector2(500, 500)
    
    def update(self):
        self.rotation += 1

        self.image = self.image_base
        defRect = self.image_base.get_rect()

        self.image = pygame.transform.scale(self.image, (defRect.w * self.scale, defRect.h * self.scale))
        self.image = pygame.transform.rotate(self.image, self.rotation)

        # Rotation Correction
        self.rect = self.image.get_rect(center=defRect.center)

        # Positioning
        self.rect.x += self.position.x
        self.rect.y += self.position.y

class SheetGuy(pygame.sprite.Sprite):
    def __init__(self, image, x : int, y : int):
        pygame.sprite.Sprite.__init__(self)

        #self.image = image
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

        self.framesX = x
        self.framesY = y

    def set_active_frame(self):
        self.activeframe.fill(pygame.Color(0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        newRect = pygame.Rect(self.rect)
        newRect.x = self.curframe[0] * self.rect.w
        newRect.y = self.curframe[1] * self.rect.h
        self.activeframe.blit(self.image_base, (0, 0), newRect)
        

    def increment_frames(self):
        if(self.curframe[0] >= self.framesX):
            if self.curframe[1] >= self.framesY:
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