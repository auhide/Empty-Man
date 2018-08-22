import pygame
import time
import random
from game_classes import *

# game_classes has:
# 	class Player:
#		method print_image()
#	class Obstacle:
#		class Fence:
#			method print_fence()
#		class Drop:
#			method print_drop()

pygame.init() # <---Initializes all imported pygame modules

FPS = 60

black = (0, 0, 0)

clock = pygame.time.Clock() # We regulate the fps with |clock|

# DISPLAY SIZE
display_w = 800
display_h = 600

# WINDOW SETUP
gameDisplay = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Empty Guy')
bg = pygame.image.load('background.png')

# CHARACTER
image_w 	 = 50
image_h 	 = 125
char_normal  = "figure.png"
char_blurred  = "figure_blured.png"
char_moving  = "figure_walking.png"
char_jumping = "figure_jumping.png"

# OBSTACLES INFO
# Fence
obstacle1 	= pygame.image.load('obstacle1.png')
obstacle_w 	= 70
obstacle_h 	= 75
# Rain drop
drop 	= pygame.image.load('drop.png')
drop_w 	= 31
drop_h 	= 53

# POINTS IMAGE
points_img = pygame.image.load('points_img.png')
points_img = pygame.transform.scale(points_img, (90, 30))

# METHODS
def print_on_screen(image, x, y):
	gameDisplay.blit(image, (x, y))

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf', 70)
	TextSurf, TextRect = text_objects(text, largeText) # TextSurf = Text surface; TextRect = Rectangle that contains the text
	TextRect.center = (display_w/2, display_h/2)
	gameDisplay.blit(TextSurf, TextRect)

	pygame.display.update()

	time.sleep(2)

	game_loop()

def collision():
	message_display('')

def fences_dodged(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render(str(count), True, black)
	gameDisplay.blit(text, (95, 10))

def quitgame():
	pygame.quit()
	quit()

#  //////////////////////////////////////////////////   MAIN    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# ////////////////////////////////////////////////// GAME METHOD \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def game_loop():

	# Character Starting Coordinates
	x = 10
	y = image_h*3.45

	# Background Coordinates
	bg_x 	 = 0
	bg_y 	 = 0
	bg_speed = 2.5
	bg_x1 	 = display_w

	gameExit = False

	x_change = 0

	# Choosing which image to print to the screen 
	currentImage = 0 
	# 0 for NORMAL_IMAGE
	# 1 for MOVING_IMAGE
	# 2 for JUMPING_IMAGE

	# Fence
	obstacle_x 		= 1400
	obstacle_y 		= 480
	obstacle_speed 	= 2.5
	# Drop
	drop_x 			= random.randrange(0, display_w - drop_w) 
	drop_y 			= -display_h
	drop_speed		= 5

	inJump 	  = False
	jumpCount = 10

	points = 0

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()
			elif event.type == pygame.KEYUP: # <----if the key is released
				if event.key == pygame.K_a or event.key == pygame.K_d:
					x_change = 0
				currentImage = 0

		keys = pygame.key.get_pressed()

		if not inJump:
			if keys[pygame.K_ESCAPE]:
				quitgame()

			if keys[pygame.K_a]:
				x_change = -10
				currentImage = 1

			if keys[pygame.K_d]:
				x_change = 10
				currentImage = 1
			if keys[pygame.K_w]:
				inJump = True

		if inJump:
			currentImage = 2
			if jumpCount >= -10:
				neg = 1
				if jumpCount < 0:
					neg = -1
				y -= (jumpCount**2)*0.5*neg
				jumpCount -= 1
			else:
				inJump = False
				jumpCount = 10
				
			

		x += x_change


		# Moving background
		rel_x = bg_x % bg.get_rect().width
		# NOTE: -1 % 800 = 799

		print_on_screen(bg, rel_x - bg.get_rect().width, bg_y)
		if rel_x < display_w:
			print_on_screen(bg, rel_x, bg_y)

		print_on_screen(points_img, 0, 0)

		bg_x -= bg_speed # With bg_x we can regulate the speed of the moving background image


		fences_dodged(points)
		
		obstacle1 = Obstacle(obstacle_x, obstacle_y)
		obstacle1.fence.print_fence()

		obstacle2 = Obstacle(drop_x, drop_y)
		obstacle2.drop.print_drop()

		obstacle_x -= obstacle_speed
		drop_y += drop_speed


		if x > display_w - image_w:
			x = display_w - image_w
		elif x < 0:
			x = 0


		
		# Here we decide what image to print
		if currentImage == 0:
			player = Player(char_normal, x, y)
			player.print_image()
		elif currentImage == 1:
			player = Player(char_moving, x, y)
			player.print_image()
			player = Player(char_blurred, x, y)
			player.print_image()
		elif currentImage == 2:
			player = Player(char_jumping, x, y)
			player.print_image()

		
		# Conditions for the Fence
		if obstacle_x < 0 - obstacle_w:
			obstacle_x = display_w + 100
			obstacle_speed += 0.5
			bg_speed += 0.5# To increase the speed of the background
			points += 1
		# Conditions for the Rain Drop
		if drop_y > display_h:
			drop_y = 0 - drop_h*3
			drop_x = random.randrange(0, display_w - drop_w) 
			drop_speed += 0.4

		
		# Collision with the Fence
		if ((y + image_h/2) < (obstacle_y + obstacle_h)) and ((y + image_h/2) > obstacle_y):
			print("y crossover")
			if ( (x < (obstacle_x + obstacle_w/1.5) and (x + image_w/1.5)> obstacle_x)):
				print("x crossover")
				collision()
		# Collision with the Rain Drop
		if ((y + image_h/2) < (drop_y + drop_h)) and ((y + image_h/2) > drop_y):
			print("y DROP crossover")
			if ( (x < (drop_x + drop_w/1.5) and (x + image_w/1.5) > drop_x)):
				print("x DROP crossover")
				collision()


		pygame.display.update()

		clock.tick(FPS)


if __name__ == '__main__':
	game_loop()