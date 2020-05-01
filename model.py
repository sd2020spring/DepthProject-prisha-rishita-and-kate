'''Model Class that runs the game, and code that creates an instance of the model'''
#https://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
#https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/
#https://kidscancode.org/blog/2016/08/pygame_1-3_more-about-sprites/
#isinstance(sprite, BaseItem) Steve mentioned that this could be useful...
from objects import *
import random
import pygame
import datetime
import os

#constant values
k_default_move_value = 1
k_intial_jump_velocity = .5
k_gravity = -9.8
k_max_health = 100
k_max_zest = 100
k_floor_offset = 200
k_wall_offset = 50
WIDTH_GW = 1024  # width of our game window
HEIGHT_GW = 600 # height of our game window
FPS = 30 # frames per second - try and do dynamically?
BLACK = (0,0,0)
PLAYER_ACC = 3
PLAYER_GRAV = 0
PLAYER_FRICTION = -.5

class Model:
    """
    Updates the game based on Controller input.
    """
    def __init__(self, num_tp = 5, num_sick_people = 3, num_masks = 4, num_eggs = 4):
        '''
        platform_list: list of each platform object to be used for finding where they are
        platform_locations: dictionary of each platforms corners format {'left_bound', 'right_bound', 'top_bound', 'bottom_bound'}
        object_list: list of each object object to be used for finding where they are
        available_objects: objects that aren't currently on screen, and could be on screen
        unavailable_objects: the opposite of available_objects, all objects are in one or the other of
        these lists.
        object_locations: dictionary of each object corners format {'left_bound', 'right_bound', 'top_bound', 'bottom_bound'}
            - should probably figure out if characters are also going to have the same properties as objects or
              if they are going to move around and stuff like that.
        '''

        # initialize pygame and create window
        pygame.init()
        self.game_screen = pygame.display.set_mode((WIDTH_GW, HEIGHT_GW))
        pygame.display.set_caption("COVID-19 Game")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()

        # set up asset folders
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        player_img = pygame.image.load(os.path.join(img_folder, 'human.jpg')).convert()
        tp_img = pygame.image.load(os.path.join(img_folder, 'tp.jpg')).convert()
        sick_img = pygame.image.load(os.path.join(img_folder, 'sick.png')).convert()
        egg_img = pygame.image.load(os.path.join(img_folder, 'egg.png')).convert()
        mask_img = pygame.image.load(os.path.join(img_folder, 'mask.jpg')).convert()
        '''guitar = pygame.image.load(os.path.join(img_folder, 'guitar.png')).convert()
        paint = pygame.image.load(os.path.join(img_folder, 'paint.png')).convert()
        social = pygame.image.load(os.path.join(img_folder, 'social.png')).convert()
        ventilator_img = pygame.image.load(os.path.join(img_folder, 'ventilator.png')).convert()'''

        self.platform_list = []
        self.platform_locations = []
        self.object_list = []
        self.available_objects = []
        self.unavailable_objects = []
        self.object_locations = []
        self.player_character = PlayerCharacter(player_img)
        self.events = pygame.event.get()

        for tp in range(num_tp):
            self.object_list.append(Object(self.player_character.get_toilet_paper, 1, tp_img))
        for sick_people in range(num_sick_people):
            self.object_list.append(Object(self.player_character.corona_contracted, 15, sick_img))
        for mask in range(num_masks):
            self.object_list.append(Object(self.player_character.health_improvement, 5, mask_img))
        for egg in range(num_eggs):
            self.object_list.append(Object(self.player_character.change_zest, 5, egg_img))
        for object in self.object_list:
            self.all_sprites.add(object)
            self.object_sprites.add(object)
        self.all_sprites.add(self.player_character)
        self.available_objects = self.object_list.copy()


    def run(self):
        """
        Get input from controller, evaluate what to do based on the input and current
        game state.
        Handles collisions between the player and objects.
        """
        #update any inputs, as well as check if the game has been closed
        self.events = pygame.event.get()

        #make sure we aren't dead before doing anything else
        if self.player_character.health > 0 and self.player_character.zest > 0:
            #EVERYTHING DEALING WITH OBJECTS:
            #choose to add an object to screen
            if (random.randint(0,100) == 0) and (len(self.available_objects) > 0):
                #potentially need to add thing to show the object
                object_to_move = self.available_objects[random.randint(0,len(self.available_objects)-1)]
                self.available_objects.remove(object_to_move)
                self.unavailable_objects.append(object_to_move)
            #move each object that is on screen
            for object in self.unavailable_objects:
                object.x -= k_default_move_value
                #if the object has reached the edge of the screen, remove it
                if object.x <=0:
                    #potentially need to add a thing to hide the object
                    self.unavailable_objects.remove(object)
                    self.available_objects.append(object)
                    object.restart()

            object_collissions = pygame.sprite.spritecollide(self.player_character, self.object_sprites, False)
            for object in object_collissions:
                if object in self.unavailable_objects:
                    self.unavailable_objects.remove(object)
                    self.available_objects.append(object)
                object.contact_player()
                object.restart()


            #update pygame display
            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Draw / render
            self.all_sprites.update()
            self.game_screen.fill(BLACK)
            self.all_sprites.draw(self.game_screen)
            # after drawing everything, flip the display to make it visible to viewer
            pygame.display.flip()


if __name__ == '__main__':
    model = Model()
    running = True
    while running:
        model.run()
        for event in model.events:
            if event.type == pygame.QUIT:
                running = False
