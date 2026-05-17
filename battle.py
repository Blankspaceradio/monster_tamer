import pygame
from constants import *
from menus import *
from items import *
import random

class Battle:
    def __init__(self, player, player_monster, enemy_monster, menu_font):
        self.player_monster = player_monster
        self.enemy_monster = enemy_monster

        self.phase = PLAYER_TURN
        self.message = []
        self.player = player
        self.rewards_given = False
        self.end_messages = []

        self.selected_move = None
        self.active_menu = "actions"
        self.action_menu = Menu(
            lambda: ["Fight", "Item", "Switch", "Flee"],
            menu_font,
            50, 400
        )
        self.item_menu = Menu(
            lambda: list(self.player.inventory.keys()),
            menu_font,
            250,400,
            formatter=lambda item: f"{item.name} x{self.player.inventory[item]}"
        )
        self.switch_menu = Menu(
            lambda:self.player.team,
            menu_font,
            250,
            400,
            formatter=lambda monster: f"{monster.name} HP:{monster.hp} EN: {monster.energy}"
        )

        self.move_menu = Menu(
            lambda:self.player_monster.moves,
            menu_font,
            250,
            400,
            formatter=lambda move: f"{move.name} ({move.cost})"
        )
    
    def handle_input(self,event):
        if self.phase == BATTLE_END:
            return self.handle_battle_end(event)
        
        if self.active_menu == "actions":
            return self.handle_action_menu(event)
        
        elif self.active_menu == "moves":
            return self.handle_move_menu(event)
        
        elif self.active_menu == "items":
            return self.handle_item_menu(event)
        
        elif self.active_menu == "switch":
            return self.handle_switch_menu(event)
        
    def handle_action_menu(self,event):
        result = self.action_menu.handle_input(event)

        if result == "Fight":
            self.active_menu = "moves"

        elif result == "Item":
            self.active_menu = "items"

        elif result == "Switch":
            self.active_menu = "switch"

        elif result == "Flee":
            return "battle_over"
        
    def handle_move_menu(self, event):
        result = self.move_menu.handle_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                self.active_menu = "actions"

        if result:
            self.selected_move = result

            self.execute_turn()

            self.active_menu = "actions"

    def handle_switch_menu(self, event):
        result = self.switch_menu.handle_input(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                self.active_menu = "actions"

        if result:
            self.player_monster = result

            self.message = (f"Go {result.name}!")

            self.active_menu = "actions"
            
    
    def handle_item_menu(self,event):
        result = self.item_menu.handle_input(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                self.active_menu = "actions"
        
        if result:
            result.use(self.player_monster)

            self.player.remove_item(result)

            self.message = (f"Used {result.name}")

            self.action_menu = "actions"

    def handle_battle_end(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "battle_over"
            
        
    def handle_player_turn(self, event):
        result = self.move_menu.handle_input(event)

        if result:
            self.selected_move = result
            self.execute_turn()

    def execute_turn(self):
        player_move = self.selected_move
        if not self.enemy_monster.moves:
            return
        enemy_move = random.choice(self.enemy_monster.moves)

        #determine turn order
        first, first_move, second, second_move = self.determine_turn_order(
            self.player_monster,
            player_move,
            self.enemy_monster,
            enemy_move
        )

        #first attack
        result = first_move.use(first,second)
        self.message.extend(result["messages"])
        if second.is_alive():
           result = second_move.use(second,first)
           self.message.extend(result["messages"])

        self.check_battle_end()

    def determine_turn_order(self, m1, move1,m2,move2):
        if m1.speed >= m2.speed:
            return m1, move1, m2, move2
        else:
            return m2, move2, m1, move1
        
    def check_battle_end(self):
        if not self.player_monster.is_alive():
            self.phase = BATTLE_END
            self.message = "You Lost!"

        elif not self.enemy_monster.is_alive():
            self.phase = BATTLE_END
            self.handle_victory()

    def handle_victory(self):
        if self.rewards_given:
            return
        self.rewards_given = True
        self.end_messages = []

        exp_gain = self.enemy_monster.level * 10

        self.player_monster.gain_exp(exp_gain)
        self.end_messages.append(f"{self.player_monster.name} gained {exp_gain} EXP!")

        #Loot
        gold_gain = random.randint(5,20)

        self.player.add_gold(gold_gain)

        self.end_messages.append(f"You found {gold_gain} gold!")

        if random.random() < 0.25:
            item = potion

            self.player.add_item(item)
            self.end_messages.append(f"Found {item.name}!")

    def draw(self, screen, font):
        self.draw_monsters(screen, font)

        for i, message in enumerate(self.message[-12:]):
            text = font.render(
                message,
                True,
                (255, 255, 255)
            )
            screen.blit(text, (460, 140 + i * 35))

        if self.phase == BATTLE_END:
            for i, message in enumerate(self.end_messages):
                text = font.render(
                    message,
                    True,
                    (255, 255, 255)
                )
                screen.blit(text,(50, 300 + i * 40))
            continue_text = font.render(
                "Press ENTER to continue",
                True,
                (200, 200, 200)
            )
            screen.blit(continue_text, (50, 500))
        
        else:

            if self.active_menu == "actions":
                self.action_menu.draw(screen)

            elif self.active_menu == "moves":
                self.move_menu.draw(screen)

            elif self.active_menu == "items":
                self.item_menu.draw(screen)

            elif self.active_menu == "switch":
                self.switch_menu.draw(screen)

        #self.draw_ui(screen, font)
    
    def draw_monsters(self, screen, font):
        player_text = font.render(
        f"{self.player_monster.name} HP: {self.player_monster.hp}/{self.player_monster.max_hp}",
        True,
        (255, 255,255)
        )
        player_monster_text = font.render(
            f"Energy: {self.player_monster.energy}/{self.player_monster.max_energy}",
            True,
            (255, 255,255)
        )

        enemy_text = font.render(
            f"{self.enemy_monster.name} HP: {self.enemy_monster.hp}/{self.enemy_monster.max_hp}",
            True,
            (255, 255, 255)
        )
        enemy_monster_text = font.render(
            f"Energy: {self.enemy_monster.energy}/{self.enemy_monster.max_energy}",
            True,
            (255, 255,255)
        )

        stats = [
            ("Courage", self.player_monster.courage),
            ("Power", self.player_monster.power),
            ("Wisdom", self.player_monster.wisdom),
            ("Speed",self.player_monster.speed),
        ]

        screen.blit(player_text,(50, 50))
        screen.blit(player_monster_text, (50, 100))
        screen.blit(enemy_text, (500, 50))
        screen.blit(enemy_monster_text, (500, 100))

        for i, (label, value) in enumerate(stats):
            text = font.render(
                f"{label}: {value}",
                True,
                (255, 255, 255)
            )
            screen.blit(text, (50, 150 + i * 40))

    def draw_ui(self, screen,font):
        message_text = font.render(
            self.message,
            True,
            (255,255,255)
        )
        screen.blit(message_text, (50,350))

    