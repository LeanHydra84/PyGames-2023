import pygame
import rendering.stategraph as graph
import character.feet as feet

detectRange = 450**2
splits = 32

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

    # Suuuuper hacky line-of-sight pathing. Checks n (n=splits) points along line between self and player for colliders
    def can_see_point(self, point: pygame.Vector2, map) -> bool:
        direction = (point - self.position).normalize() * (self.position.distance_to(point) / splits)
        for i in range(splits - 1):
            if not map.get_collision_at_point(self.position + i * direction):
                return False
        return True

    def ai_tick(self, state):
        targetPos: pygame.Vector2 = state.player.position

        if self.position.distance_squared_to(targetPos) < detectRange and self.can_see_point(targetPos, state.map):
            mov = (targetPos - self.position).normalize()
            self.position += mov * self.speed
            self.rotation = -(targetPos - self.position).as_polar()[1]
        
    def update(self, state):
        
        # Animate
        self.graph.tick()

        # Set sprite
        self.image = pygame.transform.rotate(self.graph.activeFrame, self.rotation)
        self.rect = self.image.get_rect()

        # AI TICK
        self.ai_tick(state)

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