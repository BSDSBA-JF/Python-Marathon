from abc import ABC, abstractmethod
import pygame
import os
import sys
from Settings import Settings
from TextSprite import TextSprite, ButtonSprite
from Sprite import *

class GameState():
    def __init__(self):
        self.state = 'introduction'
        self.mode = 'Easy'
        self.game = Settings.get_settings()
        self.game.start_game()
    
    def introduction(self):
        all_group = pygame.sprite.Group()
        game = Settings.get_settings()

        starting_sound = pygame.mixer.Sound("/Users/jfv/Desktop/Serpent Sprint/Sound/Starting Game.mp3")
        
        introduction_screen = ButtonSprite(name_image="Introduction",
                                           location_x=0,
                                           location_y=0,
                                           groups=(all_group))

        name = TextSprite(name_image= f"Name: {game.name}",
                          location_x=351,
                          location_y=424,
                          groups=(all_group))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(game.name) > 0:
                    game.name = game.name[:-1]
                elif event.key == pygame.K_RETURN and game.name != "":
                    self.state = 'difficulty'
                    starting_sound.play()
                else:
                    if event.unicode.isprintable() and len(game.name) < 8:
                        game.name += event.unicode

        game.screen.fill('white')
        all_group.draw(Settings.get_settings().screen)
        all_group.update()
        pygame.display.update()
    
    def choose_difficulty(self):
        all_group = pygame.sprite.Group()
        game = Settings.get_settings()

        starting_sound = pygame.mixer.Sound("/Users/jfv/Desktop/Python Marathon/Sound/Starting Game.mp3")

        easy_button = ButtonSprite(name_image='Easy',
                                   location_x=80,
                                   location_y=160,
                                   groups=(all_group))

        medium_button = ButtonSprite(name_image='Medium',
                                   location_x=80,
                                   location_y=314,
                                   groups=(all_group))
        
        hard_button = ButtonSprite(name_image='Hard',
                                   location_x=80,
                                   location_y=468,
                                   groups=(all_group))

        story_button = ButtonSprite(name_image='StoryMode',
                                   location_x=789,
                                   location_y=160,
                                   groups=(all_group))
        
        difficulty_text = TextSprite(name_image="C H O O S E  D I F F I C U L T Y",
                                     location_x=80, 
                                     location_y=70,
                                     groups=(all_group))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_clicked(event):
                    self.mode = 'Easy'
                    self.state = 'game'
                    
                if medium_button.is_clicked(event):
                    self.mode = 'Medium'
                    self.state = 'game'
                
                if hard_button.is_clicked(event):
                    self.mode = 'Hard'
                    self.state = 'game'
                
                if story_button.is_clicked(event):
                    self.mode = 'Easy'
                    self.state = 'story'
                
                starting_sound.play()
            
            game.screen.fill((255, 255, 255))
            all_group.draw(game.screen)
            all_group.update()
            pygame.display.update()
        
        #  Create an input, menu, and start rectangle in accordance to the rendered text
        #input_rect = pygame.Rect(midpoint[0] - title_image.get_width() // 2, midpoint[1] - title_image.get_height() // 2 + 200, name_rect.size[0], name_rect.size[0]/box_image.get_width()*box_image.get_height())

    def story(self):
        pass

states = GameState()

while True:
    if states.state == 'introduction':
        states.introduction()
    if states.state == 'difficulty':
        states.choose_difficulty()
    if states.state == 'game':
        mode = {'Easy': 3, 'Medium': 4, 'Hard': 5}
        states.game(mode[states.mode])
    if states.state == 'story':
        states.story()

