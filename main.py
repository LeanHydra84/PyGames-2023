import pygame
import map.room_creator as room_creator
import character.player as player
import character.enemy as enemy

from rendering.layerManager import LayerManager
from capture.menu import build_pause_menu
from capture.textbox import Textbox

SCREENSIZE = (1280, 720)
backgroundColor = pygame.Color(100, 100, 100, 255)

class State: # Gamestate handler for all things gaming
    def __init__(self):
        self.paused = False
        self.keys = [False, False, False, False, False]
        self.running = True
        self.captureState = None

    def quit(self):
        self.running = False
    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False
    def togglepause(self):
        self.paused = not self.paused

def main():
    pygame.init()
    
    state = State()

    screen = pygame.display.set_mode(SCREENSIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("School Game")

    room_creator.room_scale = 7
    map = room_creator.Map()
    map.create_rooms()

    char = player.createplayer(5)
    enemy1 = enemy.create_enemy_hallmonitor_test(5)

    layers = LayerManager()
    layers.add(map.group, "Map")

    layers.add_new("Character").add(char)
    layers.find("Character").layer.add(enemy)

    char.feet.add(layers.add_new("Legs"))
    enemy.feet.add(layers.find("Legs").layer)

    layers.add_new("Text")

    pauseMenu = build_pause_menu(state)
    text = Textbox(state)

    keys = state.keys
    while state.running:
        
        for event in pygame.event.get():

            # Process Events
            if event.type == pygame.QUIT:
                state.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pauseMenu.togglecapture()
                    state.togglepause()

                if event.key == pygame.K_e:
                    # Interact
                    
                    pass

                if event.key == pygame.K_j:
                    print("Test")
                    text.read("Lorem ipsum test string\nHere is line two swag here we go")
                    text.togglecapture()
                    state.pause()


                
                if event.key == pygame.K_w:
                    keys[0] = True
                elif event.key == pygame.K_a:
                    keys[1] = True
                elif event.key == pygame.K_s:
                    keys[2] = True
                elif event.key == pygame.K_d:
                    keys[3] = True
                elif event.key == pygame.K_LSHIFT:
                    keys[4] = True

            if event.type == pygame.KEYUP:
                keys = state.keys
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False
                elif event.key == pygame.K_LSHIFT:
                    keys[4] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state.captureState != None:
                    state.captureState.register_click(pygame.mouse.get_pos())
                else:
                    char.attack_pressed()

        # Update
        if not state.paused:
            char.update(state, pygame.Vector2(pygame.mouse.get_pos()), map)
            # update enemies, etc

        # Draw
        screen.fill(backgroundColor)
        layers.render(screen)

        if state.captureState != None:
            state.captureState.update()
            state.captureState.render(screen)


        clock.tick(60)
        pygame.display.flip()



if __name__ == "__main__":
    main()