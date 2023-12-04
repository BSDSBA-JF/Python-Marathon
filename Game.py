"""
File: Game.py

This module focuses on the creating the game.
This module contains the code to play the game. It imports all previous modules to combine and use them so that 
it can leverage pre-existing functionality and organize the game logic in a modular and efficient manner.

Creator: John Francis Y. Viray and Farell Alastair T. Lu
"""

import pygame
import sys
from Settings import Settings
from TextSprite import TextSprite, ButtonSprite, TextSpriteWhite
from Sprite import *

class GameState():
    def __init__(self):
        self.state = 'introduction'
        self.mode = ''
        self.game = Settings.get_settings()
        self.game.start_game()
        self.player = None
        self.background_image = None
        self.number_pythons = 3
    
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
                    print(True)
                    
                if medium_button.is_clicked(event):
                    self.mode = 'Medium'
                    self.state = 'game'
                
                if hard_button.is_clicked(event):
                    self.mode = 'Hard'
                    self.state = 'game'
                
                if story_button.is_clicked(event):
                    self.mode = 'Story'
                    self.state = 'game'
                
                starting_sound.play()
            
            game.screen.fill((255, 255, 255))
            all_group.draw(game.screen)
            all_group.update()
            pygame.display.update()


states = GameState()
game = Settings.get_settings()
obstaclesprites = pygame.sprite.Group()
textsprites = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
story_group = pygame.sprite.Group()

# These are the sprites that will be displayed on the screen.
frog = PlayerSprite(name_image = 'Frog', 
                number_frames = 2,
                location_x = 0,
                location_y = 350, 
                strategy_pattern = PlayerUpdating, 
                groups = (player_group),
                velocity = 6,
                is_facing_left = False, 
                framespeed = 0.1)
frog.rescale_percentage(0.85)

rabbit = PlayerSprite(name_image = 'Rabbit', 
                number_frames = 2,
                location_x = 0,
                location_y = 350, 
                strategy_pattern = PlayerUpdating, 
                groups = (player_group),
                velocity = 9,
                is_facing_left = False, 
                framespeed = 0.1)
rabbit.rescale_percentage(0.85)

chick = PlayerSprite(name_image = 'Chick', 
                number_frames = 3,
                location_x = 0,
                location_y = 350, 
                strategy_pattern = PlayerUpdating, 
                groups = (player_group),
                velocity = 4,
                is_facing_left = False, 
                framespeed = 0.1)
chick.rescale_percentage(0.91)

bird = PlayerSprite(name_image = 'LetterBird', 
                number_frames = 7,
                location_x = 0,
                location_y = 350, 
                strategy_pattern = PlayerUpdating, 
                groups = (player_group),
                velocity = 3,
                is_facing_left = False, 
                framespeed = 0.1)
bird.rescale_percentage(0.3)


players = [frog, rabbit, chick, bird]
game = Settings.get_settings()
letter_bird = ObstalceSprite(name_image='LetterBird',
                                number_frames=7,
                                location_x= 461,
                                location_y= 256,
                                strategy_pattern=BirdUpdating,
                                groups=(story_group),
                                framespeed=0.2)

is_paused = False
is_game_over = False
is_intro_running = True
is_story_running = False
is_story_running_2 = False

while is_intro_running:
    if states.state == 'introduction':
        states.introduction()
    if states.state == 'difficulty':
        states.choose_difficulty()
    if states.state == 'game': 
        if states.mode == 'Easy':
            player_group.remove(chick, rabbit, bird)
            states.background_image = pygame.image.load(f"/Users/jfv/Desktop/Serpent Sprint/Graphics/Background/FrogBackground.png").convert()
            states.player = frog
            states.number_pythons = 4
            Settings.get_settings().mode = 'Easy'
        elif states.mode == 'Medium':
            player_group.remove(frog, chick, bird)
            states.background_image = pygame.image.load(f"/Users/jfv/Desktop/Serpent Sprint/Graphics/Background/RabbitBackground.png").convert()
            states.player = rabbit
            states.number_pythons = 5
            Settings.get_settings().mode = 'Medium'
        elif states.mode == 'Hard':
            player_group.remove(frog, rabbit, bird)
            states.background_image = pygame.image.load(f"/Users/jfv/Desktop/Serpent Sprint/Graphics/Background/ChickBackground.png").convert()
            states.player = chick
            states.number_pythons = 6
            Settings.get_settings().mode = 'Hard'
        elif states.mode == 'Story':
            print('went through')
            player_group.remove(frog, rabbit, chick)
            states.background_image = pygame.image.load(f"/Users/jfv/Desktop/Serpent Sprint/Graphics/Background/FrogBackground.png").convert()
            states.player = bird
            states.number_pythons = 4
            is_story_running = True
            Settings.get_settings().mode = 'Story'
        is_intro_running = False


delivery_text = TextSprite(name_image=f"Tweet tweet!! Delivery for {game.name}!!",
                          location_x=game.width_screen,
                          location_y=150,
                          groups=(story_group))
instructional_text = TextSprite(name_image=f"Press Enter to open it!!",
                          location_x=game.width_screen,
                          location_y=200,
                          groups=(story_group))

delivery_text.draw_middle()
instructional_text.draw_middle()

while is_story_running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                states.state = 'game'
                states.state = 'Story'
                is_story_running = False
                is_story_running_2 = True

    game.screen.fill('white')
    story_group.draw(game.screen)
    story_group.update()
    pygame.display.update()

story2_group = pygame.sprite.Group()
letter2 = ButtonSprite(name_image='Letter',
                       location_x=0,
                       location_y=0,
                       groups = (story2_group))

while is_story_running_2:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                states.state = 'game'
                states.state = 'Story'
                is_story_running_2 = False

    game.screen.fill('white')
    story2_group.draw(game.screen)
    story2_group.update()
    pygame.display.update()


for _ in range(states.number_pythons):
    create_obstacle(width=random.randint(600, 1120), group=obstaclesprites, )

game_over_group = pygame.sprite.Group()
pause_group = pygame.sprite.Group()

python_marathon_title = ButtonSprite(
    name_image = 'PythonMarathonTitle', 
    location_x = 452, 
    location_y = 94,
    groups = (game_over_group, pause_group))

end_game = ButtonSprite(
    name_image='End',
    location_x=442,
    location_y=266,
    groups = (game_over_group))

game_over = TextSprite(name_image = 'GAME OVER', 
                    location_x = 373, 
                    location_y = 365,
                    groups = (game_over_group))
game_over.draw_middle()


game_over = TextSprite(name_image = 'PAUSED', 
                    location_x = 373, 
                    location_y = 365,
                    groups = (pause_group))
game_over.draw_middle()

score_screen = TextSpriteWhite(name_image = f'Score {game.score}', 
                    location_x = 0, 
                    location_y = 0,
                    groups = (textsprites, allsprites))

health = TextSpriteWhite(name_image = f'Health: {states.player.health}', 
                    location_x = 0, 
                    location_y = 20 + score_screen.rect.height,
                    groups = (textsprites, allsprites)) 

def draw_game_over():
    game = Settings.get_settings()
    pygame.draw.rect(game.surface, (128, 128, 128, 150), [0, 0, Settings.get_settings().width_screen, Settings.get_settings().height_screen ])
    game.screen.blit(game.surface, (0, 0) )
    game_over_group.draw(game.screen)
    game_over_group.update()

def draw_pause():
    game = Settings.get_settings()
    pygame.draw.rect(game.surface, (128, 128, 128, 150), [0, 0, Settings.get_settings().width_screen, Settings.get_settings().height_screen ])
    game.screen.blit(game.surface, (0, 0) )
    pause_group.draw(game.screen)
    pause_group.update()


is_game_running = True
while is_game_running:
    import sys
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_paused:
                    is_paused = False
                    print('f')
                else:
                    is_paused = True
                    print('t')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if end_game.is_clicked(event):
                Settings.get_settings().update_csv()
                is_game_running = False

        if game.health <= 0:
            is_game_over = True
            draw_game_over()
            
    game.screen.blit(states.background_image, (0, 0))

    obstaclesprites.draw(game.screen)
    #allsprites.draw(game.screen)
    textsprites.draw(game.screen)
    player_group.draw(game.screen)
    
    if not is_paused and not is_game_over:
        obstaclesprites.update()
        textsprites.update()
        #allsprites.update()
        player_group.update()
        
    if is_paused:    
        draw_pause()
    
    if is_game_over:
        draw_game_over()

    # Use the function of spritecollide where it checks if the player object has collided with any of the Obstacle sprites
    collision_obstacles = pygame.sprite.spritecollide(states.player, obstaclesprites, True)
    collision_text = pygame.sprite.spritecollide(states.player, textsprites, False)

    score_screen.name_image = f'Score: {game.score}'

    if collision_obstacles:
        #print("Player collided with an enemy!")
        create_obstacle(group=obstaclesprites)
        game = Settings.get_settings()
        game.health -= 1
        health.name_image = f'Health: {game.health}'
        health.image = health.font.render(health.name_image, False, 'black')
    
    if game.health <= 0:
        draw_game_over()

