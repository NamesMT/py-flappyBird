from random import randint

import pygame

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 560

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Learning - FlappyBird")

# Global defines
font = pygame.font.Font("assets/04B_19.TTF", 24)

# Image loading
bird_img = pygame.image.load("assets/birds/blue/1.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipes/pipe-green.png").convert_alpha()

background_img = pygame.image.load("assets/background-day.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
base_img = pygame.image.load("assets/base.png").convert()
base_img = pygame.transform.scale(base_img, (int(base_img.get_width() * 1.3), int(base_img.get_height() * 1.3)))
gameover_img = pygame.image.load("assets/gameover.png").convert_alpha()

# Color define
GREEN = (13, 179, 20)
BLACK = (0, 0, 0)

# Groups
pipe_group = pygame.sprite.Group()


# Classes
class World:
    def __init__(self):
        self.speed = 2
        self.gravity = 0.75
        self.scroll = 0
        self.score = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 250
        self.alive = True
        self.velocity = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if pygame.sprite.spritecollide(self, pipe_group, False) or self.rect.y > 470:
            if self.alive:
                self.velocity = -4
            world.speed = 0
            world.gravity = 0.1


            self.alive = False

        if self.velocity < 10:
            self.velocity += world.gravity

        self.rect.y += self.velocity


class Pipe(pygame.sprite.Sprite):
    def __init__(self, img, isFlip=False, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 400 - randint(0, 200)
        self.Pointed = False
        pipe_group.add(self)

        if not isFlip:
            Pipe(pipe_img, True, self.rect.y)
        else:
            self.image = pygame.transform.flip(img, False, True)
            self.rect.y = y - 480
            self.Pointed = True

    def update(self):
        self.rect.x -= world.speed

        if self.rect.x < bird.rect.x and self.Pointed == False:
            world.score += 1
            self.Pointed = True


# Functions
def draw_text(text, color, x, y, rightalign=False):
    textimg = font.render(text, True, color)
    if rightalign:
        x = SCREEN_WIDTH - textimg.get_width() - x

    screen.blit(textimg, (x, y))


def draw_background():
    screen.blit(background_img, (0, 0))


def draw_base():
    screen.blit(base_img, (0 + world.scroll, 480))


# Object init
world = World()
bird = Bird(bird_img)
Pipe(pipe_img)


CREATE_PIPE = pygame.USEREVENT

pygame.time.set_timer(CREATE_PIPE, 1500)
running = True
while running:
    clock.tick(60)

    # Bat va xu ly event
    for event in pygame.event.get():
        if event.type == CREATE_PIPE:
            Pipe(pipe_img)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if bird.alive and \
                    event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                bird.velocity = -11

    ###
    world.scroll -= world.speed
    if world.scroll < -60:
        world.scroll = 0
    ###
    draw_background()

    pipe_group.update()
    pipe_group.draw(screen)

    draw_base()

    bird.update()
    bird.draw()

    if not bird.alive:
        screen.blit(gameover_img, (85, 200))


    draw_text(f"Score: {world.score}", BLACK, 10, 10)
    draw_text(f"Alive: {bird.alive}", BLACK, 10, 10, True)
    pygame.display.update()
pygame.quit()
