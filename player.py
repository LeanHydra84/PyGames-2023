import pygame
import feet
import math

from character import ImageBase

class StateGraph:
    def __init__(self, sheets):

        self.sheet = sheets
        self.states : list[ImageBase] = []
        self.transfergraph = []

        self._state = 0

        # TEST CODE

        self.states.append(sheets[0])
        self.states.append(sheets[2])

        self.transfergraph.append(0)
        self.transfergraph.append(0)

        # END TEST CODE

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
        
def check_collider(collider: pygame.Surface, point: list[int]) -> bool:

    colrect = collider.get_rect()
    if point[0] < colrect.w and point[0] >= 0 and point[1] < colrect.h and point[1] >= 0:
        if collider.get_at(point) == pygame.Color(255, 255, 255, 255):
            return True
        return False
    return True
    

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet: tuple[ImageBase]):
        pygame.sprite.Sprite.__init__(self)

        # Persistent Data (Sprites that do not change)
        self.sheet = sheet
        self.stategraph = StateGraph(sheet)
        self.feet = feet.Feet(self, sheet[1])

        # Sprite draw data -- NOT PERSISTENT --
        self.image : pygame.Surface = None
        self.rect : pygame.Rect = None

        # Movement
        self.position = pygame.Vector2()
        self.rotation = 0
        self.speed = 1
        self.moving = False

    def attack_pressed(self):
        if self.stategraph.state() == 0:
            self.stategraph.force_state(1)

    def update(self, keys, mousepos : pygame.Vector2, map):
        
        # Animation
        self.stategraph.tick()

        # Set Image

        self.rotation = -(mousepos - self.position).as_polar()[1]
        self.image = pygame.transform.rotate(self.stategraph.activeFrame, self.rotation)
        self.rect = self.image.get_rect(center=self.position)

        # Movement
        mx = 1 if keys[3] else -1 if keys[1] else 0
        my = 1 if keys[2] else -1 if keys[0] else 0

        if mx != 0 or my != 0:
            mv = pygame.Vector2(mx, my).normalize() * self.speed
            if keys[4]:
                mv *= 1.7

            room = map.get_inside(self)
            if room != None:
                collider : pygame.Surface = room.collider
                pixelindex = [int(self.position.x + mv.x - room.rect.x), int(self.position.y + mv.y - room.rect.y)]
                colrect = collider.get_rect()

                if check_collider(collider, pixelindex):
                    self.position += mv
                elif check_collider(collider, [int(self.position.x + mv.x - room.rect.x), int(self.position.y - room.rect.y)]):
                    self.position.x += mv.x
                elif check_collider(collider, [int(self.position.x - room.rect.x), int(self.position.y + mv.y - room.rect.y)]):
                    self.position.y += mv.y

            else:
                self.position += mv

            if self.moving == False:
                #self.feet.add(self.groups()[0])
                self.feet.set_visible(True)
            self.moving = True
        else:
            if self.moving == True:
                #self.feet.kill()
                self.feet.set_visible(False)
            self.moving = False

        # Positioning
        self.rect.center = self.position
        self.feet.update()
        


        
def createplayer(scale) -> Player:
    img = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\girl1.png").convert_alpha(), scale)
    attack = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\attack.png").convert_alpha(), scale)
    feet = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\leg2.png").convert_alpha(), scale / 1.5)

    sheet = ( ImageBase(img, (2, 0), 25), ImageBase(feet, (0, 0), 21), ImageBase(attack, (3, 0), 2) )
    char = Player(sheet)
    char.speed = 3
    char.position = pygame.Vector2(500, 500)

    return char