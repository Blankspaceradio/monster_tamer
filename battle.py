import pygame
from constants import *
from menus import *
import random

class Battle:
    def __init__(self, player_monster, enemy_monster, menu_font):
        self.player_monster = player_monster
        self.enemy_monster = enemy_monster

        self.phase = PLAYER_TURN
        self.message = ""

        self.selected_move = None

       # self.action_menu = Menu(
       #     lambda: ["Fight", "Item", "Run"],
        #    menu_font,
         #   50, 400
        #)

        self.move_menu = Menu(
            lambda:self.player_monster.moves,
            menu_font,
            250,
            400,
            formatter=lambda move: f"{move.name} ({move.cost})"
        )
    
    def handle_input(self,event):
        if self.phase == PLAYER_TURN:
            return self.handle_player_turn(event)
        elif self.phase == BATTLE_END:
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
        first_move.use(first,second)

        if second.is_alive():
            second_move.use(second,first)
        
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
            self.message = "You Won!"

    def draw(self, screen, font):
        self.draw_monsters(screen, font)

        if self.phase == PLAYER_TURN:
            self.move_menu.draw(screen)

        self.draw_ui(screen, font)
    
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

    