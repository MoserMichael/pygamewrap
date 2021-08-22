# PygameWrap - a tools for writing games with pygame

## Intro

I have been trying to prepare a python course for my kids [here](https://github.com/MoserMichael/pythoncourse); one of the things that i would like to do is a game with pygame.
Now there are lots of nice pygame tutorials, I followed the following [Pygame primer](https://realpython.com/pygame-a-primer/) by Jon Fincher, the source code for the tutorial is [here](https://github.com/realpython/materials/tree/master/pygame-a-primer)

The tutorial was great, the documentation for pygame is perfectly adequate, however there was one thing missing - fun; doing something in pygame is hard work!

Compare that to what I had in my youth: I got my intro to programming on a [TI 99/4A home computer](https://en.wikipedia.org/wiki/Texas_Instruments_TI-99/4A) with a 16 kilobyte extended Basic ROM cartridge; I had tons of fun programming games with the sprite graphics on that machine, and the result in 1986 was not so much different as compared to what you have today with pygames, in this age, some thirty five years later (well, maybe only my games didn't get any better, despite me having got rid of using goto ;-)

Now this project is trying to make a wrapper, that is hiding some of the complexity and boilerplate setup of the pygame package.
Here is the result: 

1) The PyWrap module holds the wrapper for pygame
2) the root directory holds a sequence of files that develop a game, each one is adding a feature on top of the previous one. The sample game implements the same game as in the  [Pygame primer](https://realpython.com/pygame-a-primer/) by Jon Fincher, and it is using the same graphics and sounds. I also added some additional features, like animated sprites and caching & reuse of sprites etc.

I am not perfectly happy with the result, it does simplify things a bit, however the result is still somewhat complex.
The [original tutorial](https://github.com/realpython/materials/blob/master/pygame-a-primer/py_tut_with_images.py) was 221 lines long, my result [is here](https://github.com/MoserMichael/pygamewrap/blob/master/08-add-sounds.py) (without wrapper library) and is 222 lines long (well, I am adding a few features here and there, to be fair)

I think that the code is arguably cleaner with the pygame wrapper, less involved with the pygame API, more focussed on the game logic, that is; it is more high level than pygame, on the other hand it is much more basic then a real game engine.
Well, anyway, here is the result for you to judge.

## Installation

* You must use this with python3, 
* You need to install pygames 

You can get this library

* with pip ```pip3 install PygameWrap```  (also see this module on [pypi.org](https://pypi.org/project/PygameWrap/))
* via git ```git clone https://github.com/MoserMichael/pygamewrap.git```


## The API

the module has the following classes:

```PyGame``` the main class, create an instance of this class first.

* the constructor has the following optional arguments
    * ```framerate``` - default to 30
    * ```width``` - of the screen, defaults to 800
    * ```height``` - of the screen, defaults to 600
    * ```font``` - font name for text display (default Courier)
    * ```spritecachesize``` - killed sprites for types with the reuse method get cached, this is the size of the per class cache, it defaults to 1000
* after the constructor, you need to create sprite types and event handlers, these must be added to the ```PyGame``` instance, these will be handled during the ```run``` method, where the game loop is run. You can call the following functions:
    * ```add_timer_event(timeInMillis, handlerFunc)``` adds a timer event, the handler function argument looks as follows ```myTimerHandler(game)``` - game is a ```PyGame``` object.
    * ```add_key_pressed_event(key, handlerFunc)```, ```add_key_up_event(key, handlerFunc)```, ```add_key_down_event(key, handlerFunc)``` - key event handlers, 1) handler called for each frame while a key is down, 2) key up event 3) key down event. the handler function is ```key_handler(game)```
    * ```add_sprite``` adds a sprite to the game, sprite is derived form either ```ImageSprite``` or  ```AnimatedSprite``` class, and is displayed during each frame of the game, until you call the kill method of the sprite.
    * ```run``` starts the game loop, goes on until ```exit``` is called.
    * You can override the following mehods of the ```PyGame``` class
        * ```on_start_frame``` called for each frame, draw the background of the game on the ```Pygame.screen```  here (the default is to draw a light blue background), after that the events are handled and sprites drawn on to the off screen buffer, which is currently not displayed, after that the offscreen buffer is displayed, override ```on_collision_test``` to check for collisions between sprites.
    * text display functions: ```set_font(font_name, font_size)```, ```set_text_colors(background_color, foreground_color)```, ```print(x, y, *args)``` shows a single line string, ```print_text(x, y, *args)``` shows a multi line string, ```print_dialog(*args)``` shows a multiline text, and waits for the user to press the space bar.
    * media caching; ```load_image(filename)``` loads pygame image with ```pygame.image.load``` and caches is, returns cached image if already displayed. ```play_sound(filename, loop=0)``` loads (if not already cached) and plays a music file, ```stop_all_sounds``` - stops the music.
    * optional sprite caching; If a sprite object derived from ```ImageSprite``` or ```AnimatedSprite``` is implementing a ```reuse``` method: when the sprite is killed, it is added to the cache, to reuse such a sprite: call ```get_cached_sprite(class_of_cached_sprite)``` then call the reuse method. See [example usage](https://github.com/MoserMichael/pygamewrap/blob/master/11-add-sprite-caching.py). Without caching of sprites and media items you may run into ugly garbage collection delays with the python memory manager.

The sprite classes derive from ```pygame.sprite.Sprite``` create instances and add them to the ```PyGame``` object by calling ```add_sprite```
* ```ImageSprite```, constructor is ```ImageSprite(imageFileName, transparentBackgroundColor, initialPosition, layer)```
* ```AnimatedSprite``` - animated sprite, constructor is ```AnimatedSprite(imageFileNameList, transparentBackgroundColor, initialPosition, layer)``` a list of image files names is passed, each image file name stands for an animation frame, on each consecutive frame of the game it displays the next image from list of images and cycles back to the first image from the list after displaying the last one.


## Issues

The pygame windows does not automatically get the focus, it is not brought to the foreground. I didn't find a way to do this, in a platform independent manner.
It helps to have some background music in the game that starts once the game is running, this way the user is alerted that the game is running, even when the game window is not popping up.

# License 

licensed under MIT license


