
# this program adds collision test between the missiles and the player, upon collision the game is stopped.

from pygame.constants import K_h, K_k
import pywrap
import random
import pygame

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
        
)


class Game(pywrap.WrapPyGrame):
    def __init__(self):
        super(Game, self).__init__()
        self.goodguy= None
        self.badguys = pygame.sprite.Group()

    def addGoodPlayer(self, player):
        self.goodguy = player

    def addBadPlayer(self, player):
        self.badguys.add(player)

    def on_colission_test(self):
        if pygame.sprite.spritecollideany(self.goodguy, self.badguys):
            print("game over")
            self.exit()

# create an instance of the game
game = Game()


# sprite that draws a cloud, all clouds move with the same speed.
class Player(pywrap.WrapSprite):
    def __init__(self, width, height):
        super(Player, self).__init__(
            "jet.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (width/3, height/2),    # initial position of sprite
            2)                      # layer number
        self.screen_width = width
        self.screen_height = height

    def handleKeyUp(self, game):
        self.rect.move_ip(0, -5)
        if self.rect.top <= 0:
            self.rect.top = 0

    def handleKeyDown(self, game):
        self.rect.move_ip(0, 5)
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    def handleKeyLeft(self, game):
        self.rect.move_ip(-5, 0)
        if self.rect.top <= 0:
            self.rect.top = 0

    def handleKeyRight(self, game):
        self.rect.move_ip(5, 0)
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width


player = Player(game.screen_width, game.screen_height)
game.add_key_pressed_event(K_UP, player.handleKeyUp)
game.add_key_pressed_event(K_k, player.handleKeyUp)

game.add_key_pressed_event(K_DOWN,player.handleKeyDown)
game.add_key_pressed_event(K_j, player.handleKeyDown)

game.add_key_pressed_event(K_LEFT, player.handleKeyLeft)
game.add_key_pressed_event(K_h, player.handleKeyLeft)

game.add_key_pressed_event(K_RIGHT, player.handleKeyRight)
game.add_key_pressed_event(K_l, player.handleKeyRight)

game.add_sprite(player)
game.addGoodPlayer(player)

# sprite that dkraws a cloud, all clouds move with the same speed.
class Cloud(pywrap.WrapSprite):
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
    cloud = Cloud(game.screen_width, game.screen_height)
    # add the cloud sprite to the game.
    game.add_sprite(cloud)

# add a timer to the game. once per second (100ms) is is calling the addCloud function
game.add_timer_event(1000, addCloud)

# sprite that draws a missile, missiles have different velocity
class Missile(pywrap.WrapSprite):
    def __init__(self, width, height):
        super(Missile, self).__init__(
            "missile.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (random.randint(width + 20, width + 100),random.randint(0, height)), # initial position of sprite
            1)
        self.speed = random.randint(5, 20)

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() 

# is being called when the time event fires (see call to add_timer_event)
def addMissile(game):
    # create a new cloud sprite
    missile = Missile(game.screen_width, game.screen_height)
    # add the cloud sprite to the game.
    game.add_sprite(missile) # add as last of the sprites, so it will be drawn above the clouds
    game.addBadPlayer(missile)


# add timer, once every 250 millisecond the addMissile function will be called.
game.add_timer_event(250, addMissile)

# run the game loop
game.run()