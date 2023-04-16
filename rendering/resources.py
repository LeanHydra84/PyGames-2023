import pygame
from rendering.animation_set import AnimationCollection

class GlobalResources:
    def __init__(self, scale):
        self.scale = scale

    def load(self):

        # MAIN MENU
        self.MAIN_MENU_BACKGROUND = pygame.image.load("assets\\menu\\main_menu_720.png").convert()
        self.MAIN_MENU_BUTTON_START = pygame.image.load("assets\\menu\\start1.png").convert_alpha()
        self.MAIN_MENU_QUIT_BUTTON = pygame.transform.scale_by(pygame.image.load("assets\\menu\\mm_quit.png").convert_alpha(), 2.5)

        # SPRITE SHEETS
        self.PLAYER = AnimationCollection("assets\\player.json", self.scale)
        self.HALLMONITOR = AnimationCollection("assets\\hallmonitor.json", self.scale)
        self.TEACHER = AnimationCollection("assets\\teacher.json", self.scale / 2)
        self.FEET = AnimationCollection("assets\\feet.json", self.scale)
        self.MRS_FLIPS = AnimationCollection("assets\\mrs_flips.json", self.scale / 2)

        # STATIC SPRITES
        self.DEADBODY_TESTSPRITE = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\DEBUG_X.png").convert_alpha(), self.scale )
        self.PROJECTILE = pygame.transform.scale_by( pygame.image.load("assets\\shespriteonmy\\projectile.png").convert_alpha(), self.scale )
        self.DEATH_TEXT = pygame.image.load("assets\\menu\\deathtext.png").convert_alpha()

        # ITEMS
        self.TRAY = pygame.transform.scale_by(pygame.image.load("assets\\items\\tray.png").convert_alpha(), self.scale * 0.75)
        self.RULER = pygame.transform.scale_by(pygame.image.load("assets\\items\\ruler.png").convert_alpha(), self.scale * 0.75)

        self.TRAY_HINT = pygame.transform.scale_by(pygame.image.load("assets\\items\\tray_hint.png").convert_alpha(), 1.5)

        # AUDIO
        self.SND_PUNCH = pygame.mixer.Sound("assets\\audio\\punch_test.wav")
        self.SND_WHIFF = pygame.mixer.Sound("assets\\audio\\whiff_test.mp3")
        self.SND_HADOUKEN = pygame.mixer.Sound("assets\\audio\\hadouken.mp3")
        self.SND_TONK = pygame.mixer.Sound("assets\\audio\\tonk.wav")
        self.SND_PICKUP_ITEM = pygame.mixer.Sound("assets\\audio\\temp_coinsound.wav")
        self.SND_DEATH_SOUND = pygame.mixer.Sound("assets\\audio\\InstagramBoom.mp3")

        self.SND_PUNCH.set_volume(0.5)
        self.SND_WHIFF.set_volume(0.5)
        self.SND_HADOUKEN.set_volume(1)
        self.SND_TONK.set_volume(1)
        self.SND_PICKUP_ITEM.set_volume(0.5)
        self.SND_DEATH_SOUND.set_volume(0.5)

    def release(self):
        del self.PLAYER
        del self.HALLMONITOR
        del self.FEET