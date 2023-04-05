import pygame

class BasicTextObject(pygame.sprite.Sprite):
    def __init__(self, text: str, font: pygame.font.Font, color = pygame.Color(255, 255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.text = text
        self.font = font

        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()


class SingleLineWritingTextObject(pygame.sprite.Sprite):
    def __init__(self, text: str, font: pygame.font.Font, framedelta = 10, color = pygame.Color(255, 255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.framedelta = framedelta
        self.framecounter = 0
        self.letter = 0

        self.font = font
        self.text = text

        self.callback = None
        self.color = color

        self.recalculate_surface()

    def recalculate_surface(self):
        self.image = self.font.render(self.text[:self.letter], True, self.color)
        self.rect = self.image.get_rect()

    def is_complete(self) -> bool:
        return len(self.text) == self.letter
    
    def force_complete(self):
        self.letter = len(self.text)
        self.recalculate_surface()

    def update(self):
        if self.is_complete():
            return

        self.framecounter += 1
        if self.framecounter >= self.framedelta:
            self.letter += 1
            self.framecounter = 0
            self.recalculate_surface()

            if len(self.text) - 1 == self.letter and self.callback != None:
                self.callback()

class MultilineWritingTextObject(pygame.sprite.Sprite):
    def __init__(self, text: list[str], font: pygame.font.Font, framedelta = 10, color = pygame.Color(255, 255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.text = text
        self.font = font
        self.color = color

        self._surfArr: list[pygame.Surface] = [None for i in text]
        self.callback = None

        self.framedelta = framedelta
        self.framecount = 0
        self.line = 0
        self.letter = 0

        self.image = pygame.Surface(self.calc_dimension(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def is_complete(self):
        return self.line >= len(self.text)
    
    def force_complete(self):
        for i in range(len(self.text)):
            self._surfArr[i] = self.font.render(self.text[i], True, self.color)
        self.compile()
        self.line = len(self.text)

    def set_position(self, position):
        self.rect.topleft = position

    def compile(self):
        self.image.fill((0, 0, 0, 0))

        height = self.font.get_height()
        counter = 0

        for surf in self._surfArr:
            if surf == None:
                counter += 1
                continue
            self.image.blit(surf, (0, counter * height))
            counter += 1

    def recalculate_line(self, line: int):
        if line > len(self.text):
            return
        
        newtext = (self.text[line])[:self.letter]
        self._surfArr[line] = self.font.render(newtext, True, self.color)

    def calc_dimension(self):
        x = 0
        y = 0
        for string in self.text:
            individualsize = self.font.size(string)
            x = max(individualsize[0], x)
            y += individualsize[1]
        return (x, y)

    def update(self):
        if self.is_complete():
            return
        
        self.framecount += 1
        if self.framecount >= self.framedelta:
            self.framecount = 0
            self.letter += 1
            if self.letter > len(self.text[self.line]):
                self.line += 1
                self.letter = 0
            else:
                self.recalculate_line(self.line)
            
            self.compile()

            if self.is_complete():
                self.callback()



def create_static_text_object(string):
    font = pygame.font.SysFont("Arial", 25)
    txt = BasicTextObject(string, font)
    return txt

def create_writing_text_object(string, framespeed):
    font = pygame.font.SysFont("Arial", 25)
    txt = SingleLineWritingTextObject(string, font, framespeed)
    txt.callback = lambda: print("Cum")
    return txt

def create_multiline_writing_text_object(string, framespeed):
    font = pygame.font.SysFont("Arial", 25)
    strings = string.split("\n")
    txt = MultilineWritingTextObject(strings, font, framespeed)
    return txt