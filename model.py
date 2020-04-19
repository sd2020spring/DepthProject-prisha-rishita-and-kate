'''This should likely be renamed as something that is more descriptive, but this is my best guess
for a name based on mp4'''
from objects import *
import random
import pygame
import datetime

k_default_move_value = 1
k_intial_jump_velocity = .5
k_gravity = -9.8

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
        self.platform_list = []
        self.platform_locations = []
        self.object_list = []
        self.available_objects = []
        self.unavailable_objects = []
        self.object_locations = []
        self.player_character = PlayerCharacter()

        for tp in range(num_tp):
            self.object_list.append(Object(self.player_character.get_toilet_paper, 1, 'tp'))
        for sick_people in range(num_sick_people):
            self.object_list.append(Object(self.player_character.change_health, 15, 'sick person'))
        for mask in range(num_masks):
            self.object_list.append(Object(self.player_character.change_health, 5, 'mask'))
        for egg in range(num_eggs):
            self.object_list.append(Object(self.player_character.change_zest, 5, 'egg'))

        self.available_objects = self.object_list.copy()

    def run(self):
        """
        Get input from controller, evaluate what to do based on the input and current
        game state.
        Handles collisions between the player and objects.
        """
        #make sure we aren't dead first
        if player_character.health > 0 and player_character.zest > 0:
            #EVERYTHING DEALING WITH OBJECTS:
            #choose to add an object to screen
            if random.randint(0,10) == 0:
                #potentially need to add thing to show the object
                object_to_move = available_objects[random.randint(0,len(available_objects))]
                available_objects.remove(object_to_move)
                unavailable_objects.append(object_to_move)
            #move each object that is on screen
            for object in unavailable_objects:
                object.x -= k_default_move_value
                #if the object has reached the edge of the screen, remove it
                if object.x <=-3: #CHANGE NUMBER LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #potentially need to add a thing to hide the object
                    unavailable_objects.remove(object)
                    available_objects.append(object)
                    object.x = 270 #CHANGE THIS NUMBER TO THE EDGE OF THE SCREEN
                    object.y = 320 #ALSO CHANGE THIS
            #EVERTHING DEALING WITH THE PLAYER

            if event.key == pygame.K_LEFT:
                self.player_character.x -= k_default_move_value
            if event.key == pygame.K_RIGHT:
                self.player_character.x += k_default_move_value
            if event.key == pygame.K_UP:
                self.player_character.jumping = True
                self.player_character.jump_start_time = datetime.time.seconds
            if self.player_character.jumping:
                delta_t = datetime.time.seconds - self.player_character.jump_start_time
                y = (k_intial_jump_velocity*delta_t) + (.5*k_gravity*(delta_t**2))


    def update_locations(self):
        '''
        Go through each platform and object and update its location.
        This should at some point check to see if the object is still on the screen
        and remove any objects from the list that are no longer on the screen. maybe?
            - platform.location is likely a placeholder name and probably will be changed once
              the platform class is made.
            - location should be a dictionary of the bounds

        Returns: None
        '''
        self.platform_locations = []
        for platform in self.platform_list:
            self.platform_locations.append(platform.location)
        self.object_locations = []
        for object in self.object_list:
            self.object_locations.append(object.location)
        pass


    def motions_possible(self, character_object, delta):
        '''
        Takes a character object, and evaluates in which directions motion is motions_possible
        based on platform locations.
        Delta: how far to check in each direction if the character can move.

        Returns: a dictionary containing each direction and a boolean value of if it can move
        there or not
            -this could also check if a character is going to run into the player character in the
             case of sick people too, need to consider more
            -i also included up as a direction of motion, not sure if this is needed or not?
            -character object location should be in the same format with the corners
            - also it feels like there has to be a better way of checking if they are intersecting but idk what
            - this is also assuming that the top left corner is 0,0
        '''
        current_location = character_object.location
        directions = {'left':True, 'right':True, 'up':True, 'down':True}
        for platform in self.platform_locations:
            #check if it can move left/right
            if (current_location['top_bound'] in range(platform['top_bound'],platform['bottom_bound']) or
                        current_location['bottom_bound'] in range(platform['top_bound'],platform['bottom_bound'])):
                if current_location['left_bound'] - delta in range(platform['left_bound'],platform['right_bound']):
                    directions['left'] = False
                elif current_location['right_bound'] + delta in range(platform['left_bound'],platform['right_bound']):
                    directions['right'] = False
            #check if it can move up/down
            if (current_location['left_bound'] in range(platform['left_bound'],platform['right_bound']) or
                        current_location['right_bound'] in range(platform['left_bound'],platform['right_bound'])):
                if current_location['top_bound'] - delta in range(platform['top_bound'],platform['bottom_bound']):
                    directions['up'] = False
                elif current_location['bottom_bound'] + delta in range(platform['top_bound'],platform['bottom_bound']):
                    directions['down'] = False
        return directions

if __name__ == '__main__':
    model = Model()
