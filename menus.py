import pygame

class Menu:
    def __init__(self, options, font, x, y, spacing=50, formatter=None):
        self.options = options
        self.font = font
        self.x = x
        self.y = y
        self.spacing = spacing
        self.selected = 0

        self.formatter = formatter if formatter else lambda x: str(x)

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)

        elif event.key == pygame.K_RETURN:
            return self.options[self.selected]

        return None

    def titleDraw(self, screen):
        for i, option in enumerate(self.options):
            y = self.y + i * self.spacing

            text = self.font.render(option, False, (255, 0, 0))
            text_rect = text.get_rect(center=(self.x, y))
            screen.blit(text, text_rect)

            if i == self.selected:
                arrow = self.font.render(">", False, (255, 0, 255))
                arrow_rect = arrow.get_rect(midright=(text_rect.left - 10, text_rect.centery))
                screen.blit(arrow, arrow_rect)
    
    def draw(self, screen, active=True):
        color = (255, 0, 0) if active else (100, 100, 100)

        for i, option in enumerate(self.options):
            y = self.y + i * self.spacing

            label = self.formatter(option)
            text = self.font.render(label, False, color)
            text_rect = text.get_rect(topleft=(self.x, y))
            screen.blit(text, text_rect)

            if active and i == self.selected:
                arrow = self.font.render(">", False, (255, 0, 255))
                arrow_rect = arrow.get_rect(midright=(text_rect.left - 10, text_rect.centery))
                screen.blit(arrow, arrow_rect)