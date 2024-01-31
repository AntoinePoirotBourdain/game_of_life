import numpy as np
import itertools


seed_matrix  = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],])

# seed_matrix  = np.array([
#     [0,1,0,0],
#     [0,1,0,0]])


class GameState:
    n_generations = 0
    max_line = 0
    max_column = 0
    game_matrix = []
    neighbours_matrix = []

    def __init__(self,seed_matrix):
        self.n_generations = 0
        self.max_line = np.shape(seed_matrix)[0]
        self.max_column = np.shape(seed_matrix)[1]
        self.game_matrix = seed_matrix
        self.neighbours_matrix = np.zeros([self.max_line ,self.max_column],int)
        self.calculate_neighbours()
    


    def print_debug(self):
        print("n_generation : ",self.n_generations)
        print("max_line : ",self.max_line)
        print("max_column : ",self.max_column)
        print("\ngame_matrix : ")
        print_matrix(self.game_matrix)
        print("\nneighbour_ matrix : ")
        print_matrix(self.neighbours_matrix)

    def print_state(self):
        print_matrix(self.game_matrix)
    



    def calculate_neighbours(self):
            
        def is_in_game(line,column):


            if (line in list(range(self.max_line))) and (column in list(range(self.max_column))):
                # print("valid lines : ",list(range(self.max_line)))
                # print("valid columns : ",list(range(self.max_column)))
                # print("line is_in_game ", line)
                # print("column is_in_game ", column)
                return True
            return False
        
        def create_neighbour_list(line,column):
            neighbour_list = []
            for i, j in itertools.product([-1,0,1],[-1,0,1]):
                if (not(i==0 and j ==0) and is_in_game(line+i,column+j)):
                    neighbour_list.append([line+i,column+j])
            return neighbour_list
        
        def count_alive_neighbours(neighbour_list):
            total_alive_neighbour = 0
            for neighbour in neighbour_list:
                line = neighbour[0]
                column = neighbour[1]

                if self.game_matrix[line][column] == 1:
                    total_alive_neighbour += 1
            return total_alive_neighbour

        
        for (line,column) in itertools.product(range(self.max_line),range(self.max_column)):
            neighbour_list = create_neighbour_list(line,column)
            # print(neighbour_list)
            # print(self.neighbours_matrix[line][column])
            # print(self.game_matrix)
            self.neighbours_matrix[line][column] = count_alive_neighbours(neighbour_list)
        return self
    
    def next_generation_state(self):

        self.n_generations += 1
 
        next_generation_matrix = np.zeros([self.max_line ,self.max_column],int)

        def calculate_new_state(line,column):

            living_status = self.game_matrix[line][column]
            number_neighbour = self.neighbours_matrix[line][column]
            if living_status == 0 and number_neighbour == 3:
                return 1
            if living_status == 0:
                return 0
            if number_neighbour < 2 or number_neighbour > 3:
                return 0
            return 1 

        for line, column in itertools.product(list(range(self.max_line)),list(range(self.max_column))):
            next_generation_matrix[line][column] = calculate_new_state(line,column)
        self.game_matrix = next_generation_matrix
        self.calculate_neighbours()
        return self
                    



def print_matrix(matrix):
    for line in matrix:
        print(line)



game = GameState(seed_matrix)
print("#Game at sart : \n")
game.print_state()

for i in range(20):
    print("\ngame at generation :",game.n_generations)
    game.next_generation_state()
    game.print_state()

