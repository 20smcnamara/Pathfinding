import pygame
from PathfindingMain import Client

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


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            Client.send(str="{quit}")
            quit()
        if event.type == pygame.KEYDOWN:
            key = str(event.key)
            Client.send(str=("KEYDOWN" + key))
        if event.type == pygame.KEYDOWN:
            key = str(event.key)
            Client.send(str=("KEYUP" + key))
    Client.game_map.draw()
    for bullet in Client.Bullets:
        bullet.draw()
    for player in Client.players:
        player.draw()


scene = []
read_current_scene()
colors = [(255, 0, 0), (0, 255, 0)]
tile_size = size[0] / 25
guns = [Pistol(), MiniGun()]
directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [0, 0]]  # 0:Right, 1:Left, 2:Down, 3: Up 4: Still
