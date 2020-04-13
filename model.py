'''This should likely be renamed as something that is more descriptive, but this is my best guess
for a name based on mp4'''

class Model:
    """
    Updates the game based on Controller input.
    """
    def __init__(self):
        '''
        platform_list: list of each platform object to be used for finding where they are
        platform_locations: dictionary of each platforms corners format {'left_bound', 'right_bound', 'top_bound', 'bottom_bound'}
        object_list: list of each object object to be used for finding where they are
        object_locations: dictionary of each object corners format {'left_bound', 'right_bound', 'top_bound', 'bottom_bound'}
            - should probably figure out if characters are also going to have the same properties as objects or
              if they are going to move around and stuff like that.
        '''
        self.platform_list = []
        self.platform_locations = []
        self.object_list = []
        self.object_locations = []


    def run(self):
        """
        Get input from controller, evaluate what to do based on the input and current
        game state.
        Handles collisions between the player and objects.
        """
        #While the health value is > 0 and the boredom value is < 100, get input from
        #controller, eventually will check if moves are valid based on if the player
        #is contacting any walls.

        #Update player health, boredom, and toilet paper values if contacting any
        #objects or other characters.
        pass


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
        for object in self.platform_list:
            self.platform_locations.append(object.location)
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
