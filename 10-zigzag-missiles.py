# the missiles and bullets can move in different directions.
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

        Space   shoot back, straight
        x       shoot back, up
        c       shoot back, down

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
    K_x,
    K_c,
    K_SPACE
)


class Game(pywrap.WrapPyGrame):
    def __init__(self):
        super(Game, self).__init__()
        self.goodguy= None
        self.badguys = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # the score for this game.
        self.score = 0
        self.bullet_speed = 5
        self.max_missile_speed = 10

    def run(self):
        self.PlayBackgroundSound("Apoxode_-_Electric_1.mp3")
        self.PrintDialog(OpeningScreen)
        super().run()
        self.StopAllSounds()
        self.PrintDialog("Game Over\nYour Score: ", self.score,"\nBullet speed:", self.bullet_speed, "\nEnemy missile speed:", self.max_missile_speed)

    def addGoodPlayer(self, player):
        self.goodguy = player

    def addBadPlayer(self, player):
        self.badguys.add(player)

    def addBullet(self, bullet):
        self.bullets.add(bullet)

    def onCollissionTest(self):
        if pygame.sprite.spritecollideany(self.goodguy, self.badguys):
            self.PlaySound("Collision.ogg")
            print("game over. your score is:", self.score)
            self.exit()
        
        for bullet in self.bullets:
            collide = pygame.sprite.spritecollideany(bullet, self.badguys)
            if collide:
                self.PlaySound("Collision.ogg")
                collide.kill()
                bullet.kill()
                # increment the score - when a bullet collides with a missile (bad guy)
                self.score += 1
                if self.score % 5 == 0:
                    self.max_missile_speed += 1
                    self.bullet_speed += 1

    def onStartFrame(self):
        super().onStartFrame()
        self.Print(0, self.screen_height - self.font_size, "Score: ", self.score, "Weapon:", self.bullet_speed, "Enemy:", self.max_missile_speed)


# sprite that draws a bullet shot by the player
class Bullet(pywrap.WrapSprite):
    def __init__(self, game, x, y, dy):
        super(Bullet, self).__init__(
            "bullet.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (x, y) ) # initial position of sprite
        self.speed = game.bullet_speed
        self.width = game.screen_width
        self.dy = dy
        self.game = game

    # Move the bullet based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, self.dy)
        if self.rect.right > self.width:
            self.kill() 
        if self.rect.top <= 0 or self.rect.bottom >= self.game.screen_height:
            self.dy = - self.dy


# create an instance of the game
game = Game()


# sprite that draws a cloud, all clouds move with the same speed.
class Player(pywrap.WrapSprite):
    def __init__(self, game):
        super(Player, self).__init__(
            "jet.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (game.screen_width/3, game.screen_height/2),    # initial position of sprite
            2)
        self.game = game
        

    def handleKeyUp(self, game):
        self.rect.move_ip(0, -2)
        if self.rect.top <= 0:
            self.rect.top = 0
        game.PlaySound("Rising_putter.ogg")


    def handleKeyDown(self, game):
        self.rect.move_ip(0, 2)
        if self.rect.bottom >= game.screen_height:
            self.rect.bottom = game.screen_height
        game.PlaySound("Falling_putter.ogg")


    def handleKeyLeft(self, game):
        self.rect.move_ip(-5, 0)
        if self.rect.top <= 0:
            self.rect.top = 0

    def handleKeyRight(self, game):
        self.rect.move_ip(5, 0)
        if self.rect.right > game.screen_width:
            self.rect.right = game.screen_width

    def shoot(self, game):
        self.addShot(game, 0)

    def shootUp(self, game):
        self.addShot(game, -1)

    def shootDown(self, game):
        self.addShot(game, 1)

    def addShot(self, game, dy):
        bullet = Bullet(game, self.rect.x+self.rect.width, self.rect.y+self.rect.height/2, dy)
        game.addSprite(bullet)
        game.addBullet(bullet)


player = Player(game)
game.addKeyPressedEvent(K_UP, player.handleKeyUp)
game.addKeyPressedEvent(K_k, player.handleKeyUp)

game.addKeyPressedEvent(K_DOWN,player.handleKeyDown)
game.addKeyPressedEvent(K_j, player.handleKeyDown)

game.addKeyPressedEvent(K_LEFT, player.handleKeyLeft)
game.addKeyPressedEvent(K_h, player.handleKeyLeft)

game.addKeyPressedEvent(K_RIGHT, player.handleKeyRight)
game.addKeyPressedEvent(K_l, player.handleKeyRight)

game.addKeyDownEvent(K_SPACE, player.shoot)
game.addKeyDownEvent(K_x, player.shootUp)
game.addKeyDownEvent(K_c, player.shootDown)



game.addSprite(player)
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

# is being called when the time event fires (see call to addTimerEvent)
def addCloud(game):
    # create a new cloud sprite
    cloud = Cloud(game.screen_width, game.screen_height)
    # add the cloud sprite to the game.
    game.addSprite(cloud)

# add a timer to the game. once per second (100ms) is is calling the addCloud function
game.addTimerEvent(1000, addCloud)

# sprite that draws a missile, missiles have different velocity
class Missile(pywrap.WrapSprite):
    def __init__(self, game):
        super(Missile, self).__init__(
            "missile.png",    # the picture of the sprite
            (255, 255, 255),        # background color of the sprite
            (random.randint(game.screen_width + 20, game.screen_width + 100),random.randint(0, game.screen_height)), # initial position of sprite\
            1)
        self.speed = random.randint(5, game.max_missile_speed)
        self.speed_dy = random.randint(-2, 2)
        self.game = game

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, self.speed_dy)
        if self.rect.right < 0:
            self.kill() 
        if self.rect.top <= 0 or self.rect.bottom > self.game.screen_height:
            self.speed_dy = - self.speed_dy

# is being called when the time event fires (see call to addTimerEvent)
def addMissile(game):
    # create a new cloud sprite
    missile = Missile(game)
    # add the cloud sprite to the game.
    game.addSprite(missile) # add as last of the sprites, so it will be drawn above the clouds
    game.addBadPlayer(missile)


# add timer, once every 250 millisecond the addMissile function will be called.
game.addTimerEvent(250, addMissile)

# run the game loop
game.run()
