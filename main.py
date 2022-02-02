import pygame
from code import gui
from code import cycle
from code import data
from code import deck
from sys import exit
from code.openings import opening_dictionary as openings

pygame.init()
screen_width = 812
screen_height = 512
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chess Cards')

font = pygame.font.SysFont(None, 40)

in_menu = True
choosing_opening = False

piece_assets, user_data = data.import_all()
# print(user_data)

main_menu = gui.Menu(screen, {'Practice Repetoire':'', 'Choose Opening': openings,'Manage Repetoire':'', 'Statistics': '', 'Settings': ''}, font, 'Main Menu', '', alphabetical=False)
color_button = pygame.sprite.Group()
color_button_sprite = gui.Color_button()
color_button.add(color_button_sprite)
current_menu = main_menu

while True:
    inputs = pygame.event.get()
    for event in inputs:
        if event.type == pygame.QUIT:
            data.export(progress=user_data['progress'])
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
                        if user_choice == 'Choose Opening' or choosing_opening:
                            choosing_opening = True
                            if current_menu.final_menu:
                                in_menu = False
                                choosing_opening = False
                                path = f'{current_menu.path}/{user_choice}/{color_button_sprite.color}'
                                current_cycle = cycle.Cycle(current_menu.sub_menus_dict[user_choice], path, piece_assets, screen, font, color=color_button_sprite.color, progress=user_data['progress'])
                            else:
                                for sub_menu in current_menu.sub_menus:
                                    if sub_menu.name == user_choice:
                                        current_menu = sub_menu

                        elif user_choice == 'Practice Repetoire':
                            in_menu = False
                            current_deck = deck.Deck(user_data['progress'], piece_assets, screen, font)

                if event.button > 3:
                    current_menu.scroll(event)

        current_menu.display()
        if current_menu != main_menu:
            color_button.draw(screen)

    if not in_menu:
        try:
            if current_deck.done or current_deck.current_cycle.current_board.to_menu:
                del current_deck
                in_menu = True
                current_menu = main_menu

            else:
                screen.fill('black')
                current_deck.update(inputs)
        except:
            if not current_cycle.current_board.to_menu:
                screen.fill('black')
                current_cycle.update(inputs)
            else:
                del current_cycle
                in_menu = True
                current_menu = main_menu

    pygame.display.update()
    clock.tick(60)
