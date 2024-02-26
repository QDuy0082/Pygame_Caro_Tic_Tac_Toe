import pygame, sys
from pygame.locals import *
from pygame import mixer 
import math


pygame.init()
FPSCLOCK = pygame.time.Clock()

FPS = 120
WINDOWWIDTH = 1000
WINDOWHEIGHT = 700

YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('caro')


class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int (width * scale), int (height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				win_sound.play()
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
		 	self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))


start_btn_bf = pygame.image.load('start_btn_bf.png').convert_alpha()
start_btn_at = pygame.image.load('start_btn_at.png').convert_alpha()
bg_win = pygame.image.load('bg_win.jpg').convert()
win_sound = pygame.mixer.Sound('button-25.wav')
start_btn_at_img = Button(338, 296, start_btn_at, 0.97)
start_btn_bf_img = Button(330, 400, start_btn_bf, 0.3)


bg_win_width =  bg_win.get_width()
scroll = 0
til = math.ceil(WINDOWWIDTH/bg_win_width)+1

mixer.music.load('Bgmusic.wav')


while True:
	for i in range (0, til):
		DISPLAYSURF.blit(bg_win,(i*bg_win_width+scroll,0))
	scroll -= 0.5
	if abs(scroll) > bg_win_width:
		scroll =0

	start_btn_bf_img.draw(DISPLAYSURF)

	pos = pygame.mouse.get_pos()
	if start_btn_bf_img.rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == 1:
			start_btn_at_img.draw(DISPLAYSURF)
			pygame.display.update()
			pygame.time.wait(200)

	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()


	pygame.display.update()
	FPSCLOCK.tick(FPS)
    