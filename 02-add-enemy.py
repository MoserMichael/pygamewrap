
# this program adds enemy missile that fly from the right to left side of the screen. 
# the missiles all have different speeds.

import pywrap
import random

# create an instance of the game
game = pywrap.WrapPyGrame()


# sprite that draws a cloud, all clouds move with the same speed.
class Cloud(pywrap.WrapSprite):
    def __init__(self, width, height):
        super(Cloud, self).__init__(
            "cloud.png",    # the picture of the sprite
            (0,0,0),        # background color of the sprite
            (random.randint(width + 20, width + 100),random.randint(0, height)) ) # initial position of sprite

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

# add a timer to the game. once per second (100ms) is is calling the addCloud function
game.add_timer_event(1000, addCloud)

# sprite that draws a missile, missiles have different velocity
class Missile(pywrap.WrapSprite):
    def __init__(self, width, height):
        super(Missile, self).__init__(
            "missile.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (random.randint(width + 20, width + 100),random.randint(0, height)), # initial position of sprite
            1) # layer 1 - above the clouds
        self.speed = random.randint(5, 20)

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() 

# is being called when the time event fires (see call to add_timer_event)
def add_missile(game):
    # create a new cloud sprite
    missile = Missile(game.screen_width(), game.screen_height())
    # add the cloud sprite to the game.
    game.add_sprite(missile) # add as last to list of all sprites, so it will be drawn above the clouds

# add timer, once every 250 millisecond the add_missile function will be called.
game.add_timer_event(250, add_missile)

# run the game loop
game.run()