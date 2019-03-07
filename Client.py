#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pygame
import time


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg.startswith("a"):
                global ID
                if ID == -1:
                    ID = eval(msg.split("a")[0])
            if msg.startswith("ID"):
                # global ID
                ID = eval(msg.split("ID")[1])
            if msg.startswith("cords"):
                msg = msg.split("cords")[1]
                split = msg.split("|")
                cords = split[1].split(":")
                players[eval(split[0])].cords = [eval(cords[0]), eval(cords[1])]
            if msg.startswith("bullets"):
                msg = msg.split("bullets")[1]
                msgs = msg.split(":")
                global bullets
                bullets = []
                for x in range(0, len(msgs), 4):
                    bullets.append(Bullet([eval(msgs[x]), eval(msgs[x + 1])], eval(msgs[x + 2]),
                                          guns[eval(msgs[x + 3])]))
        except OSError:  # Possibly client has left the chat.
            break
        except SyntaxError:
            break
        update()


def send(event=None, msg=""):  # event is passed by binders.
    """Handles sending of messages."""
    # my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    # my_msg.set("{quit}")
    send()


if __name__ == "__main__":
    pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinder")
playing = True


class Map:

    def __init__(self):
        self.map = scene

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

    def __init__(self, bullet_size=(10, 5)):
        self.bullet_size = bullet_size

    def get_bullet_size(self):
        return self.bullet_size


class Pistol(Gun):

    def __init__(self):
        super().__init__((25, 30))


class MiniGun(Gun):

    def __init__(self):
        super().__init__((5, 7))


class Bullet:

    def __init__(self, cords, direction, weapon):
        self.cords = cords
        self.size = weapon.get_bullet_size()
        if direction > 1:
            self.size = [self.size[1], self.size[0]]
        self.direction = direction

    def draw(self):
        x = self.cords[0] * tile_size + tile_size / 2 - self.size[0] / 2
        y = self.cords[1] * tile_size + tile_size / 2 - self.size[1] / 2
        pygame.draw.rect(screen, (255, 25, 25), (x, y, self.size[0], self.size[1]))


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


def read_current_scene():
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


def draw():
    game_map.draw()
    for bullet in bullets:
        bullet.draw()
    for player in players:
        player.draw()
    pygame.display.update()


def update():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                send(str="{quit}")
                quit()
            if event.type == pygame.KEYDOWN:
                key = str(event.key)
                send(str=("KEYDOWN" + key))
            if event.type == pygame.KEYDOWN:
                key = str(event.key)
                send(str=("KEYUP" + key))
        clock.tick(30)


def main():
    if __name__ == "__main__":
        update_thread = Thread(target=update)
        receive_thread = Thread(target=receive)
        update_thread.start()
        update_thread.start()
        update_thread.join()
        receive_thread.join()


scene = []
read_current_scene()
clock = pygame.time.Clock()
colors = [(255, 0, 0), (0, 255, 0)]
tile_size = size[0] / 25
guns = [Pistol(), MiniGun()]
directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [0, 0]]  # 0:Right, 1:Left, 2:Down, 3: Up 4: Still


# My stuff
game_map = Map()
bullets = []

# ----Now comes the sockets part----
HOST = ''  # input('Enter host: ')
PORT = 8443   # input('Enter port: ')


BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
ID = 0
IDs = [0, 1]
IDs.remove(ID)
players = [Dud([23, 12], (0, 0, 0)), Dud([1, 12], (0, 0, 0))]
players[ID].color = colors[1]
players[IDs[0]].color = colors[0]


main()
