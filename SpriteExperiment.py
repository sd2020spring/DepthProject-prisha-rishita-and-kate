#https://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
#https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/
#https://kidscancode.org/blog/2016/08/pygame_1-3_more-about-sprites/
#isinstance(sprite, BaseItem) Steve mentioned that this could be useful...

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

#list of images of objects which decrease boredom
dec_bore_objs = [guitar, paint, egg, social]

# initialize pygame and create window
pygame.init()
game_screen = pygame.display.set_mode((WIDTH_GW, HEIGHT_GW))
pygame.display.set_caption("COVID-19 Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


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

	def update(self): #if this is randomly selected for all objects, we can prob form this func outside and call in each class
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

class DecreaseBoredom(pygame.sprite.Sprite) #common sprite for all objects which decrease boredom
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = random.choice(dec_bore_objs) #pick randomly from a list of images of objects
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = #randomly place object on screen


# class Guitar(pygame.sprite.Sprite): #sprite for guitar
#     	def __init__(self):
#       		pygame.sprite.Sprite.__init__(self)
#       		self.image = guitar_img
# 	        self.image.set_colorkey(BLACK)
#       		self.rect = self.image.get_rect()
#       		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized

# class PaintBrush(pygame.sprite.Sprite): #sprite for paint brush
# 	def __init__(self):
#       		pygame.sprite.Sprite.__init__(self)
#       		self.image = paint_img
# 		self.image.set_colorkey(BLACK)
#       		self.rect = self.image.get_rect()
#      		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized

# class Egg(pygame.sprite.Sprite): #sprite for egg
#     	def __init__(self):
# 		pygame.sprite.Sprite.__init__(self)
# 	      	self.image = egg_img
# 		self.image.set_colorkey(BLACK)
# 	     	self.rect = self.image.get_rect()
# 	      	self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized

# class SocialMedia(pygame.sprite.Sprite): #sprite for social media
#     	def __init__(self):
# 		pygame.sprite.Sprite.__init__(self)
#       		self.image = social_img
# 	   	self.image.set_colorkey(BLACK)
#      		self.rect = self.image.get_rect()
#       		self.rect.center = (WIDTH_GW / 2, HEIGHT_GW / 2) #this needs to be randomized

#it may be worth exploring collision of sprites with this code...
BoredomCollisison = pygame.sprite.spritecollide(player, DecreaseBoredom, False)
if BoredomCollisison:
    change_zest(self, delta = 5) # this function is in the objects.py

SickCollision = pygame.sprite.spritecollide(player, SickPerson, False)
if SickCollision:
    change_health(self, delta = 20) # this function is in the objects.py

TPCollision =  pygame.sprite.spritecollide(player, TP, False)
if TPCollision:
	get_toilet_paper(self, num_tp) #this function is in the objects.py

MaskCollision = pygame.sprite.spritecollide(player, Mask, False)
if MaskCollision:
	#write function for this

VentilatorCollision = pygame.sprite.spritecollide(player, Ventilator, False)
if VentilatorCollision:
	#write function for this

# Game Loop
running = True
while running:
    # Process input (events)

    # Update
   # Update
    all_sprites.update() #group of all sprites are updated

    # keep loop running at the right speed
    clock.tick(FPS)

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen) #all updated sprites drawn

    # after drawing everything, flip the display to make it visible to viewer
    pygame.display.flip()


# objects should move front and back on screen?
#check for collision between player and others
	#if collides with toilet paper - points increase

	#if collides with sick person - health decrease
	#if collides with mask - health increase
	#if collides with ventilator - health increase x2

	#if collides with guitar, paint brushes, eggs, or social media - entertainment increase
