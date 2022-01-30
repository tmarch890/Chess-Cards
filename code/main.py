import pygame, gui, board, data, cycle
from sys import exit
from openings import opening_dictionary

pygame.init()
screen_width = 812
screen_height = 512
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chess Cards')

font = pygame.font.SysFont(None, 40)

in_menu = True

openings = opening_dictionary
piece_assets = data.import_all()

menus = openings
main_menu = gui.Menu(screen, {'Flashcard Practice':'', 'Choose Opening': menus,'Manage Repetoire':'', 'Settings': ''}, font, 'Main Menu', '')
color_button = pygame.sprite.Group()
color_button_sprite = gui.Color_button()
color_button.add(color_button_sprite)
current_menu = main_menu
move_count_max = 100

while True:
    inputs = pygame.event.get()
    for event in inputs:
        if event.type == pygame.QUIT:
            data.export_all()
            pygame.quit()
            exit()

    if in_menu:
        current_menu.final_menu = False
        for event in inputs:
            # print(current_menu.name)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if color_button_sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        color_button_sprite.swap()
                    user_choice = current_menu.user_choice()
                    if user_choice != '':
                        if current_menu.final_menu:
                            in_menu = False
                            path = f'{current_menu.path}/{user_choice}/{color_button_sprite.color}'
                            path_list = path.split('/')
                            current_cycle = cycle.Cycle(color_button_sprite.color, move_count_max, current_menu.sub_menus_dict[user_choice], path_list, piece_assets, screen, font)
                            # game_board = board.Board(piece_assets, path_list[-3], path_list[-2], color_button_sprite.color, current_menu.sub_menus_dict[user_choice], screen, font)
                        else:
                            for sub_menu in current_menu.sub_menus:
                                if sub_menu.name == user_choice:
                                    current_menu = sub_menu

                if event.button > 3:
                    current_menu.scroll(event)

        current_menu.display()
        if current_menu != main_menu:
            color_button.draw(screen)

    if not in_menu:
        if not current_cycle.current_board.to_menu:
            screen.fill('black')

            current_cycle.update(inputs)
        else:
            del current_cycle
            in_menu = True
            current_menu = main_menu

    pygame.display.update()
    clock.tick(60)
