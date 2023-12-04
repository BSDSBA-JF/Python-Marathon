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
    #game = Settings.get_settings
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
        self.rect.topleft
        self.image
    
    def draw_middle(self):
        midpoint_x = (Settings.get_settings().width_screen - self.rect.width) // 2
        #midpoint_y = (Settings.height() - self.rect.height) // 2
        self.rect.topleft = (midpoint_x, self.location_y)

class TextSpriteWhite(TextSprite):
    def update(self):
        pygame.draw.rect(Settings.get_settings().screen, (255, 255, 255, 0), [self.location_x, self.location_y, self.rect.width, self.rect.height])
        Settings.get_settings().screen.blit(self.image, self.rect)
        self.image = self.font.render(self.name_image, False, 'black')
        self.rect = self.image.get_rect(topleft = (self.location_x, self.location_y))

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, name_image, location_x, location_y, groups):
        super().__init__(groups)
        self.name_image = name_image
        self.location_x = location_x
        self.location_y = location_y
        self.image = pygame.image.load(f'/Users/jfv/Desktop/Serpent Sprint/Graphics/Button/{name_image}.png')
        self.rect = self.image.get_rect(topleft = (self.location_x, self.location_y))

    def update(self):
        self.image
        self.rect
    
    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

if __name__ == "__main__":
    import sys
    game = Settings.get_settings()
    game.start_game()
    
    obstaclesprites = pygame.sprite.Group()
    separatesprites = pygame.sprite.Group()
    
    python_marathon_title = ButtonSprite(
        name_image = 'PythonMarathonTitle', 
        location_x = 452, 
        location_y = 94,
        groups = (obstaclesprites)
        )
    resume = ButtonSprite(
        name_image='Resume',
        location_x=296,
        location_y=258,
        groups = (obstaclesprites)
    )
    menu = ButtonSprite(
        name_image='Menu',
        location_x=575,
        location_y=258,
        groups = (obstaclesprites)
    )
    game_over = TextSprite(name_image = 'GAME OVER', 
                        location_x = 373, 
                        location_y = 365,
                        groups = (separatesprites))
    score = TextSprite(name_image = f'SCORE: {game.score}', 
                        location_x = 360, 
                        location_y = 427,
                        groups = (separatesprites))
    
    background = pygame.image.load('/Users/jfv/Desktop/Serpent Sprint/Graphics/Background/ChickBackground.png')
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume.is_clicked(event):
                    print(True)
                if menu.is_clicked(event):
                    print(False)
                
        game.screen.blit(background, (0, 0))
        
        obstaclesprites.draw(game.screen)
        obstaclesprites.update()
        game_over.draw_middle()
        score.draw_middle()
        separatesprites.draw(game.screen)
        separatesprites.update()
        pygame.display.flip()
