import pygame

import rendering.stategraph as graph

import character.enemybase as eb
import character.feet as feet
import character.unconscious as unconscious

from enum import Enum

detectRange = 450**2

# TODO: Market research these values
forgetTime = 120
spotTime = 45
attackrange = 65**2
attackTime = 12
attackCooldown = 50

# AI MODES
class aimodes(Enum):
    IDLE = 1
    ALERTED = 2     # AI has line-of-sight with target, not fully spotted yet.
    CHASING = 3     # AI has had line-of-sight with target long enough to fully spot.
    SEARCHING = 4   # AI does not have line-of-sight with target, is following target trail.



class HallMonitor(pygame.sprite.Sprite):
    def __init__(self, resources, rsFeet, state):
        pygame.sprite.Sprite.__init__(self)
        
        self.graph = graph.StateGraph(resources)

        self.feet = feet.Feet(self, rsFeet)
        self.feet.add(state.renderLayers.find("Feet"))

        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

        self.speed = 2.1

        self.rotation = 0
        self.position = pygame.Vector2(100, 100)

        self.attackTimer = 0
        self.attacking = False
        self.cooldown = False
        self.spotTimer = 0
        self.aimode = aimodes.IDLE


        self.tracksheet = None

    # Suuuuper hacky line-of-sight pathing. Checks n (n=splits) points along line between self and player for colliders


    def ai_tick(self, state):

        if not state.player.alive():
            self.aimode = aimodes.IDLE
            return

        """
            TODO:
                this works pretty good,
                but the ai actually follows a backwards path I think?? Like it copies the queue when the
                most recent position is unseen, but all the positions behind that should have been seen because
                it's adding them on top. so I don't know. Could be worth looking into, but if this works who cares.
        """

        targetPos = state.player.position
        if self.position.distance_squared_to(targetPos) > detectRange:
            return

        if self.aimode == aimodes.IDLE:
            # Turning, sweeping, etc

            if eb.can_see_point(self.position, targetPos, state):
                self.aimode = aimodes.ALERTED

            pass

        elif self.aimode == aimodes.ALERTED:
            if eb.can_see_point(self.position, targetPos, state):
                eb.move_towards(self, targetPos, self.speed * 0.5)
            
                self.spotTimer += 1
                if self.spotTimer >= spotTime:
                    self.aimode = aimodes.CHASING
                    self.spotTimer = 0
            else:
                self.aimode = aimodes.IDLE
        
        elif self.aimode == aimodes.CHASING:
            if self.position.distance_squared_to(state.player.position) < attackrange and not self.cooldown:
                self.attacking = True

            if eb.can_see_point(self.position, targetPos, state):
                eb.move_towards(self,targetPos, self.speed)
            else:
                self.attackTimer = 0
                self.aimode = aimodes.SEARCHING
                self.spotTimer = 0
                self.tracksheet = state.player.history.copy()

        elif self.aimode == aimodes.SEARCHING:
            targetPos = self.tracksheet[0]
            if self.position_reached(targetPos):
                self.tracksheet.popleft()
                if len(self.tracksheet) == 0:
                    self.aimode = aimodes.IDLE
                    self.spotTimer = 0
                    self.tracksheet = None
                    return
                else:
                    targetPos = self.tracksheet[0]
            
            eb.move_towards(self, targetPos, self.speed)

            if eb.can_see_point(self.position, state.player.position, state):
                self.aimode = aimodes.CHASING
                self.tracksheet = None
                self.spotTimer = 0
                return

            self.spotTimer += 1
            if self.spotTimer >= forgetTime:
                self.aimode = aimodes.IDLE
                self.tracksheet = None
                self.spotTimer = 0
            
    def attack(self, state):
        self.graph.force_state(1)
        self.attackTimer = 0

        if self.position.distance_squared_to(state.player.position) < attackrange:
            state.player.kill()
            newspr = unconscious.Unconscious(state.RESOURCES.DEADBODY_TESTSPRITE, state.player.position)
            state.renderLayers.add_to("DeadBodies", newspr)

            state.RESOURCES.SND_PUNCH.play()
        else:
            state.RESOURCES.SND_WHIFF.play()
            
    def attack_tick(self, state):

        if self.cooldown:
            self.attackTimer += 1
            if self.attackTimer >= attackCooldown:
                self.attackTimer = 0
                self.cooldown = False
                return

        elif self.attacking:
            self.attackTimer += 1
            if self.attackTimer >= attackTime:
                self.attackTimer = 0
                self.attack(state)
                self.attacking = False
                self.cooldown = True

    def kill(self):
        super().kill()
        self.feet.kill()

    def update(self, state):
        
        # Animate
        self.graph.tick()

        # Set sprite
        self.image = pygame.transform.rotate(self.graph.activeFrame, self.rotation)
        self.rect = self.image.get_rect()

        # AI TICK
        self.ai_tick(state)
        self.attack_tick(state)

        # Feet
        if self.feet.alive() and self.aimode == aimodes.IDLE:
            self.feet.set_visible(False)
        if not self.feet.alive() and self.aimode != aimodes.IDLE:
            self.feet.set_visible(True)
        

        # Position
        self.rect.center = self.position + state.camera
        self.feet.update(self.position + state.camera)