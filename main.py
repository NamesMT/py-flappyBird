from random import randint, randrange

import pygame

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 560

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Learning - FlappyBird")

# Global defines
font = pygame.font.Font("assets/04B_19.TTF", 20)


# Sound class and Music loading
class SFX:
	fx_flap = pygame.mixer.Sound('sound/sfx_wing.wav')
	fx_die = pygame.mixer.Sound('sound/sfx_die.wav')
	fx_hit = pygame.mixer.Sound('sound/sfx_hit.wav')
	fx_point = pygame.mixer.Sound('sound/sfx_point.wav')


# Array image loading
birds = []
pipes = []
# Birds loader
for color in ['blue', 'red', 'yellow']:
	bird = []
	for index in range(3):
		bird.append(pygame.image.load(f"assets/birds/{color}/{index}.png").convert_alpha())
	birds.append(bird)
# Pipes loader
for color in ['green', 'red']:
	pipes.append(pygame.image.load(f"assets/pipes/pipe-{color}.png").convert_alpha())

# Image loading
bird_img = birds[0]
pipe_img = pipes[0]

background_img = pygame.image.load("assets/background-day.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
base_img = pygame.image.load("assets/base.png").convert()
base_img = pygame.transform.scale(base_img, (int(base_img.get_width() * 1.3), int(base_img.get_height() * 1.3)))
gameover_img = pygame.image.load("assets/gameover.png").convert_alpha()
welcome_img = pygame.image.load("assets/message.png").convert_alpha()

# Color define
GREEN = (13, 179, 20)
BLACK = (0, 0, 0)

# Groups
pipe_group = pygame.sprite.Group()


# Classes
class World:
	def __init__(self, is_restart=False):
		self.speed = 3
		self.gravity = 0.75
		self.scroll = 0
		self.score = 0

		if not is_restart:
			self.state = "Welcome"
			self.highscore = 0

	def restart(self):
		self.__init__(True)
		self.state = "Running"
		bird.__init__(birds[randrange(0, len(birds))])
		pipe_group.empty()

		global pipe_img
		pipe_img = pipes[randrange(0, len(pipes))]

	def addScore(self, amount):
		SFX.fx_point.play()
		self.score += amount
		if self.score > self.highscore:
			self.highscore = self.score

		if self.score >= 30 and self.score <= 150:
			self.speed = (self.score / 15) + 1

	def draw(self):
		if world.state == "Welcome":
			screen.blit(welcome_img, (90, 50))
			draw_text("Press W/UP/Space to Start!", BLACK, 40, 350)

		if world.state == "Over":
			screen.blit(gameover_img, (90, 200))
			draw_text("Press W/UP/Space to Restart!", BLACK, 30, 250)


class Bird(pygame.sprite.Sprite):
	def __init__(self, imglist):
		pygame.sprite.Sprite.__init__(self)
		self.index = 0
		self.time = pygame.time.get_ticks()
		self.imglist = imglist
		self.image = self.animate()
		self.rect = self.image.get_rect()
		self.rect.x = 30
		self.rect.y = 250
		self.alive = True
		self.velocity = 0

	def draw(self):
		screen.blit(self.image, self.rect)

	def update(self):
		if not world.state == "Welcome":
			if pygame.sprite.spritecollide(self, pipe_group, False) or self.rect.y > 470:
				if self.alive:
					self.velocity = -4
					SFX.fx_die.play()
					SFX.fx_hit.play()
				world.speed = 0
				world.gravity = 0.1
				world.state = "Over"
				self.alive = False

			if self.velocity < 10:
				self.velocity += world.gravity

			self.rect.y += self.velocity

			self.image = self.animate()
			self.image = pygame.transform.rotate(self.image, -self.velocity * 3)

	def animate(self):
		if (pygame.time.get_ticks() > self.time + 100) and self.alive:
			self.time = pygame.time.get_ticks()
			if self.index >= 2:
				self.index = 0
			else:
				self.index += 1

		return self.imglist[self.index]


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
		if not world.state == "Welcome":
			self.rect.x -= world.speed

			if self.rect.x < bird.rect.x and self.Pointed == False:
				world.addScore(1)
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

pygame.time.set_timer(CREATE_PIPE, 1200)
running = True
while running:
	clock.tick(60)

	# Bat va xu ly event
	for event in pygame.event.get():
		if event.type == CREATE_PIPE:
			Pipe(pipe_img)
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and \
				(event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w):
			if world.state == "Running":
				bird.velocity = -11
				SFX.fx_flap.play()
			else:
				world.restart()

	### Cuộn Background
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

	# Vẽ theo trạng thái của game
	world.draw()

	draw_text(f"Score: {world.score}", BLACK, 10, 10)
	draw_text(f"High Score: {world.highscore}", BLACK, 10, 10, True)

	pygame.display.update()

pygame.quit()
