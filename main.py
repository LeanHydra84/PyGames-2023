import pygame
import map.room_creator as room_creator

from character.player import Player
from character.hallmonitor import HallMonitor

import rendering.resources as resources
from rendering.layerManager import LayerManager
from rendering.hueshift import HueShift

from capture.menu import build_pause_menu
from capture.textbox import Textbox

import random as rand

lerpSpeed = 5/60

class State: # Gamestate handler for all things gaming
    def __init__(self):
        self.screensize = (1280, 720)
        self.centerScreen = (self.screensize[0] / 2, self.screensize[1] / 2)
        self.paused = False
        self.keys = [False, False, False, False, False]
        self.running = True
        self.captureState = None

        self.camera = pygame.Vector2(0, 0)

    def quit(self):
        self.running = False
    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False
    def togglepause(self):
        self.paused = not self.paused

def init_enemy(layersObj, state):
    pos = pygame.Vector2(rand.randint(0, state.screensize[0]), rand.randint(0, state.screensize[1]))
    en = HallMonitor(state.RESOURCES.HALLMONITOR, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    layersObj.add_to("Enemies", en)
    layersObj.add_to("Feet", en.feet)

def main():
    pygame.init()
    pygame.mixer.init()

    state = State()

    screen = pygame.display.set_mode(state.screensize)
    state.DEBUGSCREEN = screen

    clock = pygame.time.Clock()
    pygame.display.set_caption("School Game")

    room_creator.room_scale = 7

    state.map = room_creator.Map()
    state.map.create_rooms()

    state.RESOURCES = resources.GlobalResources(5)
    state.RESOURCES.load()

    state.player = Player(state.RESOURCES.PLAYER, state.RESOURCES.FEET)
    state.player.position = pygame.Vector2(state.screensize[0] / 2, state.screensize[1] / 2)

    hue = HueShift(pygame.Color(100, 25, 25), 1)

    layers = LayerManager()
    state.renderLayers = layers

    layers.add(state.map.group, "Map", True)

    layers.add_new("DeadBodies", True)
    layers.add_new("Pickups", True)
    layers.add_new("Enemies", True)
    layers.add_new("Character", True)
    layers.add_new("Feet")

    layers.add_to("Character", state.player)
    layers.add_to("Feet", state.player.feet)

    for i in range(2):
        init_enemy(layers, state)

    pauseMenu = build_pause_menu(state, 5)
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
                elif state.player.alive():
                    state.player.attack_pressed(state)

        # Update
        if not state.paused:
            layers.update(state)
            # update enemies, etc

        hue.update()

        state.camera = state.camera.lerp(-state.player.position + state.centerScreen, lerpSpeed)

        # Draw
        screen.fill(hue.color())
        layers.render(screen)

        if state.captureState != None:
            state.captureState.update()
            state.captureState.render(screen)


        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()