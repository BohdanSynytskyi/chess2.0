import numpy as np
import random


class Bot:

    def __init__(self):
        self.input = []
        self.weights = []
        self.output = []

    def create_input_value(self, possible_moves):
        self.input = [[[value[0], value[1]] for value in value_list] for value_list in possible_moves]

    def make_move(self, possible_moves):    # possible_moves --> { piece : [(x1,y1), (x2,y2)...]}
        keys = list(possible_moves.values())
        self.create_input_value(keys)
        # creating weights
        for i in range(2):
            self.weights.append(random.randint(-10,2))
        self.weights = np.array(self.weights)

        for i in range(len(self.input)):
            list1 = []
            for j in range(len(self.input[i])):
                list1.append(np.dot(self.input[i][j], self.weights))
            self.output.append(list1)

        i1, i2 = self.create_output_coordinates(self.output)
        move = keys[i1][i2]
        piece = list(possible_moves.keys())[list(possible_moves.values()).index(keys[i1])]

        self.input = []
        self.weights = []
        self.output = []

        return piece, move   # returns --> { piece : move }

    def random_move(self, possible_moves):
        keys = list(possible_moves.values())
        self.create_input_value(keys)

        index1 = random.randint(0, len(self.input) - 1)
        index2 = random.randint(0, len(self.input[index1]) - 1)

        move = keys[index1][index2]
        piece = list(possible_moves.keys())[list(possible_moves.values()).index(keys[index1])]

        return piece, move  # returns --> { piece : move }




    def create_output_coordinates(self, moves):
        max_values = []
        for piece_moves in moves:
            max_values.append(max(piece_moves))
        max_val = max(max_values)
        index1 = max_values.index(max_val)
        index2 = moves[index1].index(max_val)
        return index1, index2

# bot1 = Bot()
# print(bot1.make_move({'a': [(1,2),(3,4)],'b':[(2,3),(4,1)]}))
