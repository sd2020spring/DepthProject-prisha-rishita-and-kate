'''Model Class that runs the game, and code that creates an instance of the model'''
#https://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
#https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/
#https://kidscancode.org/blog/2016/08/pygame_1-3_more-about-sprites/
#isinstance(sprite, BaseItem) Steve mentioned that this could be useful...
from objects import *
from constant_values import *
import random
import pygame
from pygame.locals import *
import time
import os


class Model:
    """
    Updates the game:
        -moves game_items and platforms around screen
        -gets keyboard input and evaluates how to move the player character
        -evaluates collisions and calls appropriate functions accordingly
        -checks if the player has died and ends loop based on that
    """
    def __init__(self, num_tp = 10, num_sick_people = 16, num_masks = 4, num_eggs = 3,
                num_guitars = 3, num_paint = 3, num_vent = 1, num_platforms = 3):
        '''
        start pygame window,

        '''
        # initialize pygame and create window
        pygame.init()
        self.game_screen = pygame.display.set_mode((WIDTH_GW, HEIGHT_GW))
        pygame.display.set_caption("COVID-19 Game")
        self.clock = pygame.time.Clock()
        self.game_over = False

        #load all the images for sprites
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        player_img = pygame.image.load(os.path.join(img_folder, 'ryangosling.png')).convert_alpha()
        tp_img = pygame.image.load(os.path.join(img_folder, 'tp.png')).convert_alpha()
        sick_img = pygame.image.load(os.path.join(img_folder, 'sickperson2.png')).convert_alpha()
        egg_img = pygame.image.load(os.path.join(img_folder, 'eggnflour2.png')).convert_alpha()
        mask_img = pygame.image.load(os.path.join(img_folder, 'mask.png')).convert_alpha()
        ground_img = pygame.image.load(os.path.join(img_folder, 'ground.png')).convert()
        guitar_img = pygame.image.load(os.path.join(img_folder, 'guitar.png')).convert_alpha()
        paint_img = pygame.image.load(os.path.join(img_folder, 'paint.png')).convert_alpha()
        platform_img = pygame.image.load(os.path.join(img_folder, 'platform.png')).convert_alpha()
        ventilator_img = pygame.image.load(os.path.join(img_folder, 'ventilator.png')).convert_alpha()
        self.background_img = pygame.image.load(os.path.join(img_folder, 'background.jpg')).convert()

        #list of platforms that are/aren't currently on screen
        self.offscreen_platforms = []
        self.onscreen_platforms = []
        #keep track of where the platforms are so they vary in heights
        self.last_platform_height = [1]
        #lists of all game_items (eggs, tp, sick people) that are/aren't currently on screen
        self.offscreen_obejcts = []
        self.onscreen_obejcts = []

        #set up  time for when game_items should move across the screen
        self.start_boredom_time = time.time()
        self.start_game_item_time = time.time() - k_time_between_game_items
        self.start_platform_time = time.time() - k_time_between_platforms
        #also set up things ending the game if the player has gone off screen
        self.out_of_box_time = 0
        self.is_out_of_box = False

        #create groups of sprites
        self.all_sprites = pygame.sprite.Group()
        self.game_item_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.sick_sprites = pygame.sprite.Group()
        self.events = pygame.event.get()

        #create the player and add to sprite groups
        self.player_character = PlayerCharacter(player_img)
        self.all_sprites.add(self.player_character)

        #Create all game_items and add them to appropriate groups
        for tp in range(num_tp):
            self.offscreen_obejcts.append(Game_Item([self.player_character.get_toilet_paper], [1], tp_img))
        for sick_people in range(num_sick_people):
            self.offscreen_obejcts.append(Sick_People([self.player_character.change_health,self.player_character.bounce_away_from_sickness], [-15,k_bounce_dist], sick_img))
            self.sick_sprites.add(self.offscreen_obejcts[-1])
        for mask in range(num_masks):
            self.offscreen_obejcts.append(Game_Item([self.player_character.change_health], [5], mask_img))
        for egg in range(num_eggs):
            self.offscreen_obejcts.append(Game_Item([self.player_character.change_zest], [5], egg_img))
        for paint in range(num_paint):
            self.offscreen_obejcts.append(Game_Item([self.player_character.change_zest], [5], paint_img))
        for guitar in range(num_guitars):
            self.offscreen_obejcts.append(Game_Item([self.player_character.change_zest], [5], guitar_img))
        for ventilator in range(num_vent):
            self.offscreen_obejcts.append(Game_Item([self.player_character.change_health], [k_max_health], ventilator_img))
        for game_item in self.offscreen_obejcts:
            self.all_sprites.add(game_item)
            self.game_item_sprites.add(game_item)

        #create the platforms and ground of the game
        for platform in range(num_platforms):
            self.offscreen_platforms.append(Platform(platform_img,x=WIDTH_GW+k_platform_offset))
            self.platform_sprites.add(self.offscreen_platforms[-1])
            self.all_sprites.add(self.offscreen_platforms[-1])
        self.ground = Platform(ground_img)
        self.all_sprites.add(self.ground)
        self.platform_sprites.add(self.ground)

    def home_screen(self):
        '''text to be displayed at the beginning of the game'''
        self.game_screen.blit(self.background_img,(0,0))
        self.draw_text_on_screen("Can You Beat Corona?", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        self.draw_text_on_screen("Press a key to begin", 18, WIDTH_GW / 2, HEIGHT_GW * 3/8, BLACK)
        self.draw_text_on_screen("Arrow keys move player. Collect as many toilet paper rolls as you can"
                                +"before dying of corona or boredom.", 22, WIDTH_GW / 2, HEIGHT_GW / 2, BLACK)
        self.draw_text_on_screen("Jump on sick people to get bonus points!", 20, WIDTH_GW / 2, HEIGHT_GW * 5/8, BLACK)
        self.draw_text_on_screen("Health: Start at 100%, decreases if player collides with sick person,"
                                +"increases if player collects masks/ ventilators.", 18, WIDTH_GW / 2, HEIGHT_GW * 3/4, BLACK)
        self.draw_text_on_screen("Zest for Life: Start at 100%, decreases over time,"
                                +"increases if player collects eggs/social media icons/paint brushes/guitars.", 18,
                                WIDTH_GW / 2,HEIGHT_GW * 7/8, BLACK)
        pygame.display.flip()

    def end_screen(self):
        '''text that gets displayed at the end of the game'''
        self.game_screen.blit(self.background_img,(0,0))
        if self.player_character.health <= 0:
            self.draw_text_on_screen("You died of the virus", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        elif self.player_character.zest <= 0:
            self.draw_text_on_screen("You died of boredom", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        else:
            self.draw_text_on_screen("You died by falling off the face of the planet", 64, WIDTH_GW / 2, HEIGHT_GW / 4, BLACK)
        self.draw_text_on_screen("Your score was {}".format(self.player_character.num_tp), 18, WIDTH_GW / 2, HEIGHT_GW * 3/8, BLACK)
        pygame.display.flip()

    def draw_text_on_screen(self, text, size = 64, xpos = WIDTH_GW/2, ypos = HEIGHT_GW/4, color = WHITE):
        '''distplays the parameter text at a certain size and position on screen '''
        font = pygame.font.Font(k_font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (xpos, ypos)
        self.game_screen.blit(text_surface, text_rect)

    def collisions(self, player):
        """ determines which game_items have collided with the given player game_item
        if the player contacts a sick person, the sick person doesnt disappear
        all other sprites change a value of the player character and reset
        """
        #get all the current collisions
        game_item_collisions = pygame.sprite.spritecollide(player, self.game_item_sprites, False)
        for game_item in game_item_collisions:
            #make sure we are actually colliding with something visible
            if game_item in self.onscreen_obejcts:
                #if we collide with a sick sprite, then bounce away or attack them
                if game_item in self.sick_sprites:
                    #if player jumps on them, they die
                    if (game_item.pos.y - (4*game_item.rect.height/5) > player.pos.y):
                        game_item.restart()
                        self.onscreen_obejcts.remove(game_item)
                        self.offscreen_obejcts.append(game_item)
                        #player gets bonus toilet paper
                        player.get_toilet_paper(5)
                    #if sick person hits the player, player loses health and both bounce away
                    else:
                        if game_item.pos.x > player.pos.x:
                            game_item.delta_value[1] = -k_bounce_dist
                            game_item.pos.x += k_bounce_dist
                        else:
                            game_item.delta_value[1] = k_bounce_dist
                            game_item.pos.x -= k_bounce_dist
                        game_item.contact_player()
                #if its any other sprite, reset the game_item, and move it to the onscreen list
                else:
                    game_item.restart()
                    self.onscreen_obejcts.remove(game_item)
                    self.offscreen_obejcts.append(game_item)
                    game_item.contact_player()

    def gravity_collisions(self, player):
        """checks to see if the player is on the ground or not """
        #get all the platform collisions
        platform_collisions = pygame.sprite.spritecollide(player, self.platform_sprites, False)
        #if player is touching a platform and are moving downwards, evaluate if if should stop or not
        if len(platform_collisions) > 0 and player.vel.y >= 0:
            player.on_ground = False
            #check each platform
            for platform in platform_collisions:
                #if the player is above the platform when hitting it, it is on the ground
                if platform.y >= player.pos.y + k_game_item_offset/2:
                    player.on_ground = True
        #if not touching any platforms or moving upwards, player is not on the ground
        else:
            player.on_ground = False

    def check_for_death(self,player):
        """checks the input players stats to see if they have died"""
        #if health or zest are too low, you die
        if player.health <= 0 or player.zest <= 0:
            self.game_over = True
        #if you are out of x bounds, keep track of how long you are out for
        if (player.pos.x < -k_out_of_bounds or player.pos.x > WIDTH_GW + k_out_of_bounds) and self.is_out_of_box == False:
            self.out_of_box_time = time.time()
            self.is_out_of_box = True
        #if you are out of y bounds, also keep track
        if (player.pos.y < -k_out_of_bounds or player.pos.y > HEIGHT_GW + k_out_of_bounds) and self.is_out_of_box == False:
            self.out_of_box_time = time.time()
            self.is_out_of_box = True
        #if you go back in bounds, you are safe and not dead yet
        if player.pos.y >= 0 and player.pos.y <= HEIGHT_GW:
            if player.pos.x >= 0 and player.pos.x <= WIDTH_GW:
                self.out_of_box_time = 0
                self.is_out_of_box = False
        #however if you take too long getting back in bounds, you die
        elif (time.time() - self.out_of_box_time > k_out_of_box_time) and self.is_out_of_box:
            self.game_over = True

    def get_keyboard_input(self, player, left, right, up, down):
        """ gets keyboard input from the input keys left, right, up and down
        these could be either arrows or wasd.
        moves the player character based on those arrow inputs"""
        #left/right
        keys = pygame.key.get_pressed()
        if keys[left]:
            self.player_character.move('left')
            stop = False
        elif keys[right]:
            self.player_character.move('right')
            stop = False
        else:
            #if we aren't pressing keys, tell player to not move horizontally
            self.player_character.move('stop_horizontal')
        #up/down
        if keys[up]:
            self.player_character.move('up')
        elif keys[down]:
            self.player_character.move('down')
        else:
            self.player_character.move('stop_vertical')

    def update_player_boredon(self,player):
        """decrease the players boredom a certain amount per some unit of time"""
        if (time.time()-self.start_boredom_time) > k_time_between_boredom_drop:
            self.start_boredom_time = time.time()
            player.change_zest(k_boredom_drop_value)

    def run(self):
        """
        Get input from keyboard, evaluate what to do based on the input and current
        game state.
        Handles collisions between the player and game_items.
        Checks if the player has died
        """
        #update any inputs, as well as check if the game has been closed
        self.events = pygame.event.get()
        #make sure we aren't dead before doing anything else
        if self.game_over == False:
            #PLATFORM MOTION
            #if time.time() > k_time_between_platforms + self.start_platform_time:
            if  (len(self.offscreen_platforms) > 0):
                if (len(self.onscreen_platforms) == 0 or self.onscreen_platforms[-1].x < WIDTH_GW-(self.onscreen_platforms[-1].rect.width) or
                    abs((self.onscreen_platforms[-1].x - WIDTH_GW) % (self.onscreen_platforms[-1].rect.width/2)) < 5):
                    if (random.randint(0,4) == 0):
                        #select a platform
                        platform_to_move = self.offscreen_platforms[random.randint(0,len(self.offscreen_platforms)-1)]
                        #put it at one of two heights, make it probable to be opposite of the last few heights
                        if random.randint(1,(self.last_platform_height.count(2)+1))> 1:
                            height_multiplier = 1
                        else:
                            height_multiplier = 2
                        self.last_platform_height.append(height_multiplier)
                        self.last_platform_height.remove(self.last_platform_height[0])
                        #set the height of the platform based on the above number
                        platform_to_move.y = ((HEIGHT_GW-k_ground_height)/3)*height_multiplier + k_ground_height
                        #move it from the available list to the unavailable list and restart timer between sending platforms
                        self.offscreen_platforms.remove(platform_to_move)
                        self.onscreen_platforms.append(platform_to_move)
                        self.start_platform_time = time.time()
            #move each game_item that is on screen as the game scrolls
            for platform in self.onscreen_platforms:
                #change the x value of the platform to move it
                platform.x -= k_game_item_move_value
                #if the game_item has reached the edge of the screen, remove it from the moving list
                if platform.x <=0 - k_platform_offset:
                    self.onscreen_platforms.remove(platform)
                    self.offscreen_platforms.append(platform)
                    #and reset the x and y values of the platfrom
                    platform.restart()

            #EVERYTHING DEALING WITH ITEMS:
            #choose to add an game_item to screen
            if time.time() > k_time_between_game_items + self.start_game_item_time:
                #if we have waited long enough decide if there should be an game_item
                if (random.randint(0,30) == 0) and (len(self.offscreen_obejcts) > 0):
                    #create an game_item and start it on the ground
                    game_item_to_move = self.offscreen_obejcts[random.randint(0,len(self.offscreen_obejcts)-1)]
                    game_item_to_move.pos.y = HEIGHT_GW - k_ground_height - k_game_item_offset
                    #and randomly choose if it should really be on a platform instead
                    if random.randint(0,5) > 0:
                        #find any platforms we could start on
                        potential_start_locations = []
                        for platform in self.onscreen_platforms:
                            if platform.x > WIDTH_GW-(platform.rect.width/4) and platform.x < WIDTH_GW + (3*platform.rect.width/4):
                                potential_start_locations.append(platform)
                        #if there are platforms, then choose one randomly
                        if len(potential_start_locations) > 0:
                            platform = potential_start_locations[random.randint(0,len(potential_start_locations)-1)]
                            game_item_to_move.pos.y = platform.y - k_game_item_offset
                        #otherwise give up and leave the game_item on the ground
                    #move the game_item to the unavailable moving list
                    self.offscreen_obejcts.remove(game_item_to_move)
                    self.onscreen_obejcts.append(game_item_to_move)
                    self.start_game_item_time = time.time()
                #move each game_item that is on screen
            for game_item in self.onscreen_obejcts:
                #do some different things with the sick people speed and check gravity
                if game_item in self.sick_sprites:
                    game_item.pos.x += -k_sick_speed
                    if game_item.pos.x > WIDTH_GW or game_item.pos.x < 0:
                        game_item.on_ground = True
                    else:
                        self.gravity_collisions(game_item)
                #everything else just moves at a nice rate and cant fall
                else:
                    game_item.pos.x -= k_game_item_move_value
                    #if the game_item has reached the edge of the screen, remove it
                if game_item.pos.x <=0:
                    self.onscreen_obejcts.remove(game_item)
                    self.offscreen_obejcts.append(game_item)
                    game_item.restart()


            #check for player collisions with game_items and act upon that
            self.collisions(self.player_character)
            self.gravity_collisions(self.player_character)

            #change player motion based on keyboard
            self.get_keyboard_input(self.player_character, pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN)

            #change player boredom as time passes
            self.update_player_boredon(self.player_character)

            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Draw / render
            #update each sprite position
            self.all_sprites.update()
            #set the background and draw each sprite
            self.game_screen.blit(self.background_img,(0,0))
            self.all_sprites.draw(self.game_screen)
            #display score
            self.draw_text_on_screen('Zest 4 Life ' + str(self.player_character.zest), 20, 3*WIDTH_GW/4, 10) #display zest on screen
            self.draw_text_on_screen('Toilet Paper Score ' + str(self.player_character.num_tp), 20, WIDTH_GW/2, 10) #display num of tp on screen
            self.draw_text_on_screen('Health ' + str(self.player_character.health), 20, WIDTH_GW/4, 10) #display health on screen
            # after drawing everything, flip the display to make it visible to viewer
            pygame.display.flip()

        #check if the player has died
        self.check_for_death(self.player_character)

if __name__ == '__main__':
    model = Model()
    game_loop = False
    end_screen = False
    home = True
    model.home_screen()
    time.sleep(.5)
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
        pygame.mixer.music.load('tokyodrift.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        while model.game_over == False:
            model.run()
            if model.game_over == True:
                end_screen = True
            for event in model.events:
                if event.type == pygame.QUIT:
                    game_loop= False
                    model.game_over = True
                    end_screen = False
                    pygame.quit()
        if (end_screen):
            model.end_screen()
            pygame.mixer.music.fadeout(1000)
            time.sleep(.5)
        while end_screen == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_screen = False
                    game_loop = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    model.game_over = False
                    end_screen = False
                    for sprite in model.all_sprites:
                        sprite.restart()
