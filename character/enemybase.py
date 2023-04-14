import pygame

import rendering.stategraph as graph
import character.feet as feet
import character.unconscious as unconscious
from enum import Enum

playerHaltDistance = 20**2

# AI MODES
class aimodes(Enum):
    IDLE = 1
    ALERTED = 2     # AI has line-of-sight with target, not fully spotted yet.
    CHASING = 3     # AI has had line-of-sight with target long enough to fully spot.
    SEARCHING = 4   # AI does not have line-of-sight with target, is following target trail.

splits = 32
reachedThreshold = 10**2 # Distance before target position is considered "reached"

class EnemyBase(pygame.sprite.Sprite):
    attackCooldown = 0
    attackTime = 0

    def __init__(self, resources, rsFeet, state, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.graph = graph.StateGraph(resources)

        self.feet = feet.Feet(self, rsFeet)
        self.feet.add(state.renderLayers.find("Feet"))

        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

        self.speed = speed

        self.rotation = 0
        self.position = pygame.Vector2(100, 100)

        self.attackTimer = 0
        self.attacking = False
        self.cooldown = False
        self.spotTimer = 0
        self.aimode = aimodes.IDLE


    def attack_tick(self, state):
        if self.cooldown:
            self.attackTimer += 1
            if self.attackTimer >= type(self).attackCooldown:
                self.attackTimer = 0
                self.cooldown = False
                return

        elif self.attacking:
            self.attackTimer += 1
            if self.attackTimer >= type(self).attackTime:
                self.attackTimer = 0
                self.attack(state)
                self.attacking = False
                self.cooldown = True

    # Suuuuper hacky line-of-sight pathing. Checks n (n=splits) points along line between self and player for colliders
    def can_see_point(self, point: pygame.Vector2, state) -> bool:
        direction = (point - self.position).normalize() * (point.distance_to(self.position) / splits)
        adjp = self.position + state.camera
        for i in range(splits - 1):
            if not state.map.get_collision_at_point(adjp + i * direction):
                return False
        return True

    def move_towards(self, target, speed, state):
        mov = (target - self.position).normalize()
        newPos = self.position + mov * speed
        self.rotation = -(target - self.position).as_polar()[1]
        
        if state.map.get_collision_at_point(newPos) and self.position.distance_squared_to(state.player.position) > playerHaltDistance:
            self.position = newPos

    def position_reached(self, pos: pygame.Vector2):
        return self.position.distance_squared_to(pos) < reachedThreshold
    
    def kill(self):
        super().kill()
        self.feet.kill()

    def ai_tick(self, state):
        pass

    def attack(self, state):
        pass

    def forward(self):
        ward = pygame.Vector2.from_polar((1, self.rotation))
        ward.y = -ward.y
        return ward

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



