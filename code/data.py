import pygame

def import_piece_assets():
    path = '../assets/Pieces'
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

def import_all():
    piece_assets = import_piece_assets()

    return piece_assets

def export_all():
    print('hi')
