
'''
Main driver for gridworld game board.
All code provided by Winter 2019, CSE 150 course.
'''

import pygame
import random
import sys

from pygame.locals import *
from methods import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 82, 33)
GREY = (220, 220, 220)
DARKGREY = (128, 128, 128)
GREENGREY = (125, 164, 120)
RED = (160, 27, 16)
REDGREY = (182, 128, 109)
AISLE = (250, 250, 250)
PURPLE = (128, 0, 128)
GOLD = (230, 230, 138)
YELLOW = (255, 255, 0)
YELLOW_2 = (150, 150, 0)

AISLES = [(1, 1), (2, 1), (3, 1), (1, 3), (2, 3), (3, 3)]

START_POSITION_X = 0
START_POSITION_Y = 0

SCREEN_RES_X = 500
SCREEN_RES_Y = 500

NODE_WIDTH = 100
NODE_HEIGHT = 100

class GridWorld():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grid World")
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [SCREEN_RES_X, SCREEN_RES_Y]
        self.font = pygame.font.SysFont("Calibri", 16)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        self.show_checked = True
        self.quit = False
        self.type = "bfs"
        self.grid = None
        self.new_grid()
    def new_grid(self):
        saved_start = None
        if self.grid:
            print("Saved start")
            saved_start = self.grid.start

        self.grid = Grid(self)
        if saved_start:
            self.grid.start = saved_start
        self.agent = Agent(self.grid, self.grid.start, self.grid.goal, self.type)
        self.grid.set_aisle()
        self.run = False
    def loop(self):
        while True:
            self.draw()
            self.clock.tick(60)
            self.mpos = pygame.mouse.get_pos()
            if self.run:
                if self.agent.finished:
                    self.agent.show_result()
                    self.run = False
                elif self.agent.failed:
                    self.run = False
                else:
                    self.agent.make_step()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        self.run = not self.run
                    if event.key == K_c:
                        self.new_grid()
                    if event.key == K_2:
                        self.grid.clear_path()
                        self.type = "bfs"
                        self.agent.new_plan(self.type)
#                    if event.key == K_4:
#                        self.grid.clear_path()
#                        self.type = "astar"
#                        self.agent.new_plan(self.type)
    def draw(self):
        self.screen.fill(0)
        self.grid.update()
#        self.blitInfo()
        pygame.display.update()

class Grid:
    def __init__(self, game):
        self.game = game
        self.width = int(self.game.screen_res[0]/NODE_WIDTH)
        self.height = int((self.game.screen_res[1]/NODE_HEIGHT))
#        print(self.game.screen_res[1])
#        print(NODE_HEIGHT)
        self.nodes = {(i, j):Node(self, (i, j)) for i in range(self.height) for j in range(self.width)}
        self.row_range = self.width
        self.col_range = self.height
        self.start = (START_POSITION_X, START_POSITION_Y)
        self.goal = (random.randint(0, self.height-1), random.randint(0, self.width-1))
        while self.goal == self.start or self.goal in AISLES:
            self.goal = (random.randint(0, self.height-1), random.randint(0, self.width-1))
    def update(self):
        for node in self.nodes.values():
            node.update()
            node.draw(self.game.screen)
        for i in range(self.width):
            pygame.draw.line(self.game.screen, [200, 200, 200], (NODE_WIDTH*i, 0), (NODE_WIDTH*i, 750))
        for i in range(self.height):
            pygame.draw.line(self.game.screen, [200, 200, 200], (0, (NODE_HEIGHT*i)+0), (750, (NODE_HEIGHT*i)+0))
    def set_aisle(self):
        for node in self.nodes.values():
            if node.pos in AISLES:
                node.aisle = True
    def clear_path(self):
        for node in self.nodes.values():
            if node.checked:
                node.checked = False
            if node.in_path:
                node.in_path = False
            if node.frontier:
                node.frontier = False

class Node():
    def __init__(self, grid, pos):
        self.grid = grid
        self.game = self.grid.game
        self.pos = pos
        self.blit_pos = [self.pos[1]*NODE_WIDTH, self.pos[0]*NODE_HEIGHT]
        self.color = BLACK
        self.image = pygame.Surface((NODE_WIDTH, NODE_HEIGHT))
        self.rect = self.image.get_rect(topleft=self.blit_pos)
        self.in_path = False
        self.checked = False
        self.frontier = False
        self.aisle = False
        self.start = False
        self.goal = False
    def update(self):
        #The order of these lines is important
        if self.aisle:
            self.color = AISLE
        elif self.start:
            self.color = YELLOW
        elif self.goal:
            self.color = YELLOW_2
        elif self.in_path:
            self.color = RED
        elif self.frontier:
            self.color = GREY
        elif self.checked:
            self.color = DARKGREY
        elif not self.game.run:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.game.mpos):
                self.aisle = True
            if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(self.game.mpos):
                self.aisle = False
        else:
            self.color = BLACK
    def draw(self, screen):
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)

if __name__ == '__main__':
    game = GridWorld()
    game.loop()
