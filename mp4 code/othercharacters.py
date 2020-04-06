class SickPeople:
    """
    The sick people that must be avoided by the character

    Attributes:
        x_dir: the x coordinate of the sick
        y_dir: the y coordinate of the sick
        size: the number of sick people in that area
        sick_view: actual representation of the sick
        neg_health: health that it decreases when they come into contact
    """
    def __init__(self, x_dir=0, y_dir=0, size=0, sick_view='@', neg_health=-5)
        """
        Creates the sick people
        """
        # initialize the variables of the sick people
        pass

    def move(self, direction)
        """
        Moves the sick people in a random direction
        """
        # unlike the main character, the sick move in a random direction
            #sometimes stand still
        # have to be avoided by the main character or they lose health
        pass

    def num_sicks(self, size, x_coor, y_coor):
        """
        Chooses the number of sick people in a certain x & y coordinate

        Args:
            size: the number of sick people
        """
        # number of sick people is chosen to increase difficulty

        pass

    def decrease_health(main_char, delta):
        """
        Decreases the health of the main character by delta

        Args:
            delta: the amount of main character's health changes by
        """
        # decreases main character's health
        pass


class Doctors:
    """
    The doctors that can help the the main character

    Attributes:
        x_dir: the x coordinate of the doctors
        y_dir: the y coordinate of the doctors
        size: the number of doctors in that area
        pos_health: boost in health when main character comes into contact
    """
    def __init__(self, x_dir=0, y_dir=0, size=0, neg_health=0)
        """
        Creates the doctors
        """
        # initialize the variables of the doctors
        pass

    def move(self, direction)
        """
        Doctors are in certain areas of the game to increase main character's health
        """
        # helps the main character

        pass

    def num_doctors(self, size, x_coor, y_coor):
        """
        Chooses the number of doctors in a certain x & y coordinate

        Args:
            size: the number of doctors
            x_coor: x coordinate of the doctors
            y_coor: y coordinate of the doctors
        """
        # number of doctors is chosen to increase/decrease difficulty
        # doctors are set to a specific location, they aren't wandering around
        
        pass

    def increase_health(main_char, delta):
        """
        increases the health of the main character by delta

        Args:
            delta: the amount of main character's health changes by
        """
        # increases main character's health
        pass
