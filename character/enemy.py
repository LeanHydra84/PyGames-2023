import pygame
import rendering.stategraph as graph
import character.feet as feet

from enum import Enum

detectRange = 450**2
reachedThreshold = 10**2 # Distance before target position is considered "reached"
splits = 32

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
    def can_see_point(self, point: pygame.Vector2, map) -> bool:
        direction = (point - self.position).normalize() * (self.position.distance_to(point) / splits)
        for i in range(splits - 1):
            if not map.get_collision_at_point(self.position + i * direction):
                return False
        return True

    def position_reached(self, pos: pygame.Vector2):
        return self.position.distance_squared_to(pos) < reachedThreshold

    def move_towards(self, target, speed):
        mov = (target - self.position).normalize()
        self.position += mov * speed
        self.rotation = -(target - self.position).as_polar()[1]


    def ai_tick(self, state):

        if not state.player.alive():
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

            if self.can_see_point(targetPos, state.map):
                self.aimode = aimodes.ALERTED

            pass

        elif self.aimode == aimodes.ALERTED:
            if self.can_see_point(targetPos, state.map):
                self.move_towards(targetPos, self.speed * 0.5)
            
                self.spotTimer += 1
                if self.spotTimer >= spotTime:
                    self.aimode = aimodes.CHASING
                    self.spotTimer = 0
            else:
                self.aimode = aimodes.IDLE
        
        elif self.aimode == aimodes.CHASING:
            if self.position.distance_squared_to(state.player.position) < attackrange and not self.cooldown:
                self.attacking = True

            if self.can_see_point(targetPos, state.map):
                self.move_towards(targetPos, self.speed)
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
            
            self.move_towards(targetPos, self.speed)

            if self.can_see_point(state.player.position, state.map):
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
            newspr = pygame.sprite.Sprite()
            newspr.image = state.RESOURCES.DEADBODY_TESTSPRITE
            newspr.rect = newspr.image.get_rect(center=state.player.position)
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

    def update(self, state):
        
        # Animate
        self.graph.tick()

        # Set sprite
        self.image = pygame.transform.rotate(self.graph.activeFrame, self.rotation)
        self.rect = self.image.get_rect()

        # AI TICK
        self.ai_tick(state)
        self.attack_tick(state)

        # Position
        self.rect.center = self.position
        
# DEPRECATED
def create_enemy_hallmonitor_test(scale):
    idle = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\hallmonitor1.png"), scale)
    feet = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\leg2.png").convert_alpha(), scale / 1.5)

    sheet = ( graph.ImageBase(idle, (2, 0), 10), graph.ImageBase(feet, (0, 0), 4) )

    enemy = HallMonitor(sheet)
    enemy.position = (300, 300)
    return enemy