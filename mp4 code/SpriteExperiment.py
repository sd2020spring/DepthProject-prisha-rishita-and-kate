#https://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
#https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/
#https://kidscancode.org/blog/2016/08/pygame_1-3_more-about-sprites/

import pygame
import random
import os

WIDTH_GW = 360  # width of our game window
HEIGHT_GW = 480 # height of our game window
FPS = 30 # frames per second
BLACK = (0,0,0)

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'human.png')).convert()
tp_img = pygame.image.load(os.path.join(img_folder, 'tp.png')).convert()
sick_img = pygame.image.load(os.path.join(img_folder, 'sick.png')).convert()
ventilator_img = pygame.image.load(os.path.join(img_folder, 'ventilator.png')).convert()
mask_img = pygame.image.load(os.path.join(img_folder, 'mask.png')).convert()
guitar = pygame.image.load(os.path.join(img_folder, 'guitar.png')).convert()
paint = pygame.image.load(os.path.join(img_folder, 'paint.png')).convert()
egg = pygame.image.load(os.path.join(img_folder, 'egg.png')).convert()
social = pygame.image.load(os.path.join(img_folder, 'social.png')).convert()

# initialize pygame and create window
pygame.init()
game_screen = pygame.display.set_mode((WIDTH_GW, HEIGHT_GW))
pygame.display.set_caption("COVID-19 Game")
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
    # Process input (events)
    
    # Update
    
    # keep loop running at the right speed
    clock.tick(FPS)
    
    # Draw / render
    screen.fill(BLACK)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()
    
    
class Player(pygame.sprite.Sprite): #sprite for player
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2)
		self.speedx = 0
		#self.speedy = 0
		
	def update(self, event):
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
		if event.key == pygame.K_LEFT:#move left
		    player.speedx = -5
		if event.key == pygame.K_RIGHT: #move right
		    player.speedx = 5
		#if event.key == pygame.K_UP:
		    #player.speedy = 5 #move up 
		#if event.key == pyfame.K_DOWN:
		    #player.speedy = -5 #move down

	
class TP(pygame.sprite.Sprite): #sprite for toilet paper
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
      		self.image = tp_img
	    	self.image.set_colorkey(BLACK)
    		self.rect = self.image.get_rect()
      		self.rect.x = random.randrange(WIDTH_GW - self.rect.width) #TP will randomly appear in the GW frame
        	self.rect.y = random.randrange(0, 50) #TP will stay near ground since we are working on non platformer version
        	self.speedx = random.randrange(-5, 5) #TP will move around screen 
		
	def update(self):
        	self.rect.x += self.speedx #speed in x direction gets randomized
        	if self.rect.top > HEIGHT_GW:
		    self.rect.x = random.randrange(WIDTH_GW - self.rect.width)
		    self.rect.y = random.randrange(0, 50)
		    self.speedx = random.randrange(-5, 5)

class SickPerson(pygame.sprite.Sprite): #sprite for sick person
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
      		self.image = sick_img
		self.image.set_colorkey(BLACK)
      		self.rect = self.image.get_rect()
      		self.rect.x = random.randrange(WIDTH_GW - self.rect.width) #TP will randomly appear in the GW frame
        	self.rect.y = random.randrange(0, 50) #TP will stay near ground since we are working on non platformer version
        	self.speedx = random.randrange(-5, 5) #TP will move around screen 
		
	def update(self): #same movement as TP for the time being
        	self.rect.x += self.speedx #speed in x direction gets randomized
        	if self.rect.top > HEIGHT_GW:
		    self.rect.x = random.randrange(WIDTH_GW - self.rect.width)
		    self.rect.y = random.randrange(0, 50)
		    self.speedx = random.randrange(-5, 5)

class Ventilator(pygame.sprite.Sprite): #sprite for ventilator
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
      		self.image = ventilator_img
	    	self.image.set_colorkey(BLACK)
     		self.rect = self.image.get_rect()
      		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized

class Mask(pygame.sprite.Sprite): #sprite for mask
    	def __init__(self):
     		pygame.sprite.Sprite.__init__(self)
      		self.image = mask_img
	    	self.image.set_colorkey(BLACK)
      		self.rect = self.image.get_rect()
      		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized
	
class Guitar(pygame.sprite.Sprite): #sprite for guitar
    	def __init__(self):
      		pygame.sprite.Sprite.__init__(self)
      		self.image = guitar_img
	        self.image.set_colorkey(BLACK)
      		self.rect = self.image.get_rect()
      		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized
	
class PaintBrush(pygame.sprite.Sprite): #sprite for paint brush
	def __init__(self):
      		pygame.sprite.Sprite.__init__(self)
      		self.image = paint_img
		self.image.set_colorkey(BLACK)
      		self.rect = self.image.get_rect()
     		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized
	
class Egg(pygame.sprite.Sprite): #sprite for egg
    	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
	      	self.image = egg_img
		self.image.set_colorkey(BLACK)
	     	self.rect = self.image.get_rect()
	      	self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized
	
class SocialMedia(pygame.sprite.Sprite): #sprite for social media
    	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
      		self.image = social_img
	   	self.image.set_colorkey(BLACK)
     		self.rect = self.image.get_rect()
      		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized

	
#add sprite for toilet paper, sick person, ventilator, mask, guitar, paint brushes, eggs, and social media
#all of these except player should be randomly placed but not on each other- should be randomly placed
# objects should move front and back on screen?
#player should move based on keyboard movements
#check for collision between player and others
	#if collides with toilet paper - points increase
	
	#if collides with sick person - health decrease
	#if collides with mask - health increase
	#if collides with ventilator - health increase x2
	
	#if collides with guitar, paint brushes, eggs, or social media - entertainment increase
#talked with NINJA, in update function, you can randomly choose a sprite and add it to a list and those in the list will appear on screen
