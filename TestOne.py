import pygame
import time

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic Tac Toe")
playing = True


class Map:

    def __init__(self, passed_map):
        self.map = passed_map
        self.searching = True

    def draw(self):
        for col in range(len(self.map)):
            for row in range(len(self.map[col])):
                if self.map[row][col] == 0:
                    pygame.draw.rect(screen, (25, 25, 75),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                if self.map[row][col] == 1:
                    pygame.draw.rect(screen, (50, 50, 150),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))

    def find_route(self, leaving, entering, made_moves=[], length_to_here=0):  # Leaving and entering are indexes for this method rn
        # Makes sure a route has not been found yet
        if not self.searching:
            return [False, [], 0]

        # Reformat rows and cols to be more intuitive
        leaving = [leaving[1], leaving[0]]
        entering = [entering[1], entering[0]]
        new_made_moves = made_moves.copy()
        if len(new_made_moves) == 0:
            self.searching = True

        # Check if we are where we want to be
        if leaving[0] == entering[0] and leaving[1] == entering[1]:  # TODO does the simple version work?
            new_made_moves.append(leaving)
            # print(leaving, 1)
            self.searching = False
            return [True, new_made_moves, length_to_here + 1]

        # Check the place where we are starting is valid
        if self.map[leaving[0]][leaving[1]] == 0 or len(self.map) < leaving[0] < 0 or len(self.map[0]) < leaving[1] < 0:
            new_made_moves.append(leaving)
            print(leaving, 2)
            made_moves.append(leaving)
            return [False, new_made_moves, length_to_here]

        # Checks the place we are leaving has not been checked by current path
        if leaving in new_made_moves:
            print(leaving, 3)
            return [False, new_made_moves, length_to_here]

        # Tris moving in all directions as long as move has not already been made
        length_to_here += 1  # The number one can be changed later
        paths = []
        works = True
        for move in new_made_moves:
            if leaving[0] + 1 == move[0] and leaving[1] == move[1]:
                works = False
        if works:
            paths.append(self.find_route([leaving[0] + 1, leaving[1]], entering, new_made_moves, length_to_here))
        works2 = True
        for move in new_made_moves:
            if leaving[0] - 1 == move[0] and leaving[1] == move[1]:
                works2 = False
        works3 = True
        for move in new_made_moves:
            if leaving[0] == move[0] and leaving[1] + 1 == move[1]:
                works3 = False
        works4 = True
        for move in new_made_moves:
            if leaving[0] == move[0] and leaving[1] - 1 == move[1]:
                works4 = False
        new_made_moves.append(leaving)
        if works:
            paths.append(self.find_route([leaving[0] + 1, leaving[1]], entering, new_made_moves, length_to_here))
        if works2:
            paths.append(self.find_route([leaving[0] - 1, leaving[1]], entering, new_made_moves, length_to_here))
        if works3:
            paths.append(self.find_route([leaving[0], leaving[1] + 1], entering, new_made_moves, length_to_here))
        if works4:
            paths.append(self.find_route([leaving[0], leaving[1] - 1], entering, new_made_moves, length_to_here))
        lowest_working = [-1, 0]
        for path in paths:
            if path[0]:
                if lowest_working[0] == -1 or lowest_working[1] > path[1]:
                    lowest_working = [paths.index(path), path[2]]
        print(leaving, 4)
        if len(paths) == 0:
            return [False, [], 435243543]
        return [True, paths[lowest_working[0]][1], lowest_working[1]]


#         0  1  2  3  4  5  6  7  8  9
scene = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 0
         [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # 1
         [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],  # 2
         [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],  # 3
         [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 4
         [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # 5
         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],  # 6
         [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 7
         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # 8
         [0, 1, 1, 1, 1, 1, 1, 0, 0, 0]]  # 9

game_map = Map(scene)
print("START")
print(game_map.find_route([0, 1], [1, 7]))

while playing:
    screen.fill((255, 255, 255))
    game_map.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
    pygame.display.update()
