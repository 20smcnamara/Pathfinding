import pygame
import random
import time

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
display_size = [800, 800]
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("Pathfinder")
playing = True


def recurse(stopby, current_cords, map):
    # print(time.time() - stopby)
    map[current_cords[0]][current_cords[1]] = 1
    if stopby < time.time():
        return 0

    possible_cords = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    for index, cords in enumerate(possible_cords):
        possible_cords[index] = [cords[0] + current_cords[0], cords[1] + current_cords[1]]

    to_remove = []
    for cords in possible_cords:
        if not(0 < cords[0] < len(map)) or not(0 < cords[1] < len(map)):
            to_remove.append(cords)
            continue

        if map[cords[0]][cords[1]] != 0:
            to_remove.append(cords)

    for cords in to_remove:
        possible_cords.remove(cords)

    if len(possible_cords) == 0:
        return 1

    cords = possible_cords.pop(random.randint(0, len(possible_cords) - 1))
    returned = recurse(stopby, cords, map)
    while returned == 1 and len(possible_cords) > 0:
        if len(possible_cords) > 0:
            possible_cords.pop(random.randint(0, len(possible_cords) - 1))
            returned = recurse(stopby, cords, map)

    time.sleep(.1)
    if returned == 1:
        return 1

    return 0


def make_random_scene(size):
    map = []
    size = size
    for x in range(size):
        row = []
        for y in range(size):
            row.append(0)
        map.append(row)
    recurse(time.time() + 7, [random.randint(0, size - 1), random.randint(0, size - 1)], map)
    return map


def print_map(map):
    for row in map:
        print(row)
