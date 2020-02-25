import pygame
import neat
import time
import os
import random

from Bird import Bird

pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
SCORE_FONT = pygame.font.SysFont("GoudyStout", 25)
GAME_OVER_FONT = pygame.font.SysFont("Microsoft Sans Serif", 70)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird): #pixel perfect collision
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        #how far top left corners are from eachother
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) #returns none if no collision

        if t_point or b_point:
            return True

        return False

class Base:
    VEL = 5 #should be same as pipe velocity
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self. y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #cycles the two images for a constantly moving base
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, bird, pipes, base, score, run):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    text = SCORE_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    if run == False:
        gameover = GAME_OVER_FONT.render("GAME OVER", 1, (255, 0, 0))
        win.blit(gameover, (round((WIN_WIDTH - gameover.get_width()) / 2), round(WIN_HEIGHT / 2)))
    else:
        bird.draw(win)
    pygame.display.update()


def main():
    score = 0
    pipeSpawnDist = 600
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(pipeSpawnDist)]
    win = pygame.display.set_mode((WIN_WIDTH ,WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)  # at most 30 ticks per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        base.move()
        bird.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                #pass
                run = False
                break
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  #checks if pipe has already passed screen
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score+=1
            pipes.append(Pipe(pipeSpawnDist))

        for remove in rem:
            pipes.remove(remove)

        draw_window(win, bird, pipes, base, score, run)

    RUN = True
    while RUN:
        draw_window(win, bird, pipes, base, score, run)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
    pygame.quit()
    quit()
main()