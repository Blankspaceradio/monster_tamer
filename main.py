import pygame
from constants import SCREEN_HIEGHT
from constants import SCREEN_WIDTH
from logger import log_state

def main():
    pygame.init()
    clock= pygame.time.Clock()
    dt = 0
    
    start_menu_options = ["Start Game", "Exit Game"]
    selected = 0



    print("Hello from monster-tamer!")
 
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIEGHT))
    screen_rect = screen.get_rect()

    #title font
    title_font = pygame.font.SysFont('comicsans', 100)
    text_title = title_font.render('Hello Monster Tamer', False, (255, 0, 0))
    text_rect_title = text_title.get_rect(center=(SCREEN_WIDTH // 2, 100))

    #Start Game Font
    menu_font = pygame.font.SysFont('comicsans', 50)
    text_start_game = menu_font.render('Start Game', False, (255, 0, 0))
    text_rect_start_game = text_start_game.get_rect(center=(SCREEN_WIDTH // 2, 300))

    #Exit Game
    text_exit_game = menu_font.render('Exit Game', False, (255, 0,0))
    text_rect_exit_game = text_exit_game.get_rect(center=(SCREEN_WIDTH // 2, 400))


    while 1 < 2:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected -1) % len(start_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected +1) % len(start_menu_options)
        
        screen.fill("black")
        screen.blit(text_title, text_rect_title)
        for i, options in enumerate(start_menu_options):
            text = menu_font.render(options, False, (255,0,0))
            y = 300 + i * 50
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y))
            screen.blit(text, text_rect)

            if i == selected:
                arrow  = menu_font.render(">", False, (255, 0, 255))
                arrow_rect = arrow.get_rect(midright=(text_rect.left - 10, text_rect.centery))
                screen.blit(arrow,arrow_rect)
       
    


    
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
