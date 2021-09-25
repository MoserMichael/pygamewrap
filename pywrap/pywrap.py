from random import gammavariate
from types import prepare_class
from typing import NamedTuple, Tuple, Callable, Type

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
    RLEACCEL
)

class PygameGlobal:
    game = None

    @staticmethod
    def get_game() -> 'PyGame':
        return PygameGlobal.game

    @staticmethod
    def set_game(game : 'PyGame') -> None:
        PygameGlobal.game = game


class CacheableSprite(pygame.sprite.Sprite):

    def __init__(self, layer : int):
        self._layer  = layer
        super(CacheableSprite, self).__init__()

    def kill(self) -> None:
        # remove sprite from all groups
        super().kill()

        # adds the sprite to the cache - if the sprite type supports caching (if the derived class has a reuse method)
        PygameGlobal.get_game().add_to_cache_(self)



class AnimatedSprite(CacheableSprite):

    def __init__(self, imageFileList : list, transparentBackgroundColor : Tuple[int, int, int], initPos: Tuple[int, int], layer : int = 0):
        super(AnimatedSprite, self).__init__(layer)

        self.images = list()

        for img_name in imageFileList:
            surf = PygameGlobal.get_game().load_image(img_name).convert()
            surf.set_colorkey(transparentBackgroundColor, RLEACCEL)
            self.images.append( surf )

        self.surf = self.images[0]
        self.rect = self.surf.get_rect(center = initPos)
        self.current_frame = -1

    # draws the buffer on the current screen buffer.
    def draw_on_buffer(self, game : 'PyGame') -> None:
        self.current_frame = (self.current_frame + 1) % len(self.images)
        game.screen.blit(self.images[ self.current_frame ], self.rect)


# sprite wrapping class
class ImageSprite(CacheableSprite):

    # sprite constructor, loads an image file from imageFile, with the transparent color transparentBackgroundColor
    # placed to the initial position initPos
    def __init__(self, imageFile : str, transparentBackgroundColor : Tuple[int,int,int], initPos : Tuple[int,int], layer : int =0):
        super(ImageSprite, self).__init__(layer)

        #self.surf = pygame.image.load(imageFile).convert()
        self.surf = PygameGlobal.get_game().load_image(imageFile).convert()
        self.surf.set_colorkey(transparentBackgroundColor, RLEACCEL)
        self.rect = self.surf.get_rect(center = initPos)

    # draws the buffer on the current screen buffer.
    def draw_on_buffer(self, game : 'PyGame') -> None:
        game.screen.blit(self.surf, self.rect)






# wraps the pygame screen and game loop
class PyGame:

    def __init__(self, **kwargs):
        pygame.init()
        self.clock = pygame.time.Clock()

        if "framerate" in kwargs:
            self.framerate = kwargs["framerate"]
        else:
            self.framerate = 30

        if "width" in kwargs:
            self.display_width = kwargs["width"]
        else:
            self.display_width = 800


        if "height" in kwargs:
            self.display_height = kwargs["height"]
        else:
            self.display_height = 600


        if "font" in kwargs:
            font_name = kwargs["font"]
        else:
            font_name = "Courier" #"Arial"

        if "fontSize" in kwargs:
            font_size = int(kwargs["fontSize"])
        else:
            font_size = 32

        if "spritecachesize" in kwargs:
            self.sprite_cache_size = int(kwargs["spritecachesize"])
        else:
            self.sprite_cache_size = 100

        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.last_timer_event = pygame.USEREVENT + 1
        self.event_handler = dict()
        self.key_down_handlers = dict()
        self.key_up_handlers = dict()
        self.key_pressed_handlers = dict()
        self.running = True

        self.add_event_handler( pygame.QUIT, self.exit )

        self.set_font(font_name, font_size)
        self.set_text_colors((128, 0, 0), (135, 206, 250))

        self.map_file_to_sound = dict()
        self.map_file_to_image = dict()
        self.map_type_to_spritecache = dict()


        # Setup for sounds, defaults are good
        pygame.mixer.init()

        PygameGlobal.set_game(self)

    def screen_width(self) -> int:
        return self.display_width

    def screen_height(self) -> int:
        return self.display_height


    # add event handler
    def add_event_handler(self, event_type, handler_func : Callable[['PyGame'], None]) -> None:
        self.event_handler[ event_type ] = handler_func

    # add key down event handler
    def add_key_down_event(self, key : int, handler_func : Callable[['PyGame'], None]) -> None:
        self.key_down_handlers[ key ] = handler_func

    # add key up event handler
    def add_key_up_event(self, key : int, handler_func: Callable[['PyGame'], None]) -> None:
        self.key_up_handlers[ key ] = handler_func

    # add key pressed handler, is being called on each frame if the key is still pressed.
    def add_key_pressed_event(self, key : int, handler_func: Callable[['PyGame'], None]) -> None:
        self.key_pressed_handlers[ key ] = handler_func

    # add a timer event, the handler_func function argument will be called once per time_in_millisecond milliseconds.
    def add_timer_event(self, time_in_millisecond : int, handler_func: Callable[['PyGame'], None]) -> None:
        timer_val = self.last_timer_event
        self.add_event_handler( timer_val, handler_func)
        pygame.time.set_timer(timer_val, time_in_millisecond)
        self.last_timer_event += 1
        return timer_val


    # add a sprite the the group of all sprites, Note that the sprite is being rendered according to its layer (see ImageSprite init)
    def add_sprite(self, player : pygame.sprite.Sprite) -> None:
        self.all_sprites.add(player)

    # run the game loop
    def run(self) -> None:
        while self.running:

            # start of frame, draw the empty stage  here.
            self.on_start_frame()

            # handle all events
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key in self.key_down_handlers:
                        handler = self.key_down_handlers[event.key]
                        handler(self)

                elif event.type == KEYUP:
                    if event.key in self.key_up_handlers:
                        handler = self.key_up_handlers[event.key]
                        handler(self)

                elif event.type in self.event_handler:
                    handler = self.event_handler[event.type]
                    handler(self)

                elif event.type == pygame.QUIT:
                    self.exit()
                    continue

            pressed_keys = pygame.key.get_pressed()

            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()

            for key in self.key_pressed_handlers.keys():
                if pressed_keys[key]:
                    handler = self.key_pressed_handlers[ key ]
                    handler(self)

            # change position of all sprites
            for sprite in self.all_sprites:
                sprite.update()

            # draw all sprites for this frame on the current buffer (the current buffer is not visible)
            for entity in self.all_sprites:
                entity.draw_on_buffer(self)

            # make current buffer visible.
            pygame.display.flip()

            self.on_colission_test()

            self.clock.tick(self.framerate)

        #pygame.quit()

    # calling this function will cause the game loop to exit, provided that run has been called earlier.
    def exit(self) -> None:
        self.running = False

    # called on the beginning of each frame; here you can override to fill in the backgraound picture.
    def on_start_frame(self) -> None:
        self.screen.fill((135, 206, 250))

    # finished the frame and flipped the display, now it's time to test for collisions.
    def on_colission_test(self) -> None:
        pass

    # set the current font that is used.
    def set_font(self, font_name : str, font_size : int) -> None:
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.SysFont(font_name, font_size)

    # set color of text
    def set_text_colors(self, fgcolor : Tuple[int,int,int], bgcolor : Tuple[int,int,int] = None) -> None:
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor

    # print a line of text on the screen
    def print(self, pos_x : int, pos_y : int,  *args) -> None:
        msg = ' '.join(map(str, args))
        text_surface = self.font.render(msg, True, self.fgcolor, self.bgcolor)
        self.screen.blit(text_surface, (pos_x, pos_y))


    # print a lot of text on the screen, text that does not fit the line is shown on the next line.
    def print_text(self, pos_x : int, pos_y : int, *args) -> None:

        msg = ' '.join(map(str, args))

        space = self.font.size(' ')[0]  # The width of a space.
        cur_x, cur_y = pos_x, pos_y
        for line in str(msg).splitlines():
            for word in line.split(" "):
                word_surface = self.font.render(word, 0, self.fgcolor)
                word_width, word_height = word_surface.get_size()
                if cur_x + word_width >= self.display_width:
                    cur_x = pos_x  # Reset the x.
                    cur_y += word_height  # Start on new row.
                self.screen.blit(word_surface, (cur_x, cur_y))
                cur_x += word_width + space
            cur_x = pos_x  # Reset the x.
            cur_y += word_height  # Start on new row.


    # print text on the screen, wait for the user to spress space
    def print_dialog(self, *args) -> None:

        self.screen.fill((135, 206, 250))
        self.print_text(0,0, *args)
        self.print(0, self.display_height - self.font_size, "Press Space To Continue")
        pygame.display.flip()

        cont = True
        while cont:
            for event in pygame.event.get():
                if (event.type == KEYDOWN and event.key == K_SPACE) or event.type == pygame.QUIT:
                    cont = False
                    break
            self.clock.tick(30)

    def load_image(self, file_name : str) -> None:
        if not file_name in self.map_file_to_image:
            image = pygame.image.load(file_name)
            if image is None:
                print("Can't load image file", file_name)
            self.map_file_to_image[ file_name ] = image
            return image

        return self.map_file_to_image[ file_name ]

    def play_sound(self, file_name : str, loops : int = 0) -> None:
        if not file_name in self.map_file_to_sound:
            sound = pygame.mixer.Sound(file_name)
            self.map_file_to_sound[ file_name ] = sound
        else:
            sound = self.map_file_to_sound[ file_name ]

        if sound is not None:
            sound.play(loops)
        else:
            print("sound: ", file_name, "not found!")

    def play_background_sound(self, file_name : str) -> None:
        self.play_sound(file_name, -1)

    def stop_all_sounds(self):
        for val in self.map_file_to_sound.values():
            val.stop()

    def get_cached_sprite(self, sprite_class : Type) -> None:
        type_name = str(sprite_class)
        if  type_name in self.map_type_to_spritecache:
            cache = self.map_type_to_spritecache[ type_name ]

            if len(cache) != 0:
                return cache.pop()
        return None



    def add_to_cache_(self, sprite : CacheableSprite) -> None:

        # check if sprite is cacheable - it is if it has the reuse method
        reuse_method = getattr(sprite,"reuse", None)
        if reuse_method is not None and callable(reuse_method):

            # this trick returns the type of the sprites derived class.
            type_name = str(sprite.__class__)

            # get per sprite type cache
            if type_name not in self.map_type_to_spritecache:
                self.map_type_to_spritecache[ type_name ] = list()

            sprite_cache = self.map_type_to_spritecache[ type_name ]

            # check if cache is not too big.
            if len(sprite_cache) < self.sprite_cache_size:

                # cache the sprite
                sprite_cache.append(sprite)
