from code.openings import opening_dictionary
from code.cycle import Cycle

class Deck:
    def __init__(self, progress, piece_assets, screen, font):
        self.repetoire = []
        self.opening_sets = []
        colors = []
        for line in progress:
            if progress[line][0]:
                self.repetoire.append(line)

        for path in self.repetoire:
            colors.append(path.split('/')[-1])
            path = path.split('/')[2:-1]
            line = opening_dictionary
            for key in path:
                line = line[key]
            self.opening_sets.append(line)

        self.deck = []
        for cycle_setup in zip(self.opening_sets, self.repetoire, colors):
            new_cycle = Cycle(cycle_setup[0], cycle_setup[1], piece_assets, screen, font, color=cycle_setup[2], progress=progress)
            self.deck.append(new_cycle)

        self.index = -1
        self.done = False
        self.deck_cycle()
        

    def deck_cycle(self):
        self.index += 1
        if self.index > len(self.deck):
            self.done = True
        else:
            self.current_cycle = self.deck[self.index]

    def update(self, inputs):
        if self.current_cycle.to_next:
            self.deck_cycle()

        self.current_cycle.update(inputs)
