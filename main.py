import pygame
from constants import *
from logger import log_state
from menus import *
from items import *
from player import *
from battle import *
from explore import *
from monsterDetailsScreen import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock= pygame.time.Clock()
    dt = 0

    #Fonts
    title_font = pygame.font.SysFont('comicsans', 100)
    menu_font = pygame.font.SysFont('comicsans', 50)
    extra_controls = pygame.font.SysFont('comicsans', 30)


    #Basic player
    player = Player("Mark")

    

    #Shop Items
    shop_items = [CatchItem("Catcher", 100, 50), HealingItem("Potion", 200,20),  TrainingItem("Weights", 300, 5,"Power")]

    #Menus
    title_menu = Menu(
        ["Start Game", "Exit Game"], menu_font, SCREEN_WIDTH// 2, 250
    )
    main_menu = Menu(
        ["Explore", "Manage Team", "Inventory", "Train", "Shop", "Back"], menu_font, 100, 150
    )
    shop_actions_menu = Menu(
        ["Buy", "Sell", "Back"], menu_font, 100, 150
    )
    shop_inventory_menu = Menu(
        lambda: shop_items, 
        menu_font, 
        300, 
        150,
        formatter=lambda item: f"{item.name} - ${item.price}" 
    )
    player_inventory_menu = Menu(
        lambda: list(player.inventory.keys()),
        menu_font,
        300, 150,
        formatter=lambda item:inventory_formatter(item, player.inventory)
    )
    player_inventory_sell_menu = Menu(
        lambda: list(player.inventory.keys()),
        menu_font,
        300,150,
        formatter=lambda item:inventory_formatter_sell(item, player.inventory)
    )
    explore_menu = Menu(
        lambda: [forest, mountain],
        menu_font,
        100,
        100,
        formatter=lambda area: area.name
    )
    team_menu = Menu(
        lambda: player.team,
        menu_font,
        100,
        150,
        formatter=lambda monster: f"{monster.name} Lv{monster.level}"
    )
    storage_menu = Menu(
        lambda: player.storage,
        menu_font,
        500,
        150,
        formatter=lambda monster: f"{monster.name} Lv{monster.level}"
    )





    state = MENU_TITLE
   
    active_menu = "actions"
    popup_message = None
    previous_state = None
    

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
                
                if result == "Explore":
                    state = MENU_EXPLORE

                elif result == "Manage Team":
                    state = MENU_TEAM
                    active_panel = "team"

                elif result == "Shop":
                    state = MENU_SHOP

                elif result == "Inventory":
                    state = MENU_PLAYER_INVENTORY
                
                elif result == "Back":
                    state = MENU_TITLE
            
            elif state == MENU_PLAYER_INVENTORY:
                result = player_inventory_menu.handle_input(event)
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE):
                    state = MENU_MAIN
                
            
            elif state == MENU_SHOP:
                if active_menu == "actions":
                    result = shop_actions_menu.handle_input(event)

                    if result == "Buy":
                        active_menu = "shop inventory"
                    
                    elif result == "Sell":
                        active_menu = "player sell"
                    
                    elif result == "Back":
                        state = MENU_MAIN

                elif active_menu == "shop inventory":
                    result = shop_inventory_menu.handle_input(event)

                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        active_menu = "actions"

                    elif result:
                        if player.spend_gold(result.price):
                            player.add_item(result)
                        else:
                            popup_message = "Not enough gold"
                            previous_state = state
                            state = POPUP
                            continue
                elif active_menu == "player sell":
                    state = MENU_PLAYER_SELL_INVENTORY

            elif state == MENU_PLAYER_SELL_INVENTORY:
                result = player_inventory_sell_menu.handle_input(event)

                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        active_menu = "actions"
                        state = MENU_SHOP
                elif result:
                    player.remove_item(result)
                    player.add_gold(result.price//2)

            elif state == BATTLE:
                Battle.handle_input(event)
                Battle.darw(screen, menu_font)
            
            elif state == MENU_EXPLORE:
                result = explore_menu.handle_input(event)

                if result:
                    selected_area = result
                    encounters = selected_area.generate_encounters()
                    state = MENU_ENCOUNTER
                
                encounter_menu = Menu(
                    lambda: encounters,
                    menu_font,
                    300, 
                    150,
                    formatter=lambda monster: f"{monster.name} Lv{monster.level}"
                )
            
            elif state == MENU_ENCOUNTER:
                result = encounter_menu.handle_input(event)
                if result:
                    enemy_monster = result

            elif state == MENU_TEAM:
                if active_panel == "team":
                    result = team_menu.handle_input(event)

                elif active_panel == "storage":
                    result = storage_menu.handle_input(event)

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE):
                    state = MENU_MAIN

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if active_panel == "team":
                        monster = team_menu.get_selected()
                    elif active_panel == "storage":
                        monster = storage_menu.get_selected()
                    
                    if monster:
                        monster_details_screen = MonsterDetailsScreen(
                            monster,
                            menu_font,
                            title_font,
                        )
                        previous_state = state
                        state = MONSTER_DETAILS

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    active_panel = "team"
                elif  event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    active_panel = "storage"

                if active_panel == "team" and result:
                    player.move_to_storage(result)

                if active_panel == "storage" and result:
                    success = player.move_to_team(result)

                    if not success:
                        popup_message = "Team is full"
                        state = POPUP
                        previous_state= MENU_TEAM
            
            elif state == MONSTER_DETAILS:
                result = monster_details_screen.handle_input(event)

                if result == "back":
                    state = MENU_TEAM
            
            
        
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

        elif state == MENU_PLAYER_INVENTORY:
            text_player_inventory_title = title_font.render('Inventory', False, (255, 0, 0))
            text_rect_player_inventory_title = text_player_inventory_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(text_player_inventory_title, text_rect_player_inventory_title)
            player_inventory_menu.draw(screen)

        elif state == MENU_SHOP:
            text_shop_title = title_font.render('Shop', False, (255, 0, 0))
            text_rect_shop_title = text_shop_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            text_shop_gold = menu_font.render(f"${player.gold}", False, (255,0,0))
            text_rect_gold = text_shop_gold.get_rect(center=(1100, 100))
            screen.blit(text_shop_gold, text_rect_gold)
            screen.blit(text_shop_title, text_rect_shop_title)
            
            shop_actions_menu.draw(screen)
            shop_inventory_menu.draw(screen)
        elif state == MENU_PLAYER_SELL_INVENTORY:
            text_shop_title = title_font.render('Inventory: SELL', False, (255, 0, 0))
            text_rect_shop_title = text_shop_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            text_shop_gold = menu_font.render(f"${player.gold}", False, (255,0,0))
            text_rect_gold = text_shop_gold.get_rect(center=(1100, 100))
            screen.blit(text_shop_gold, text_rect_gold)
            screen.blit(text_shop_title, text_rect_shop_title)

            shop_actions_menu.draw(screen)
            player_inventory_sell_menu.draw(screen)

        elif state == MENU_EXPLORE:
            text_explore_title = title_font.render('Explore', False, (255, 0, 0))
            text_rect_explore_title = text_explore_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(text_explore_title, text_rect_explore_title)
            explore_menu.draw(screen)
        
        elif state == MENU_ENCOUNTER:
            encounter_menu.draw(screen)

        elif state == MENU_TEAM:
            text_team_title = title_font.render('Manage Team', False, (255, 0, 0))
            text_rect_team_title = text_team_title.get_rect(center=(SCREEN_WIDTH//2, 100))
            
            text_extra = extra_controls.render("Enter: Move Monster\nSpace: View Details\nESC: Back", False, (255,0,0))
            text_rect_extra = text_extra.get_rect(center=(500, 500))
            screen.blit(text_team_title, text_rect_team_title)
            screen.blit(text_extra, text_rect_extra)
            team_menu.draw(screen, active=(active_panel == "team"))
            storage_menu.draw(screen, active=(active_panel=="storage"))

        elif state == MONSTER_DETAILS:
            monster_details_screen.draw(screen)

        elif state == POPUP:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE):
                    state = previous_state
            
            if previous_state == MENU_SHOP:
                shop_actions_menu.draw(screen)
                shop_inventory_menu.draw(screen)
            
            draw_popup(screen,menu_font,popup_message)
           
       
    
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
