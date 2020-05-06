"""Creates the player character class and game_items class"""
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
        self.rect.center = (WIDTH_GW/2, HEIGHT_GW-k_ground_height-k_game_item_offset)
        self.pos = pygame.math.Vector2(self.rect.center[0],self.rect.center[1])
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.on_ground = True

    def move(self,direction, value = PLAYER_ACC):
        """ move player
        direction: string - 'left', 'right', 'up' 'stop_horizontal'
        """
        if direction == 'left':
            self.acc.x = -value
        elif direction == 'right':
            self.acc.x = value
        elif direction == 'up':
            self.acc.y = k_gravity
            if self.on_ground:
                self.vel.y = -k_initial_jump_velocity
        elif direction == 'down':
            if self.pos.y < HEIGHT_GW - k_ground_height - k_game_item_offset:
                self.acc.y = k_gravity + k_drop_acceleration
            else:
                self.acc.y = 0
                self.vel.y = 0
        elif direction == 'stop_horizontal':
            self.acc.x = 0
        elif direction == 'stop_vertical':
            self.acc.y = k_gravity
            if self.on_ground:
                self.acc.y = 0
                if self.vel.y > 0:
                    self.vel.y = 0

    def update(self):
        """updates the player position based on modified x and y coordinates
        """
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos


    def change_health(self, delta = 20):
        """
        Changes the health of the character

        @delta      signed integer that changes the health
        @max_health integer that represents the max health of character

        returns     True if the health change results in a value greater than zero False if the character is dead!
        """


        if self.health + delta <= k_max_health:
            self.health = self.health + delta
        else:
            self.health = k_max_health

    def change_zest(self, delta = 5):
        """
        Changes the zest of the character

        @delta    signed integer that changes the zest
        @max_zest integer that represents the max zest health of character

        returns   True if the zest change results in a value less than max_zest False if the character reaches max zest and dies!
        """
        if self.zest + delta <= k_max_zest:
            self.zest += delta
        else:
            self.zest = k_max_zest

    def get_toilet_paper(self, num_tp):
       #you would only call this function if your hits a toilet paper. in which case, would it not be easier to just add 1 instead of having this whole function?
        """
        Gets another roll of toilet paper.
        """
        # Increase character's toilet paper by one
        self.num_tp += num_tp 

    def bounce_away_from_sickness(self,x_amount):
        """moves back a direction when hit by a sick person"""
        self.pos.x += x_amount

    def restart(self):
        """resets the player after dying"""
        self.health = 100
        self.zest = 100
        self.num_tp = 0
        self.jumping = False
        self.jump_start_time = 0
        self.rect.center = (WIDTH_GW/2, HEIGHT_GW-k_ground_height-k_game_item_offset)
        self.pos = pygame.math.Vector2(self.rect.center[0],self.rect.center[1])
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.on_ground = True


class Ground(pygame.sprite.Sprite):
    """
    Ground that the player character can walk on and jump off of
    """
    def __init__(self, image, x=WIDTH_GW/2, y=HEIGHT_GW-k_ground_height):
        """
        Create an game_item.
        """
        # Initialize variables
        self.x = x
        self.y = y
        self.init_x = x
        self.init_y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def restart(self):
        self.x = self.init_x
        self.y = self.init_y
        self.rect.center = (self.x,self.y)


class Platform(Ground):
    def update(self):
        self.rect.center = (self.x,self.y)


class Game_Item(pygame.sprite.Sprite):
    """
    The different game_items that interact with the player.

    Attributes:
        delta_function: a list of the functions to call when a collision occurs, ex. player.get_toilet_paper,
        delta_value: a list of the amounts that each delta_function will change a value by
        image: the image that shows up when you display the game_item
        x: the x-location of the game_item
        y: the y-location of the game_item

    Examples of different game_items:
        toilet paper: increases toilet paper by 1
        masks: increase health by 5
        activities: decrease zest by 5
        ventilator: increases health by 100
    """
    def __init__(self, delta_function, delta_value, image, x=WIDTH_GW + k_wall_offset, y=HEIGHT_GW - k_ground_height-k_game_item_offset):
        """
        Create an game_item.
        """
        # Initialize variables
        self.delta_function = delta_function
        self.delta_value = delta_value
        self.pos = pygame.math.Vector2(x,y)
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def update(self):
        """updates the game_item position based on modified x and y coordinates
        """
        self.rect.center = self.pos


    def contact_player(self):
        """
        Call the delta_function if the game_item collides with the player character

        Returns: None
        """
        n = 0
        for function in self.delta_function:
            function(self.delta_value[n])
            n += 1


    def restart(self):
        """move game_item back to starting location after contact or reaching end of screen
        """
        self.pos.x=WIDTH_GW + k_wall_offset
        self.pos.y=HEIGHT_GW - k_ground_height - k_game_item_offset

class Sick_People(Game_Item):
    """ sick people that move if contacting player and can fall off platforms"""
    def __init__(self,delta_function, delta_value, image, x=WIDTH_GW + k_wall_offset, y=HEIGHT_GW - k_ground_height):
        super().__init__(delta_function, delta_value, image, x=WIDTH_GW + k_wall_offset, y=HEIGHT_GW - k_ground_height)
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.on_ground = True

    def update(self):
        """check if on the ground, and fall if not"""
        self.acc = pygame.math.Vector2(0,k_gravity)
        if self.on_ground:
            self.acc.y = 0
            if self.vel.y > 0:
                self.vel.y = 0
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
