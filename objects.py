"""Creates the player character class and objects class"""
from constant_values import *
import pygame


class PlayerCharacter(pygame.sprite.Sprite):
    """
    The player character of a platformer style game

    Attributes:
        display_char: the character to display for this character
        health: how much health the character has left (out of 100)
        zest: how bored your character is (max 100)
        num_tp: number of toilet paper rolls your character has

    """
    def __init__(self, image, health=100, zest=100, num_tp=0):
        """
        Create a player character.
        """
        self.health = health
        self.zest = zest
        self.num_tp = num_tp
        self.jumping = False
        self.jump_start_time = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH_GW/2, HEIGHT_GW-k_floor_offset)
        self.pos = pygame.math.Vector2(self.rect.center[0],self.rect.center[1])
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.on_ground = True


    def jump(self):
        #jump only if standing on a platform
        if self.on_ground:
            self.vel.y = -k_initial_jump_velocity


    def update(self):
        """updates the player position based on modified x and y coordinates
        """
        self.acc = pygame.math.Vector2(0, k_gravity)
        if self.on_ground:
            self.acc.y = 0
            if self.vel.y > 0:
                self.vel.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            self.jump()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos
        #print('health',self.health)
        #print('tp', self.num_tp)


    def change_health(self, delta = 20):
        """
        Changes the health of the character

        @delta      signed integer that changes the health
        @max_health integer that represents the max health of character

        returns     True if the health change results in a value greater than zero False if the character is dead!

        Raises:
            ValueError: if delta isn't an integer #don't know how to raise errors
        """


        if self.health + delta <= k_max_health:
            self.health = self.health + delta
        # Raise ValueError if delta isn't integer
        pass

    def change_zest(self, delta = 5):
        """
        Changes the zest of the character

        @delta    signed integer that changes the zest
        @max_zest integer that represents the max zest health of character

        returns   True if the zest change results in a value less than max_zest False if the character reaches max zest and dies!

        Raises:
            ValueError: if delta isn't an integer         #don't know how to raise errors
        """
        if self.zest + delta <= k_max_zest:
            self.zest += delta

        # Raise ValueError if delta isn't integer
        pass

    def get_toilet_paper(self, num_tp):
       #you would only call this function if your hits a toilet paper. in which case, would it not be easier to just add 1 instead of having this whole function?
        """
        Gets another roll of toilet paper.
        """
        # Increase character's toilet paper by one
        self.num_tp += 1
        pass

    def restart(self):
        """resets the player after dying"""
        self.health = 100
        self.zest = 100
        self.num_tp = 0
        self.jumping = False
        self.jump_start_time = 0
        self.rect.center = (WIDTH_GW/2, HEIGHT_GW-k_floor_offset)
        self.pos = pygame.math.Vector2(self.rect.center[0],self.rect.center[1])
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.on_ground = True


class Platform(pygame.sprite.Sprite):
    """
    Platforms, including the ground, that the player character can walk on and jump off of
    """
    def __init__(self, image, x=WIDTH_GW/2, y=HEIGHT_GW-50):
        """
        Create an object.
        """
        # Initialize variables
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def restart(self):
        self.x = WIDTH_GW/2
        self.y = HEIGHT_GW-50
        self.rect.center = (self.x,self.y)


class Object(pygame.sprite.Sprite):
    """
    The different objects that interact with the player.

    Attributes:
        delta_function: the function to call when a collision occurs, ex. player.get_toilet_paper,
        delta_value: the amount that the delta_function will change a value by
        image: the image that shows up when you display the object
        x: the x-location of the object
        y: the y-location of the object

    Examples of different objects:
        toilet paper: increases toilet paper by 1
        masks: increase health by 5
        activities: decrease zest by 5
        ventilator: increases health by 100
    """
    def __init__(self, delta_function, delta_value, image, x=WIDTH_GW + k_wall_offset, y=HEIGHT_GW - k_floor_offset):
        """
        Create an object.
        """
        # Initialize variables
        self.delta_function = delta_function
        self.delta_value = delta_value
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


    def update(self):
        """updates the object position based on modified x and y coordinates
        """
        self.rect.center = (self.x,self.y)


    def contact_player(self):
        """
        Call the delta_function if the object collides with the player character

        Returns: None
        """
        self.delta_function(self.delta_value)

    def restart(self):
        """move object back to starting location after contact or reaching end of screen
        """
        self.x=WIDTH_GW + k_wall_offset
        self.y=HEIGHT_GW - k_floor_offset
