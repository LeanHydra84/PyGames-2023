import pygame
import rendering.stategraph as graph
import character.feet as feet

from collections import deque
MAXTIME = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, rsFeet):
        pygame.sprite.Sprite.__init__(self)

        # Persistent Data References
        self.stategraph = graph.StateGraph(sheet)
        self.feet = feet.Feet(self, rsFeet)

        # Sprite draw data -- NOT PERSISTENT --
        self.image : pygame.Surface = None
        self.rect : pygame.Rect = None

        # Movement
        self.position = pygame.Vector2(500, 500)
        self.rotation = 0
        self.speed = 3
        self.moving = False

        self.history = deque(maxlen=MAXTIME)

    def forward(self):
        ward = pygame.Vector2.from_polar((1, self.rotation))
        ward.y = -ward.y
        return ward

    def attack_pressed(self, state):
        if self.stategraph.state() == 0:
            self.stategraph.force_state(1)

            enemygroup: pygame.sprite.Group = state.renderLayers.find("Enemies").layer
            
            attackRadius = 30
            attackdist = 30

            attackPos: pygame.Vector2 = self.position + (self.forward() * attackdist)

            # Debug attack circle
            #pygame.draw.circle(state.DEBUGSCREEN, (255, 0, 0), attackPos, attackRadius)

            hitflag = False
            for spr in enemygroup:
                if attackPos.distance_squared_to(spr.position) < attackRadius**2:
                    deadpos = spr.position
                    spr.kill()

                    newspr = pygame.sprite.Sprite()
                    newspr.image = state.RESOURCES.DEADBODY_TESTSPRITE
                    newspr.rect = newspr.image.get_rect(center=deadpos)

                    state.renderLayers.add_to("DeadBodies", newspr)
                    hitflag = True
                
            if hitflag:
                state.RESOURCES.SND_PUNCH.play()
            else:
                state.RESOURCES.SND_WHIFF.play()



    def update(self, state):
        
        # Animation
        self.stategraph.tick()

        # Set Image

        mousepos = pygame.mouse.get_pos()
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

            room = state.map.get_inside(self)
            if room != None:
                if graph.check_collider(room,   [int(self.position.x + mv.x), int(self.position.y + mv.y)]):
                    self.position += mv
                elif graph.check_collider(room, [int(self.position.x + mv.x), int(self.position.y)]):
                    self.position.x += mv.x
                elif graph.check_collider(room, [int(self.position.x), int(self.position.y + mv.y)]):
                    self.position.y += mv.y

            else:
                self.position += mv

            if self.moving == False:
                self.feet.set_visible(True)
            self.moving = True
        else:
            if self.moving == True:
                self.feet.set_visible(False)
            self.moving = False

        # Positioning
        #state.camPos = self.position
        
        self.rect.center = self.position
        self.feet.update()

        # Update position history
        self.history.append(self.position.copy())        

    def kill(self):
        super().kill()
        self.feet.kill()


# DEPRECATED
def createplayer(scale) -> Player:
    img = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\girl1.png").convert_alpha(), scale)
    attack = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\attack.png").convert_alpha(), scale)
    feet = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\leg2.png").convert_alpha(), scale / 1.5)

    sheet = ( graph.ImageBase(img, (2, 0), 25), graph.ImageBase(feet, (0, 0), 21), graph.ImageBase(attack, (3, 0), 2) )
    char = Player(sheet)
    char.speed = 3
    char.position = pygame.Vector2(500, 500)

    return char