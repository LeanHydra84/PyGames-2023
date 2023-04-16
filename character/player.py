import pygame
import rendering.stategraph as graph
import character.feet as feet
import character.unconscious as unconscious

import capture.deathscreen as death

from math import acos
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
        self.position = pygame.Vector2(0, 0)
        self.rotation = 0
        self.speed = 3
        self.moving = False

        self.history = deque(maxlen=MAXTIME) # make this better, future me
        self.shielded = False

        # ITEMS
        self.hasTray = False
        self.hasRuler = False


    def pickup_item(self, type):
        if type == "Tray":
            self.hasTray = True
        elif type == "Ruler":
            self.hasRuler = True
            self.stategraph.set_idle(5)
            self.stategraph.force_state(5)

    def forward(self) -> pygame.Vector2:
        ward = pygame.Vector2.from_polar((1, self.rotation))
        ward.y = -ward.y
        return ward
    
    def attack_pressed(self, state):

        # Janky
        attackRadius, anim = (30, 1) if self.stategraph.state() == 0 else (60, 6) if self.stategraph.state() == 5 and self.hasRuler else (0, -1)

        if attackRadius != 0:
            self.stategraph.force_state(anim)

            enemygroup: pygame.sprite.Group = state.renderLayers.find("Enemies").layer

            attackdist = 30
            attackPos: pygame.Vector2 = self.position + (self.forward() * attackdist)

            # Debug attack circle
            #pygame.draw.circle(state.DEBUGSCREEN, (255, 0, 0), attackPos, attackRadius)

            hitflag = False
            for spr in enemygroup:
                if attackPos.distance_squared_to(spr.position) < attackRadius**2:
                    deadpos = spr.position
                    spr.kill()

                    body = unconscious.Unconscious(state.RESOURCES.DEADBODY_TESTSPRITE, deadpos)
                    state.renderLayers.add_to("DeadBodies", body)

                    hitflag = True
                
            if hitflag:
                state.RESOURCES.SND_PUNCH.play()
            else:
                state.RESOURCES.SND_WHIFF.play()

    def shield(self, boolval):
        if not self.hasTray:
            return
        sv = self.stategraph.state()
        if boolval:
            if self.stategraph.is_idle():
                self.stategraph.force_state(2)
                self.shielded = True
        else:
            if sv == 3 or sv == 2:
                self.stategraph.force_state(self.stategraph.idle)
                self.shielded = False

    def hit_by_enemy_attack(self, srcDir: pygame.Vector2, state) -> bool:
        if self.stategraph.state() == 3:
            sfwd = self.forward()
            anglebtwn =  acos( sfwd.dot(srcDir) / (sfwd.magnitude() * srcDir.magnitude()) )

            if anglebtwn < 1.8:
                self.kill_me(state)
                return True

            else:
                state.RESOURCES.SND_TONK.play()
                return False
        else:
            self.kill_me(state)
            return True


    def kill_me(self, state):
        self.kill()
        newspr = unconscious.Unconscious(state.RESOURCES.DEADBODY_TESTSPRITE, self.position)
        state.renderLayers.add_to("DeadBodies", newspr)

        #death.DeathScreen(state, state.RESOURCES.DEATH_TEXT, 100, 5, 2).togglecapture()
        death.create_death_screen(state).togglecapture()
        state.pause()
        state.RESOURCES.SND_DEATH_SOUND.play()

    def update(self, state):
        
        # Animation
        self.stategraph.tick()

        # Set Image

        mousepos = pygame.mouse.get_pos()
        self.rotation = -(mousepos - (self.position + state.camera)).as_polar()[1]
        self.image = pygame.transform.rotate(self.stategraph.activeFrame, self.rotation)
        self.rect = self.image.get_rect(center=(self.position + state.camera))

        # Movement
        mx = 1 if state.keys[3] else -1 if state.keys[1] else 0
        my = 1 if state.keys[2] else -1 if state.keys[0] else 0

        if mx != 0 or my != 0:
            trueSpeed = self.speed if not self.shielded else self.speed / 2
            mv = pygame.Vector2(mx, my).normalize() * trueSpeed
            if state.keys[4]:
                mv *= 1.7

            adjPos = self.position + state.camera
            if state.map.get_collision_at_point(adjPos + mv):
                self.position += mv
            elif state.map.get_collision_at_point(adjPos + pygame.Vector2(mv.x, 0)):
                self.position.x += mv.x
            elif state.map.get_collision_at_point(adjPos + pygame.Vector2(0, mv.y)):
                self.position.y += mv.y

            if self.moving == False:
                self.feet.set_visible(True)
            self.moving = True
        else:
            if self.moving == True:
                self.feet.set_visible(False)
            self.moving = False

        # Positioning
        #state.camPos = self.position
        
        self.rect.center = self.position + state.camera
        self.feet.update(self.position + state.camera)

        # Update position history
        self.history.append(self.position.copy())        

    def kill(self):
        super().kill()
        self.feet.kill()
