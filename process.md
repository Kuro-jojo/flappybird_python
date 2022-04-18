1. import modules
2. initialize the game
3. create the display surface
4. implement the frame rate limitation 
5. load images 
6. for collision detection
   1. can use rectangle with surface.get_rect(position=())
   2. gravity for falling down 
7. look for events 
   1. quit 
8. display surface on the screen (blit)
9.  
10. display all things on the screen (update)


## pipes process
1. import image on surface
2. put rect around surface
3. blit(surface, rect)

## collision detection
check if pipes rect are collided the bird

## rotate bird
use rotozoom method and alpha value for conversion to remove black square

## text in pygame
1. create a font
2. render the font
3. use the resulting text surface

## sound
1. import pygame.mixer