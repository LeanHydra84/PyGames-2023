import pygame
import character.enemybase as eb
from character.projectile import Projectile

detectRange = 650**2
attackRange = 500**2
stopAdvancingrange = 300**2
spotTime = 30
forgetTime = 120

class Teacher(eb.EnemyBase):
    attackCooldown = 60
    attackTime = 12

    def __init__(self, resources, rsFeet, state):
        super().__init__(resources, rsFeet, state, 1.8)

    def ai_tick(self, state):
        if not state.player.alive():
            self.aimode = eb.aimodes.IDLE
            return
        
        # Range Detection
        targetPos = state.player.position
        if self.position.distance_squared_to(targetPos) > detectRange:
            return
        
        # IF Idle
        if self.aimode == eb.aimodes.IDLE:
            if self.can_see_point(targetPos, state):
                self.aimode = eb.aimodes.ALERTED

        elif self.aimode == eb.aimodes.ALERTED:
            if self.can_see_point(targetPos, state):
                self.move_towards(targetPos, self.speed * 0.5, state)
        
                self.spotTimer += 1
                if self.spotTimer >= spotTime:
                    self.aimode = eb.aimodes.CHASING
                    self.spotTimer = 0
            else:
                self.aimode = eb.aimodes.IDLE


        elif self.aimode == eb.aimodes.CHASING:
            if self.position.distance_squared_to(state.player.position) < attackRange and not self.cooldown:
                self.attacking = True

            if self.can_see_point(targetPos, state):
                withinAdvRange = self.position.distance_squared_to(state.player.position) > stopAdvancingrange
                adjustedspeed = 0 if withinAdvRange else self.speed * 0.1 if self.attacking else self.speed
                self.move_towards(targetPos, adjustedspeed, state)
            else:
                self.attackTimer = 0
                self.aimode = eb.aimodes.SEARCHING
                self.spotTimer = 0
                self.tracksheet = state.player.history.copy()

        elif self.aimode == eb.aimodes.SEARCHING:
            targetPos = self.tracksheet[0]
            if self.position_reached(targetPos):
                self.tracksheet.popleft()
                if len(self.tracksheet) == 0:
                    self.aimode = eb.aimodes.IDLE
                    self.spotTimer = 0
                    self.tracksheet = None
                    return
                else:
                    targetPos = self.tracksheet[0]
            
            self.move_towards(targetPos, self.speed, state)

            if self.can_see_point(state.player.position, state):
                self.aimode = eb.aimodes.CHASING
                self.tracksheet = None
                self.spotTimer = 0
                return

            self.spotTimer += 1
            if self.spotTimer >= forgetTime:
                self.aimode = eb.aimodes.IDLE
                self.tracksheet = None
                self.spotTimer = 0

    def attack(self, state):
        self.attackTime = 0

        state.RESOURCES.SND_HADOUKEN.play()

        spr = pygame.transform.rotate(state.RESOURCES.PROJECTILE, self.rotation)
        newprojectile = Projectile(spr, self.forward(), self.position)

        state.renderLayers.add_to("Interactable", newprojectile)