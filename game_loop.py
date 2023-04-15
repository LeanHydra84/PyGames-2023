import pygame
import random as rand

import map.map_generator as mapgen

from rendering.layerManager import LayerManager
from rendering.hueshift import HueShift

from character.hallmonitor import HallMonitor
from character.teacher import Teacher
from character.pickup import Pickup

from character.player import Player

from capture.menu import build_pause_menu
from capture.textbox import Textbox

lerpSpeed = 5/60

playerPickupDistance = 30**2

def init_enemy_atpos(layersObj, state, pos):
    en = HallMonitor(state.RESOURCES.HALLMONITOR, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    layersObj.add_to("Enemies", en)
    layersObj.add_to("Feet", en.feet)

def init_enemy(layersObj, state):
    pos = pygame.Vector2(rand.randint(0, state.screensize[0]), rand.randint(0, state.screensize[1]))
    init_enemy_atpos(layersObj, state, pos)

def init_teacher_atpos(layersObj, state, pos):
    en = Teacher(state.RESOURCES.TEACHER, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    layersObj.add_to("Enemies", en)
    layersObj.add_to("Feet", en.feet)

# Helper function used to round the lerped return of the camera pos -- keeping that pixel-aligned stops collision issues
def vec_round(vec: pygame.Vector2) -> pygame.Vector2:
    nv = vec.copy()
    nv.x = round(nv.x)
    nv.y = round(nv.y)
    return nv


def game_loop(state, screen):

    clock = pygame.time.Clock()
    pygame.display.set_caption("School Game")

    mapgen.SCALE = 15
    state.map = mapgen.createmap(5)

    state.player = Player(state.RESOURCES.PLAYER, state.RESOURCES.FEET)

    hue = HueShift(pygame.Color(100, 25, 25), 1)
    layers = LayerManager()

    state.renderLayers = layers
    layers.add(state.map.group, "Map", True)

    layers.add_new("DeadBodies", True)
    layers.add_new("Interactable", True)
    layers.add_new("Feet")
    layers.add_new("Enemies", True)
    layers.add_new("Character", True)

    layers.add_to("Character", state.player)
    layers.add_to("Feet", state.player.feet)

    # TEST PICKUP

    traypickup = Pickup(state.RESOURCES.TRAY, "Tray", (100, 0), state.RESOURCES.TRAY_HINT)
    layers.add_to("Interactable", traypickup)

    # TEST SPAWN ENEMIES
    for pos in state.map.details.deadEnds:
        if rand.choice([True, False]):
            init_enemy_atpos(layers, state, pygame.Vector2(pos[0]))
        else:
            init_teacher_atpos(layers, state, pygame.Vector2(pos[0]))

    state.pauseMenu = build_pause_menu(state, 5)
    state.text = Textbox(state)

    

    keys = state.keys
    while state.running:
        
        for event in pygame.event.get():

            # Process Events
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if not state.player.alive():
                    state.running = False


                if event.key == pygame.K_ESCAPE:
                    if state.captureState == None or state.captureState == state.pauseMenu:
                        state.pauseMenu.togglecapture()
                        state.togglepause()

                if event.key == pygame.K_j:
                    state.text.begin_conversation(["Here is some\nepic text for you to read", "And here is some extra more\ntext for you to read like a big boy.", "Finally, here is last text"])
                    state.text.togglecapture()
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

                    if event.button == 1: # Left Click
                        state.player.attack_pressed(state)
                    elif event.button == 3: # Right Click
                        state.player.shield(True)

            if event.type == pygame.MOUSEBUTTONUP:
                if state.captureState == None:
                    if event.button == 3: # Right Click
                        state.player.shield(False)

        # Update
        if not state.paused:
            layers.update(state)

            interactableNear = pygame.sprite.spritecollide(state.player, layers.find("Interactable").layer, False)
            pressedkey = bool(pygame.key.get_pressed()[pygame.K_e])
            for c in interactableNear:
                if state.player.position.distance_squared_to(c.position) < playerPickupDistance:
                    c.interact(state, pressedkey)

            state.camera = vec_round(state.camera.lerp(-state.player.position + state.centerScreen, lerpSpeed))


        hue.update()

        # Draw
        screen.fill(hue.color())
        layers.render(screen)

        if state.captureState != None:
            state.captureState.update()
            state.captureState.render(screen)


        clock.tick(60)
        pygame.display.flip()

    return True