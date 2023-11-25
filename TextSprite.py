"""
File: TextSprite.py

This module focuses on the TextSprite Class. 
By the name, instances of this class will focus on text.

Creator: John Francis Y. Viray and Rohan A. Sachdev
"""

# Importing modules 
import pygame
from Settings import Settings

class TextSprite(pygame.sprite.Sprite):
    """
    TextSprite is mainly for strings to be displayed on the game screen.
    
    Attributes:
        text (str): The text that will be displated on the screen
        location_x: The number of pixels away from the leftmost side of the game screen
        location_y: The number of pixels away from the topmost side of the game screen
        font (Font): The font that will be used for the text
        surface (Surface): It is a drawable area, similar to a canvas for painting.
            As such, we first create the area that can be drawn and then put the text into it. 
        rect (Rectangle): It is for the placement of the image. Using the canvas analogy, the rectangle is the easel of the instantiated TextSprite object.
            If the text_rect moves, the text_surface and thus the image also moves.
        groups (Group): A container that holds and manages a collection of sprite objects

    Methods:
        __init__(self, text): Constructs the TextSprite and its corresponding attributes
        blit_text_middle(self): Displays the text in the middle but the location in the y-axis is dependent on the parameter
        blit_text(self): Displays the text in any location
        update(): The text sprites will not move, so the method is just passing.
    """

    def __init__(self, name_image, location_x, location_y):
        """
        Constructor creates the TextSprite objects based on the text.
        """

        # Initialize the text, location, font, and surface
        super().__init__()
        self.text = name_image
        self.location_x = location_x
        self.location_y = location_y
        self.font = pygame.font.Font('/Users/jfv/Desktop/Python Marathon/Graphics/Pokemon_GB.ttf', 30)
        self.surface = self.font.render(self.text, False, 'black')
        
        # Get the coordinate if the sprite wants to be placed in the middle
        width_game = Settings.get_settings().width_screen
        width_surface = self.surface.get_width()
        self.middle_x = (width_game - width_surface) // 2

        # Get the rectangle
        self.rect = self.surface.get_rect(midleft = (self.middle_x, location_y))
    
    def blit_text_middle(self):
        """
        Blits/Displays the text in the middle of the game screen
        """

        screen = Settings.get_settings().screen
        screen.blit(self.surface, self.rect)

    def blit_text(self):
        """
        Blits/Displays the text anywhere based on the parameters given
        """

        screen = Settings.get_settings().screen
        self.rect.midleft = (self.location_x, self.location_y)
        screen.blit(self.surface, self.rect)
    

if __name__ == "__main__":
    game = Settings.get_settings()
    game.start_game()

    text_sprite_1 = TextSprite(
        name_image = 'Text Sprite 1', 
        location_x = 100, 
        location_y = 100)
    
    running = True
    while running:
        game.make_basic_loop()

        game.screen.fill(game.background_color)
        text_sprite_1.blit_text_middle()