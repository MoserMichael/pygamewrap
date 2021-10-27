# this program generates random clowds that flow over the screen from right to left.
# these clouds will be the background of the game.

import pywrap
import random

# create an instance of the game
game = pywrap.PyGame()

# is being called when the time event fires (see call to add_timer_event)
def addCloud(game):
    # create a new cloud sprite
    cloud = Cloud(game.screen_width(), game.screen_height())
    # add the cloud sprite to the game.
    game.add_sprite(cloud)


# add a timer to the game. once per second is is calling the addCloud function
game.add_timer_event(1000, addCloud)

# sprite that draws a cloud, all clouds move with the same speed.
class Cloud(pywrap.ImageSprite):
    def __init__(self, width, height):
        super(Cloud, self).__init__(
            "cloud.png",  # the picture of the sprite
            (0, 0, 0),  # background color of the sprite
            (random.randint(width + 20, width + 100), random.randint(0, height)),
        )  # initial position of sprite

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# run the game loop
game.run()
