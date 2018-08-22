import pygame

display_w = 800
display_h = 600

gameDisplay = pygame.display.set_mode((display_w, display_h))

class Player:
	def __init__(self, image_name, width, height):
		self.w 			 = width
		self.h 			 = height
		self.image_w 	 = 50
		self.image_h	 = 125
		self.image_load  = pygame.image.load(image_name)
		self.image_load = pygame.transform.scale(self.image_load, (self.image_w, self.image_h))

	def print_image(self):
		gameDisplay.blit(self.image_load, (self.w, self.h))


class Obstacle:
	def __init__(self, width, height):
		self.fence = self.Fence(width, height)
		self.drop  = self.Drop(width, height)

	class Fence:
		def __init__(self, width, height):
			self.fence_load = pygame.image.load('obstacle1.png')
			self.fence_w 	= width
			self.fence_h 	= height

		def print_fence(self):
			gameDisplay.blit(self.fence_load, (self.fence_w, self.fence_h))


	class Drop:
		def __init__(self, width, height):
			self.drop_load = pygame.image.load('drop.png')
			self.drop_w    = width
			self.drop_h    = height

		def print_drop(self):
			gameDisplay.blit(self.drop_load, (self.drop_w, self.drop_h))