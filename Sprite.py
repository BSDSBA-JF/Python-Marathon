"""
File: Sprite.py

This module focuses on the Sprite Class. It utilizes the Strategy design pattern by having an abstract class, UpdatingStrategy.
Moreover, it has a subclass, PlayableSprite. 
By the name, instances of this class will focus on sprites such as the Text, PowerUp, Serpent, Bird, and Rope.

Creator: John Francis Y. Viray, Bianca M. Manatad, and Caitlin Elaine L. Sebastian
"""

# Importing modules 
from abc import ABC, abstractmethod
import pygame
import math
from Settings import Settings
from TextSprite import TextSprite
import random

class CharacterSprite(ABC, pygame.sprite.Sprite):
    def __init__(self, name_image, number_frames, location_x, location_y, strategy_pattern, groups, velocity = 1, is_facing_left = True, framespeed = 0.02):
        """
        The constructor method will initialize the following variables:
            name_image (str): The name of the sprite
            number_frames (int): The number of frames needed for animation
            location_x (int): The distance, measured in pixels, between the rectangle and the leftmost side of the game screen
            location_y (int): The distance, measured in pixels, between the rectangle and the topmost side of the game screen
            strategy_pattern (Strategy): The algorithm of how the sprite will movement
            groups (Group): A class by Pygame to ease the managing and organizing of sprites
            velocity (int) : The velocity of the sprite in moving the horizontal direction
            is_facing_left (bool) : True if the sprite is facing to the left.
            framespeed (int) : The rate of change with the frames. The default is 1 frame per 1/30 second.
            
        These variables are based on the given above:
            images (list of Surface objects): A collection of images needed to display visual graphics
            image (Surface): An element from the images list
            index (list): The index for referring to the elements in the images list. It is here for animation.
            rect (Rectangle): A rectangle where all of the positions of the images will be determined
        """

        super(CharacterSprite, self).__init__(groups)
        self.name_image = name_image
        self.number_frames = number_frames
        self.location_x = location_x
        self.location_y = location_y
        self.framespeed = framespeed
        self.velocity = velocity
        self.is_facing_left = is_facing_left
        self.images = []
        self.append_images()
        self.image = self.images[int(self.number_frames - 1)]
        self.index = 0
        
        # This rectangle is often used for collision detection and positioning the sprite on the screen.
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.location_x, self.location_y)

        self.strategy_pattern = strategy_pattern(self.images, self.location_x, self.location_y, self.rect, self.framespeed, self.velocity, self.number_frames, self.is_facing_left)

    def create_indices(self):
        """
        create_indices() is a helper method that will create a list of indices so that the frames are loopable.
        If there are 7 frames, then the list will be '1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2
        """

        # Create an integer list of indices that will start from 1 go to the maximum number of frames then back to 1
        indices = [int(x) for x in range(1, self.number_frames+1)]
        for i in range(self.number_frames-1, 1, -1):
            indices.append(int(i))
        
        return indices
    
    def append_images(self): 
        """append_images() is a helper method that will append a list of images so that sprite can have a loopable animation with its frames.""" 
        # Append the frames to self.images
        for i in self.create_indices():
            self.images.append(
                pygame.image.load(f'/Users/jfv/Desktop/Serpent Sprint/Graphics/{self.name_image}/{self.name_image}{str(i)}.png').convert_alpha())
            
    def rescale_percentage(self, percentage):
        """
        rescale_percentage() is a helper method that will rescale a list of images so that sprite can fit inside the game screen.
        Because the images are usually larger than needed, it is more often that they will be sized down.
        
        Args:
            percentage (int) : The percent decrease to the new file. 
                               For example, if you want to decrease the image by 99%, you put rescale_percentage(0.99)
        """
        assert percentage < 1, "Percentage has to be less than 1 since if greater, the width or height will become negative"

        for index in range(len(self.images)):
            new_width = (self.images[index].get_rect().width) * (1 - percentage)
            new_height = (self.images[index].get_rect().height) * (1 - percentage)
            self.images[index] = pygame.transform.scale(self.images[index], (new_width, new_height))
        
        self.rect.width = new_width
        self.rect.height = new_height
        self.strategy_pattern.rect.width = self.rect.width
        self.strategy_pattern.rect.height = self.rect.height
    
    
    #def flip_images(self):
        """flip_images() is a helper method that will flip the images"""
        #for index in range(len(self.images)):
            #self.images[index] = pygame.transform.flip(self.images[index], flip_x=1, flip_y=0)

    @abstractmethod
    def update(self):
        pass

class PlayerSprite(CharacterSprite):
    def __init__(self, name_image, number_frames, location_x, location_y, strategy_pattern, groups, velocity = 1, is_facing_left = True, framespeed = 0.02):
        super().__init__(name_image, number_frames, location_x, location_y, strategy_pattern, groups, velocity, is_facing_left, framespeed)
        self.health = 3
        self.score = 0
        
    def create_indices(self):
        """create_images() is a helper method that will append a list of images so that sprite can have a loopable animation with its frames."""

        # Create an integer list of indices that will start from 1 go to the maximum number of frames then back to 1
        if self.number_frames != 1:
            total_frames = self.number_frames * 2
            
            #this will create the 1 to number_frames
            indices = [int(x) for x in range(1, self.number_frames+1)]

            for i in range(self.number_frames-1, 1, -1):
                indices.append(int(i))

            for i in range(self.number_frames+1, total_frames+1):
                indices.append(int(i))
            
            for i in range(total_frames-1, self.number_frames+1, -1):
                indices.append(int(i))
        elif self.number_frames == 1:
            indices = [1, 2]

        return indices
    
    def append_images(self):  
        """Append the images to the list self.images"""
        for i in self.create_indices():
            self.images.append(
                pygame.image.load(f'/Users/jfv/Desktop/Serpent Sprint/Graphics/{self.name_image}/{self.name_image}{str(i)}.png').convert_alpha())
    
    def update(self):
        """
        The sprite will update itself using the strategy pattern stated in its instantiation. 

        Updating basically just means that:
            1)  The sprite will move up, down, left or right. This is mainly seen in the names. 
                The sprites can move linearly, in a sine wave, upwards, downwards, or even through player input.
            2)  The sprites will be animated. Because we are dealing with 2D animation, we made it so that the each 
                change of frame is done incrementally through a function.
        Thus, the update method will have to deal with these two roles.

        A strategy then is just the different types of way it can deal with its roles.
        For example, movement can be described by a line; a sine wave; an indepence between horizontal and vertical velocities; 
        a player's input; and so on and so forth.
        """
        # This is where the Strategy Design Pattern is used. 
        self.rect.topleft = self.strategy_pattern.move()
        self.image = self.images[self.strategy_pattern.change_index_frames()]

class ObstalceSprite(CharacterSprite):
    def update(self):
        self.rect.topleft = self.strategy_pattern.move()
        self.image = self.images[self.strategy_pattern.change_index_frames()]

# Below are Updating Strategies.
class UpdatingStrategy(ABC):
    def __init__(self, images, location_x, location_y, rect, framespeed, velocity, number_frames, is_facing_left):
        """
        The constructor method will initialize an updating strategy using the variables also used in 
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images[0]
        self.location_x = location_x
        self.location_y = location_y
        self.rect = rect
        self.framespeed = framespeed
        self.velocity = velocity
        self.index = 0
        self.number_frames = number_frames
        self.is_facing_left = is_facing_left
        self.up = True
        
        # This rectangle is often used for collision detection and positioning the sprite on the screen.
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.location_x, self.location_y)

    @abstractmethod
    def move(self):
        """
        Moves and updates the sprite. Since UpdatingStrategy is just an interface, there is no concrete implementation yet.
        """
        pass

    def change_index_frames(self):
        """Change the indices so that there is animation in the sprite"""
        self.index += self.framespeed
        
        # To loop the code. If self.index is greater than the length of self.images, the animation must loop
        if self.index > len(self.images):
            self.index = 0
            #self.up = not self.up
        return int(self.index)

    def reappear(self):
        """
        We learned today that since the classes 'LinearUpdating' and 'NonPlayableSprite' are not the same. 
        LinearUpdating does not inherit the variables of the NonPlayableSprite, so even if the variables have the same name, 
        the SCOPE OF EACH VARIABLE IS SO DIFFERENT.
        """
        
        # If the image crosses the left side of the border, reset it to be back at the right
        if self.location_x <= -self.images[0].get_rect().width:
            random_height = random.randint(0, Settings.get_settings().height_screen-self.images[0].get_rect().height)
            self.rect.topleft = (Settings.get_settings().width_screen, random_height)
            self.location_x = self.rect.topleft[0]
            self.location_y = self.rect.topleft[1]
            Settings.get_settings().score += 1
            #print('first case worked', self.rect.topleft)

        
        # If the image crosses the right side of the border, reset it to be back at the left
        elif self.location_x >= Settings.get_settings().width_screen + self.images[0].get_rect().width:
            random_height = random.randint(0, Settings.get_settings().height_screen-self.images[0].get_rect().height)
            self.rect.topleft = (-self.images[0].get_rect().width, random_height)
            self.location_x = self.rect.topleft[0]
            self.location_y = self.rect.topleft[1]
            Settings.get_settings().score += 1
            #print('second case worked', self.rect.topleft)
        
        # If the image crosses the top border, reset it at the lower bottom
        elif self.location_y <= -self.images[0].get_rect().height:
            random_height = random.randint(Settings.get_settings().height_screen // 2, Settings.get_settings().height_screen*2)
            self.rect.topleft = (Settings.get_settings().width_screen, random_height)
            self.location_x = self.rect.topleft[0]
            self.location_y = self.rect.topleft[1]
            Settings.get_settings().score += 1
            #print('third case worked', self.rect.topleft)

        # If the image crosses the bottom border, reset it at the top 
        elif self.location_y >= Settings.get_settings().height_screen + self.images[0].get_rect().height:
            random_height = random.randint(-Settings.get_settings().height_screen*2, -Settings.get_settings().height_screen // 2)
            self.rect.topleft = (Settings.get_settings().width_screen, random_height)
            self.location_x = self.rect.topleft[0]
            self.location_y = self.rect.topleft[1]
            Settings.get_settings().score += 1
            #print('fourth case worked', random_height)



class PlayerUpdating(UpdatingStrategy):
    """
    Movement is handled by the player's input.
    """
    def __init__(self, images, location_x, location_y, rect, framespeed, velocity, number_frames, is_facing_left):
        super().__init__(images, location_x, location_y, rect, framespeed, velocity, number_frames, is_facing_left)
        self.is_right = not self.is_facing_left
        self.is_left = self.is_facing_left

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.location_x <= Settings.get_settings().width_screen - self.images[0].get_rect().width:
            self.location_x += self.velocity
            self.is_right = True
            self.is_left = False

        if keys[pygame.K_LEFT] and self.location_x >= 0:
            self.location_x -= self.velocity
            self.is_right = False
            self.is_left = True

        if keys[pygame.K_UP] and self.location_y >= 0:
            self.location_y -= self.velocity
        
        if keys[pygame.K_DOWN] and self.location_y <= Settings.get_settings().height_screen - self.images[0].get_rect().height:
            self.location_y += self.velocity

        self.rect.topleft = (self.location_x, self.location_y)
        return self.rect.topleft

    def change_index_frames(self):
        self.index += self.framespeed

        middle_index = (self.number_frames * 2 - 2)
    
        if self.is_right and self.index >= middle_index: 
            self.index = 0

        if self.is_left and self.index < middle_index:
            self.index = middle_index

        if self.is_left and self.index >= middle_index * 2:
            self.index = middle_index
        
        return int(self.index)

class LinearUpdating(UpdatingStrategy):
    """Movement of the sprite can be described by a line"""
    def move(self):
        self.location_x -= self.velocity
        self.rect.topleft = (self.location_x, self.location_y)
        self.reappear()
        return self.rect.topleft

class BirdUpdating(UpdatingStrategy):
    """
    The movement of BirdUpdating is a change in the vertical axis similar to a sine wave; however, it does not move in the horizontal axis

    Attr:
        location_x (int): The distance, measured in pixels, between the rectangle and the leftmost side of the game screen
        location_y (int): The distance, measured in pixels, between the rectangle and the topmost side of the game screen
        speed (int) : The rate of change with the frames. The default is 1 frame per 1/30 second.
        
        rect (Rectangle): It is for the placement of the image. 
        images (list): Contains the images needed for a loopable animation
    """

    def move(self):
        # math.pi for the wave, len(self.images) so it goes up and down,
        change = 15 * math.sin(self.index * math.pi / len(self.images))

        # The bird actually goes up or down
        
        change_y = self.location_y + (change if self.up else -change)

        # Recenter the rectangle
        self.rect.topleft = [self.location_x, change_y]

        return self.rect.topleft
    
    def change_index_frames(self):
        self.index += self.framespeed
        
        # To loop the code. If self.index is greater than the length of self.images, the animation must loop
        if self.index >= len(self.images):
            self.index = 0
            self.up = not self.up
        return int(self.index)

class SinoidUpdating(UpdatingStrategy):
    """Movement of a sprite can be described as a sine wave."""
    def move(self):
        change_x = -self.velocity
        change_y = (self.velocity) * math.sin((math.pi * self.location_x)/(40 * self.velocity))

        # The python actually goes up or down
        self.location_x += change_x
        self.location_y += change_y

        # Recenter the rectangle and thus also the python
        self.rect.topleft = [self.location_x, self.location_y]

        self.reappear()

        return self.rect.topleft
    
    def reappear(self):
        if self.location_x <= -self.images[0].get_rect().width:
            length_image = self.images[0].get_rect().height
            # self.velocity is the peak/trough of any sine wave due to how transformations of functions work
            random_height = random.randint(self.velocity, Settings.get_settings().height_screen - length_image - self.velocity)
            self.rect.topleft = (Settings.get_settings().width_screen, random_height)
            self.location_x = self.rect.topleft[0]
            self.location_y = random_height

class UpwardsUpdating(UpdatingStrategy):
    """
    The velocities in the horizontal and vertical direction will most likely be different unless stated by the instance variable, 'velocity'.
    It may be described similarly to free falling with horizontal and vertical components, 
    but there is no gravity since vertical velocity is constant
    """
    def move(self):
        self.location_x -= self.velocity
        self.location_y -= 2
        self.rect.topleft = [self.location_x, self.location_y]
        self.reappear()
        return self.rect.topleft

class DownwardsUpdating(UpdatingStrategy):
    """
    The movement is similar to UpwardsUpdating.
    """
    def move(self):
        self.location_x -= self.velocity
        self.location_y += 2
        self.rect.topleft = [self.location_x, self.location_y]
        self.reappear()
        return self.rect.topleft

def create_obstacle(group, width = Settings.get_settings().width_screen):
    import random

    random_strategy = random.choice([LinearUpdating, SinoidUpdating, UpwardsUpdating])
    random_height = random.randint(0, Settings.get_settings().height_screen-100)
    
    obstacle = ObstalceSprite(name_image='Python', 
                      number_frames=2, 
                      location_x=width, 
                      location_y=random_height, 
                      strategy_pattern = random_strategy, 
                      groups = group, 
                      velocity=random.randint(3,5), 
                      is_facing_left=False)
    obstacle.rescale_percentage(0.93)
    
    return obstacle

if __name__ == "__main__":    
    game = Settings.get_settings()
    game.start_game()
    obstaclesprites = pygame.sprite.Group()
    textsprites = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()

    def draw_pause():
        pygame.draw.rect(game.surface, (128, 128, 128, 150), [0, 0, Settings.get_settings().width_screen, Settings.get_settings().height_screen ])
        game.screen.blit(game.surface, (0, 0) )



    # These are the sprites that will be displayed on the screen.

    
    chick = PlayerSprite(name_image = 'Frog', 
                    number_frames = 2,
                    location_x = 0,
                    location_y = 350, 
                    strategy_pattern = PlayerUpdating, 
                    groups = (allsprites),
                    velocity = 3,
                    is_facing_left = False, 
                    framespeed = 0.1)
    chick.rescale_percentage(0.91)

    for _ in range(5):
        create_obstacle(width=random.randint(600, 1120), group=obstaclesprites)

    score = TextSprite(name_image = f'Score {game.score}', 
                        location_x = 0, 
                        location_y = 0,
                        groups = (textsprites, allsprites))
    
    health = TextSprite(name_image = f'Health: {chick.health}', 
                        location_x = 0, 
                        location_y = 20 + score.rect.height,
                        groups = (textsprites, allsprites)) 

    is_paused = False
    running = True

    while running:
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
            
        game.screen.blit(Settings.get_settings().background_image, (0, 0))
    
        obstaclesprites.draw(game.screen)
        allsprites.draw(game.screen)
        textsprites.draw(game.screen)
        
        if not is_paused:
            obstaclesprites.update()
            textsprites.update()
            allsprites.update()
            
        if is_paused:    
            draw_pause()


        # Use the function of spritecollide where it checks if the player object has collided with any of the Obstacle sprites
        collision_obstacles = pygame.sprite.spritecollide(chick, obstaclesprites, True)
        collision_text = pygame.sprite.spritecollide(chick, textsprites, False)
        
        # Track the deleted sprites
        #deleted_sprites = [enemy for enemy in obstaclesprites if enemy not in collision_obstacles]

        score.name_image = f'Score: {game.score}'

        if collision_obstacles:
            #print("Player collided with an enemy!")
            create_obstacle(group=obstaclesprites)
            chick.health -= 1
            health.name_image = f'Health: {chick.health}'
            health.image = health.font.render(health.name_image, False, 'black')
        
        #if chick.health == 0:
            #running = False
            #game.update_csv()
            #running=False 
