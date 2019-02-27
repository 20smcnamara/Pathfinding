import pygame
import time

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinder")
playing = True


class Map:

    def __init__(self, passed_map):
        self.map = passed_map
        self.highlighted_map = self.copy_map(passed_map)

    def copy_map(self, passed_map):
        new_map = []
        for row in passed_map:
            new_row = []
            for place in row:
                new_row.append(place)
            new_map.append(new_row)
        return new_map

    def draw(self):
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
        for col in range(len(self.map)):
            for row in range(len(self.map[col])):
                if self.highlighted_map[row][col] == 0:
                    pygame.draw.rect(screen, (25, 25, 75),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 1:
                    pygame.draw.rect(screen, (50, 50, 150),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 2:
                    pygame.draw.rect(screen, (0, 255, 161),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 3:
                    pygame.draw.rect(screen, (255, 103, 48),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 4:
                    pygame.draw.rect(screen, (255, 48, 234),
                                     (col * (size[0] / len(self.map)), row * (size[1] / len(self.map[0])),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
        pygame.display.update()

    def find_route(self, leaving, entering, made_moves=[], length_to_here=0, first_time=True):
        # Setup for return
        if first_time:
            leaving = [leaving[1], leaving[0]]
            entering = [entering[1], entering[0]]
        can_find_route = False
        made_moves.append(leaving)
        new_made_moves = made_moves.copy()
        length_to_point = length_to_here + 1
        can_return = False

        # Draw where checking
        # before = self.map[leaving[0]][leaving[1]]
        # if len(self.map) <= leaving[0] or leaving[0] < 0 or len(self.map[0]) <= leaving[1] or \
        #         leaving[1] < 0 or self.map[leaving[0]][leaving[1]] == 0:
        #     self.highlighted_map[leaving[0]][leaving[1]] = 3
        #     can_return = True
        # elif leaving == entering:
        #     self.highlighted_map[leaving[0]][leaving[1]] = 4
        # else:
        #     self.highlighted_map[leaving[0]][leaving[1]] = 2
        # self.draw()
        # time.sleep(.1)
        # self.highlighted_map[leaving[0]][leaving[1]] = before
        self.highlight_route(new_made_moves, is_route=False)
        self.draw()
        time.sleep(.1)

        # Check if at entering
        if leaving == entering:
            can_find_route = True
            can_return = True  # Don't ask why I don't just return here

        # Try all moves
        tries = []
        if not can_return:
            usable_cords = [[leaving[0] + 1, leaving[1]],
                            [leaving[0] - 1, leaving[1]],
                            [leaving[0], leaving[1] + 1],
                            [leaving[0], leaving[1] - 1]]

            # Checks all spots are on the map and not going backwards
            cords_to_remove = []
            for cords_index in range(len(usable_cords)):
                cords = usable_cords[cords_index]
                if cords in made_moves or len(self.map) <= cords[0] or cords[0] < 0 or len(self.map[0]) <= cords[1] or \
                        cords[1] < 0:
                    cords_to_remove.append(cords_index)

            # Checks all spots are not walls
            for cords_index in range(len(usable_cords)):
                cords = usable_cords[cords_index]
                if cords_index not in cords_to_remove and self.map[cords[0]][cords[1]] == 0:
                    cords_to_remove.append(cords_index)

            # Sort indexes to be removed
            for index in cords_to_remove:
                for index_index in range(len(cords_to_remove) - 1):
                    if cords_to_remove[index_index] > cords_to_remove[index_index + 1]:
                        temp = cords_to_remove[index_index + 1]
                        cords_to_remove[index_index + 1] = cords_to_remove[index_index]
                        cords_to_remove[index_index] = temp

            # Removes unsuitable places
            for cords in range(len(cords_to_remove)):
                del usable_cords[cords_to_remove[cords] - cords]

            # Tries all good routes and removes non-working ones
            for cords in usable_cords:
                route = self.find_route(cords, entering, new_made_moves, length_to_point, first_time=False)
                if route[0]:
                    tries.append(route)

            # Check all valid routes for shortest route if there is one
            if len(tries) > 0:
                can_find_route = True
                least_moves = -1
                least_moves_index = 0
                for route in range(len(tries)):
                    if tries[route][2] < tries[least_moves_index][2] or least_moves == -1:
                        least_moves = tries[route][2]
                        least_moves_index = route
                for move in tries[least_moves_index][1]:
                    new_made_moves.append(move)
                length_to_point += tries[least_moves_index][2]
            else:
                can_find_route = False

        # Return
        return [can_find_route, new_made_moves, length_to_point]

    def highlight_route(self, route, is_route=True):
        for row in range(len(self.map)):
            for place in range(len(self.map[row])):
                if self.highlighted_map[row][place] > 1:
                    self.highlighted_map[row][place] = self.map[row][place]
        if is_route:
            for cords in route[1]:
                self.highlighted_map[cords[0]][cords[1]] = 4
        else:
            for cords in route:
                self.highlighted_map[cords[0]][cords[1]] = 4

    def to_string(self):
        for row in self.map:
            print(row)


def flip_route(moves):
    new_moves = []
    for move in moves[1]:
        new_moves.append([move[1], move[0]])
    return [moves[0], new_moves, moves[2]]


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
found_route = game_map.find_route([0, 1], [1, 7])
print(flip_route(found_route))
game_map.highlight_route(found_route)

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            quit()
    game_map.draw()

