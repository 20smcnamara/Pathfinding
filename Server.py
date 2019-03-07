#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
# from PathfindingMain import SeverAssets


# My Stuff
import pygame
import math
import random

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [800, 800]
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

        # Check if at entering
        if leaving == entering:
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
                if cords in new_made_moves or len(self.map) <= cords[0] or cords[0] < 0 or len(self.map[0]) <= cords[
                    1] or \
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


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=(10, 5), fire_rate=15, ID=-1):
        self.ammo = ammo
        self.damage = damage
        self.clip_size = clip_size
        self.ammo_in_clip = 0
        self.bullet_size = bullet_size
        self.fire_rate = fire_rate
        self.reload()
        self.ID = ID

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
        super().__init__((25, 30), 100, 10, ID=0)


class MiniGun(Gun):

    def __init__(self):
        super().__init__((5, 7), 1000, 100, (5, 5), ID=1)


class Player:

    def __init__(self, cords, weapon, direction):
        self.cords = cords
        self.weapon = weapon
        self.direction = direction
        self.health = 100
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
            # print(self.cords, [self.cords[0] + direction[0], self.cords[1] + direction[1]])
            bullets.append(Bullet([self.cords[0] + direction[0], self.cords[1] + direction[1]], self.direction,
                                  self.weapon))
        to_remove = []
        for bullet in bullets:
            if bullet.update():
                to_remove.append(bullet)
        for remove in to_remove:
            bullets.remove(remove)

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
            if game_map.get_map_value(new_cords) == 1:
                self.cords = new_cords


class Human(Player):

    def __init__(self, cords, weapon, direction=0):
        super().__init__(cords, weapon, direction)

    def check_touch_down(self, key):
        if key == pygame.K_a:
            self.direction = 0
            self.is_moving = True
        if key == pygame.K_d:
            self.direction = 1
            self.is_moving = True
        if key == pygame.K_s:
            self.direction = 2
            self.is_moving = True
        if key == pygame.K_w:
            self.direction = 3
            self.is_moving = True
        if key == pygame.K_SPACE:
            self.shooting = True

    def check_touch_up(self, key):
        if key == pygame.K_a or key == pygame.K_d or key == pygame.K_s or key == pygame.K_w:
            self.is_moving = False
        if key == pygame.K_SPACE:
            self.shooting = False


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


# Their stuff

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    clients[client] = name
    client.send(bytes("", "utf8")+bytes('ID' + str(len(clients) - 1)))

    while True:
        accept_incoming_connections()
        for client in clients:
            handle_client(client)
        for player in range(len(players)):
            broadcast("cords" + str(player) + str(players[player].cords[0]) + ":" + str(players[player].cords[1]))
        bullet_data_to_send = "bullets" + "|"
        for bullet in range(len(bullets)):
            bull = bullets[bullet]
            bullet_data_to_send += str(bull.cords[0]) + ":" + str(bull.cords[1]) + ":" + str(
                bull.directions) + ":" + \
                                   str(bull.weapon.ID)
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            # broadcast(msg)
            if msg.startswith("KEYDOWN"):
                msg = msg.split("KEY")[1]
                client_index = find_index_of_dict(clients, client)
                players[client_index].check_touch_down(msg)
            if msg.startswith("KEYUP"):
                msg = msg.split("KEY")[1]
                client_index = find_index_of_dict(clients, client)
                players[client_index].check_touch_up(msg)
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the game." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


def find_index_of_dict(dict_passed, item):
    for i in range(len(dict_passed.keys)):
        if dict_passed[dict_passed.keys[i]] == item:
            return i


# My game stuff
scene = []
read_current_scene()
game_map = Map(scene)
players = [Human([23, 12], Pistol()), Human([1, 12], Pistol())]
tile_size = size[0] / len(scene)
move_timer_max = 5
move_timer = move_timer_max
bullets = []
directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [0, 0]]  # 0:Right, 1:Left, 2:Down, 3: Up 4: Still


# Server Stuff Mostly
clients = {}
addresses = {}

HOST = ''
PORT = 8443
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    print("END")
    SERVER.close()
