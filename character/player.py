import pygame
import rendering.stategraph as graph
import character.feet as feet



class Player(pygame.sprite.Sprite):
    def __init__(self, sheet: tuple[graph.ImageBase]):
        pygame.sprite.Sprite.__init__(self)

        # Persistent Data References
        self.sheet = sheet
        self.stategraph = graph.StateGraph(sheet)
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

    def update(self, state, mousepos : pygame.Vector2, map):
        
        # Animation
        self.stategraph.tick()

        # Set Image

        self.rotation = -(mousepos - self.position).as_polar()[1]
        self.image = pygame.transform.rotate(self.stategraph.activeFrame, self.rotation)
        self.rect = self.image.get_rect(center=self.position)

        # Movement
        mx = 1 if state.keys[3] else -1 if state.keys[1] else 0
        my = 1 if state.keys[2] else -1 if state.keys[0] else 0

        if mx != 0 or my != 0:
            mv = pygame.Vector2(mx, my).normalize() * self.speed
            if state.keys[4]:
                mv *= 1.7

            room = map.get_inside(self)
            if room != None:
                collider : pygame.Surface = room.collider
                pixelindex = [int(self.position.x + mv.x - room.rect.x), int(self.position.y + mv.y - room.rect.y)]
                colrect = collider.get_rect()

                if graph.check_collider(collider, pixelindex):
                    self.position += mv
                elif graph.check_collider(collider, [int(self.position.x + mv.x - room.rect.x), int(self.position.y - room.rect.y)]):
                    self.position.x += mv.x
                elif graph.check_collider(collider, [int(self.position.x - room.rect.x), int(self.position.y + mv.y - room.rect.y)]):
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

    sheet = ( graph.ImageBase(img, (2, 0), 25), graph.ImageBase(feet, (0, 0), 21), graph.ImageBase(attack, (3, 0), 2) )
    char = Player(sheet)
    char.speed = 3
    char.position = pygame.Vector2(500, 500)

    return char