"""
File: Settings.py

This module focuses on the Settings class, which follows the Singleton design pattern. 
The Settings class is to modularize the setting up of the game. 
Instead of having to write out the boilerplate code "pygame.init()..." in the main file, it is quicker to write in the code:
    "game = Settings.get_settings()
    game.start_game()"

Creator: John Francis Y. Viray and Caitlin Elaine L. Sebastian
"""

import pygame

class Settings():
    """
    The Settings class follows the Singleton design pattern since there can only be one instantiated object so as to prevent multiple screens/displays being made.

    Attributes:
        width_screen (int) : The width of the screen.
        height_screen (int) : The height of the screen.
        background_color (tuple) : The RGB representation of a color. The color right now is white.
        fps (int) : The frames per second of the game.
        __instance (Settings): A class variable indicating whether an instance of the Settings class exists.

    Methods:
        get_settings(): Returns the instantiated Settings object. If it hasn't been created yet, it will create one. This is a static method.
        __init__(): Instantiates a Settings object only if it hasn't been created yet. This is a constructor.
        start_game(): Sets up the game using pygame's functions such as pygame.init().
    """

    __instance = None

    @staticmethod
    def get_settings():
        """
        Returns an instance of the Settings class
        """
        if Settings.__instance is None:
            Settings.__instance  = Settings(1120, 700, (255, 255, 255), 30)
        return Settings.__instance
    
    def __init__(self, width_screen, height_screen, background_color, fps):
        """
        Constructor creates the Settings object based on the width and height of the screen, the background color, and the frames-per-second (fps) of the game.
        """
        
        if Settings.__instance is not None:
            raise RuntimeError("Settings class is a singleton. There should only be one object of this kind.\nSettings class should be instantiated using get_settings()")
        
        self.width_screen = width_screen
        self.height_screen = height_screen
        self.background_color = background_color
        self.screen = pygame.display.set_mode((self.width_screen, self.height_screen))
        self.fps = fps
        self.clock = pygame.time.Clock()
    
    def start_game(self):
        """
        Initialize Pygame for the visual effects and Pygame.mixer for the sound effects
        """
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Serpent Sprint")

    def make_basic_loop(self):
        """
        make_basic_loops is strictly just for testing since with the final game, there will be many more events than just quit.
        This function is so that when someone tests a mechanic, they can just call upon make_basic_loop()
        """
        import sys
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        self.screen.fill(self.background_color)
    
# This is to test out if the Settings class works as expected.
if __name__ == "__main__":
    game = Settings.get_settings()
    game.start_game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        game.screen.fill(game.background_color)

        pygame.display.flip()