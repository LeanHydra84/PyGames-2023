import pygame
import rendering.stategraph as graph
import character.feet as feet

class HallMonitor(pygame.sprite.Sprite):
    def __init__(self, resources):
        pygame.sprite.Sprite.__init__(self)
        
        
        self.graph = graph.StateGraph(resources)
        self.feet = feet.Feet(self, resources[1])

        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

        self.rotation = 0
        self.position = pygame.Vector2(0, 0)

    def ai_tick(self):

        pass

    def update(self):
        
        # Animate
        self.graph.tick()

        # Set sprite
        self.image = pygame.transform.rotate(self.graph.activeFrame, self.rotation)
        self.rect = self.image.get_rect()

        # AI TICK
        self.ai_tick()

        # Position
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
def create_enemy_hallmonitor_test(scale):
    idle = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\hallmonitor1.png"), scale)
    feet = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\leg2.png").convert_alpha(), scale / 1.5)

    sheet = ( graph.ImageBase(idle, (2, 0), 10), graph.ImageBase(feet, (0, 0), 4) )

    enemy = HallMonitor(sheet)
    enemy.position = (300, 300)
    return enemy