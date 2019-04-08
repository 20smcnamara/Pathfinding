import pygame
import time

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
display_size = [800, 800]
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("Pathfinder")
playing = True

class SceneMaker:

    def __init__(self, size):
        self.map = []
        self.size = size
        self.last_pressed = []
        self.doing = -1
        for x in range(size):
            row = []
            for y in range(size):
                row.append(0)
            self.map.append(row)

    def draw(self):
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 0:
                    pygame.draw.rect(screen, (25, 25, 75),
                                     (col * (display_size[0] / len(self.map[0])),
                                      row * (display_size[1] / len(self.map)),
                                      display_size[0] / len(self.map), display_size[1] / len(self.map[0])))
                else:
                    pygame.draw.rect(screen, (50, 50, 150),
                                     (col * (display_size[0] / len(self.map[0])),
                                      row * (display_size[1] / len(self.map)),
                                      display_size[0] / len(self.map), display_size[1] / len(self.map[0])))
        pygame.display.update()

    def update(self):
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            pos = [pos[0], pos[1]]
            while pos[0] % (display_size[0] / self.size) != 0:
                pos[0] -= 1
            while pos[1] % (display_size[1] / self.size) != 0:
                pos[1] -= 1
            pos = [int(pos[1] / (display_size[0] / self.size)), int(pos[0] / (display_size[0] / self.size))]
            if self.doing == -1:
                if self.map[pos[0]][pos[1]] == 0:
                    self.doing = 1
                else:
                    self.doing = 0
            self.map[pos[0]][pos[1]] = self.doing
        else:
            self.doing = -1
            self.last_pressed = []


game_map = SceneMaker(50)
scene = []


def read_current_scene(name):
    with open(name) as f:
        contents = f.read()
    in_list = contents.split("\n")
    for line in in_list:
        row = []
        for status in line:
            row.append(int(status))
        if row:
            scene.append(row)


def write_map():
    file_name = input("What file do you want to write to? ")
    final_string = ""
    for row in game_map.map:
        row_string = ""
        for item in row:
            row_string += str(item)
        final_string += row_string + "\n"
    file_object = open(file_name, "w")
    file_object.write(final_string)


if input("Do you want to load a file ") == "yes":
    name = input("What is the name of the file ")
    try:
        read_current_scene(name)
        game_map.map = scene
        game_map.size = len(scene)
    except:
        print("File not found")
else:
    size = eval(input("What size do you want your map "))
    game_map = SceneMaker(size)


while playing:
    game_map.draw()
    game_map.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                write_map()
                playing = False
