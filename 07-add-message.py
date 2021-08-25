
# this program adds an opening screen with some explanations, and an exit screen
from pygame.constants import K_SPACE, K_h, K_k
import pywrap
import random
import pygame

OpeningScreen = """
Basic Shooter Game 

Move your figher and shoot down missiles

Instructions:
        h,Left  move left
        l,Right move right
        j,Up    move up
        k,Down  move down
        Space   shoot back

You get a point for every downed missile!
"""

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_h,
    K_j,
    K_k,
    K_l,
    K_SPACE
)


class Game(pywrap.PyGame):
    def __init__(self):
        super(Game, self).__init__()
        self.goodguy= None
        self.badguys = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # the score for this game.
        self.score = 0

    def run(self):
        self.print_dialog(OpeningScreen)
        super().run()
        self.print_dialog("Game Over\nYour Score: ", self.score)



    def add_good_player(self, player):
        self.goodguy = player

    def add_bad_player(self, player):
        self.badguys.add(player)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def on_colission_test(self):
        if pygame.sprite.spritecollideany(self.goodguy, self.badguys):
            print("game over")
            self.exit()
        
        for bullet in self.bullets:
            collide = pygame.sprite.spritecollideany(bullet, self.badguys)
            if collide:
                collide.kill()
                bullet.kill()
                # increment the score - when a bullet collides with a missile (bad guy)
                self.score += 1

    def on_start_frame(self):
        super().on_start_frame()
        self.print(0, self.screen_height() - self.font_size, "Score: ", self.score)


# sprite that draws a bullet shot by the player
class Bullet(pywrap.ImageSprite):
    def __init__(self, width, x, y):
        super(Bullet, self).__init__(
            "bullet.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (x, y) ) # initial position of sprite
        self.speed = 5
        self.width = width

    # Move the bullet based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > self.width:
            self.kill() 


# create an instance of the game
game = Game()


# sprite that draws a cloud, all clouds move with the same speed.
class Player(pywrap.ImageSprite):
    def __init__(self, width, height):
        super(Player, self).__init__(
            "jet.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (width/3, height/2),    # initial position of sprite
            2)
        self.screen_width = width
        self.screen_height = height

    def handle_key_up(self, game):
        self.rect.move_ip(0, -2)
        if self.rect.top <= 0:
            self.rect.top = 0

    def handle_key_down(self, game):
        self.rect.move_ip(0, 2)
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    def handle_key_left(self, game):
        self.rect.move_ip(-5, 0)
        if self.rect.left <= 0:
            self.rect.left = 0

    def handle_key_right(self, game):
        self.rect.move_ip(5, 0)
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def shoot(self, game):
        bullet = Bullet(game.screen_width(), self.rect.x+self.rect.width, self.rect.y+self.rect.height/2)
        game.add_sprite(bullet)
        game.add_bullet(bullet)


player = Player(game.screen_width(), game.screen_height())
game.add_key_pressed_event(K_UP, player.handle_key_up)
game.add_key_pressed_event(K_k, player.handle_key_up)

game.add_key_pressed_event(K_DOWN,player.handle_key_down)
game.add_key_pressed_event(K_j, player.handle_key_down)

game.add_key_pressed_event(K_LEFT, player.handle_key_left)
game.add_key_pressed_event(K_h, player.handle_key_left)

game.add_key_pressed_event(K_RIGHT, player.handle_key_right)
game.add_key_pressed_event(K_l, player.handle_key_right)

game.add_key_down_event(K_SPACE, player.shoot)


game.add_sprite(player)
game.add_good_player(player)

# sprite that dkraws a cloud, all clouds move with the same speed.
class Cloud(pywrap.ImageSprite):
    def __init__(self, width, height):
        super(Cloud, self).__init__(
            "cloud.png",    # the picture of the sprite
            (0,0,0),        # background color of the sprite
            (random.randint(width + 20, width + 100),random.randint(0, height)),  # initial position of sprite
            0)


    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()       

# is being called when the time event fires (see call to add_timer_event)
def addCloud(game):
    # create a new cloud sprite
    cloud = Cloud(game.screen_width(), game.screen_height())
    # add the cloud sprite to the game.
    game.add_sprite(cloud)

# add a timer to the game. once per second is is calling the addCloud function
game.add_timer_event(1000, addCloud)

# sprite that draws a missile, missiles have different velocity
class Missile(pywrap.ImageSprite):
    def __init__(self, width, height):
        super(Missile, self).__init__(
            "missile.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (random.randint(width + 20, width + 100),random.randint(0, height)), # initial position of sprite\
            1)
        self.speed = random.randint(5, 10)

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() 

# is being called when the time event fires (see call to add_timer_event)
def add_missile(game):
    missile = Missile(game.screen_width(), game.screen_height())
    game.add_sprite(missile) 
    game.add_bad_player(missile)


# add timer, once every 250 millisecond the add_missile function will be called.
game.add_timer_event(250, add_missile)

# run the game loop
game.run()
