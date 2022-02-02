import pygame
from code.openings import opening_dictionary
from code.gui import Button

class Square(pygame.sprite.Sprite):
    def __init__(self, rank, file):
        super().__init__()
        self.rank = rank
        self.file = file
        self.screen_pos = (self.file * 64, self.rank * 64)
        self.image = pygame.Surface((64, 64))
        self.reset_color()
        self.rect = self.image.get_rect(topleft = self.screen_pos)

    def highlight(self):
        self.image.fill((0, 180, 180))

    def reset_color(self):
        if (self.rank % 2) - (self.file % 2) == 0:
            self.image.fill((240, 217, 181))
        else:
            self.image.fill((181, 136, 99))

class Piece(pygame.sprite.Sprite):
    def __init__(self, type, pos, image):
        super().__init__()
        self.type = type
        self.rank = pos[0]
        self.file = pos[1]
        self.screen_pos = (self.file*64, self.rank*64)
        self.moving = False
        self.captured = False
        if self.type.isupper():
            self.color = 'White'
        else:
            self.color = 'Black'

        # self.get_assets()
        # self.image = pygame.Surface((32,32))
        # font = pygame.font.SysFont(None, 90)

        self.image = image

        # self.image = font.render(self.type, True, self.color)
        # self.image.fill((random.randint(1,255), random.randint(1,255), random.randint(1,255)))
        self.rect = self.image.get_rect(topleft = self.screen_pos)

    def move(self):
        self.rect = self.image.get_rect(center = pygame.mouse.get_pos())

    def snap(self):
        self.rank = int((self.rect.y+32)/64)
        self.file = int((self.rect.x+32)/64)
        (self.rect.y, self.rect.x) = (self.rank*64, self.file*64)



    def update(self, color):
        if self.moving:
            self.move()

class Board:
    def __init__(self, piece_assets, name1, name2, color, opening, move_count_max, screen, font):
        self.screen = screen
        self.piece_assets = piece_assets

        # Sidebar
        self.sidebar = pygame.Surface((300,512))
        self.sidebar.fill((90,60,50))
        self.font = font
        self.opening_text1 = self.font.render(name1, True, 'White')
        self.opening_text2 = self.font.render(name2, True, 'White')
        self.correct_text = self.font.render('', True, 'White')
        self.buttons = pygame.sprite.Group()
        new_button = Button('Return to menu', (280,50), (660,400), self.font)
        self.buttons.add(new_button)

        initial = 'rnbqkbnr/pppppppp/        /       /        /        /PPPPPPPP/RNBQKBNR'
        self.pieces = pygame.sprite.Group()
        self.squares = pygame.sprite.Group()
        self.board = initial.split('/')
        self.color = color
        self.correct = True
        self.board_end = False
        self.to_next_board = False
        self.to_menu = False
        self.all_comp_moves = False
        # print(opening)
        self.opening = opening.split()
        self.move_count_max = move_count_max
        if self.move_count_max >= len(self.opening) - 1:
            self.move_count_max = len(self.opening) - 1
        self.set_board()
        self.line = []
        self.move_timer = 46
        self.highlight = True

    def set_board(self):
        self.move_count = 0
        self.pieces.empty()
        self.squares.empty()
        for rank in range(8):
            for file in range(8):
                if self.board[rank][file-1].isalpha():
                    image = self.piece_assets[self.board[rank][file]]
                    piece = Piece(self.board[rank][file], (rank, file), image)
                    self.pieces.add(piece)
                square = Square(rank, file)
                self.squares.add(square)
        self.start_move = 0
        if self.color == 'black':
            self.flip()
            self.color = 'black'
            self.start_move = 1

    def reset(self):
        self.set_board()
        self.correct = True
        self.board_end = False
        self.to_next_board = False
        self.all_comp_moves = False
        self.line = []
        self.move_timer = 46
        self.correct_text = self.font.render('', True, 'White')
        self.buttons.empty()
        new_button = Button('Return to menu', (280,50), (660,400), self.font)
        self.buttons.add(new_button)

    def capture(self, piece):
        captured = False
        for other_piece in self.pieces:
            if piece.rect.colliderect(other_piece) and not other_piece.moving:
                other_piece.kill()
                captured = True
        return captured

    def inputs(self, inputs):
        for event in inputs:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == 'Show correct move':
                            moves = self.move_count
                            self.set_board()
                            self.all_comp_moves = True
                            for move in range(moves):
                                self.comp_move()
                        elif button.text == 'Next line':
                            self.to_next_board = True
                        elif button.text == 'Return to menu':
                            self.to_menu = True

                if not self.board_end:
                    for piece in self.pieces:
                        if piece.rect.collidepoint(mouse_pos):
                            piece.moving = True

            if event.type == pygame.MOUSEBUTTONUP:
                for piece in self.pieces:
                    if piece.moving:
                        self.move_count += 1

                        # Castling
                        if piece.type == 'K' and (piece.rank, piece.file) == (7,4):

                            piece.snap()
                            if self.color == 'black':
                                square =  'hgfedcba'[piece.file] + str(piece.rank + 1)
                            else:
                                square =  'abcdefgh'[piece.file] + str(8 - piece.rank)

                            if square == 'g1':
                                castle_side = 'king'
                            elif square == 'c1':
                                castle_side = 'queen'
                            else:
                                castle_side = ''
                            self.castle('white', castle_side)

                        elif piece.type == 'k' and (piece.rank, piece.file) == (7,3):

                            piece.snap()
                            if self.color == 'black':
                                square =  'hgfedcba'[piece.file] + str(piece.rank + 1)
                            else:
                                square =  'abcdefgh'[piece.file] + str(8 - piece.rank)

                            if square == 'g8':
                                castle_side = 'king'
                            elif square == 'c8':
                                castle_side = 'queen'
                            else:
                                castle_side = ''
                            self.castle('black', castle_side)

                        else:
                            piece.snap()
                            if self.color == 'black':
                                square =  'hgfedcba'[piece.file] + str(piece.rank + 1)
                            else:
                                square =  'abcdefgh'[piece.file] + str(8 - piece.rank)

                            if self.capture(piece):
                                capture = 'x'
                            else:
                                capture = ''
                            self.line.append(f'{self.move_count}.{piece.type}{capture}{square}')

                        piece.moving = False
                        self.check_move()
                        self.move_timer = 1
                        piece.snap()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.flip()

    def comp_move(self):
        capture = False
        castle = False
        move = self.opening[self.move_count]
        move = move.split('.')[1]
        index = 0

        if move[1] == 'x':
            capture = True
            index += 1
        elif move[0] == 'O':
            castle = True

        piece_to_move = move[0]
        for x in range(8):
            if 'abcdefgh'[x] == move[index + 1]:
                file = x
        rank = 8 - int(move[index + 2])

        possible_pieces = []
        for piece in self.pieces:
            if piece.type == piece_to_move:
                if piece_to_move.lower() == 'p':
                    if not capture and piece.file == file:
                        possible_pieces.append(piece)
                    if capture:
                        if piece.file + 1 == file or piece.file - 1 == file:
                            if (self.color == 'white' and piece.rank == rank - 1) or (self.color == 'black' and piece.rank == rank + 1):
                                possible_pieces.append(piece)
                            elif self.all_comp_moves:
                                if (self.color == 'black' and piece.rank == rank - 1) or (self.color == 'white' and piece.rank == rank + 1):
                                    possible_pieces.append(piece)

                if piece_to_move.lower() == 'n':
                    if piece.file - 1 == file:
                        if piece.rank - 2 == rank or piece.rank + 2 == rank:
                            possible_pieces.append(piece)
                    if piece.file - 2 == file:
                        if piece.rank - 1 == rank or piece.rank + 1 == rank:
                            possible_pieces.append(piece)
                    if piece.file + 1 == file:
                        if piece.rank - 2 == rank or piece.rank + 2 == rank:
                            possible_pieces.append(piece)
                    if piece.file + 2 == file:
                        if piece.rank -  1 == rank or piece.rank + 1 == rank:
                            possible_pieces.append(piece)

                if piece_to_move.lower() == 'b':
                    for x in range(8):
                        if (piece.rank - x == rank and piece.file - x == file) or (piece.rank + x == rank and piece.file - x == file) or (piece.rank - x == rank and piece.file + x == file) or (piece.rank + x == rank and piece.file + x == file):
                            possible_pieces.append(piece)

                if piece_to_move.lower() == 'r':
                        if piece.rank == rank or piece.file == file:
                            possible_pieces.append(piece)

                if piece_to_move.lower() == 'q':
                    possible_pieces.append(piece)

                if piece_to_move.lower() == 'k':
                    possible_pieces.append(piece)

        if len(possible_pieces) > 1:
            print('more that one possible piece, please specify which piece to move')
            for x in range(8):
                if 'abcdefgh'[x] == move[index + 2]:
                    piece_file = x
            piece_rank = 8 - int(move[index + 4])
            for piece in possible_pieces:
                if piece.rank != piece_rank or piece.file != piece_file:
                    possible_pieces.remove(piece)
        piece = possible_pieces[0]
        piece.moving = True
        if self.color == 'black':
            (piece.rect.x, piece.rect.y) = (448 - file*64, 448 - rank*64)
        else:
            (piece.rect.x, piece.rect.y) = (file*64, rank*64)
        piece.snap()
        if self.color == 'black':
            piece.rank = 7 - piece.rank
            piece.file = 7 - piece.file
        if capture:
            self.capture(piece)
        piece.moving = False

        #
        # if castle:

        self.correct_text = self.font.render('', True, 'White')
        self.move_count += 1
        if self.highlight:
            self.square_highlight()

    def check_move(self):
        if self.move_count >= self.move_count_max:
            self.board_end = True
            self.move_timer = 1

        if self.line == self.opening[self.start_move:self.move_count:2]:
            self.correct_text = self.font.render('Correct', True, 'Green')
            self.correct = True
        else:
            self.correct_text = self.font.render('Incorrect', True, 'Red')
            self.correct = False

        if not self.correct:
            self.move_timer = 0
            self.board_end = True
            new_button = Button('Show correct move', (280,50), (660,250), self.font)
            self.buttons.add(new_button)
            new_button = Button('Next line', (175,50), (660,325), self.font)
            self.buttons.add(new_button)

    def castle(self, castle_color, castle_side):
        for piece in self.pieces:
            if castle_color == 'white':
                if castle_side == 'king':
                    if piece.type == 'R' and piece.file == 7:
                        piece.rect.x -= 128
                        self.line.append(f'{self.move_count}.O-O')
                elif castle_side == 'queen':
                    if piece.type == 'R' and piece.file == 0:
                        piece.rect.x += 192
                        self.line.append(f'{self.move_count}.O-O-O')
            elif castle_color == 'black':
                if castle_side == 'king':
                    if piece.type == 'r' and piece.file == 0:
                        piece.rect.x += 128
                        self.line.append(f'{self.move_count}.O-O')
                elif castle_side == 'queen':
                    if piece.type == 'r' and piece.file == 7:
                        piece.rect.x -= 192
                        self.line.append(f'{self.move_count}.O-O-O')

    def flip(self):
        if self.color == 'black':
            self.color = 'white'
        else:
            self.color = 'black'
        for piece in self.pieces:
            piece.rect.x = 448 - piece.rect.x
            piece.rect.y = 448 - piece.rect.y

    def square_highlight(self):
        if self.move_count % 2 == self.start_move:
            move = self.opening[self.move_count]
            move = move.split('.')[1]
            index = 0

            if move[1] == 'x':
                capture = True
                index += 1
            elif move[0] == 'O':
                castle = True

            piece_to_move = move[0]
            for x in range(8):
                if 'abcdefgh'[x] == move[index + 1]:
                    file = x
            rank = 8 - int(move[index + 2])

            if self.color == 'black':
                rank = 7 - rank
                file = 7 - file

            for square in self.squares:
                if square.rank == rank and square.file == file:
                    square.highlight()
                else:
                    square.reset_color()

    def update(self, inputs):
        self.screen.blit(self.sidebar, (512,0))
        self.screen.blit(self.opening_text1, (550,50))
        self.screen.blit(self.opening_text2, (550,90))
        self.screen.blit(self.correct_text, (600,150))
        self.buttons.draw(self.screen)
        for button in self.buttons:
            button.update(self.screen)

        self.squares.draw(self.screen)

        if self.board_end:
            if self.correct:
                if self.move_timer == 60:
                    self.to_next_board = True
            else:
                self.inputs(inputs)


        else:
            if self.move_timer == 60:
                if self.color == 'white':
                    self.move_timer = 0
                else:
                    self.move_timer = 1
            if self.move_timer == 0:
                self.inputs(inputs)
            if self.move_timer == 30:
                self.comp_move()
                self.move_timer = 0

        if self.move_timer > 0:
            self.move_timer += 1

        self.pieces.update(self.color)
        self.pieces.draw(self.screen)
