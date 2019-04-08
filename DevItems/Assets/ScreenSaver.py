import pygame
import random
import time
import math
from PathfindingMain.DevItems.Assets.Maps.SceneReader import read_current_scene


class Map:

    def __init__(self, scene):
        self.map = scene
        self.walls = []
        self.load_walls()

    def load_walls(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.get_map_value([x, y]) == 0:
                    self.walls.append([y, x])

    def get_map_value(self, cords):
        return self.map[cords[0]][cords[1]]

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 0:
                    pygame.draw.rect(screen, (25, 25, 75),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.map[row][col] == 1:
                    pygame.draw.rect(screen, (50, 50, 150),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.map[row][col] == 2:
                    pygame.draw.rect(screen, (0, 255, 161),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.map[row][col] == 3:
                    pygame.draw.rect(screen, (255, 103, 48),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.map[row][col] == 4:
                    pygame.draw.rect(screen, (255, 48, 234),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))
                elif self.map[row][col] == 5:
                    pygame.draw.rect(screen, (84, 242, 0),
                                     (col * (size[0] / len(self.map[0])), row * (size[1] / len(self.map)),
                                      size[0] / len(self.map), size[1] / len(self.map[0])))


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=7, fire_rate=15):
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
        super().__init__([20, 35], 100, 12)


class MiniGun(Gun):

    def __init__(self):
        super().__init__([5, 7], 10000, 1000, fire_rate=1)


class Bullet:

    def __init__(self, cords, direction, weapon, shooter):
        self.cords = cords
        self.size = weapon.get_bullet_size()
        self.damage = weapon.get_damage()
        self.direction = direction
        self.shot_by = shooter

    def update(self):
        self.update_pos()
        return self.check_organism_collision() or self.check_valid()

    def update_pos(self):
        self.cords = [self.cords[0] + self.direction[0], self.cords[1] + self.direction[1]]

    def check_valid(self):
        x = int(self.cords[0])
        y = int(self.cords[1])
        if x >= size[0] or y >= size[1] or x < 0 or y < 0:
            return True
        if tile_size < self.size:
            x2 = x + self.size
            y2 = y + self.size
            while x2 % tile_size != 0:
                x2 -= 1
            while y2 % tile_size != 0:
                y2 -= 1
            if game_map.map[int(x2/tile_size)][int(y2/tile_size)] == 0:
                return True
        while x % tile_size != 0:
            x -= 1
        while y % tile_size != 0:
            y -= 1
        if game_map.map[int(x/tile_size)][int(y/tile_size)] == 0:
            return True
        return False

    def check_organism_collision(self):
        rects = [pygame.Rect(self.cords[0] + self.size, self.cords[1], 5, self.size * 2),
                 pygame.Rect(self.cords[0] + self.size, self.cords[1], self.size * 2, 5),
                 pygame.Rect(self.cords[0] + self.size / 2, self.cords[1] + self.size / 2, 3, 3),
                 pygame.Rect(self.cords[0] + self.size / 2 * 3, self.cords[1] + self.size / 2, 3, 3),
                 pygame.Rect(self.cords[0] + self.size / 2, self.cords[1] + self.size / 2 * 3, 3, 3),
                 pygame.Rect(self.cords[0] + self.size / 2 * 3, self.cords[1] + self.size / 2 * 3, 3, 3)]
        if self.shot_by != "Player":
            for player in players:
                cords = player.rect
                if pygame.Rect(cords[0], cords[1], tile_size - 20, tile_size - 20).collidelist(rects) != -1:
                    print(self.cords, self.direction)
                    player.take_damage(self.damage)
                    return True
        if self.shot_by != "Boss":
            for boss in bosses:
                cords = [boss.x, boss.y, boss.width, boss.height]
                if pygame.Rect(cords).collidelist(rects) != -1:
                    print(self.cords, self.direction)
                    boss.take_damage(self.damage)
                    return True
        return False

    def draw(self):
        pygame.draw.circle(screen, bullet_colors[self.shot_by], [int(self.cords[0]), int(self.cords[1])], self.size)


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


class Boss:

    def __init__(self, file_name, health=1000):
        self.width = 134
        self.height = 109
        self.file_name = file_name
        self.x = random.randint(0, size[0] - 134)
        self.y = random.randint(0, size[1] - 109)
        self.x_add = random.choice([-2, 2])
        self.y_add = random.choice([-2, 2])
        self.x_last_switch = 0
        self.y_last_switch = 0
        self.increasing = True
        self.scale = 0
        self.countdown = 0
        self.countdown_top = 10
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        pass

    def update(self):
        if self.increasing:
            self.scale += 1
            if self.scale > 150:
                self.increasing = False
        else:
            self.scale -= 1
            if self.scale < 1:
                self.increasing = True

        if (self.x < 0 or self.x > size[0] - self.width - self.scale) and time.time() - self.x_last_switch > 0.5:
            self.x_last_switch = time.time()
            self.x_add *= -1

        if (self.y < 0 or self.y > size[1] - self.height - self.scale) and time.time() - self.y_last_switch > 0.5:
            self.y_last_switch = time.time()
            self.y_add *= -1

        self.x += self.x_add
        self.y += self.y_add
        if self.countdown == 0:
            self.take_shots()
            self.countdown = self.countdown_top
        self.countdown -= 1

    def take_shots(self):
        pass

    def draw(self):
        screen.blit(pygame.transform.smoothscale(pygame.image.load(self.file_name),
                                                 [self.width + self.scale, self.height + self.scale]), [self.x, self.y])
        pygame.draw.rect(screen, (255, 0, 0), (self.x + self.width / 2 + self.scale / 2, self.y + self.height / 2 + self.scale / 2, 10, 10))


class TheHoff(Boss):

    def __init__(self):
        super(TheHoff, self).__init__("TheHoff.png")
        self.countdown_top = 100

    def take_shots(self):
        x = self.x + self.width / 2 + self.scale / 2
        y = self.y + self.height / 2 + self.scale / 2
        targets = [[1, 0], [0, 1], [-1, 0], [0, -1],
                   [1, 1], [-1, 1], [1, -1], [-1, -1],
                   [2, 1], [1, 2], [-2, 1], [1, -2], [-2, -1], [-1, 2], [-1, -2], [2, -1]]
        for target in targets:
            shoot(direction=target, leaving=[x, y], shot_by="Boss")

    def die(self):
        bosses.remove(self)


class Player:

    def __init__(self, cords, weapon, color):
        self.cords = cords
        self.weapon = weapon
        self.bullets = []
        self.health = 100
        self.color = color
        self.bullet_cool_down = weapon.get_fire_rate()
        self.shooting = True
        self.starting_cords = [cords[0], cords[1]]
        self.deaths = 0
        self.delta = [0, 0]
        self.last_shot = 0
        self.rect = (self.cords[0], self.cords[1], tile_size - 20, tile_size - 20)

    def update(self):
        self.handle_weapons()
        self.handle_movement()

    def handle_weapons(self):
        if self.weapon.is_loaded() and self.shooting and time.time() - self.last_shot > self.weapon.get_fire_rate() / 60:
            self.shoot()
            self.last_shot = time.time()

    def handle_movement(self):
        x = int(self.cords[0])
        y = int(self.cords[1])
        x2 = int(self.cords[0]) + tile_size - 20
        y2 = int(self.cords[1]) + tile_size - 20

        while x2 % tile_size != 0:
            x2 -= 1
        while y2 % tile_size != 0:
            y2 -= 1
        while x % tile_size != 0:
            x -= 1
        while y % tile_size != 0:
            y -= 1

        x /= tile_size
        y /= tile_size
        x2 /= tile_size
        y2 /= tile_size

        if self.delta[0] < 0 and (game_map.get_map_value([int(x), int(y)]) == 0 or
                                  game_map.get_map_value([int(x), int(y2)]) == 0):
            self.delta[0] = 0
            self.cords[0] = x * tile_size + tile_size
        if self.delta[0] > 0 and (game_map.get_map_value([int(x2), int(y)]) == 0 or
                                  game_map.get_map_value([int(x2), int(y2)]) == 0):
            self.delta[0] = 0
            self.cords[0] = x2 * tile_size - tile_size + 20
        if self.delta[1] < 0 and (game_map.get_map_value([int(x), int(y)]) == 0 or
                                  game_map.get_map_value([int(x2), int(y)]) == 0):
            self.delta[1] = 0
            self.cords[1] = y * tile_size + tile_size
        if self.delta[1] > 0 and (game_map.get_map_value([int(x), int(y2)]) == 0 or
                                  game_map.get_map_value([int(x2), int(y2)]) == 0):
            self.delta[1] = 0
            self.cords[1] = y2 * tile_size - tile_size + 20

        if self.delta[0] > 5:
            self.delta[0] = 5
        if self.delta[0] < -5:
            self.delta[0] = -5
        if self.delta[1] > 5:
            self.delta[1] = 5
        if self.delta[1] < -5:
            self.delta[1] = -5

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 1:
            self.cords = self.starting_cords
            self.deaths += 1
            self.health = 100

    def get_cords(self):
        return self.cords

    def shoot(self):
        pass

    def move(self):
        self.cords = [self.cords[0] + self.delta[0], self.cords[1] + self.delta[1]]
        self.rect = (self.cords[0], self.cords[1], tile_size - 20, tile_size - 20)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw()


class Human(Player):

    def __init__(self, cords, weapon, color=(0, 255, 0)):
        super().__init__(cords, weapon, color)

    def shoot(self):
        target = pygame.mouse.get_pos()
        shoot(target=target, leaving=([self.cords[0] + ((tile_size - 20) / 2), self.cords[1] + ((tile_size - 20) / 2)]),
              weapon=self.weapon)
        self.weapon.ammo -= 1

    def check_touch(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.delta[0] += 5
            if event.key == pygame.K_d:
                self.delta[0] -= 5
            if event.key == pygame.K_s:
                self.delta[1] += 5
            if event.key == pygame.K_w:
                self.delta[1] -= 5
            if event.key == pygame.K_SPACE:
                self.shooting = True
            if event.key == pygame.K_LSHIFT:
                global running
                running = True
            if event.key == pygame.K_r:
                self.weapon.reload()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.delta[0] -= 5
            if event.key == pygame.K_d:
                self.delta[0] += 5
            if event.key == pygame.K_s:
                self.delta[1] -= 5
            if event.key == pygame.K_w:
                self.delta[1] += 5
            if event.key == pygame.K_SPACE:
                self.shooting = False


def update_bullets():
    to_remove = []
    for bullet in bullets:
        if bullet.update():
            to_remove.append(bullet)

    for remove in to_remove:
        bullets.remove(remove)


def draw_bullets():
    for bullet in bullets:
        bullet.draw()


def shoot(target=[], leaving=[], direction=[], shot_by="Player", weapon=Pistol()):
    if len(direction) == 0:
        axis_distances = [math.fabs(leaving[0] - target[0]), math.fabs(leaving[1] - target[1])]
    else:
        axis_distances = direction
    x_direction = 1
    y_direction = 1
    if len(target) != 0:
        if target[0] < leaving[0]:
            x_direction = -1
        if target[1] < leaving[1]:
            y_direction = -1
    distance = (axis_distances[0]**2 + axis_distances[1]**2)**0.5 / 5
    try:
        towards = [axis_distances[0] / distance * x_direction]
    except ZeroDivisionError:
        towards = [axis_distances[0] * x_direction]
    try:
        towards.append(axis_distances[1] / distance * y_direction)
    except ZeroDivisionError:
        towards.append(axis_distances[1] * y_direction)
    bullets.append(Bullet([leaving[0] + towards[0] * 5, leaving[1] + towards[1] * 5], towards, weapon, shot_by))


pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ScreenSaver")
Hoff = pygame.image.load('TheHoff.png')
playing = True
running = True
bullets = []
tile_size = size[0] / 25
game_map = Map(read_current_scene(name="CleanMap"))
players = [Human([size[0] / 2, size[0] / 2], MiniGun(), (125, 255, 125))]
clock = pygame.time.Clock()
bullet_colors = {"Player": (50, 255, 50), "Boss": (255, 50, 50)}

bosses = []
for x in range(1):  # eval(input("Number of Pictures: "))):
    bosses.append(TheHoff())

while running:
    game_map.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

    update_bullets()
    draw_bullets()
    for boss in bosses:
        boss.update()
        boss.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                for player in players:
                    player.take_damage(100)
        for player in players:
            player.check_touch(event)
    for player in players:
        player.update()
        player.draw()
        player.move()
    pygame.display.update()
    clock.tick(60)
