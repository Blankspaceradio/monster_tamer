import pygame

class MonsterDetailsScreen:
    def __init__(self, monster, font, title_font):
        self.monster = monster

        self.font = font
        self.title_font = title_font

    def draw(self, screen):
        monster = self.monster

        #title
        title = self.title_font.render(monster.name, True, (255, 255, 255))
        screen.blit(title, (50,30))

        level_text = self.font.render(
            f"Level: {monster.level}",
            True,
            (255, 255, 255)
        )
        screen.blit(level_text, (50,120))

        elements = ", ".join(monster.element)

        element_text = self.font.render(
            f"Elements: {elements if elements else'None'}",
            True,
            (255, 255, 255)
        )
        screen.blit(element_text, (50,160))

        stats = [
            ("HP", f"{monster.hp}/{monster.max_hp}"),
            ("Energy", monster.energy),
            ("Courage", monster.courage),
            ("Power", monster.power),
            ("Wisdom", monster.wisdom),
            ("Speed", monster.speed),
        ]

        for i, (label, value) in enumerate(stats):
            text = self.font.render(
                f"{label}: {value}",
                True,
                (255, 255, 255)
            )
            screen.blit(text, (50, 220 + i * 40))

        moves_title = self.font.render(
            "Moves",
            True,
            (255, 255, 0)
        )
        screen.blit(moves_title, (400,120))

        for i, move in enumerate(monster.moves):
            move_text = self.font.render(
                move.name,
                True,
                (255, 255, 255)
            )
            screen.blit(move_text, (400, 170 + i * 40))

    def handle_input(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                return "back"