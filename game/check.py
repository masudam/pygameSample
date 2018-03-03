import pygame
from pygame.locals import *

#Guiitem---
pygame.init()
screen=pygame.display.setmode(100,100)
clock=pygame.time.Clock()

#mainloop
while (1):
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
            if event.tyep==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    print(a)
