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
    
    def __init__(self, name_image, location_x, location_y, groups):
        """
        Constructor creates the TextSprite objects based on the text.
        """

        # Initialize the text, location, font, and surface
        super().__init__(groups)
        pygame.font.init()

        self.name_image = name_image
        self.location_x = location_x
        self.location_y = location_y
        self.font = pygame.font.Font('/Users/jfv/Desktop/Python Marathon/Graphics/Pokemon_GB.ttf', 30)
        self.image = self.font.render(self.name_image, False, 'black')
        
        # Get the rectangle
        self.rect = self.image.get_rect(topleft = (self.location_x, self.location_y))
        self.background_rect = pygame.Rect(self.location_x, self.location_y, self.image.get_width(), self.image.get_height())

    def update(self):
        #pygame.draw.rect(Settings.get_settings().screen, (0, 0, 0), self.background_rect)
        self.rect.topleft
        self.image
    
    def blit_rect(self):
        Settings.get_settings().screen.blit(self.background_rect)

if __name__ == "__main__":
    game = Settings.get_settings()
    game.start_game()
    
    obstaclesprites = pygame.sprite.Group()
    text_sprite_1 = TextSprite(
        name_image = 'Text Sprite 1', 
        location_x = 100, 
        location_y = 100,
        groups = (obstaclesprites))
    
    running = True
    while running:
        game.make_basic_loop()

        game.screen.fill(game.background_color)
        obstaclesprites.draw(game.screen)
        obstaclesprites.update()
