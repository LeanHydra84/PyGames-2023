import pygame
import rendering.resources as resources
import capture.menu as menu

from game_loop import game_loop

class State: # Gamestate handler for all things gamings
    def __init__(self):
        self.screensize = (1280, 720)
        self.centerScreen = (self.screensize[0] / 2, self.screensize[1] / 2)
        self.paused = False
        self.keys = [False, False, False, False, False]
        self.running = True
        self.captureState = None
        self.winGame = False
        self.camera = pygame.Vector2(self.centerScreen) - (0, 200)

        self.answers = [False, False, False]

    def quit(self):
        self.running = False
    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False
    def togglepause(self):
        self.paused = not self.paused

    def get_answer(self, string):
        match string:
            case "Hist":
                self.answers[0] = True
            case "Sci":
                self.answers[1] = True
            case "Math":
                self.answers[2] = True
    
    def win_condition(self) -> bool:
        return self.answers[0] and self.answers[1] and self.answers[2]
    
    def answer_count(self) -> int:
        count = 0
        for x in self.answers:
            if x == True:
                count += 1

        return count

class MenuState:
    def __init__(self):
        self.do_startgame = False
        self.running = True

    def start_game(self):
        self.do_startgame = True
    
    def stop_running(self):
        self.running = False

def main():
    
    print(pygame.ver)

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Cram Crawl")


    clock = pygame.time.Clock()

    resourcedictionary = resources.GlobalResources(5)
    resourcedictionary.load()

    pygame.display.set_icon(resourcedictionary.HM_UNC)

    # FLAGS
    menustate = MenuState()

    # MENU
    mainmenu = menu.OverlayMenu(None)
    mainmenu.multColor = pygame.Color(255, 255, 255)

    playbutton = menu.MenuButton(resourcedictionary.MAIN_MENU_BUTTON_START)
    playbutton.rect.center = (1280 / 2, 720 - 150)
    playbutton.hoverColor = pygame.Color(100, 100, 100)
    mainmenu.add_button(playbutton, menustate.start_game)

    quitbutton = menu.MenuButton(resourcedictionary.MAIN_MENU_QUIT_BUTTON)
    quitbutton.rect.bottomleft = (25, 720 - 25)
    quitbutton.hoverColor = pygame.Color(200, 30, 30)
    mainmenu.add_button(quitbutton, menustate.stop_running)


    title = menu.BounceText(resourcedictionary.MAIN_MENU_TITLE, (1280/2, 0), 2)
    mainmenu.add_static(title)

    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.load("assets\\music\\main_menu.wav")
    pygame.mixer.music.play(-1)

    # Menu Loop
    while menustate.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menustate.stop_running()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mainmenu.register_click(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.set_volume(0)
        
        
        if menustate.do_startgame:
            state = State()
            state.RESOURCES = resourcedictionary
            state.DEBUGSCREEN = screen

            returncode = game_loop(state, screen)
            if returncode == False:
                break

            pygame.mixer.music.load("assets\\music\\main_menu.wav")
            pygame.mixer.music.play(-1)
            menustate.do_startgame = False

        mainmenu.update()

        # Draw

        screen.blit(resourcedictionary.MAIN_MENU_BACKGROUND, (0, 0))
        mainmenu.render(screen)

        # End frame
        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()