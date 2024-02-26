import pygame, sys
from pygame import *

shape = ('X','O')

def button(width,height,iconsize,pos,elevation,count):
	pressed = False
	dynamic_elevation = 0
	original_x_pos = pos[0]
	original_y_pos = pos[1]
	original_top_rect_width = width
	original_top_rect_height = height


	top_rect = pygame.Rect(pos,(width,height))
	top_color = '#475F77'

	top_rect.x = original_x_pos + dynamic_elevation
	top_rect.y = original_y_pos + dynamic_elevation

	top_rect.height = original_top_rect_height - 2*dynamic_elevation
	top_rect.width = original_top_rect_width - 2*dynamic_elevation

	text = shape[count]
	pygame.draw.rect(screen,top_color,top_rect)