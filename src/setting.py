import pygame

pygame.init()

class Setting:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.SIZE = 8
        self.ROWS = self.COLS = self.SIZE
        self.SQUARE_SIZE = self.WIDTH//self.COLS
        self.themes =  {"dark": (119, 154, 88), 
                        "light": (234, 235, 200), 
                        "outline": (0, 0, 0)}
        
        self.capture_sound = pygame.mixer.Sound("./assets/sounds/capture_sound.mp3")
        self.castle_sound = pygame.mixer.Sound("./assets/sounds/castle_sound.mp3")
        self.check_sound = pygame.mixer.Sound("./assets/sounds/check_sound.mp3")
        self.checkmate_sound = pygame.mixer.Sound("./assets/sounds/checkmate_sound.mp3")
        self.game_over_sound = pygame.mixer.Sound("./assets/sounds/gameover_sound.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/sounds/start_sound.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move_sound.mp3")
        self.stalemate_sound = pygame.mixer.Sound("./assets/sounds/stalemate_sound.mp3")
        self.pop = pygame.mixer.Sound("./assets/sounds/pop.mp3")



Config = Setting()
