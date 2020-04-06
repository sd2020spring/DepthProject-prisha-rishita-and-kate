class View:
    """
    A textual representation of the current state of the game.

    Attributes:
        model: the game state to display
    """
    def __init__(self, model):
        """
        Create an instance of the game view.

        Args:
            model: the game state to display
        """
        self.model = model

    def draw(self):
        """
        Draw the representation of the game state.

        Looks something like this:

        # # # # # # # #    HEALTH:      100
        # _ _ @ _ _ _ #    BOREDOM:     25
        # _ _ _ _ _ o #    TOILETPAPER: 2
        # _ P _ _ _ _ #
        # _ _ _ _ _ _ #
        # # # # # # # #

        Returns:
            A string representing the current state of the game (print to display)
        """
        # Iterate through the tiles and add the corresponding character for each one
            # Add newlines/spaces as appropriate
            # For the first three rows also display health/boredom/tp as above

        # Return the string
        pass

class Controller:
    """
    Controller Lets people interact with the model and updates the view.

    Attributes:
        model: the game state model.
        view: the view of the game.
    """

    def __init__(self):
        """
        Create an instance of the controller.
        """
        # Create a new game room.
            # Randomly/procedurally place objects/people in the room

        # Create a view of the game state
        pass

    def run(self):
        """
        Gets input for moving the player and passes on to the model.

        Returns: None.
        """
        #Allow user to use arrow keys to move their player around the board.

        # Check if a move is valid and allow it if it is. If a move is onto an object,
        # let the model call the object's collision function.

        pass

class Model:
    """
    Updates the game based on Controller input.
    """
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
