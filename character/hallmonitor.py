import pygame

import character.enemybase as eb
import character.unconscious as unconscious


detectRange = 450**2

# TODO: Market research these values
forgetTime = 120
spotTime = 45
attackrange = 65**2




class HallMonitor(eb.EnemyBase):
    attackCooldown = 50
    attackTime = 12

    def __init__(self, resources, rsFeet, state):
        super().__init__(resources, rsFeet, state, 2.6)

    def ai_tick(self, state):

        if not state.player.alive():
            self.aimode = eb.aimodes.IDLE
            return

        """
            TODO:
                this works pretty good,
                but the ai actually follows a backwards path I think?? Like it copies the queue when the
                most recent position is unseen, but all the positions behind that should have been seen because
                it's adding them on top. so I don't know. Could be worth looking into, but if this works who cares.

                >>>Brother it also walks through walls.
        """

        targetPos = state.player.position
        if self.position.distance_squared_to(targetPos) > detectRange:
            return

        if self.aimode == eb.aimodes.IDLE:
            # Turning, sweeping, etc

            if self.can_see_point(targetPos, state):
                self.aimode = eb.aimodes.ALERTED

            pass

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
            if self.position.distance_squared_to(state.player.position) < attackrange and not self.cooldown:
                self.attacking = True

            if self.can_see_point(targetPos, state):
                self.move_towards(targetPos, self.speed, state)
            else:
                self.attackTimer = 0
                self.aimode = eb.aimodes.SEARCHING
                self.spotTimer = 0
                self.tracksheet = state.player.history.copy()

        elif self.aimode == eb.aimodes.SEARCHING:
            targetPos = self.tracksheet[-1]
            if self.position_reached(targetPos):
                self.tracksheet.pop()
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
        self.graph.force_state(1)
        self.attackTimer = 0

        if self.position.distance_squared_to(state.player.position) < attackrange:
            hit = state.player.hit_by_enemy_attack(self.forward(), state)
            if hit:
                state.RESOURCES.SND_PUNCH.play()
        else:
            state.RESOURCES.SND_WHIFF.play()
