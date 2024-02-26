import pygame, sys
from pygame import *

pygame.init()
w=1000
h=700
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()


base_font = pygame.font.Font(None,32)
user_text = ''

win_font = pygame.font.Font(None,70)

BLACK = (0,0,0)
WHITE = (255,255,255)

YELLOW = (255,215,0)
LIGHTGREEN = (124,252,0)

MIDBLUE = (30,144,255)
BGCOLOR = MIDBLUE

color_win = (YELLOW,LIGHTGREEN)


input_rect = pygame.Rect(200,200,140,32)
color_active = Color('lightskyblue3')
color_passive = Color('gray15')
d = 0


active = False

col_spd = 5
col_dir = [1,1,1]
def_col = [50,50,50]

minimum = 0
maximun = 255


def draw_text(text,size,col,x,y):
	font = pygame.font.Font(None,size)
	text_surface = font.render(text,True,col)
	screen.blit(text_surface,(x,y))

def col_change(col,direct):
	for i in range(3):
		col[i] = ((col[i]+col_spd*direct[i]) + 255) % 255


class Button():
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
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
		 	self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


while True:
	screen.fill(BGCOLOR)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	draw_text("CHIEN THANG",70,YELLOW,80,50)
	draw_text("X chien thang",50,def_col,120,100)
	col_change(def_col,col_dir)


	pygame.display.update()
	clock.tick(60)