
# Intro

I have been trying to make a schedule for a python course for my kids [here](https://github.com/MoserMichael/pythoncourse); one of the things that i would like to do is a game with pygame.
Now there are lots of nice pygame tutorials, I followed the following [Pygame primer](https://realpython.com/pygame-a-primer/) by Jon Fincher, the source code for the tutorial is [here](https://github.com/realpython/materials/tree/master/pygame-a-primer)

The tutorial was great, the documentation for pygame is perfectly adequate, however there was one thing missing - fun; doing something in pygame is hard work!

Compare that to what I had in my youth: I got my intro to programming on a [TI 99/4A home computer](https://en.wikipedia.org/wiki/Texas_Instruments_TI-99/4A) with a 16 kilobyte extended Basic ROM cartridge; I had tons of fun programming games with the sprite graphics on that machine, and the result in 1986 was not so much different as compared to what you have today with pygames, in this age, some thirty five years later (well, maybe only my games didn't get any better, even if i got rid of goto ;-)

Now this project is trying to make a wrapper, that is hiding some of the complexity and boilerplate setup of the pygame package.
Here is the result: 

1) The PyWrap module holds the wrapper for pygame
2) the root directory holds a sequence of files that develop a game, each one is adding a feature on top of the previous one. The game implements the same game as in the  [Pygame primer](https://realpython.com/pygame-a-primer/) by Jon Fincher, and is using the same graphics and sounds.

I am not perfectly happy with the result, it does simplify things a bit, however the result is still somewhat complex.
The [original tutorial](https://github.com/realpython/materials/blob/master/pygame-a-primer/py_tut_with_images.py) was 221 lines long, my result [is here](https://github.com/MoserMichael/pygamewrap/blob/master/08-add-sounds.py) (without wrapper library) and is 222 lines long (well, I am adding a few features here and there, to be fair)

Well, anyway, here is the result for you to judge.

# Issues

The pygame windows does not automatically get the focus, it is not brought to the foreground. I didn't find a way to do this, in a platform independent manner.

# License 

licensed under MIT license


