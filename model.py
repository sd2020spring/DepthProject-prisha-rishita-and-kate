'''Model Class that runs the game, and code that creates an instance of the model'''
#https://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
#https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/
#https://kidscancode.org/blog/2016/08/pygame_1-3_more-about-sprites/
#isinstance(sprite, BaseItem) Steve mentioned that this could be useful...
from objects import *
from constant_values import *
import random
import pygame
import time
import os


class Model:
    """
    Updates the game based on Controller input.
    """
    def __init__(self, num_tp = 5, num_sick_people = 8, num_masks = 4, num_eggs = 3, num_guitars = 3, num_paint = 3, num_vent = 1):
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
        self.platform_sprites = pygame.sprite.Group()
        self.sick_sprites = pygame.sprite.Group()
        self.game_over = False

        # set up asset folders
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        player_img = pygame.image.load(os.path.join(img_folder, 'ryangosling.png')).convert_alpha()
        tp_img = pygame.image.load(os.path.join(img_folder, 'tp.png')).convert_alpha()
        sick_img = pygame.image.load(os.path.join(img_folder, 'sickperson.png')).convert_alpha()
        egg_img = pygame.image.load(os.path.join(img_folder, 'eggnflour2.png')).convert_alpha()
        mask_img = pygame.image.load(os.path.join(img_folder, 'mask.png')).convert_alpha()
        ground_img = pygame.image.load(os.path.join(img_folder, 'ground.png')).convert()
        guitar_img = pygame.image.load(os.path.join(img_folder, 'guitar.png')).convert_alpha()
        paint_img = pygame.image.load(os.path.join(img_folder, 'paint.png')).convert_alpha()
        #social = pygame.image.load(os.path.join(img_folder, 'social.png')).convert()
        ventilator_img = pygame.image.load(os.path.join(img_folder, 'ventilator.png')).convert_alpha()
        self.background_img = pygame.image.load(os.path.join(img_folder, 'background.jpg')).convert()

        self.platform_list = []
        self.platform_locations = []
        self.object_list = []
        self.available_objects = []
        self.unavailable_objects = []
        self.object_locations = []
        self.player_character = PlayerCharacter(player_img)
        self.all_sprites.add(self.player_character)
        self.events = pygame.event.get()
        self.start_boredom_time = time.time()
        self.start_object_time = time.time()

        #Create all objects and platforms, and add them to appropriate groups
        for tp in range(num_tp):
            self.object_list.append(Object(self.player_character.get_toilet_paper, 1, tp_img))
        for sick_people in range(num_sick_people):
            self.object_list.append(Object(self.player_character.change_health, -15, sick_img))
            self.sick_sprites.add(self.object_list[-1])
        for mask in range(num_masks):
            self.object_list.append(Object(self.player_character.change_health, 5, mask_img))
        for egg in range(num_eggs):
            self.object_list.append(Object(self.player_character.change_zest, 5, egg_img))
        for paint in range(num_paint):
            self.object_list.append(Object(self.player_character.change_zest, 5, paint_img))
        for guitar in range(num_guitars):
            self.object_list.append(Object(self.player_character.change_zest, 5, guitar_img))
        for ventilator in range(num_vent):
            self.object_list.append(Object(self.player_character.change_health, k_max_health, ventilator_img))
        for object in self.object_list:
            self.all_sprites.add(object)
            self.object_sprites.add(object)
        self.available_objects = self.object_list.copy()

        self.ground = Platform(ground_img)
        self.all_sprites.add(self.ground)
        self.platform_sprites.add(self.ground)

    def home_screen(self):
        self.game_screen.blit(self.background_img,(0,0))
        self.draw_text_on_screen("Can You Beat Corona?", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        self.draw_text_on_screen("Press a key to begin", 18, WIDTH_GW / 2, HEIGHT_GW * 3/8, BLACK)
        self.draw_text_on_screen("Arrow keys move player. Collect as many toilet paper rolls as you can before dying of corona or boredom.", 22, WIDTH_GW / 2, HEIGHT_GW / 2, BLACK)
        self.draw_text_on_screen("Health: Start at 100%, decreases if player collides with sick person, increases if player collects masks/ ventilators.", 18, WIDTH_GW / 2, HEIGHT_GW * 3/4, BLACK)
        self.draw_text_on_screen("Zest for Life: Start at 100%, decreases over time, increases if player collects eggs/social media icons/paint brushes/guitars.", 18, WIDTH_GW / 2, HEIGHT_GW * 7/8, BLACK)
        pygame.display.flip()

    def end_screen(self):
        self.game_screen.blit(self.background_img,(0,0))
        if self.player_character.health <= 0:
            self.draw_text_on_screen("You died of the virus", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        else:
            self.draw_text_on_screen("You died of boredom", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        self.draw_text_on_screen("Your score was {}".format(self.player_character.num_tp), 18, WIDTH_GW / 2, HEIGHT_GW * 3/8, BLACK)
        pygame.display.flip()

    def draw_text_on_screen(self, text, size, xpos, ypos, color = WHITE):
        font = pygame.font.Font(k_font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (xpos, ypos)
        self.game_screen.blit(text_surface, text_rect)


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
            if time.time() > k_time_between_objects + self.start_object_time:
                if (random.randint(0,30) == 0) and (len(self.available_objects) > 0):
                    #potentially need to add thing to show the object
                    object_to_move = self.available_objects[random.randint(0,len(self.available_objects)-1)]
                    if not(object_to_move in self.sick_sprites):
                        object_to_move.y = random.randint(0,k_floor_offset)
                    self.available_objects.remove(object_to_move)
                    self.unavailable_objects.append(object_to_move)
                    self.start_object_time = time.time()
                #move each object that is on screen
            for object in self.unavailable_objects:
                object.x -= k_object_move_value
                #if the object has reached the edge of the screen, remove it
                if object.x <=0:
                    #potentially need to add a thing to hide the object
                    self.unavailable_objects.remove(object)
                    self.available_objects.append(object)
                    object.restart()

            #check for collisions with objects and act upon that
            object_collisions = pygame.sprite.spritecollide(self.player_character, self.object_sprites, False)
            for object in object_collisions:
                if object in self.unavailable_objects:
                    self.unavailable_objects.remove(object)
                    self.available_objects.append(object)
                object.contact_player()
                object.restart()

            current_boredom = time.time()
            if (current_boredom-self.start_boredom_time) > k_time_between_boredom_drop:
                self.start_boredom_time = time.time()
                self.player_character.change_zest(k_boredom_drop_value)

            #check if we are standing on ground or jumping
            platform_collisions = pygame.sprite.spritecollide(self.player_character, self.platform_sprites, False)
            if len(platform_collisions) > 0:
                self.player_character.on_ground = True
            else:
                self.player_character.on_ground = False

            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Draw / render
            self.all_sprites.update()
            self.game_screen.blit(self.background_img,(0,0))
            self.all_sprites.draw(self.game_screen)
            self.draw_text_on_screen('Zest 4 Life ' + str(self.player_character.zest), 20, 3*WIDTH_GW/4, 10) #display zest on screen
            self.draw_text_on_screen('Toilet Paper Score ' + str(self.player_character.num_tp), 20, WIDTH_GW/2, 10) #display num of tp on screen
            self.draw_text_on_screen('Health ' + str(self.player_character.health), 20, WIDTH_GW/4, 10) #display health on screen
            # after drawing everything, flip the display to make it visible to viewer
            pygame.display.flip()
        else:
            self.game_over = True


if __name__ == '__main__':
    model = Model()
    game_loop = False
    end_screen = False
    home = True
    model.home_screen()
    time.sleep(.01)
    while home:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                home = False
            if event.type == pygame.KEYDOWN:
                playing = True
                game_loop = True
                home = False
    while game_loop:
        while model.game_over == False:
            model.run()
            if model.game_over == True:#this was just added. we need to make this equal false when player dies of corona or boredom. havent done that yet.
                health = 100
                zest = 100
                num_tp = 0
                end_screen = True
                for sprite in model.all_sprites:
                    sprite.restart()
            for event in model.events:
                if event.type == pygame.QUIT:
                    game_loop= False
                    model.game_over = True
                    end_screen = False
                    pygame.quit()
        if (end_screen):
            model.end_screen()
        while end_screen == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_screen = False
                    game_loop = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    model.game_over = False
                    end_screen = False
