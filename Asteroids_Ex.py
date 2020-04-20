"""
Pseudo Code and function declarations for a simple game of asteroids in python using PyGame
Written by Nathan Faber, Rishita Sarin, and Sam Mendel
"""
import pygame
from pygame.locals import *
import time
import math
import random


class PyGameWindowView:
    """
    A view of our Asteroids game and methods used to update the view"""

    def __init__(self, model, size):
        """
        # TODO: Make View
        # TODO: Make Screen
        # TODO: Make other graphics, (asteroids, ship, bullet)
        """
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height) """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 40)  # a fun font

    def draw(self):
        """
        Set the background to get rid of all other graphics and draw all the other things on the screen"""
        self.screen.fill(pygame.Color(0, 0, 0))  # setting play area to black
        self.draw_asteroids()
        self.draw_ship()
        self.draw_bullet()

        pygame.display.update()  # puts the new visuals on the screen

    def draw_asteroids(self):
        """
        Iterate through List of Asteroids and Draw the Asteroids
        """
        for i in self.model.asteroids:
            #draw the asteroid based on location size, and type
        # screen.register_shape(key,values)
        pass

    def draw_ship(self):
        """
        Draws shape of a ship on screen based on coordinates given
        """
        pass
        # screen.register_shape(hey, values)

    def draw_bullet(self):
        """
        Iterate through the list of bullets and Draw each one
        """
        for i in self.model.bullets:
            # Draw the bullet
        # screen.register_shape(key, values)
        pass


class space_object:
    """
    Base class that we will be using across the screen, these objects all have similar properties
    aka position, velocity, dimensions/size for collisions. etc
    Contains functions to speed up object and check for collsiosn between two objects
    """

    def __init__(self, pos_x, pos_y, vel_x, vel_y, rot_vel, deccel, colli_rad):
        """
        @pos_x      position on the screen in x
        @pos_y      position on the screen in y
        @vel_x      velocity in pixel change per second in x direction
        @vel_y      velocity in pixel change per second in x direction
        @rot_vel    rate at which the object it rotating
        @deccel     rate at which the object deccelerates (mainly for spaceship and bullets, positive for asteroids?!)
        @colli_rad  radius in which a collsion will be detected
        """
        self.pos_x = pos_x
        # etc
        pass

    def update(self, loop_rate):
        """
        function that simply does loop iterations/value changes for a space object based on the velocities, deccel
        use modulo to deal with borders
        @loop_rate      parameter to be sure that velocities map to the correct speed irl"""

        self.pos_x = + self.vel_x / loop_rate
        # etc
        pass

    def check_collision(spc_obj):
        """
        Checks an object to see if it is colliding with a passed object
        @spc_obj    object that is being checked for a collsision with
        returns     Boolean true or false if there is a collision
        """
        pass


class Asteroid(space_object):
    """
    Asteroid Class calls space object init but adds indication of which style of asteroid it is
    """

    def __init__(self, pos_x=0, pos_y=0, vel_x=0, vel_y=0, rot=0, deccel=-0.01, colli_rad=2, style=0):
        """
        See Base class for main variables
        @style      integer that indicates which style of graphic to draw(first iteration would have just one type)
        """
        super().__init__(pos_x, pos_y, vel_x, vel_y, rot, deccel, colli_rad)
        self.style = style
        pass


class Bullet(space_object):
    """
    Bullet Class calls space object init but adds indication of how far bullet has traveled
    as well as the max range that it can go
    """

    def __init__(self, pos_x=0, pos_y=0, vel_x=0, vel_y=0, rot=0, deccel=0.01, colli_rad=2, range=100):
        """
        See Base class for main variables
        @start_x   positions of the x of the bullet start
        @start_y    position of the y start of the bullet
        @range      indicates the distance that a bullet travels before erased from the screen
        """

        super().__init__(pos_x, pos_y, vel_x, vel_y, rot, deccel, colli_rad)
        self.start_x = pos_x
        self.start_y = pos_y
        self.range = range
        pass

    def update(self):
        """
        Override the super update function to update how far the bullet has traveled"""
        super().update()

    def check_distance(self):
        """
        Check to see fi the bullet has gone as far as it's range
        return False if the bullet has gotten to range(needs to be removed) or True if it should keep moving"""

        return sqrt((self.pos_x - self.start_x) ** 2 + (self.pos_y - self.start_y) ** 2) <= self.range


class Ship(space_object):
    """
    Ship Class calls space object init but adds ship parameters (see below)
    """

    def __init__(self, pos_x=0, pos_y=0, vel_x=0, vel_y=0, rot=0, deccel=0.04, colli_rad=5, max_health=100,
                 health_rate=1, max_ammo=10, relRate=1.5, bullet_vel = 3, accel=1):
        """
        See Base class for main variables
        @health         integer health that the ship has
        @ammo           number of ammo that the ship currently has
        @relRate        reload rate in bullets per second
        @bullet_vel     velocity that bullets fire from the ship in pixels/sec
        @accel          this is the amount of "Thrust" that the ship has when moving forward"""

        super().__init__(pos_x, pos_y, vel_x, vel_y, rot, deccel, colli_rad)
        self.health = max_health            # Current amount of health that the ship has
        self.max_health = max_health        # Max amount of health the ship can have
        self.health_rate = health_rate      # Rate at which health regenrates per second
        self.ammo = max_ammo                # Current amount of ammo the ship has that can be fired
        self.max_ammo = max_ammo            # Maximum amount of ammo the ship can hold
        self.relRate = relRate              # Rate at which the ship reloads it's ammo (maybe better to look at bullet list)
        self.direction = math.pi / 2        # Direction that the ship is pointing
        self.rotation_speed = 2 * math.pi   # Rotaion speed per second used for side to side rotaion
        self.accel = accel                  # Acceleration capacity of the ship (used when pressing up key)

    def change_health(self, change=5):
        """
        Changes the health of the spaceship
        @change     signed integer that changes the health
        @max_health integer that represents the max health a spaceship can have
        returns     True if the health change results in a value greater than zero False if the ship is dead!"""

        if self.health + change <= 0:
            return False
        self.health += change
        if self.health > self.max_health:
            self.health = self.max_health
        return True

    def change_ammo(self, change=-1):
        """
        Changes the amount of ammo in the spaceship
        can be used for adjusting ammo after firing and reloading
        @change     signed integer that changes amount of ammo that the ship has without going below zero
        returns     true if the operation completes succesfully, False if out of ammo"""

        if self.ammo + change < 0:
            return False
        self.ammo += change
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo
        return True

    def reset(self, new_pos_x, newpos_y):
        """
        Reset the ship to given coordinates with no velocities and full ammo etc
        @new_pos_x      represents the new position of the ship in the x
        @new_pos_y      represents the new position of the ship in the y"""

        self.pos_x = new_pos_x
        self.pos_y = new_pos_y
        self.ammo = self.max_ammo
        self.health = self.max_health
        self.direction = math.pi / 2

    def update(self, loop_rate):
        """
        Override the main update func to reload ammo and health
        @looprate   makes sure that rates (velocities are adjusted to the right speed per second"""

        super().update()
        self.change_ammo(self.rel_rate / loop_rate)
        self.change_health(self.health_rate / loop_rate)


class GameModel:
    """ Encodes a model of the game state, its functions and variables"""

    def __init__(self, size, start_asteroids):
        """
        Initialize key parameters of the game, bullet and asteroid lits and the ship
        @size               size of the screen
        @start_asteroids    indicates how many asteroids should start on the screen"""

        self.asteroids = []         # Asteroids list
        self.add_asteroids(start_asteroids)
        self.bullets = []           # Bullet List
        self.ship = Ship(20, 20, 0, 0, 0, 1, 0.04, 5, 0, 0, 10, 1.5, 3)
        self.lives = 3              # Number of lives
        self.score = 0              # Player's score
        self.width = size[0]        # Window width
        self.height = size[1]       # Window Height
        self.asteroid_rate = 3      # Asteroids spawned per second
        self.loop_rate = 100        # Number of loops per second (this may be able to be calculated)
        self.current_loop_num = 0   # keeps track of the current loop num
        self.game_over = False      # Boolesn that indicates if the game has ended
        self.paused = False         # Boolean that idicates the game is paused

    def update_all(self):
        """
        Run update funcitons to get newpositions of all objects,
        do this each loop iteration and then check for collsisions and do that cleanup
        Also spawn asteroids, and ajust score and lives etc. Spawn asteroid every give amount of loops or time"""

        if not self.paused:
            for asteroid in self.asteroids:
                asteroid.update(self.loop_rate)
            for bullet in self.bullets:
                bullet.update(self.loop_rate)
            self.ship.update(self.loop_rate)

            # Now check for bullet collisions (may be prolems with deleting from the list you are iterating through)
            for asteroid in self.asteroids:
                for bullet in self.bullets:
                    # For bullet collisions with asteroids split the asteroid
                    if bullet.collision(asteroid):
                        # THen split the asteroid and give points and remove the bullet
                        self.asteroid_split(asteroid)
                        self.change_score(20)
                        del bullet
                        # Go to the next bullet
                        continue

            # Now check ship collisions
            for asteroid in self.asteroids:
                if self.ship.collision(asteroid):
                    self.change_score(20)
                    # THen split then remove the asteroid and give points and remove health
                    if not self.ship_change_health(2 * asteroid.colli_rad):
                        if not self.change_lives(-1):
                            # Game over
                            self.game_over = True
                            break
                        self.ship.health = self.ship.max_health
                        del asteroid
                    continue  # Go to the next bullet

            # Spawn in asteroids
            if self.current_loop_num / self.loop_rate % self.asteroid_rate == 0:
                self.add_asteroids(1)


def fire(self):
    """
    Fire a bullet. Make sure that there is ammo before firing a bullet
    add a bullet to the list and assign the correct velocities"""

    if self.ship.change_ammo(-1):
        bull_vel = self.ship.bullet_vel
        ship_dir = self.ship.direction
        bullet_vel_x = bull_vel * math.cos(ship_dir)
        bullet_vel_y = bull_vel * math.sin(ship_dir)
        new_bullet = Bullet(pos_x=self.pos_x, pos_y=self.pos_y, vel_x=self.vel_x + bullet_vel_x,
                            vel_y=self.vel_y + bullet_vel_y)
        self.bullets.append(new_bullet)


def add_asteroids(self, num_asteroids, berth=20, pos_x=None, pos_y=None, size=None):
    """
    Add asteroids to the game (aka new object in the list)
    Generates random position that is more than the berth away from the ship(in a box)
    Also generates random velocities, rotation, size, style, etc.
    These ranges could be stored in a level dictionary so that it get's harder as you continue one
    @num_asteroids      number of asteroids to spawn
    @berth              minimum space away(radius) from the ship that asteroids must spawn
    @ast_x              optional parameter to spawn asteroids at one place(for when asteroids are split)
    @ast_y              ^^^"""

    for asteroid in range(num_asteroids):
        if ast_x is None and ast_y is None:
            # Get random location on screen
            x_range = self.width - berth * 2
            y_range = self.height - berth * 2
            ast_x = random.randint(0, x_range + 1)
            ast_y = random.randint(0, y_range + 1)
            if ast_x > self.ship.pos_x - berth
                ast_x += berth * 2
            if ast_y > self.ship.pos_y - berth
                ast_y += berth * 2
        # Get random velocities (could be tied to level)
        x_vel = random.rand(0, 1)
        y_vel = random.rand(0, 1)
        # Get random angular rotation
        rot = random.rand(-1, 1)
        # Get Random Acceleration
        accel = random.rand(-.1, .5)
        # Get random size for asteroid if not specified
        if size is None:
            size = random.randint(4, 21)
        # Get random type of asteroid
        ran_style = random.rand(0, 11)
        # Add the asteroid to the list
        new_asteroid = Asteroid(pos_x=ast_x, pos_y=ast_y, vel_x=x_vel, vel_y=y_vel, rot=rot, deccel=accel,
                                colli_rad=size, style=ran_style)
        self.asteroids.append(new_asteroid)


def asteroid_split(self, asteroid):
    """
    Split the asteroid into smaller asteroids if they are not too small and remove asteroid"""
    splits = 2
    if self.colli_rad < 5:
        splits = 0
    for i in range(splits):
        self.add_asteroids(splits, None, asteroid.pos_x, asteroid.pos_y, asteroid.colli_rad / 2)
    # Delete the asteroid that is split
    del asteroid
def change_score(self, change):
    """
    Changes the score by the amount specified
    @change     amount by which to change the score"""
    self.score += change
def change_lives(self, change):
    """
    Change the amount of lives the perosn
    @change     integer amount to change the number of lives

    returns     True if successfull and False if at zero lives"""
    self.lives += change
    if self.lives <= 0:
        return False
    return True
def clear_screen(self):
    """
    Gets rid off all asteroids and bullets by setting them to empty lists and resets player to center of screen"""
    self.asteroids = []
    self.bullets = []
    self.ship.reset()
def change_ship_velocity(self):
    """COULD BE MOVED TO SHIP CLASS
    Change the velocity in the direction the spaceship is pointing(deocmpose to x and y)"""
    dir = self.ship.direction
    self.ship.vel_y += self.ship.accel * math.sin(dir)
    self.ship.vel_x += self.ship.accel * math.cos(dir)
def change_ship_rotation(self, rot_dir):
    """COULD BE MOVED TO SHIP CLASS
    changes the rotation by a very small increment (rotationspeed radians per sec / loop_rate loops per second)
    @rot_dir        a 1 or -1 that indicates which way to rotate"""
    self.ship.direction = (self.ship.direction + rot_dir * self.ship.rotation_speed / self.loop_rate) % 2 * math.pi
class PyGameKeyboardController:
    """ Handles keyboard input for moving the ship and firing etc"""
    def __init__(self, model):
        self.model = model
    def handle_event(self, event):
        """
        Capture events for ship acceleration and rotation (arrow keys)
        Also add a pause button"""
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.change_ship_velocity()
        if event.key == pygame.K_LEFT:
            self.model.change_rotation(1)
        if event.key == pygame.K_RIGHT:
            self.model.change_ship_rotation(-1)
        if event.key == pygame.K_SPACE:
            self.model.fire
        if event.key == pygame.K_p:
            self.model.paused = not self.model.paused
"""
Main Game Loop Function
 """
if __name__ == '__main__':
    pygame.init()  # important for starting up a project using pygame
    size = (300, 300)
    model = GameModel(size)  # makes an instance of a model, other classes use it
    print(model)  # this shows the state of the grid at startup
    view = PyGameWindowView(model, size)
    controller = PyGameKeyboardController(model)

    while not model.game_over:  # we use a while loop to keep the game going until users exit
        for event in pygame.event.get():  # events can be key or mouse clicks etc
            if event.type == QUIT:
                running = False
            controller.handle_event(event)  # a controller has its own way to handle events
        # update our model even if no keyboard input
        model.update_all
        view.draw()
        time.sleep(.001)  # this paces our program a bit

    pygame.quit()  # we get here only if the QUIT event breaks the while loop above