import pygame
from constants import SCREEN_HIEGHT
from constants import SCREEN_WIDTH
from logger import log_state

def main():
    pygame.init()
    clock= pygame.time.Clock()
    dt = 0



    print("Hello from monster-tamer!")
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIEGHT))
    while 1 < 2:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
    



    pygame.display.flip()
    dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
