import pygame
import rendering.stategraph as graph

class HallMonitor(pygame.sprite.Sprite):
    def __init__(self, resources):
        pygame.sprite.Sprite.__init__(self)
        
        self.graph = graph.StateGraph(resources)

        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

        self.rotation = 0


    def update(self):
        
        # Animate
        self.graph.tick()

        # Set sprite
        self.image = pygame.transform.rotate(self.graph.activeFrame, self.rotation)
        self.rect = self.image.get_rect()

        # AI TICK
        
        
        pass