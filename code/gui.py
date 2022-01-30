import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, pos, font):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((115,85,75))
        self.size = size
        self.highlight = pygame.Surface((int(.95*self.size[0]), int(.8*self.size[1])))
        self.highlight.fill((135,105,95))
        self.text = text
        self.text_render = font.render(self.text, True, 'White')
        self.rect = self.image.get_rect(midtop = pos)
        self.centered_x = self.size[0]/2 - int(len(text)*7.8)
        self.centered_y = self.size[1]/2 - 13

    def update(self, screen):
        self.image.blit(self.highlight, (int(.025*self.size[0]), int(.1*self.size[1])))
        self.image.blit(self.text_render, (self.centered_x, self.centered_y))

class Color_button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = 'white'
        self.image = pygame.Surface((32,32))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = (32,32))

    def swap(self):
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'
        self.image.fill(self.color)

class Menu:
    def __init__(self, screen, sub_menus_dict, font, name, path):
        super().__init__()
        self.screen = screen
        self.name = name
        self.sub_menus_dict = sub_menus_dict
        self.final_menu = False
        self.buttons = pygame.sprite.Group()
        self.path = path
        if isinstance(self.sub_menus_dict, dict):
            (pos_x,pos_y) = (406, 50)
            self.sub_menus_list = [menu for menu in self.sub_menus_dict.keys()]
            self.sub_menus_list.sort()
            self.sub_menus = []
            for menu in self.sub_menus_list:
                if isinstance(self.sub_menus_dict[menu], dict):
                    path = f'{self.path}/{menu}'
                    new_sub_menu = Menu(self.screen, self.sub_menus_dict[menu], font, menu, path)
                    self.sub_menus.append(new_sub_menu)
                new_button = Button(menu, (300,50), (pos_x, pos_y), font)
                self.buttons.add(new_button)
                pos_y += 75

    def user_choice(self):
        mouse_pos = pygame.mouse.get_pos()
        user_choice = ''
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                user_choice = button.text
                if not isinstance(self.sub_menus_dict[user_choice], dict):
                    self.final_menu = True
        return user_choice

    def scroll(self, event):
        if event.button == 4:
            for button in self.buttons:
                button.rect.y -= 20
        if event.button == 5:
            for button in self.buttons:
                button.rect.y += 20


    def display(self):
        self.screen.fill((90,60,50))
        for button in self.buttons:
            button.update(self.screen)

        self.buttons.draw(self.screen)
