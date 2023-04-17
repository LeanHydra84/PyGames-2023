import pygame
import random as rand

import map.map_generator as mapgen

from rendering.layerManager import LayerManager
from rendering.hueshift import HueShift
from rendering.timer import FormattedCountdownTimer
from rendering.stategraph import SingleStateGraph
from rendering.win_game_scene import win_game_scene

from character.player import Player

from capture.menu import build_pause_menu
from capture.textbox import Textbox


lerpSpeed = 5/60

playerPickupDistance = 50**2

class E_Prompt(pygame.sprite.Sprite):
    def __init__(self, sheet, dim):
        pygame.sprite.Sprite.__init__(self)
        
        self.graph = SingleStateGraph(sheet, dim, 25)
        self.image = self.graph.activeFrame
        self.rect = self.image.get_rect(centerx=(1280/2), bottom=(720-10))
    
    def update(self, _):
        self.graph.tick()
        self.image = self.graph.activeFrame


# Helper function used to round the lerped return of the camera pos -- keeping that pixel-aligned stops collision issues
def vec_round(vec: pygame.Vector2) -> pygame.Vector2:
    nv = vec.copy()
    nv.x = round(nv.x)
    nv.y = round(nv.y)
    return nv


def game_loop(state, screen: pygame.Surface):

    clock = pygame.time.Clock()
    pygame.display.set_caption("School Game")

    mapgen.SCALE = 3.75
    state.map = mapgen.createmap(6)

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

    state.pauseMenu = build_pause_menu(state, 5)
    state.text = Textbox(state)

    timer = FormattedCountdownTimer(120, pygame.font.SysFont("Arial", 35))
    layers.add_to("Character", timer.timeRenderer)

    interactkey = False

    state.map.spawn_all(state)

    eprompt = E_Prompt(state.RESOURCES.E_PROMPT, [1, 0])

    pygame.mixer.music.load("assets\\music\\in_game.wav")
    pygame.mixer.music.play(-1)

    keys = state.keys
    while state.running:
        
        for event in pygame.event.get():

            # Process Events
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_m:
                    pygame.mixer.music.set_volume(0)
                if event.key == pygame.K_p:
                    state.RESOURCES.set_volume(0)

                elif event.key == pygame.K_SPACE and not state.player.alive():
                    state.running = False

                elif event.key == pygame.K_e:
                    interactkey = True

                elif event.key == pygame.K_ESCAPE:
                    if state.captureState == None or state.captureState == state.pauseMenu:
                        state.pauseMenu.togglecapture()
                        state.togglepause()
                    if state.captureState == state.text:
                        state.text.end_text()

                
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
            if state.winGame:
                return win_game_scene(screen, state.RESOURCES.WINNINGSCREEN)


            layers.update(state)
            timer.update()

            interactableNear = pygame.sprite.spritecollide(state.player, layers.find("Interactable").layer, False)

            need_e_prompt = False
            for c in interactableNear:
                if state.player.position.distance_squared_to(c.position) < playerPickupDistance:
                    if not c.interact(state, interactkey):
                        need_e_prompt = True

            if need_e_prompt:
                if not eprompt.alive():
                    layers.add_to("Character", eprompt)
            else:
                eprompt.kill()
                    

            state.camera = vec_round(state.camera.lerp(-state.player.position + state.centerScreen, lerpSpeed))

            if timer.is_time_up():
                state.player.kill_me(state)

        interactkey = False

        hue.update()

        # Draw
        screen.fill(hue.color())
        layers.render(screen)

        if state.captureState != None:
            state.captureState.update()
            state.captureState.render(screen)


        fps = str(int(clock.get_fps()))
        fpsobject = state.RESOURCES.FONT_25.render(fps, False, pygame.Color(255, 255, 255))

        screen.blit(fpsobject, (0, 50))

        clock.tick(60)
        pygame.display.flip()

    return True