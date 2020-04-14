class PlayerCharacter:
    """
    The player character of a top-down turn-based game.

    Attributes:
        x: the x-location of the character
        y: the y-location of the character
        display_char: the character to display for this character
        health: how much health the character has left (out of 100)
        boredom: how bored your character is (max 100)
        num_tp: number of toilet paper rolls your character has

    """
    def __init__(self, x=0, y=0, display_char='@', health=100, boredom=0, num_tp=0):
        """
        Create a player character.
        """
        self.x = x
        self.y = y
        self.display_char = display_char
        self.health = health
        self.boredom = boredom
        self.num_tp = num_tp
        
        # Initialize variables
        pass

    def move(self, event): 
        """
        Moves the player character.
        DOES NOT check if the move is valid.

        Args:
            direction: one of "u"p, "d"own, "l"eft, or "r"ight, representing where the character moves 
        Raises:
            ValueError: if direction one of the characters as above
        """
        # Check if direction is valid
            # If it's not, return a value error

        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.change_vertical_position() #move up #still need to create these position functions.
        if event.key == pyfame.K_DOWN:
            self.model.change_vertical_position() #move down
        if event.key == pygame.K_LEFT:
            self.model.change_horizontal_position() #move left
        if event.key == pygame.K_RIGHT:
            self.model.change_horizontal_position() #move right
            
        # Move character one square in direction indicated

        pass

    def change_health(self, delta = 20):
        """
        Changes the health of the character
        
        @delta      signed integer that changes the health
        @max_health integer that represents the max health of character
        
        returns     True if the health change results in a value greater than zero False if the character is dead!

        Raises:
            ValueError: if delta isn't an integer #don't know how to raise errors
        """
   
        if self.health + delta <= 0:
            return False
        if self.health < = self.max_health and self.health > 0:
            self.health = self.health - delta
        return True
     
        # Raise ValueError if delta isn't integer
        pass

    def change_boredom(self, delta = 5):
        """
        Changes the boredom of the character
        
        @delta    signed integer that changes the boredom
        @max_boredom integer that represents the max boredom health of character
        
        returns   True if the boredom change results in a value less than max_boredom False if the character reaches max boredom and dies!

        Raises:
            ValueError: if delta isn't an integer         #don't know how to raise errors
        """
        if self.boredom >= self.max_boredom:
            return false
        if self.boredom > 0 and self.boredom < self.max_boredom:
            self.boredom += delta
        return True
    
        # Raise ValueError if delta isn't integer
        pass

    def get_toilet_paper(self, num_tp):
        """
        Gets another roll of toilet paper.
        """
        # Increase character's toilet paper by one
        
         self.num_tp += 1
         #you would only call this function if your hits a toilet paper. in which case, would it not be easier to just add 1 instead of having this whole function?  
        pass

class Walls:
    """
    Defines the location of a specific wall and how to display it

    Attributes:
        horizontal: boolean value representing if the wall is horizontal or vertical
        x_start: the starting x coordinate for the wall
        y_start: the starting y coordinate for the wall
        delta: the change in the horizontal or vertical direction
    """
    def __init__(self, horizontal = True, x_start = 0, y_start = 0, delta = 0):
        """
        Creates a horizontal or vertical wall

        Raises:
            ValueError if x_start, y_start, or delta are not integers
        """
        #Initialize variables
        pass

class Objects:
    """
    The different objects that interact with the player.

    Attributes:
        delta_function: the function to call when a collision occurs, ex. player.get_toilet_paper,
        delta_value: the amount that the delta_function will change a value by
        display_char: the character to display for the object
        x: the x-location of the object
        y: the y-location of the object

    Examples of different objects:
        toilet paper: increases toilet paper by 1
        masks: increase health by 5
        activities: decrease boredom by 5
        ventilator: increases health by 100
    """
    def __init__(self, delta_function, display_char, delta_value, x=0, y=0):
        """
        Create an object.
        """
        # Initialize variables
        pass

    def contact_player(self):
        """
        Call the delta_function if the object collides with the player character

        Returns: None
        """
        #Call delta_function with delta_value as argument
        pass
