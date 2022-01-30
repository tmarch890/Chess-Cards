import pygame, board
from random import shuffle

class Cycle:
    def __init__(self, color, move_count_max, opening_set, path_list, piece_assets, screen, font):
        super().__init__()
        self.move_count_max = move_count_max
        self.cycle_set = []
        for opening_tree in opening_set:
            self.create_cycle_set(opening_tree, '')
        shuffle(self.cycle_set)
        # print(self.cycle_set)
        print(len(self.cycle_set))
        self.boards = []
        for line in self.cycle_set:
            new_board = board.Board(piece_assets, path_list[-3], path_list[-2], color, line, self.move_count_max, screen, font)
            new_board.square_highlight()
            self.boards.append(new_board)
            new_board = board.Board(piece_assets, path_list[-3], path_list[-2], color, line, self.move_count_max, screen, font)
            new_board.highlight = False
            self.boards.append(new_board)
        self.cycle_index = -1
        self.cycle()


    def create_cycle_set(self, opening_list, opening_root):
        length = len(opening_list)
        if length > 1:

            branches = [[opening_list[index], opening_list[index + 1]] for index in [number - 1 for number in range(length)] if isinstance(opening_list[index], str) and isinstance(opening_list[index + 1], list)]
            # print('branches: ', branches)
            for branch in branches:
                new_root = opening_root + branch[0]
                for item in branch[1:]:
                    # print('item: ', item)
                    # print('root passed on: ', new_root)
                    self.create_cycle_set(item, new_root)

            ends = [opening_list[index] for index in [number - 1 for number in range(length)] if isinstance(opening_list[index], str) and not isinstance(opening_list[index + 1], list)]
            # print('ends: ', ends)
            for item in ends:
                # print('item: ', item)
                move_number = item.split('.')[0]
                if int(move_number) > self.move_count_max:
                    full_line = opening_root
                else:
                    full_line = opening_root + item
                self.cycle_set.append(full_line)



        else:
            full_line = opening_list[0] + opening_root
            self.cycle_set.append(full_line)

        # print('cycle_set: ', self.cycle_set)

    def cycle(self):
        self.cycle_index += 1

        if self.cycle_index >= len(self.boards):
            self.cycle_index = 0
            for board in self.boards:
                board.reset()

        self.current_board = self.boards[self.cycle_index]

    def update(self, inputs):
        self.current_board.update(inputs)

        if self.current_board.to_next_board:
            if self.current_board.highlight and not self.current_board.correct:
                self.cycle()
            self.cycle()
