import numpy as np
import itertools
import pygame
import time

seed_matrix  = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

# seed_matrix  = np.array([
#     [0,1,0,0],time
#     [0,1,0,0]])


class GameState:
    n_generations = 0
    max_row = 0
    max_col = 0
    game_matrix = []
    neighbours_matrix = []

    def __init__(self,seed_matrix):
        self.n_generations = 0
        self.max_row = np.shape(seed_matrix)[0]
        self.max_col = np.shape(seed_matrix)[1]
        self.game_matrix = seed_matrix
        self.neighbours_matrix = np.zeros([self.max_row ,self.max_col],int)
        self.calculate_neighbours()
    


    def print_debug(self):
        print("n_generation : ",self.n_generations)
        print("max_row : ",self.max_row)
        print("max_col : ",self.max_col)
        print("\ngame_matrix : ")
        print_matrix(self.game_matrix)
        print("\nneighbour_ matrix : ")
        print_matrix(self.neighbours_matrix)

    def print_state(self):
        print_matrix(self.game_matrix)
    



    def calculate_neighbours(self):
            
        def is_in_game(row,col):


            if (row in list(range(self.max_row))) and (col in list(range(self.max_col))):
                # print("valid rows : ",list(range(self.max_row)))
                # print("valid cols : ",list(range(self.max_col)))
                # print("row is_in_game ", row)
                # print("col is_in_game ", col)
                return True
            return False
        
        def create_neighbour_list(row,col):
            neighbour_list = []
            for i, j in itertools.product([-1,0,1],[-1,0,1]):
                if (not(i==0 and j ==0) and is_in_game(row+i,col+j)):
                    neighbour_list.append([row+i,col+j])
            return neighbour_list
        
        def count_alive_neighbours(neighbour_list):
            total_alive_neighbour = 0
            for neighbour in neighbour_list:
                row = neighbour[0]
                col = neighbour[1]

                if self.game_matrix[row][col] == 1:
                    total_alive_neighbour += 1
            return total_alive_neighbour

        
        for (row,col) in itertools.product(range(self.max_row),range(self.max_col)):
            neighbour_list = create_neighbour_list(row,col)
            # print(neighbour_list)
            # print(self.neighbours_matrix[row][col])
            # print(self.game_matrix)
            self.neighbours_matrix[row][col] = count_alive_neighbours(neighbour_list)
        return self
    
    def next_generation_state(self):

        self.n_generations += 1
 
        next_generation_matrix = np.zeros([self.max_row ,self.max_col],int)

        def calculate_new_state(row,col):

            living_status = self.game_matrix[row][col]
            number_neighbour = self.neighbours_matrix[row][col]
            if living_status == 0 and number_neighbour == 3:
                return 1
            if living_status == 0:
                return 0
            if number_neighbour < 2 or number_neighbour > 3:
                return 0
            return 1 

        for row, col in itertools.product(list(range(self.max_row)),list(range(self.max_col))):
            next_generation_matrix[row][col] = calculate_new_state(row,col)
        self.game_matrix = next_generation_matrix
        self.calculate_neighbours()
        return self
                    
    def drow_grid(self):
        dead_color = (255, 255, 255)
        alive_color = (0, 0, 0)
        print(cell_size)

        for row in range(self.max_row):
            for col in range(self.max_col):
                if self.game_matrix[row][col] == 1:
                    color = alive_color
                else:
                    color = dead_color
                print(color)
                pygame.draw.rect(screen, color, (col*cell_size, row*cell_size, cell_size-1, cell_size-1))
        pygame.display.flip()



def print_matrix(matrix):
    for row in matrix:
        print(row)





game = GameState(seed_matrix)

cell_size = 25

width = game.max_col*cell_size
height = game.max_row*cell_size

screen = pygame.display.set_mode((width,height))
screen.fill((255,255,255))
pygame.display.flip()
pygame.display.set_caption("Game of Life")

print("#Game at sart : \n")
game.print_state()
time.sleep(0.3)

for i in range(50):
    print("\ngame at generation :",game.n_generations)
    game.next_generation_state()
    game.drow_grid()
    time.sleep(0.5)




