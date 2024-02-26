import pygame, sys
from pygame.locals import *
from pygame import mixer 
import math

pygame.init()



FPS = 120
WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
BOXSIZE = 25
GAPSIZE = 2
BOARDWIDTH = 20
BOARDHEIGHT = 20
BOARDWINWIDTH = 5
BOARDWINHEIGHT = 5
ICONSIZE = 5


class text():
	def __init__(self,width,height,pos,size):
		self.rect_text = pygame.Rect(pos,(width,height))
		self.text = ''
		self.active = False
		self.color = (255,0,255)
		self.original_size_text = size
		self.text_surface = base_font.render(self.text,True,WHITE)
		self.count = 0
		self.pos_original = pos

		self.text_rect = self.text_surface.get_rect(center = self.rect_text.center)

	def text_event(self,EVENT):
		global button_sound
		if EVENT.type == MOUSEBUTTONDOWN:
			if self.rect_text.collidepoint(EVENT.pos):
				self.active = True
				self.count+=1
				if self.count==1:
					self.text = self.text + '|'
				button_sound.play()
			else:
				self.active = False
				self.text = ''.join(self.text.split('|'))
				self.count = 0
				button_sound.play()
		if self.active == True:
			if EVENT.type == KEYDOWN:
				if EVENT.key == K_BACKSPACE:
					self.text = ''.join(self.text.split('|'))
					self.text = self.text[:-1] + '|'
				elif EVENT.key == K_RETURN:
					button_sound.play()
					self.active = False
					self.text = ''.join(self.text.split('|'))
					self.count = 0
				else:
					self.text = ''.join(self.text.split('|'))
					self.text += EVENT.unicode +'|'

	def draw(self):
		if self.active:
			self.color = Color('lightskyblue3')
		else:
			self.color = (255,0,255)

		pygame.draw.rect(DISPLAYSURF,self.color,(self.rect_text.x,self.rect_text.y,self.rect_text.w-20,self.rect_text.h))
		pygame.draw.rect(DISPLAYSURF,self.color,self.rect_text,border_radius = 12)

		self.text_surface = base_font.render(self.text,True,WHITE)

		DISPLAYSURF.blit(self.text_surface,(self.rect_text.x+13,self.rect_text.y))
		self.rect_text.w = max(self.original_size_text,self.text_surface.get_width()+25)

	def draw_main(self,pos_main):

		self.rect_text.x = pos_main[0]
		self.rect_text.y = pos_main[1]

		self.text_rect = self.text_surface.get_rect(center = self.rect_text.center)
		self.text_rect.center = self.rect_text.center


		pygame.draw.rect(DISPLAYSURF,self.color,self.rect_text,border_radius = 12)

		self.text_surface = base_font.render(self.text,True,WHITE)
		DISPLAYSURF.blit(self.text_surface,self.text_rect)
		self.rect_text.w = max(self.original_size_text,self.text_surface.get_width()+25)

	def animation_text(self):
		

	def reset_text(self):
		self.rect_text.x = self.pos_original[0]
		self.rect_text.y = self.pos_original[1]
		self.text = ''

