import time
import pygame
import random
from PathfindingMain.DevItems.Assets import RouteFinder


tile_size = None
size = None
game_map = None
players = None
screen = None
bullets = None
rects_to_update = None
scene = None


def setup(passed_tile_size, passed_size, passed_game_map, passed_players, passed_screen, passed_bullets,
          passed_rects_to_update, passed_scene):
    global tile_size, size, game_map, players, screen, bullets, rects_to_update, scene
    tile_size = passed_tile_size
    size = passed_size
    game_map = passed_game_map
    players = passed_players
    screen = passed_screen
    bullets = passed_bullets
    rects_to_update = passed_rects_to_update
    scene = passed_scene


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
                    pygame.draw.rect(screen, (15, 75, 15),
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
        self.weapon = weapon

    def update(self):
        if game_map.get_map_value(self.cords) == 0:
            return True
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
        self.weapon.draw_bullet(self.cords)


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=(10, 5), fire_rate=15):
        self.ammo = ammo
        self.damage = damage
        self.clip_size = clip_size
        self.ammo_in_clip = 0
        self.bullet_size = bullet_size
        self.fire_rate = fire_rate
        self.reload()
        self.last_show_time = time.time()

    def reload(self):
        if self.ammo - self.ammo_in_clip > 0:
            while self.ammo > 0 and self.ammo_in_clip <= self.clip_size:
                self.ammo_in_clip += 1
                self.ammo -= 1

    def get_damage(self):
        return random.randint(self.damage[0], self.damage[1])

    def is_loaded(self):
        return self.ammo_in_clip > 0 or self.ammo_in_clip == self.clip_size

    def get_bullet_size(self):
        return self.bullet_size

    def get_fire_rate(self):
        return self.fire_rate

    def draw_bullet(self, cords):
        x = cords[0] * tile_size + tile_size / 2 - self.bullet_size[0] / 2
        y = cords[1] * tile_size + tile_size / 2 - self.bullet_size[1] / 2
        pygame.draw.rect(screen, (255, 25, 25), (x, y, self.bullet_size[0], self.bullet_size[1]))


class Pistol(Gun):

    def __init__(self):
        super().__init__((45, 62), 100, 3)


class Smg(Gun):

    def __init__(self):
        super().__init__((45, 65), 5, 5)


class MiniGun(Gun):

    def __init__(self):
        super().__init__((5, 7), 1000, 100, (5, 5), 1)


class Melee(Gun):

    def __init__(self):
        super().__init__((35, 45), 10000000, 10000000, (0, 0), 1)


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
        self.id = -1
        self.last_rect = None
        self.rect = None

    def first_load(self):
        self.rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)

    def update(self):
        if self.weapon.is_loaded() and self.shooting:
            global directions
            direction = directions[self.direction]
            bullets.append(Bullet([self.cords[0] + direction[0], self.cords[1] + direction[1]], self.direction,
                                  self.weapon))
            self.weapon.ammo -= 1

    def take_damage(self, damage):
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
            if game_map.get_map_value(new_cords) != 0:
                self.cords = new_cords
        self.last_rect = self.rect
        self.rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)

    def draw(self):
        if self.id == -1:
            for index, player in enumerate(players):
                if player == self:
                    self.id = index
                    break

        rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)
        pygame.draw.rect(screen, self.color, rect)
        rects_to_update.append(self.last_rect)
        rects_to_update.append(self.rect)
        for bullet in self.bullets:
            bullet.draw()


class Human(Player):

    def __init__(self, cords, weapon, color=(0, 255, 0), direction=0):
        super().__init__(cords, weapon, color, direction)
        self.keys_pressed = []

    def check_touch(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.keys_pressed.append(0)
                #if self.keys_pressed.count(1) > 0:
                #    self.keys_pressed.remove(1)
            if event.key == pygame.K_d:
                self.keys_pressed.append(1)
                #if self.keys_pressed.count(0) > 0:
                #    self.keys_pressed.remove(0)
            if event.key == pygame.K_s:
                self.keys_pressed.append(2)
                #if self.keys_pressed.count(3) > 0:
                #    self.keys_pressed.remove(3)
            if event.key == pygame.K_w:
                self.keys_pressed.append(3)
                #if self.keys_pressed.count(2) > 0:
                #    self.keys_pressed.remove(2)
            if event.key == pygame.K_SPACE:
                self.shooting = True
            if event.key == pygame.K_LSHIFT:
                global running
                running = True
            if event.key == pygame.K_r:
                self.weapon.reload()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and self.keys_pressed.count(0) > 0:
                self.keys_pressed.remove(0)
            if event.key == pygame.K_d and self.keys_pressed.count(1) > 0:
                self.keys_pressed.remove(1)
            if event.key == pygame.K_s and self.keys_pressed.count(2) > 0:
                self.keys_pressed.remove(2)
            if event.key == pygame.K_w and self.keys_pressed.count(3) > 0:
                self.keys_pressed.remove(3)
            if event.key == pygame.K_SPACE:
                self.shooting = False
        if len(self.keys_pressed) > 0:
            self.is_moving = True
            self.direction = self.keys_pressed[len(self.keys_pressed) - 1]
        else:
            self.is_moving = False


class Computer(Player):

    def __init__(self, cords, attack_weapon=Melee(), color=(255, 0, 0), direction=0, damage=(35, 45)):
        super().__init__(cords, attack_weapon, color, direction)
        self.damage = damage

    def move(self):
        if self.cords != players[0].cords:
            bad_cords = []
            for index, cords in enumerate(players):
                if index != 0:
                    bad_cords.append(cords.cords)
            for index, cords in enumerate(bad_cords):
                bad_cords[index] = [
                    cords[1],
                                    cords[0]]
            path = RouteFinder.find_route(scene, self.cords, players[0].cords, bad_node_cords=bad_cords)
            if path:
                try:
                    before_cords = path.pop(1)
                    self.cords = [before_cords[1], before_cords[0]]
                except TypeError:
                    print("uh")
        try:
            self.last_rect = self.rect
            self.rect = (self.cords[0] * tile_size + 10, self.cords[1] * tile_size + 10, tile_size - 20, tile_size - 20)
        except IndexError:
            print("oh")

    def update(self):
        if self.cords == players[0].cords:
            players[0].take_damage(random.randint(self.damage[0], self.damage[1]))