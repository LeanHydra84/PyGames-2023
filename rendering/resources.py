import pygame

import rendering.conversations as convo
from rendering.animation_set import AnimationCollection


class GlobalResources:
    def __init__(self, scale):
        self.scale = scale

    def load(self):

        # MAIN MENU
        self.MAIN_MENU_BACKGROUND = pygame.image.load("assets\\menu\\main_menu_720.png").convert()
        self.MAIN_MENU_BUTTON_START = pygame.image.load("assets\\menu\\start1.png").convert_alpha()
        self.MAIN_MENU_QUIT_BUTTON = pygame.transform.scale_by(pygame.image.load("assets\\menu\\mm_quit.png").convert_alpha(), 2.5)
        self.MAIN_MENU_TITLE = pygame.transform.scale_by(pygame.image.load("assets\\menu\\title.png").convert_alpha(), 2)

        # SPRITE SHEETS
        self.PLAYER = AnimationCollection("assets\\player.json", self.scale)
        self.HALLMONITOR = AnimationCollection("assets\\hallmonitor.json", self.scale)
        self.TEACHER = AnimationCollection("assets\\teacher.json", self.scale / 2)
        self.FEET = AnimationCollection("assets\\feet.json", self.scale)

        self.MRS_FLIPS = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\hometeach.png").convert_alpha(), self.scale / 2)

        # COMPUTER
        self.COMPUTER = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\computer.png").convert_alpha(), self.scale)
        self.COMPUTER_OFF = pygame.transform.scale_by(pygame.image.load("assets\\shespriteonmy\\computer_off.png").convert_alpha(), self.scale)

        self.E_PROMPT = pygame.transform.scale_by(pygame.image.load("assets\\menu\\eprompt.png").convert_alpha(), self.scale)

        # STATIC SPRITES
        self.DEADBODY_TESTSPRITE = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\DEBUG_X.png").convert_alpha(), self.scale )
        self.HM_UNC = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\hallx.png").convert_alpha(), self.scale / 2.5)
        self.TC_UNC = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\teacherx.png").convert_alpha(), self.scale / 2.5)

        self.PROJECTILE = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\projectile.png").convert_alpha(), self.scale )
        self.DEATH_TEXT = pygame.image.load("assets\\menu\\deathtext.png").convert_alpha()
        self.WINNINGSCREEN = pygame.image.load("assets\\menu\\winningmed.png").convert()
        self.YOUWON = pygame.transform.scale_by(pygame.image.load("assets\\menu\\youwon.png").convert_alpha(), 1.5)

        # ITEMS
        self.TRAY = pygame.transform.scale_by(pygame.image.load("assets\\items\\tray.png").convert_alpha(), self.scale * 0.75)
        self.RULER = pygame.transform.scale_by(pygame.image.load("assets\\items\\ruler.png").convert_alpha(), self.scale * 0.75)

        self.TRAY_HINT = pygame.transform.scale_by(pygame.image.load("assets\\items\\tray_hint.png").convert_alpha(), 1.5)
        self.RULER_HINT = pygame.transform.scale_by(pygame.image.load("assets\\items\\ruler_hint.png").convert_alpha(), 1.5)

        # AUDIO
        self.SND_PUNCH = pygame.mixer.Sound("assets\\audio\\punch_test.wav")
        self.SND_WHIFF = pygame.mixer.Sound("assets\\audio\\whiff_test.mp3")
        self.SND_HADOUKEN = pygame.mixer.Sound("assets\\audio\\getback.mp3")
        self.SND_TONK = pygame.mixer.Sound("assets\\audio\\tonk.wav")
        self.SND_PICKUP_ITEM = pygame.mixer.Sound("assets\\audio\\temp_coinsound.wav")
        self.SND_DEATH_SOUND = pygame.mixer.Sound("assets\\audio\\rulersmack.wav")

        # ON GET ANSWER
        self.ON_ANSWER = pygame.image.load("assets\\menu\\answer.png").convert_alpha()
        self.MATH = pygame.image.load("assets\\menu\\math.png").convert_alpha()
        self.HISTORY = pygame.image.load("assets\\menu\\history.png").convert_alpha()
        self.SCIENCE = pygame.image.load("assets\\menu\\science.png").convert_alpha()

        # Set all Audio Volume
        self.set_volume(1)

        # FONT
        #self.FONT_25 = pygame.font.SysFont("Arial", 25)
        self.FONT_25 = pygame.font.Font("assets\\Gamefont-Regular.ttf", 25)
        self.FONT_40 = pygame.font.Font("assets\\Gamefont-Regular.ttf", 40)

        # CONVERSATIONS
        self.CONVERSATION = convo.ConversationManager("assets\\conversations.json")

    def set_volume(self, val):
        self.SND_PUNCH.set_volume(0.5 * val)
        self.SND_WHIFF.set_volume(0.5 * val)
        self.SND_HADOUKEN.set_volume(0.5 * val)
        self.SND_TONK.set_volume(1 * val)
        self.SND_PICKUP_ITEM.set_volume(0.5 * val)
        self.SND_DEATH_SOUND.set_volume(0.25 * val)