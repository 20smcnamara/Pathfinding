import pygame

class Map:

    def __init__(self, passed_map):
        self.map = passed_map
        self.highlighted_map = self.copy_map(passed_map)
        self.searching_for_route = True
        self.possible_map = self.copy_map(passed_map)

    def update(self):
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            pos = [pos[0], pos[1]]
            while pos[0] % (size[0] / len(self.map)) != 0:
                pos[0] -= 1
            while pos[1] % (size[1] / len(self.map)) != 0:
                pos[1] -= 1
            pos = [int(pos[1] / (size[0] / len(self.map))), int(pos[0] / (size[0] / len(self.map)))]
            print(pos[1], pos[0])

    def copy_map(self, passed_map):
        new_map = []
        for row in passed_map:
            new_row = []
            for place in row:
                new_row.append(place)
            new_map.append(new_row)
        return new_map

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.highlighted_map[row][col] == 0:
                    pygame.draw.rect(screen, (25, 25, 75),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 1:
                    pygame.draw.rect(screen, (50, 50, 150),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 2:
                    pygame.draw.rect(screen, (125, 255, 125),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
        pygame.display.update()

    def highlight_route(self, route, is_route=True):
        for row in range(len(self.map)):
            for place in range(len(self.map[row])):
                if self.highlighted_map[row][place] > 1:
                    self.highlighted_map[row][place] = self.map[row][place]
        if (not is_route) or route[0]:
            if is_route:
                for cords in route[1]:
                    self.highlighted_map[cords[0]][cords[1]] = 4
            else:
                for cords in route:
                    self.highlighted_map[cords[0]][cords[1]] = 4

    def get_map_value(self, cords):
        if len(self.map) > cords[0] > 0 and len(self.map) > cords[1] > 0:
            return self.map[cords[1]][cords[0]]
        else:
            return 0


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def find_route(maze, start, end, allow_diagonal_movement=False):
    start_node = Node(None, (start[1], start[0]))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, (end[1], end[0]))
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []

        for new_position in adjacent_squares:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] == 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            temp = game_map.map[child.position[0]][child.position[1]]
            game_map.highlighted_map[child.position[0]][child.position[1]] = 2
            game_map.draw()
            game_map.map[child.position[0]][child.position[1]] = temp

            open_list.append(child)


def read_current_scene():
    name = "TestingMap"
    with open(name) as f:
        contents = f.read()
    in_list = contents.split("\n")
    for line in in_list:
        row = []
        for status in line:
            row.append(int(status))
        if row:
            scene.append(row)


pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinder")
playing = True
scene = []
read_current_scene()
game_map = Map(scene)
found_route = find_route(scene, (7, 44), (17, 31))
print(found_route)
game_map.highlight_route(found_route, is_route=False)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
    game_map.update()
    game_map.draw()
    pygame.display.update()
