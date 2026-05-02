import pygame
from constants import *
from logger import log_state
from menus import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIEGHT))
    clock= pygame.time.Clock()
    dt = 0

    #Fonts
    title_font = pygame.font.SysFont('comicsans', 100)
    menu_font = pygame.font.SysFont('comicsans', 50)

    #Menus
    title_menu = Menu(
        ["Start Game", "Exit Game"], menu_font, SCREEN_WIDTH// 2, 250
    )
    main_menu = Menu(
        ["Explore", "Manage Team", "Train", "Shop", "Back"], menu_font, 200, 100
    )

    state = MENU_TITLE
   
    text_title = title_font.render('Hello Monster Tamer', False, (255, 0, 0))
    text_rect_title = text_title.get_rect(center=(SCREEN_WIDTH // 2, 100))

    while 1 < 2:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            #--TITLE MENU--
            if state == MENU_TITLE:
                
                result = title_menu.handle_input(event)

                if result == "Start Game":
                    state = MENU_MAIN
                elif result == "Exit Game":
                    return
                
            elif state == MENU_MAIN:
                result = main_menu.handle_input(event)
                if result == "Back":
                    state = MENU_TITLE
        
        screen.fill("black")
        if state == MENU_TITLE:
            text_title = title_font.render('Hello Monster Tamer', False, (255, 0, 0))
            text_rect_title = text_title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(text_title, text_rect_title)
            title_menu.draw(screen)
        elif state == MENU_MAIN:
            main_menu.draw(screen)
       
    
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
