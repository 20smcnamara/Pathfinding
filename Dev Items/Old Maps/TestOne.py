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

    def to_string(self):
        for row in self.map:
            print(row)

    def get_map_value(self, cords):
        if len(self.map) > cords[0] > 0 and len(self.map) > cords[1] > 0:
            return self.map[cords[1]][cords[0]]
        else:
            return 0


class Bullet:

    def __init__(self, cords, direction, weapon, speed=3):
        self.cords = cords
        self.damage = weapon.get_damage()
        self.size = weapon.get_bullet_size()
        self.max_cool_down = speed
        self.cool_down = self.max_cool_down
        if direction > 1:
            self.size = [self.size[1], self.size[0]]
        self.direction = direction

    def update(self):
        if self.cool_down == 0:
            self.cool_down = self.max_cool_down
        if self.max_cool_down == self.cool_down:
            self.cords = [self.cords[0] + directions[self.direction][0], self.cords[1] + directions[self.direction][1]]
        self.cool_down -= 1
        if game_map.get_map_value(self.cords) == 0:
            return True
        for player in players:
            if player.get_cords() == self.cords:
                player.take_damage(self.damage)
        return False

    def draw(self):
        x = self.cords[0] * tile_size + tile_size / 2 - self.size[0] / 2
        y = self.cords[1] * tile_size + tile_size / 2 - self.size[1] / 2
        pygame.draw.rect(screen, (255, 25, 25), (x, y, self.size[0], self.size[1]))


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=(10, 5), fire_rate=15):
        self.ammo = ammo
        self.damage = damage
        self.clip_size = clip_size
        self.ammo_in_clip = 0
        self.bullet_size = bullet_size
        self.fire_rate = fire_rate
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

    def get_fire_rate(self):
        return self.fire_rate


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
        self.bullet_cool_down = weapon.get_fire_rate()
        self.shooting = False
        self.is_moving = False
        self.starting_cords = [cords[0], cords[1]]
        self.deaths = 0

    def update(self):
        if self.bullet_cool_down == 0:
            self.bullet_cool_down = self.weapon.get_fire_rate()
        elif self.shooting:
            self.bullet_cool_down -= 1
        if self.weapon.is_loaded() and self.shooting and self.bullet_cool_down == self.weapon.get_fire_rate():
            global directions
            direction = directions[self.direction]
            print(self.cords, [self.cords[0] + direction[0], self.cords[1] + direction[1]])
            self.bullets.append(Bullet([self.cords[0] + direction[0], self.cords[1] + direction[1]], self.direction,
                                       self.weapon))
        to_remove = []
        for bullet in self.bullets:
            if bullet.update():
                to_remove.append(bullet)
        for remove in to_remove:
            self.bullets.remove(remove)

    def __take_damage__(self, damage):
        self.health -= damage
        if self.health < 1:
            self.cords = self.starting_cords
            self.deaths += 1
            self.health = 100

    def get_cords(self):
        return self.cords

    def move(self):
        if self.is_moving:
            new_cords = [self.cords[0] + directions[self.direction][0], self.cords[1] + directions[self.direction][1]]
            if game_map.get_map_value(new_cords) == 1:
                self.cords = new_cords

    def draw(self):
        rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)
        pygame.draw.rect(screen, self.color, rect)
        for bullet in self.bullets:
            bullet.draw()


class Human(Player):

    def __init__(self, cords, weapon, color=(0, 255, 0), direction=0):
        super().__init__(cords, weapon, color, direction)

    def check_touch(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.direction = 0
                self.is_moving = True
            if event.key == pygame.K_d:
                self.direction = 1
                self.is_moving = True
            if event.key == pygame.K_s:
                self.direction = 2
                self.is_moving = True
            if event.key == pygame.K_w:
                self.direction = 3
                self.is_moving = True
            if event.key == pygame.K_SPACE:
                self.shooting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_w:
                self.is_moving = False
            if event.key == pygame.K_SPACE:
                self.shooting = False


class Dud:

    def __init__(self, cords, color):
        self.__cords__ = cords
        self.color = color
        self.cords = cords

    def set_cords(self, cords):
        self.cords = cords

    def draw(self):
        rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)
        pygame.draw.rect(screen, self.color, rect)
        for bullet in self.bullets:
            bullet.draw()


def flip_route(moves):
    new_moves = []
    for move in moves[1]:
        new_moves.append([move[1], move[0]])
    return [moves[0], new_moves, moves[2]]


def read_current_scene():
    # name = input("What map file do you want to load? ")
    name = ""
    if name == "":
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


scene = []
read_current_scene()
pressed_keys = []
game_map = Map(scene)
route = game_map.find_route([8, 44], [17, 31])
print(route)
game_map.highlight_route(route)
# players = [Human([23, 12], Pistol(), 1), Dud([1, 12])]
tile_size = size[0] / len(scene)
move_timer_max = 5
move_timer = move_timer_max
directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [0, 0]]  # 0:Right, 1:Left, 2:Down, 3: Up 4: Still
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
    pygame.display.update()
    time.sleep(.01)
# TODO Use code for messages
