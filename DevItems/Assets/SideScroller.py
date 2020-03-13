import pygame
import random
import time
import math
from PathfindingMain.DevItems.Assets.Maps.SceneReader import read_current_scene
from PathfindingMain.DevItems.Assets.RouteFinder import find_route


class DrawnObject:

    def __init__(self):
        drawn_objects.append(self)

    def adjust(self, x_add, y_add):
        try:
            self.x += x_add
            self.y += y_add
        except AttributeError:
            try:
                self.cords[0] += x_add
                self.cords[1] += y_add
            except AttributeError:
                print("Well Shit")


class CollisionObject(DrawnObject):

    def __init__(self):
        self.rect = "Shit"
        self.cords = [0, 0]
        super().__init__()

    def update(self):
        try:
            self.rect = (self.cords[0], self.cords[1], self.size, self.size)
        except:
            pass

    def collide_rect(self, other):
        if self.rect == "Shit":
            print("Mistakes were made")
            return False
        try:
            print("\n1" + str(self.rect))
            print(other.left, other.top, other.width, other.height)
            other.update()
            print(other.left, other.top, other.width, other.height)
            to_return = other.colliderect(pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
            return to_return == 1
        except AttributeError:
            print("A bad thing is happening")
            return other.colliderect(self.rect) == 1



class Button:

    def __init__(self, cords, size, string="Start", colors=[(125, 0, 0), (255, 125, 125)]):
        self.cords = cords
        self.size = size
        self.string = string
        self.colors = colors

    def update(self):
        pressed = pygame.mouse.get_pressed()
        if pressed[0] == 1:
            pos = pygame.mouse.get_pos()
            if self.cords[0] - self.size[0] / 2 <= pos[0] <= self.cords[0] + self.size[0] / 2:
                if self.cords[1] - self.size[1] / 2 <= pos[1] <= self.cords[1] + self.size[1] / 2:
                    return True
        return False

    def draw(self):
        color = self.colors[0]
        pos = pygame.mouse.get_pos()
        if self.cords[0] - self.size[0] / 2 <= pos[0] <= self.cords[0] + self.size[0] / 2:
            if self.cords[1] - self.size[1] / 2 <= pos[1] <= self.cords[1] + self.size[1] / 2:
                color = self.colors[1]
        pygame.draw.rect(screen, color,
                         (int(self.cords[0] - self.size[0] / 2), int(self.cords[1] - self.size[1] / 2), self.size[0],
                          self.size[1]))
        text = pygame.font.Font.render(font, self.string, True, (0, 0, 0))
        screen.blit(text, (self.cords[0] - font.size(self.string)[0] / 2, self.cords[1] - self.size[1] / 6))


class Wall(CollisionObject):

    def __init__(self, rect, color=(25, 25, 75)):
        super().__init__()
        self.rect = rect
        self.cords = [rect[0], rect[1]]
        self.color = color

    def draw(self):
        screen.blit(pygame.transform.smoothscale(pygame.image.load("wall.png"), (int(self.rect[2]), int(self.rect[3]))),
                    [self.cords[0], self.cords[1]])


class Map:

    def __init__(self, scene):
        self.map = scene
        self.walls = [Wall((size[0] / 2 - map_size[0] / 2, 0, tile_size, map_size[1] - tile_size)),
					   Wall((size[0] / 2 - map_size[0] / 2, 0, map_size[1], tile_size)),
					   Wall((size[0] / 2 - map_size[0] / 2, size[1] / 2 + map_size[1] / 2 - tile_size, map_size[0], tile_size)),
					   Wall((size[0] / 2 + map_size[0] / 2 - tile_size, 0, tile_size, map_size[1]))]

    def draw(self):  # TODO Clean up this code and then make it blit images instead of drawing rect's then add a delta
                    # TODO to have parts of the map of screen at times. Then rework into an list of obstacles.
        screen.fill((50, 50, 150))
        for wall in self.walls:
            wall.draw()


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=7, fire_rate=15, speed=5):
        self.ammo = ammo
        self.damage = damage
        self.clip_size = clip_size
        self.ammo_in_clip = 0
        self.bullet_size = bullet_size
        self.fire_rate = fire_rate
        self.reload()
        self.last_show_time = time.time()
        self.speed = speed

    def reload(self):
        if self.ammo - self.ammo_in_clip > 0:
            while self.ammo > 0 and self.ammo_in_clip <= self.clip_size:
                self.ammo_in_clip += 1
                self.ammo -= 1

    def get_damage(self):
        return random.randint(self.damage[0], self.damage[1])

    def get_speed(self):
        return self.speed

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


class PeaShooter(Gun):

    def __init__(self):
        super().__init__([2, 7], 100, 12)


class Pistol(Gun):

    def __init__(self):
        super().__init__([20, 35], 100, 12)


class Sniper(Gun):

    def __init__(self):
        super().__init__([9800, 10000], 50, 5, bullet_size=3, fire_rate=1)


class Akkk(Gun):

    def __init__(self):
        super().__init__([47, 67], 50, 5, fire_rate=5, speed=7)


class MiniGun(Gun):

    def __init__(self):
        super().__init__([5, 7], 10000, 1000, fire_rate=3)


class Bullet(DrawnObject):

    def __init__(self, cords, direction, weapon, shooter):
        super().__init__()
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
        pass

    def check_organism_collision(self):
        rects = [pygame.Rect(self.cords[0] - self.size, self.cords[1] - self.size, 5, self.size * 2),
                 pygame.Rect(self.cords[0] - self.size, self.cords[1] - self.size, self.size * 2, 5),
                 pygame.Rect(self.cords[0] - self.size / 2, self.cords[1] - self.size + self.size / 2, 3, 3),
                 pygame.Rect(self.cords[0] - self.size / 2 * 3, self.cords[1] - self.size + self.size / 2, 3, 3),
                 pygame.Rect(self.cords[0] - self.size / 2, self.cords[1] - self.size + self.size / 2 * 3, 3, 3),
                 pygame.Rect(self.cords[0] - self.size / 2 * 3, self.cords[1] - self.size + self.size / 2 * 3, 3, 3)]
        if self.shot_by != "Player":
            for player in players:
                cords = player.rect
                if pygame.Rect(cords[0], cords[1], tile_size - 20, tile_size - 20).collidelist(rects) != -1:
                    return player.take_damage(self.damage)
            for companion in companions:
                player_x = companion.cords[0] + companion.size
                x = self.cords[0]
                if self.cords[0] + self.size < companion.cords[0]:
                    x = self.cords[0] + self.size
                    player_x = companion.cords[0]

                player_y = companion.cords[1] + companion.size
                y = self.cords[1]
                if self.cords[1] + self.size < companion.cords[1]:
                    y = self.cords[1] + self.size
                    player_y = companion.cords[1]

                dist_x = player_x - x
                dist_y = player_y - y
                dist = (dist_x ** 2 + dist_y ** 2) ** .5
                if dist <= self.size * 1.5:
                    companion.warn(self)

                cords = companion.rect
                if pygame.Rect(cords[0], cords[1], tile_size - 20, tile_size - 20).collidelist(rects) != -1:
                    return companion.take_damage(self.damage)
        if self.shot_by != "Boss":
            for enemy in enemies:
                if isinstance(enemy, Boss):
                    cords = [enemy.x, enemy.y, enemy.width, enemy.height]
                    if pygame.Rect(cords).collidelist(rects) != -1:
                        enemy.take_damage(self.damage)
                        return True
                else:
                    cords = [enemy.cords[0], enemy.cords[1], enemy.size, enemy.size]
                    if pygame.Rect(cords).collidelist(rects) != -1:
                        enemy.take_damage(self.damage)
                        return True
        return False

    def draw(self):
        pygame.draw.circle(screen, bullet_colors[self.shot_by], [int(self.cords[0]), int(self.cords[1])], self.size)


class PowerUp(DrawnObject):

    def __init__(self, delay_top):
        super().__init__()
        self.size = size[1] / 50
        self.cords = [random.randint(0, map_size[0] - self.size), random.randint(0, map_size[1] - self.size)]
        self.delay = 0
        self.delay_top = delay_top
        self.rect = []
        self.reset()

    def reset(self):
        self.cords = [random.randint(0, map_size[0] - self.size), random.randint(0, map_size[1] - self.size)]
        self.rect = [self.cords[0], self.cords[1], self.size, self.size]
        self.delay = random.randint(self.delay_top[0], self.delay_top[1])

    def activate(self, player):
        pass

    def update(self):
        if self.delay > 0:
            self.delay -= 1
            return
        self.rect = (self.cords[0], self.cords[1], self.size, self.size)
        for player in players:
            if self.cords[0] < player.cords[0] + player.size and self.cords[0] + self.size > player.cords[0] \
                    and self.cords[1] < player.cords[1] + player.size and self.cords[1] + self.size > player.cords[1]:
                self.reset()
                self.activate(player)

    def draw(self):
        if self.delay > 0:
            return
        pygame.draw.rect(screen, (125, 255, 125), (self.cords[0], self.cords[1], self.size, self.size))


class Health(PowerUp):

    def __init__(self):
        super().__init__([300, 350])

    def activate(self, player):
        player.take_damage(-50)

    def draw(self):
        if self.delay > 0:
            return
        pygame.draw.rect(screen, (200, 100, 100), (self.cords[0], self.cords[1], self.size, self.size))
        draw_text("+", (130, 255, 130), [self.cords[0] + self.size / 2, self.cords[1] + self.size / 2], size=16)


class Shield(PowerUp):

    def __init__(self):
        super().__init__([750, 800])

    def activate(self, player):
        player.stronk = 200

    def draw(self):
        if self.delay > 0:
            return
        pygame.draw.rect(screen, (100, 100, 100), (self.cords[0], self.cords[1], self.size, self.size))
        draw_text("@", (130, 130, 130), [self.cords[0] + self.size / 2, self.cords[1] + self.size / 2], size=16)


class Dud:

    def __init__(self, cords, color):
        self.__cords__ = cords
        self.color = color
        self.cords = cords

    def set_cords(self, cords):
        self.cords = cords

    def draw(self):
        rect = (self.cords[0] * tile_size + 10,
                self.cords[1] * tile_size + 10, tile_size - 20,
                tile_size - 20)
        pygame.draw.rect(screen, self.color, rect)


class Boss(DrawnObject):

    def __init__(self, file_name, health=1000, name="Dick Pickens", width=134, height=109):
        super().__init__()
        self.width = width
        self.height = height
        self.file_name = file_name
        self.x = map_size[0] / 2 - width / 2
        self.y = map_size[1] / 4 - height / 2
        point = [random.randint(0, map_size[0]), random.randint(0, map_size[1])]
        dist_x = point[0] - self.x
        dist_y = point[1] - self.y
        dist = (dist_x ** 2 + dist_y ** 2) ** .5
        self.x_add = 2 * dist_x / dist
        self.y_add = 2 * dist_y / dist
        self.x_last_switch = 0
        self.y_last_switch = 0
        self.increasing = True
        self.scale = 0
        self.countdown = 0
        self.countdown_top = 10
        self.health = health
        self.max_health = health
        self.name = name

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def update(self):
        self.move()

    def move(self):
        if self.increasing:
            # self.scale += 1
            if self.scale > 150:
                self.increasing = False
        else:
            # self.scale -= 1
            if self.scale < 1:
                self.increasing = True

        self.x += self.x_add
        self.y += self.y_add
        if self.countdown == 0:
            self.take_shots()
            self.countdown = self.countdown_top
        if self.countdown > 0:
            self.countdown -= 1

    def take_shots(self):
        pass

    def draw(self):
        screen.blit(pygame.transform.smoothscale(pygame.image.load(self.file_name),
                                                 [self.width + self.scale, self.height + self.scale]), [self.x, self.y])

    def die(self):
        try:
            enemies.remove(self)
        except ValueError:
            print("WTF")


class TheBoss(Boss):

    def __init__(self):
        super(TheBoss, self).__init__("DrHair.png", name="Dr. No Snow", width=124, height=128)
        self.countdown_top = 1
        self.theta = 0

    def take_shots(self):
        x = self.x + self.width / 2 + self.scale / 2
        y = self.y + self.height / 2 + self.scale / 2
        radius = 50
        x_num = x + radius * math.cos(math.radians(self.theta)) - x
        y_num = y + radius * math.sin(math.radians(self.theta)) - y
        self.theta += 20
        shoot(direction=[x_num, y_num], leaving=[x, y], shot_by="Boss")

    def update(self):
        if self.countdown == 0:
            self.take_shots()
            self.countdown = self.countdown_top
        self.countdown -= 1

    def die(self):
        new = BaldBoss()
        enemies.append(new)
        try:
            enemies.remove(self)
        except ValueError:
            print("WTF")


class BaldBoss(Boss):

    def __init__(self):
        super(BaldBoss, self).__init__("DrNoHair.png", name="Dr. No Snow", width=124, height=128)
        self.countdown_top = 1
        self.thetas = [0, 90, 180, 270]

    def take_shots(self):
        x = self.x + self.width / 2 + self.scale / 2
        y = self.y + self.height / 2 + self.scale / 2
        radius = 50
        for index, theta in enumerate(self.thetas):
            x_num = x + radius * math.cos(math.radians(theta)) - x
            y_num = y + radius * math.sin(math.radians(theta)) - y
            self.thetas[index] += 10
            shoot(direction=[x_num, y_num], leaving=[x, y], shot_by="Boss")


class MeatShield(DrawnObject):

    def __init__(self, cords, color=[255, 50, 50]):
        super().__init__()
        self.cords = cords
        self.following = 0
        self.health = 50
        self.delay_top = 25
        self.delay = self.delay_top
        self.color = color
        self.size = int(tile_size * .75)
        if self.size % 2 != 0:
            self.size += 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        enemies.remove(self)

    def update(self):
        self.move()
        self.shoot()

    def shoot(self):
        if self.delay < 1:
            self.delay = self.delay_top
            closest_enemy = -1
            distance = -1
            for enemy in players:
                current_distance = (enemy.cords[0] ** 2 + enemy.cords[1] ** 2) ** .5
                if current_distance > distance or distance == -1:
                    closest_enemy = enemy
                    distance = current_distance
            if closest_enemy != -1:
                shoot([closest_enemy.cords[0] + closest_enemy.size / 2 + closest_enemy.delta[0],
                       closest_enemy.cords[1] + closest_enemy.size / 2 + closest_enemy.delta[1]],
                      [self.cords[0] + self.size / 2, self.cords[1] + self.size / 2],
                      shot_by="Boss", weapon=PeaShooter())
            self.following = players.index(closest_enemy)
        else:
            self.delay -= 1

    def move(self):
        player = players[self.following]

        player_x = player.cords[0] + player.size
        x = self.cords[0]
        if self.cords[0] + self.size < player.cords[0]:
            x = self.cords[0] + self.size
            player_x = player.cords[0]

        player_y = player.cords[1] + player.size
        y = self.cords[1]
        if self.cords[1] + self.size < player.cords[1]:
            y = self.cords[1] + self.size
            player_y = player.cords[1]

        dist_x = player_x - x
        dist_y = player_y - y
        dist = (dist_x ** 2 + dist_y ** 2) ** .5
        if dist > .5:
            self.cords = [self.cords[0] + 3 * dist_x / dist, self.cords[1] + 3 * dist_y / dist]

    def draw(self):
        rect = [self.cords[0], self.cords[1], self.size, self.size]
        pygame.draw.rect(screen, self.color, pygame.Rect(rect[0], rect[1], rect[2], rect[3]))


class TheHoff(Boss):

    def __init__(self):
        super(TheHoff, self).__init__("TheHoff.png", name="The Hoff Man")
        self.countdown_top = 3

    def take_shots(self):
        x = self.x + self.width / 2 + self.scale / 2
        y = self.y + self.height / 2 + self.scale / 2
        targets = [[1, 0], [0, 1], [-1, 0], [0, -1],
                   [1, 1], [-1, 1], [1, -1], [-1, -1],
                   [2, 1], [1, 2], [-2, 1], [1, -2], [-2, -1], [-1, 2], [-1, -2], [2, -1]]
        for target in targets:
            shoot(direction=target, leaving=[x, y], shot_by="Boss")


class Player:

    def __init__(self, cords, weapon, color, name):
        self.cords = cords
        self.stronk = 0
        self.weapon = weapon
        self.bullets = []
        self.health = 100
        self.color = color
        self.color_2 = [255 - color[0], 255 - color[1], 255 - color[2]]
        self.bullet_cool_down = weapon.get_fire_rate()
        self.shooting = False
        self.starting_cords = [cords[0], cords[1]]
        self.deaths = 0
        self.delta = [0, 0]
        self.last_shot = 0
        self.boost_time = 0
        self.boost_delay = 0
        self.pressed = [False, False, False, False]
        self.name = name
        self.size = tile_size
        self.max_speed = 7
        self.rect = [self.cords[0], self.cords[1], self.size, self.size]

    def update(self):
        self.handle_weapons()
        self.handle_movement()
        self.handle_stronk()
        self.subclass_update()

    def handle_stronk(self):
        if self.stronk > 0:
            self.stronk -= 1

    def handle_weapons(self):
        if self.weapon.is_loaded() and self.shooting and time.time() - self.last_shot > self.weapon.get_fire_rate() / 60:
            self.shoot()
            self.last_shot = time.time()

    def handle_movement(self):
        # Checks if player is going too fast
        if self.delta[0] > self.max_speed:
            self.delta[0] = self.max_speed
        if self.delta[0] < -self.max_speed:
            self.delta[0] = -self.max_speed
        if self.delta[1] > self.max_speed:
            self.delta[1] = self.max_speed
        if self.delta[1] < -self.max_speed:
            self.delta[1] = -self.max_speed
        for wall in game_map.walls:
            if wall.collide_rect(pygame.Rect(int(self.rect[0]), int(self.rect[1]), int(self.rect[2]), int(self.rect[3]))):
                print("Good")
                new_cords = self.cords
                if self.delta[1] < 0 and wall.rect[1] < self.cords:
                    new_cords[1] = wall.rect[1] + wall.rect[3]
                if self.delta[1] > 0 and wall.rect[1] > self.cords:
                    new_cords[1] = wall.rect[1] - wall.rect[3]
                if self.delta[0] < 0 and wall.rect[0] < self.cords:
                    new_cords[0] = wall.rect[0] + wall.rect[2]
                if self.delta[0] > 0 and wall.rect[0] > self.cords:
                    new_cords[0] = wall.rect[0] - wall.rect[2]
                self.delta = [self.cords[0] - new_cords[0], self.cords[1] - new_cords[1]]

    def take_damage(self, damage):
        if self.boost_time > 0:
            return False
        if self.stronk > 0:
            self.stronk -= 1
            return False
        self.health -= damage
        if self.health < 1:
            self.reset()
        if self.health > 100:
            self.health = 100
        return True

    def get_cords(self):
        return self.cords

    def shoot(self):
        pass

    def move(self):
        # if self.boost_time > 0:
        #     self.cords = [self.cords[0] + self.delta[0] * 2, self.cords[1] + self.delta[1] * 2]
        #     self.boost_time -= 1
        # else:
        #     self.cords = [self.cords[0] + self.delta[0], self.cords[1] + self.delta[1]]

	    if self.boost_time > 0:
		    update_draw_objects(self.delta[0] * -2, self.delta[1] * -2)
	    else:
		    update_draw_objects(self.delta[0] * -1, self.delta[1] * -1)

    def draw(self):
        self.rect = [self.cords[0], self.cords[1], self.size, self.size]
        if self.stronk > 49 or (self.stronk < 50 and not self.stronk % 2 == 0):
            pygame.draw.rect(screen, self.color_2, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw()

    def subclass_update(self):
        pass

    def reset(self):
        if isinstance(self, Human):
            global lives
            lives -= 1
        self.cords = self.starting_cords
        self.stronk = 200
        self.deaths += 1
        self.health = 100
        self.delta = [0, 0]
        self.pressed = [False, False, False, False]


class Human(Player):

    def __init__(self, cords, weapon, color=(0, 255, 0), name="The Hoff Slayer"):
        super().__init__(cords, weapon, color, name)

    def shoot(self):
        target = pygame.mouse.get_pos()
        shoot(target=[target[0], target[1]],
              leaving=([self.cords[0], self.cords[1]]),
              weapon=self.weapon)
        self.weapon.ammo -= 1

    def check_touch(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.delta[0] -= 5
                self.pressed[0] = True
            if event.key == pygame.K_d:
                self.delta[0] += 5
                self.pressed[1] = True
            if event.key == pygame.K_s:
                self.delta[1] += 5
                self.pressed[2] = True
            if event.key == pygame.K_w:
                self.delta[1] -= 5
                self.pressed[3] = True
            if event.key == pygame.K_SPACE:
                if self.boost_delay == 0:
                    self.boost_time = 10
                    self.boost_delay = 30
            if event.key == pygame.K_r:
                self.weapon.reload()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and self.pressed[0]:
                self.delta[0] += 5
            if event.key == pygame.K_d and self.pressed[1]:
                self.delta[0] -= 5
            if event.key == pygame.K_s and self.pressed[2]:
                self.delta[1] -= 5
            if event.key == pygame.K_w and self.pressed[3]:
                self.delta[1] += 5

    def subclass_update(self):
        self.shooting = pygame.mouse.get_pressed()[0] == 1
        if self.boost_delay > 0:
            self.boost_delay -= 1


class Companion(Player):

    def __init__(self, cords, weapon, color=(0, 255, 0), player_following=0, img=None, name="De White"):
        super().__init__(cords, weapon, color, name)
        self.following = player_following
        self.img = img
        self.shooting = True

    def move_with_player(self):
        player = players[self.following]

        player_x = player.cords[0] + player.size
        x = self.cords[0]
        if self.cords[0] + self.size < player.cords[0]:
            x = self.cords[0] + self.size
            player_x = player.cords[0]

        player_y = player.cords[1] + player.size
        y = self.cords[1]
        if self.cords[1] + self.size < player.cords[1]:
            y = self.cords[1] + self.size
            player_y = player.cords[1]

        dist_x = player_x - x
        dist_y = player_y - y
        dist = (dist_x ** 2 + dist_y ** 2) ** .5
        if dist > self.size * 1.5:
            self.delta = [5 * dist_x / dist, 5 * dist_y / dist]
        else:
            self.delta = [0, 0]

    def shoot(self):
        closest_enemy = -1
        distance = -1
        for enemy in enemies:
            current_distance = (enemy.x ** 2 + enemy.y ** 2) ** .5
            if current_distance > distance or distance == -1:
                closest_enemy = enemy
                distance = current_distance
        if closest_enemy == -1:
            self.shooting = False
            return
        shoot([closest_enemy.x + closest_enemy.width / 2, closest_enemy.y + closest_enemy.height / 2],
              [self.cords[0] + self.size / 2, self.cords[1] + self.size / 2])

    def warn(self, bullet):
        if bullet.cords[0] < self.cords[0]:
            self.delta[0] = 5
        else:
            self.delta[0] = -5

        if bullet.cords[1] < self.cords[1]:
            self.delta[1] = 5
        else:
            self.delta[1] = -5

    def draw(self):
        if self.img:
            screen.blit(pygame.transform.smoothscale(pygame.image.load(self.img),
                                                     [int(tile_size * 2), int(tile_size * 2)]),
                        [int(self.cords[0] - tile_size), int(self.cords[1] - tile_size)])
        else:
            pygame.draw.rect(screen, (130, 175, 255), (self.cords[0] - 50, self.cords[1] - 50, self.size, self.size))


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
    x_direction = 1.25
    y_direction = 1.25
    if len(target) != 0:
        if target[0] < leaving[0]:
            x_direction *= -1
        if target[1] < leaving[1]:
            y_direction *= -1
    distance = (axis_distances[0]**2 + axis_distances[1]**2)**0.5 / weapon.get_speed()
    try:
        towards = [axis_distances[0] / distance * x_direction]
    except ZeroDivisionError:
        towards = [axis_distances[0] * x_direction]
    try:
        towards.append(axis_distances[1] / distance * y_direction)
    except ZeroDivisionError:
        towards.append(axis_distances[1] * y_direction)
    bullets.append(Bullet([leaving[0] + towards[0] * 5, leaving[1] + towards[1] * 5], towards, weapon, shot_by))


def draw_gui():
    for i in range(lives):
        screen.blit(pygame.transform.smoothscale(heart_img,
                                                 [200, 100]), [-20 + 50 * i, size[1] - tile_size * 3 - 10])

    for i in range(len(enemies)):
        if isinstance(enemies[i], Boss):
            draw_health_bar(enemies[i].health, enemies[i].max_health,
                            (100, tile_size * 2 + tile_size * 1.5 * i, size[0] - 200, tile_size - 10),
                            name=enemies[i].name)

    for i in range(len(players) + len(companions)):
        if i < len(players):
            draw_health_bar(players[i].health, 100,
                            (size[0] - 200, size[1] - 50 - 35 * i, size[0] - (size[0] - 150), 12), name=players[i].name,
                            size=12)
        else:
            draw_health_bar(companions[i - len(players)].health, 100,
                            (size[0] - 200, size[1] - 50 - 35 * i, size[0] - (size[0] - 150), 12),
                            name=companions[i - len(players)].name, size=12)

    if players[0].boost_delay > 0:
        dash = (100, 100, 100)
    else:
        dash = (100, 255, 100)
    pygame.draw.rect(screen, dash, (size[0] / 2 - 38, size[1] - 50, 76, 5))


def draw_health_bar(health, max_health, rect, name="", size=20):
    pygame.draw.rect(screen, (75, 75, 75), rect)
    health_ratio = health / max_health
    if health > max_health:
        pygame.draw.rect(screen, (255, 0, 0), (rect[0], rect[1], rect[2] * 1, rect[3]))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (rect[0], rect[1], rect[2] * health_ratio, rect[3]))
    draw_text(name + " " + str(health) + "/" + str(max_health),
              cords=[rect[0] + rect[2] / 2, rect[1] - rect[3] / 2], color=(255, 255, 255), size=size)


def draw_text(msg, color=(255, 0, 0), cords=[0, 0], size=20):
    if size == 20:
        used_font = font
    else:
        used_font = pygame.font.Font('freesansbold.ttf', size)
    text = pygame.font.Font.render(used_font, msg, True, color)
    screen.blit(text, (cords[0] - used_font.size(msg)[0] / 2, cords[1] - used_font.size(msg)[1] / 2))


def draw_game_over_buttons():
    for button in game_over_buttons:
        button.draw()


# def draw_menu_buttons():
#     for button in menu_buttons:
#         button.draw()


def draw_game_over():
    screen.fill((175, 125, 125))
    draw_game_over_buttons()


def spawn_bosses(number=(0, 1)):
    global enemies
    enemies = []
    for x in range(number[0]):
        enemies.append(TheHoff())
    for x in range(number[1]):
        enemies.append(TheBoss())
    for x in range(number[2]):
        cords = [[int(tile_size + 1), int(size[0] / 3)], [int(size[0] * 2 / 3), int(size[0] - tile_size * 2)]]
        x_list = random.choice(cords)
        y_list = random.choice(cords)
        enemies.append(MeatShield([random.randrange(x_list[0], x_list[1]), random.randrange(y_list[0], y_list[1])]))


def create_players():
    global players
    players = [Human([map_size[0] / 2, map_size[1] / 2], Akkk(), (125, 255, 125))]


def create_companions():
    global companions
    companions = [Companion([size[0] / 2 - tile_size, size[1] / 2 - tile_size], Pistol(), (255, 255, 255),
                            img="DWHITE.png")]


def reset():
    global lives, bullets, players, enemies, levels
    lives = 5
    players = []
    enemies = []
    levels = [[1, 0], [0, 1], [2, 0], [3, 0], [1, 1], [2, 1]]
    create_players()
    spawn_bosses()
    bullets = []


def draw_power_ups():
    for power_up in power_ups:
        power_up.draw()


def update_power_ups():
    for power_up in power_ups:
        power_up.update()


def update_draw_objects(x_add, y_add):
	for object in drawn_objects:
		object.adjust(x_add, y_add)


pygame.init()
drawn_objects = []
size = [800, 800] 
map_size = [size[0], size[1]]
lives = 5
font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ScreenSaver")
Hoff = pygame.image.load('TheHoff.png')
playing = True
running = True
bullets = []
tile_size = size[0] / 25
game_map = Map(read_current_scene(name="CleanMap"))
players = []
companions = []
create_players()
# create_companions()
clock = pygame.time.Clock()
bullet_colors = {"Player": (50, 255, 50), "Boss": (255, 50, 50)}
heart_img = pygame.image.load("Heart.png")
game_over = True
game_over_buttons = [Button([size[0] / 3, size[1] / 2], [size[0] / 3.5, size[0] / 8], string="Playererererererer Again",
                     colors=[(0, 125, 0), (125, 255, 125)]),
                     Button([size[0] / 3 * 2, size[1] / 2], [size[0] / 3.5, size[0] / 8], string="Quit")]
power_ups = [Health(), Shield()]
# spawn_bosses()
levels = [[0, 0, 1]]  # , [0, 0, 5], [0, 0, 10], [0, 0, 15], [0, 0, 25], [0, 0, 50]]
# [[1, 0, 0], [0, 1, 5], [2, 0, 5], [3, 0, 10], [1, 1, 20], [2, 1, 25]]
enemies = []

# Begin setup menu code
# menu_buttons = [Button([size[0] / 6 * 2, size[1] / 10 * 8.5], [size[0] / 6, size[1] / 20 * 1], string="Previous"),
#                 Button([size[0] / 6 * 4, size[1] / 10 * 8.5], [size[0] / 6, size[1] / 20 * 1], string="Next"),
#                 Button([size[0] / 6 * 3, size[1] / 10 * 9.25], [size[0] / 6, size[1] / 20 * 1], string="Select")]
# setup = False
# skin_index = 0
#
# while setup:
#     screen.fill((100, 100, 100))
#     draw_menu_buttons()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit(0)
#     if menu_buttons[0].update():
#         skin_index -= 1
#     if menu_buttons[1].update():
#         skin_index += 1
#     pygame.display.update()


while running:
    playing = True
    while playing:
        if len(enemies) == 0:
            try:
                spawn_bosses(levels[0])
                del levels[0]
            except IndexError:
                spawn_bosses([0, 0, 1])
        game_map.draw()
        update_bullets()
        draw_bullets()
        update_power_ups()
        draw_power_ups()
        for enemy in enemies:
            enemy.update()
            enemy.draw()
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
        for companion in companions:
            companion.update()
            companion.move_with_player()
            companion.move()
            companion.draw()
        if lives == 0:
            playing = False
        draw_gui()
        pygame.display.update()
        clock.tick(60)
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
        draw_game_over()
        if game_over_buttons[0].update():
            game_over = False
        if game_over_buttons[1].update():
            pygame.quit()
            quit(0)
        pygame.display.update()
        clock.tick(60)
    reset()
