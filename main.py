import pygame
from constants import *
from logger import log_state
from menus import Menu
from items import Item

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIEGHT))
    clock= pygame.time.Clock()
    dt = 0

    #Fonts
    title_font = pygame.font.SysFont('comicsans', 100)
    menu_font = pygame.font.SysFont('comicsans', 50)


    #Shop Items
    shop_items = [Item("Catcher", 100), Item("Potion", 200),  Item("Weights", 300)]

    #Menus
    title_menu = Menu(
        ["Start Game", "Exit Game"], menu_font, SCREEN_WIDTH// 2, 250
    )
    main_menu = Menu(
        ["Explore", "Manage Team", "Train", "Shop", "Back"], menu_font, 100, 150
    )
    shop_actions_menu = Menu(
        ["Buy", "Sell", "Back"], menu_font, 100, 150
    )
    shop_inventory_menu = Menu(
        shop_items, 
        menu_font, 
        300, 
        150,
        formatter=lambda item: f"{item.name} - ${item.price}" 
    )

    state = MENU_TITLE
   
    active_menu = "actions"

    

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
                
                if result == "Shop":
                    state = MENU_SHOP
                
                elif result == "Back":
                    state = MENU_TITLE
            
            elif state == MENU_SHOP:
                if active_menu == "actions":
                    result = shop_actions_menu.handle_input(event)

                    if result == "Buy":
                        active_menu = "inventory"
                    
                    elif result == "Sell":
                        print("selling not implemented yet")
                    
                    elif result == "Back":
                        state = MENU_MAIN

                elif active_menu == "inventory":
                    result = shop_inventory_menu.handle_input(event)

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE):
                        active_menu = "actions"

                    elif result is not None:
                        print("buying:", result) 

        
        screen.fill("black")
        if state == MENU_TITLE:
            text_title = title_font.render('Hello Monster Tamer', False, (255, 0, 0))
            text_rect_title = text_title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(text_title, text_rect_title)
            title_menu.titleDraw(screen)

        elif state == MENU_MAIN:
            text_main_title = title_font.render('Monster Tamer', False, (255, 0, 0))
            text_rect_main_title = text_main_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(text_main_title, text_rect_main_title)
            main_menu.draw(screen)

        elif state == MENU_SHOP:
            text_shop_title = title_font.render('Shop', False, (255, 0, 0))
            text_rect_shop_title = text_shop_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(text_shop_title, text_rect_shop_title)
            shop_actions_menu.draw(screen)
            shop_inventory_menu.draw(screen)
       
    
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
