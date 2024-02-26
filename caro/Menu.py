import pygame,sys
from pygame import mixer 
from pygame import *
import button
import math
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1000

pygame.init()
pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Menu caro')

start_btn_bf = pygame.image.load('start_btn_bf.png').convert_alpha()
start_btn_at = pygame.image.load('start_btn_at.png').convert_alpha()
bg = pygame.image.load('bg.jpg').convert()
theme_img = pygame.image.load('theme.png').convert_alpha()
theme_img = button.Button(150, 80, theme_img, 0.65)
button_sound = pygame.mixer.Sound('button-25.wav')
start_btn_at_img = button.Button(338, 296, start_btn_at, 0.97)
start_btn_bf_img = button.Button(330, 400, start_btn_bf, 0.3)

#Background/Backgroundmusic
clock = pygame.time.Clock()
bg_width =  bg.get_width()
FPS = 60
scroll = 0
til = math.ceil(SCREEN_WIDTH/bg_width)+1
mixer.music.load('Bgmusic.wav')
mixer.music.play(-1)

class Button_intro():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int (width * scale), int (height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()
		pygame.draw.rect(screen, self.top_color, self.rect)
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
		 	self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))
		self.check_clicked()

		return action

#Bắt đầu chạy			

while True:
	clock.tick(FPS)
	screen.fill((202, 228,  241))


	for i in range (0, til):
		screen.blit(bg,(i*bg_width+scroll,0))

	theme_img.draw(screen)
	start_btn_bf_img.draw(screen)

	pos = pygame.mouse.get_pos()
	if start_btn_bf_img.rect.collidepoint(pos):
		if start_btn_at_img.draw(screen):
			button_sound.play()
			print("Helloooo")
	 		#Qua trang tiếp theo

	scroll -= 0.5
	if abs(scroll) > bg_width:
		scroll =0
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()


	pygame.display.update()
