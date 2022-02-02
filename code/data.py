import pygame, ast

def import_piece_assets():
    path = './assets/Pieces'
    pieces = {'p': '', 'P': '', 'n': '', 'N': '', 'b': '', 'B': '', 'r': '', 'R': '', 'q': '', 'Q': '', 'k': '', 'K': ''}
    for piece in pieces:
        if piece.isupper():
            piece_path = f'{piece.lower()}2.png'
        else:
            piece_path = f'{piece}.png'
        full_path = f'{path}/{piece_path}'
        pieces[piece] = pygame.image.load(full_path).convert_alpha()
        pieces[piece] = pygame.transform.scale(pieces[piece], (64,64))

    return pieces


def import_user_data():
    files = {'progress':'', 'settings':''}
    for file in files:
        file_obj = open(f'./user_data/{file}.txt', 'rt')
        file_string = file_obj.read()
        files[file] = ast.literal_eval(file_string)
        file_obj.close()

    return files


def import_all():
    piece_assets = import_piece_assets()
    user_data = import_user_data()

    return piece_assets, user_data

def export(**kwargs):
    for file_name in kwargs:
        if kwargs[file_name]:
            file_obj = open(f'./user_data/{file_name}.txt', 'wt')
            file_obj.write(str(kwargs[file_name]))
            file_obj.close
