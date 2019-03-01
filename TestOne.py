import pygame
import time
import math
import random

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinder")
playing = True


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
                    pygame.draw.rect(screen, (0, 255, 161),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 3:
                    pygame.draw.rect(screen, (255, 103, 48),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 4:
                    pygame.draw.rect(screen, (255, 48, 234),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.highlighted_map[row][col] == 5:
                    pygame.draw.rect(screen, (84, 242, 0),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))

    def find_route(self, leaving, entering, made_moves=[], length_to_here=0, first_time=True):
        # Setup for return
        if first_time:
            self.searching_for_route = True
            leaving = [leaving[1], leaving[0]]
            entering = [entering[1], entering[0]]
            self.possible_map = self.copy_map(self.map)
        can_find_route = False
        made_moves.append(leaving)
        new_made_moves = made_moves.copy()
        length_to_point = length_to_here + 1
        can_return = False

        # Returns if a route has already been found
        if not self.searching_for_route or self.possible_map[leaving[0]][leaving[1]] == 0:
            return [False, [], -1]

        # Draw where checking
        self.highlight_route(new_made_moves, is_route=False)
        self.highlighted_map = self.possible_map
        self.draw()

        # Check if at entering
        if leaving == entering:
            print(length_to_point, made_moves)
            can_find_route = True
            # self.searching_for_route = False
            self.possible_map[leaving[0]][leaving[1]] = 2
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
                if cords in new_made_moves or len(self.map) <= cords[0] or cords[0] < 0 or len(self.map[0]) <= cords[1] or \
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

            # Determines priority
            priority = [0, 0]
            priority_priority = [1, 1]
            if entering[0] < leaving[0]:
                priority[0] = 1
            if entering[0] > leaving[0]:
                priority[0] = -1
            if entering[1] < leaving[1]:
                priority[1] = 1
            if entering[1] < leaving[1]:
                priority[1] = -1
            if math.fabs(leaving[0] - entering[0]) > math.fabs(leaving[1] - entering[1]):
                priority_priority[0] = 2
            else:
                priority_priority[1] = 2

            # Orders usable_cords by which is more likely to get to the end
            top_priority = []
            second_priority = []
            third_priority = []
            ordered_cords = []
            for x in priority_priority:
                for cords in usable_cords:
                    if (cords[0] < leaving[0] and priority[0] == -1) or (cords[0] < leaving[0] and priority[0] == 1):
                        if priority_priority[0] == 2:
                            top_priority.append(cords)
                        else:
                            second_priority.append(cords)
                    if (cords[1] < leaving[1] and priority[1] == -1) or (cords[1] < leaving[0] and priority[1] == 1):
                        if priority_priority[1] == 2:
                            top_priority.append(cords)
                        else:
                            second_priority.append(cords)
                    if cords[1] == leaving[1] and priority[1] == 0 or (cords[0] == leaving[0] and priority[0] == 0):
                        third_priority.append(cords)
            for cords in top_priority:
                if cords not in ordered_cords:
                    ordered_cords.append(cords)
            for cords in second_priority:
                if cords not in ordered_cords:
                    ordered_cords.append(cords)
            for cords in third_priority:
                if cords not in ordered_cords:
                    ordered_cords.append(cords)
            for cords in usable_cords:
                if cords not in ordered_cords:
                    ordered_cords.append(cords)

            # Tries all good routes and removes non-working ones
            for cords in ordered_cords:
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
                self.possible_map[leaving[0]][leaving[1]] = 2
            else:
                can_find_route = False
                del made_moves[len(made_moves) - 1]
                self.possible_map[leaving[0]][leaving[1]] = 0

        # Return
        return [can_find_route, new_made_moves, length_to_point]

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

    def to_string(self):
        for row in self.map:
            print(row)

    def get_map_value(self, cords):
        return self.map[cords[1]][cords[0]]


class Bullet:

    def __init__(self, cords, direction, weapon):
        self.cords = cords
        self.damage = weapon.get_damage()
        self.size = weapon.get_bullet_size()
        if direction > 1:
            self.size = [self.size[1], self.size[0]]
        self.direction = direction

    def update(self):
        self.cords = [self.cords[0] + self.direction[0], self.cords[1] + self.direction[1]]
        for player in players:
            if player.get_cords() == self.cords:
                player.take_damage(self.damage)

    def draw(self):
        pygame.draw.rect(screen, (255, 25, 25), (self.cords[0] + tile_size / 2 - self.size[0] / 2,
                                                 self.cords[1] + tile_size / 2 - self.size[1] / 2,
                                                 self.size[0], self.size[1]))


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=(10, 5)):
        self.ammo = ammo
        self.damage = damage
        self.clip_size = clip_size
        self.ammo_in_clip = 0
        self.bullet_size = bullet_size
        self.reload()

    def reload(self):
        if self.ammo - self.ammo_in_clip > 0:
            while self.ammo > 0 and self.ammo_in_clip < self.clip_size:
                self.ammo_in_clip += 1
                self.ammo -= 1

    def get_damage(self):
        return random.randint(self.damage[0], self.damage[1])

    def is_loaded(self):
        return self.ammo_in_clip > 0

    def get_bullet_size(self):
        return self.bullet_size


class Pistol(Gun):

    def __init__(self):
        super().__init__((25, 30), 100, 10)


class MiniGun(Gun):

    def __init__(self):
        super().__init__((5, 7), 1000, 100, (5, 5))


class Player:

    def __init__(self, cords, weapon, color, direction):
        self.cords = cords
        self.weapon = weapon
        self.direction = direction
        self.bullets = []
        self.health = 100
        self.color = color
        self.shooting = False

    def update(self):
        if self.weapon.is_loaded() and self.shooting:
            global directions
            direction = directions[self.direction]
            self.bullets.append(Bullet([self.cords[0] + direction[0], self.cords[1] + direction[1]], self.direction,
                                       self.weapon))

    def take_damage(self, damage):
        self.health -= damage

    def get_cords(self):
        return self.cords

    def move(self):
        new_cords = [self.cords[0] + directions[self.direction][0], self.cords[1] + directions[self.direction][1]]
        if game_map.get_map_value(new_cords) == 1:
            self.cords = new_cords

    def draw(self):
        rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)
        pygame.draw.rect(screen, self.color, rect)
        for bullet in self.bullets:
            bullet.draw()


class Human(Player):

    def __init__(self, cords, weapon, color, direction=0):
        super().__init__(cords, weapon, color, direction)

    def check_touch(self):
        for key in pressed_keys:
            if key == pygame.K_a:
                self.direction = 0
            if key == pygame.K_d:
                self.direction = 1
            if key == pygame.K_s:
                self.direction = 2
            if key == pygame.K_w:
                self.direction = 3
            if key == pygame.K_SPACE:
                self.shooting = True
            else:
                self.shooting = False


class Computer(Player):

    def __init__(self, cords, weapon, color, direction=0):
        super().__init__(cords, weapon, color, direction)


def flip_route(moves):
    new_moves = []
    for move in moves[1]:
        new_moves.append([move[1], move[0]])
    return [moves[0], new_moves, moves[2]]


def read_current_scene():
    # name = input("What map file do you want to load? ")
    name = ""
    if name == "":
        name = "MultiPlayerMap"
    with open(name) as f:
        contents = f.read()
    in_list = contents.split("\n")
    for line in in_list:
        row = []
        for status in line:
            row.append(int(status))
        if row:
            scene.append(row)


scene = []
read_current_scene()
pressed_keys = []
game_map = Map(scene)
players = [Human([23, 12], Pistol(), (0, 255, 0), 1), Computer([1, 12], Pistol(), (255, 0, 0), 0)]
tile_size = size[0] / len(scene)
move_timer_max = 5
move_timer = move_timer_max
directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]  # 0:Right, 1:Left, 2:Down, 3: Up

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            quit()
        if event.type == pygame.KEYDOWN:
            pressed_keys.append(event.key)
        if event.type == pygame.KEYUP and event.key in pressed_keys:
            pressed_keys.remove(event.key)
    players[0].check_touch()
    screen.fill((255, 255, 255))
    game_map.draw()
    for current_player in players:
        if move_timer == 0:
            move_timer = move_timer_max
        if move_timer == move_timer_max:
            current_player.move()
        move_timer -= 1
        current_player.draw()
        current_player.update()
    game_map.update()
    pygame.display.update()
# TODO Use code for messages
