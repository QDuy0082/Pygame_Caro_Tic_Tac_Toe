import pygame, sys
from pygame.locals import *
from pygame import mixer 
from PIL import Image, ImageSequence
import math
import random

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
table_exit_width = 16*(GAPSIZE+BOXSIZE)
table_exit_heigth = 10*(GAPSIZE+BOXSIZE)
table_wrong_ans_width = 800
table_wrong_ans_height = 14*(GAPSIZE+BOXSIZE)


assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = 30
YMARGIN = 100
XMARGINWIN = int((WINDOWWIDTH - BOARDWINWIDTH*(BOXSIZE+GAPSIZE))/2)
YMARGINWIN = 200

PERU = (52, 167, 179)
GRAY = (100, 100, 100)
NAVYBLUE = ( 0, 255, 154)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
LIGHTBLUE = (0,255,255)
MIDBLUE = (30,144,255)
BLACK = (0,0,0)

RECT_COLOR = '#40FFA0'
BGCOLOR = LIGHTBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = YELLOW
color_table = WHITE

arrVocab = []
arrAns = []
wrongAns = []
pointer_wrong = 0

color_active = Color('lightskyblue3')
color_passive = (255,0,255)
clicked = False
exit = False
questions = 0


# assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."



class Gamestate():
	def __init__(self):
		self.state = 'intro'

	def intro(self):
		global scroll
		for i in range (0, til):
			DISPLAYSURF.blit(bg,(i*bg_width+scroll,0))
		
		scroll -= 0.5
		if abs(scroll) > bg_width:
			scroll =0

		theme_img.draw(DISPLAYSURF)
		start_btn_bf_img.draw(DISPLAYSURF)

		pos = pygame.mouse.get_pos()
		if start_btn_bf_img.rect.collidepoint(pos):
			start_btn_at_img.draw(DISPLAYSURF)
			if pygame.mouse.get_pressed()[0] == 1:
				pygame.display.update()
				pygame.time.wait(200)
				self.state = 'mid'

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		pygame.display.update()

	def mid(self):
		global scroll
		for i in range (0, til):
			DISPLAYSURF.blit(bg,(i*bg_width+scroll,0))
		drawboard()
		textsurface1 = textsurface('FILE CAN HOC')
		textrect1 = textrect(textsurface1)
		DISPLAYSURF.blit(textsurface1,textrect1)
		button_next_bf_img.draw(DISPLAYSURF)	
		button_back_bf_img.draw(DISPLAYSURF)
		pos = pygame.mouse.get_pos()
		if button_next_bf_img.rect.collidepoint(pos):
			button_next_at_img.draw(DISPLAYSURF)			
			if pygame.mouse.get_pressed()[0] == 1:
				readFile(f"{TEXT_1.text}")
				random.shuffle(arrVocab)
				pygame.display.update()
				pygame.time.wait(200)
				self.state = 'main_game'
		if button_back_bf_img.rect.collidepoint(pos):
			button_back_at_img.draw(DISPLAYSURF)
			if pygame.mouse.get_pressed()[0] == 1:
				pygame.display.update()
				pygame.time.wait(200)
				self.state = 'intro'
		scroll -= 0.5
		if abs(scroll) > bg_width:
			scroll = 0
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and (event.key == K_KP_ENTER or event.key==K_RETURN):
				TEXT_1.text = TEXT_1.text[:-1]
				readFile(f"{TEXT_1.text}")
				random.shuffle(arrVocab)
				pygame.display.update()
				pygame.time.wait(200)
				self.state = 'main_game'
			TEXT_1.text_event(event)
		
		TEXT_1.draw_main(RECT_TEXT)

		# display_text(DISPLAYSURF,f"{TEXT_1.text}",RECT_TEXT,base_font,BLACK,330)
		pygame.display.update()
		DISPLAYSURF.fill(BGCOLOR)
	
	def main_game(self):
		global wrongAns, arrAns, arrVocab, questions
		DISPLAYSURF.blit(bgnd,(0,0))

		

		# button_next_bf_img.draw(DISPLAYSURF)	
		# button_back_bf_img.draw(DISPLAYSURF)
		# pos = pygame.mouse.get_pos()
		# if button_next_bf_img.rect.collidepoint(pos):
		# 	button_next_at_img.draw(DISPLAYSURF)			
		# 	if pygame.mouse.get_pressed()[0] == 1:
		# 		pygame.display.update()
		# 		pygame.time.wait(200)
		# 		self.state = 'end'
		# if button_back_bf_img.rect.collidepoint(pos):
		# 	button_back_at_img.draw(DISPLAYSURF)
		# 	if pygame.mouse.get_pressed()[0] == 1:
		# 		pygame.display.update()
		# 		pygame.time.wait(200)
		# 		self.state = 'mid'
		# 		TEXT_1.reset_text()
		# 		TEXT_VOCAB.reset_text()
		# 		questions = 0
		# 		arrVocab = []
		# 		arrAns = []
		# 		wrongAns = []

		display_text(DISPLAYSURF,arrVocab[questions][1],(100,200),base_font,BLACK,800)

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and (event.key == K_KP_ENTER or event.key==K_RETURN):
				TEXT_VOCAB.text = TEXT_VOCAB.text[:-1]
				pygame.display.update()
				pygame.time.wait(200)
				if checkTrue(arrAns[arrVocab[questions][0]]) == False:
					wrongAns.append([arrVocab[questions][0],f"{TEXT_VOCAB.text}"])
				questions += 1
				if questions >= len(arrVocab):
					self.state = 'end'
				else:
					TEXT_VOCAB.reset_text()
					self.state = 'main_game'
			TEXT_VOCAB.text_event(event)
		
		TEXT_VOCAB.draw_main(RECT_TEXT_VOCAB)
		pygame.display.update()


	def end(self):
		global exit, questions, arrVocab, arrAns, wrongAns, pointer_wrong
		DISPLAYSURF.blit(bg_end,(0,0))



		exit_button_bf_img.draw(DISPLAYSURF)
		button_replay_bf_img.draw(DISPLAYSURF)


		if len(wrongAns) > 0:
			text = "Ban co " + str(len(wrongAns)) + " cau tra loi sai: "
			display_text(DISPLAYSURF,text,(200,50),base_font,BLACK,700)
			draw_table_wrong_ans()
		else:
			text = "GOOD JOB! Ban khong lam sai cau nao ca!"
			display_text(DISPLAYSURF,text,(200,200),base_font,BLACK,700)

		pos = pygame.mouse.get_pos()
		if exit_button_bf_img.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				exit_button_at_img.draw(DISPLAYSURF)
				pygame.display.update()
				pygame.time.wait(200)
				exit = True

		if button_replay_bf_img.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				button_replay_at_img.draw(DISPLAYSURF)
				pygame.display.update()
				pygame.time.wait(200)
				arrVocab = []
				arrAns = []
				wrongAns = []
				questions = 0
				TEXT_1.reset_text()
				TEXT_VOCAB.reset_text()
				self.state = 'mid'


		if exit:
			draw_table_exit()

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()


		pygame.display.update()
		FPSCLOCK.tick(FPS)

	def state_manager(self):
		if self.state == 'intro':
			self.intro()
		if self.state == 'mid':
			self.mid()
		if self.state == 'mid1' :
			self.mid1()			
		if self.state == 'main_game':
			self.main_game()
		if self.state == 'end':
			self.end()

def main():
	global DISPLAYSURF, FPSCLOCK
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF.fill(BGCOLOR)
	game_state = Gamestate()

	while True:
		game_state.state_manager()
		FPSCLOCK.tick(FPS)
		

def readFile(file_text):
	global arrVocab,arrAns
	f = open(file_text,"r")
	a = True
	count = 0
	while a:
		file_line = f.readline()
		if not file_line:
			a = False
		else:
			if count % 2 == 1:
				arrVocab.append([count//2,file_line[:-1]])
				count+=1
			else:
				arrAns.append(file_line[:-1])
				count+=1

	f.close()


def checkTrue(ans_text):
	if f"{TEXT_VOCAB.text}" == ans_text:
		return True
	return False
	
def display_text(surface, text, pos, font, color, w):
	collection = [word.split(' ') for word in text.splitlines()]
	space = font.size(' ')[0]
	x,y = pos
	for lines in collection:
		for words in lines:
			word_surface = font.render(words, True, color)
			word_width , word_height = word_surface.get_size()
			if x + word_width >= w + int((WINDOWWIDTH - w)/2):
				x = pos[0]
				y += word_height
			surface.blit(word_surface, (x,y))
			x += word_width + space
		x = pos[0]
		y += word_height		

def draw_table_exit():
	global exit
	pygame.draw.rect(DISPLAYSURF,color_table,RECT_TABLE_EXIT)
	text = "Ban co chac thoat khoi chuong trinh hay khong?"
	display_text(DISPLAYSURF,text,(int((WINDOWWIDTH - table_exit_width)/2)+40,int((WINDOWHEIGHT - table_exit_heigth)/2)+50),base_font,BLACK,table_exit_width)
	button_yes_bf_img.draw(DISPLAYSURF)
	button_no_bf_img.draw(DISPLAYSURF)
	pos = pygame.mouse.get_pos()
	if button_yes_bf_img.rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == 1:
			button_yes_at_img.draw(DISPLAYSURF)
			pygame.display.update()
			pygame.time.wait(200)
			pygame.quit()
			sys.exit()

	if button_no_bf_img.rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == 1:
			button_no_at_img.draw(DISPLAYSURF)
			pygame.display.update()
			pygame.time.wait(200)
			exit = False
 
def draw_table_wrong_ans():
	global pointer_wrong, wrongAns
	pos_x = int((WINDOWWIDTH - table_wrong_ans_width)/2)+40
	pos_y = int((WINDOWHEIGHT - table_wrong_ans_height)/2)-50+30

	pygame.draw.rect(DISPLAYSURF,color_table,RECT_TABLE_WRONG_ANS)

	text = "Cau tra loi cua ban la: "
	display_text(DISPLAYSURF,text,(pos_x,pos_y),base_font,BLACK,table_wrong_ans_width)
	display_text(DISPLAYSURF,wrongAns[pointer_wrong][1],(pos_x + 50,pos_y + 33),base_font,BLACK,650)

	text = "Cau tra loi dung la: "
	display_text(DISPLAYSURF,text,(pos_x, pos_y+ 2*33),base_font,BLACK,700)
	display_text(DISPLAYSURF,arrAns[wrongAns[pointer_wrong][0]],(pos_x + 50, pos_y+ 3*33),base_font,BLACK,650)
	
	button_end_back_bf_img.draw(DISPLAYSURF)
	button_end_next_bf_img.draw(DISPLAYSURF)
	pos = pygame.mouse.get_pos()

	if button_end_back_bf_img.rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == 1:
			button_end_back_at_img.draw(DISPLAYSURF)
			if pointer_wrong > 0:
				pointer_wrong -=1
			pygame.display.update()
			pygame.time.wait(200)
			

	if button_end_next_bf_img.rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == 1:
			button_end_next_at_img.draw(DISPLAYSURF)
			if pointer_wrong < len(wrongAns)-1:
				pointer_wrong +=1
			pygame.display.update()
			pygame.time.wait(200)



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
				button_sound.play()
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))

class text():
	def __init__(self,width,height,pos,size):
		self.width = 140
		self.height = 38
		self.rect_text = pygame.Rect(pos,(self.width,self.height))
		self.text = ''
		self.active = False
		self.color = RECT_COLOR
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

	def draw_main(self,pos_main):

		global color_text
		if self.active:
			self.color = Color('#00A552')
			color_text = WHITE
		else:
			self.color = RECT_COLOR
			color_text = BLACK
		self.rect_text.x = pos_main[0]
		self.rect_text.y = pos_main[1]

		self.text_rect = self.text_surface.get_rect(center = self.rect_text.center)
		self.text_rect.center = self.rect_text.center

		pygame.draw.rect(DISPLAYSURF,self.color,self.rect_text,border_radius = 2)

		self.text_surface = base_font.render(self.text,True,color_text)
		DISPLAYSURF.blit(self.text_surface,self.text_rect)
		self.rect_text.w = max(self.original_size_text,self.text_surface.get_width()+25)

	def reset_text(self):
		self.rect_text.x = self.pos_original[0]
		self.rect_text.y = self.pos_original[1]
		self.text = ''

def drawboard():
	pygame.draw.rect(DISPLAYSURF,BLACK ,(245,175,510,300),border_radius = 0)
	pygame.draw.rect(DISPLAYSURF,'#F0F8FF' ,(250,180,480,270),border_radius = 0)


def textsurface(chu) :
	fontObj = pygame.font.Font('freesansbold.ttf', 35)
	reat= pygame.draw.rect(DISPLAYSURF,'#F0F8FF' ,(250,180,480,270),border_radius = 0)
	x,y = reat.center
	textSurfaceObj = fontObj.render(chu, True, BLACK)
	return textSurfaceObj
 
def textrect(textSurfaceObj) :
     reat=pygame.draw.rect(DISPLAYSURF,'#F0F8FF' ,(250,180,500,290),border_radius = 0)
     x,y = reat.center
     textRectObj=textSurfaceObj.get_rect()
     textRectObj.center=x,220
     return textRectObj	



DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('vocab')


# gui_font = pygame.font.Font(None,70)

base_font = pygame.font.SysFont("Cambria Math",32)

TEXT_1 = text(150,56,(338,280),330)
TEXT_VOCAB = text(WINDOWWIDTH-200,56,(100,280),800)
RECT_TEXT = (338,280)
RECT_TEXT_VOCAB = (100,280)


RECT_TABLE_EXIT = pygame.Rect(int((WINDOWWIDTH - table_exit_width)/2),int((WINDOWHEIGHT - table_exit_heigth)/2),table_exit_width,table_exit_heigth)
RECT_TABLE_WRONG_ANS = pygame.Rect(int((WINDOWWIDTH - table_wrong_ans_width)/2),int((WINDOWHEIGHT - table_wrong_ans_height)/2)-50,table_wrong_ans_width,table_wrong_ans_height)





bg = pygame.image.load('bg.png').convert()
theme_img = pygame.image.load('theme.png').convert_alpha()
theme_img = Button(218, 80, theme_img, 0.65)
button_sound = pygame.mixer.Sound('button-25.wav')
warning_sound = pygame.mixer.Sound('warning.wav')
victory_sound = pygame.mixer.Sound('Victory_sound.wav')
#button intro
start_btn_bf = pygame.image.load('start_btn_bf.png').convert_alpha()
start_btn_at = pygame.image.load('start_btn_at.png').convert_alpha()
start_btn_at_img = Button(int((WINDOWWIDTH - start_btn_at.get_width())/2),int(2*WINDOWHEIGHT/3), start_btn_at, 1)
start_btn_bf_img = Button(int((WINDOWWIDTH - start_btn_bf.get_width())/2),int(2*WINDOWHEIGHT/3), start_btn_bf, 1)

#button mid
button_next_bf = pygame.image.load('next.png').convert_alpha()
button_next_bf_img = Button(530,340,button_next_bf,0.4)
button_back_bf = pygame.image.load('back.png').convert_alpha()
button_back_bf_img = Button(280,340,button_back_bf,0.4)
button_next_at = pygame.image.load('next1.png').convert_alpha()
button_next_at_img = Button(530,340,button_next_at,0.4)
button_back_at = pygame.image.load('back1.png').convert_alpha()
button_back_at_img = Button(280,340,button_back_at,0.4)


#button main_game

#button end
exit_button_bf = pygame.image.load('exit_button_bf.png').convert_alpha()
exit_button_at = pygame.image.load('exit_button_at.png').convert_alpha()
exit_button_bf_img = Button(int(5*WINDOWWIDTH/6)-exit_button_bf.get_width(),int(5*WINDOWHEIGHT/7),exit_button_bf,1)
exit_button_at_img = Button(int(5*WINDOWWIDTH/6)-exit_button_at.get_width()-2,int(5*WINDOWHEIGHT/7)+3,exit_button_at,1)

button_replay_bf = pygame.image.load('button_replay_bf.png').convert_alpha()
button_replay_at = pygame.image.load('button_replay_at.png').convert_alpha()
button_replay_bf_img = Button(int(WINDOWWIDTH/6),int(5*WINDOWHEIGHT/7),button_replay_bf,1)
button_replay_at_img = Button(int(WINDOWWIDTH/6)+3,int(5*WINDOWHEIGHT/7)+3,button_replay_at,1)

button_yes_bf = pygame.image.load('button_yes_bf.png').convert_alpha()
button_yes_at = pygame.image.load('button_yes_at.png').convert_alpha()
button_yes_bf_img = Button(int((WINDOWWIDTH - table_exit_width)/2) + 50,table_exit_heigth + int((WINDOWHEIGHT - table_exit_heigth)/2) - 100,button_yes_bf,1)
button_yes_at_img = Button(int((WINDOWWIDTH - table_exit_width)/2) + 52,table_exit_heigth + int((WINDOWHEIGHT - table_exit_heigth)/2) - 97 ,button_yes_at,1)

button_no_bf = pygame.image.load('button_no_bf.png').convert_alpha()
button_no_at = pygame.image.load('button_no_at.png').convert_alpha()
button_no_bf_img = Button(int((WINDOWWIDTH - table_exit_width)/2) + table_exit_width - 50 - button_no_bf.get_width() ,table_exit_heigth + int((WINDOWHEIGHT - table_exit_heigth)/2) - 100,button_no_bf,1)
button_no_at_img = Button(int((WINDOWWIDTH - table_exit_width)/2) + table_exit_width - 51 - button_no_at.get_width(),table_exit_heigth + int((WINDOWHEIGHT - table_exit_heigth)/2) - 97 ,button_no_at,1)

button_end_back_bf_img = Button(int((WINDOWWIDTH - table_wrong_ans_width)/2) + 50,table_wrong_ans_height + int((WINDOWHEIGHT - table_wrong_ans_height)/2) - 100 -50,button_back_bf,0.3)
button_end_back_at_img = Button(int((WINDOWWIDTH - table_wrong_ans_width)/2) + 52,table_wrong_ans_height + int((WINDOWHEIGHT - table_wrong_ans_height)/2) - 97 -50,button_back_at,0.3)

button_end_next_bf_img = Button(int((WINDOWWIDTH - table_wrong_ans_width)/2) + table_wrong_ans_width + 280 - button_next_bf.get_width() ,table_wrong_ans_height + int((WINDOWHEIGHT - table_wrong_ans_height)/2) - 100 -50,button_next_bf,0.3)
button_end_next_at_img = Button(int((WINDOWWIDTH - table_wrong_ans_width)/2) + table_wrong_ans_width + 281 - button_next_at.get_width(),table_wrong_ans_height + int((WINDOWHEIGHT - table_wrong_ans_height)/2) - 97 -50,button_next_at,0.3)



bg_width =  bg.get_width()
scroll = 0
til = math.ceil(WINDOWWIDTH/bg_width)+1
font = pygame.font.SysFont(None, 70)

win_sound = pygame.mixer.Sound('button-25.wav')
currentFrame = 0
color_text = WHITE
bgnd = pygame.image.load('bgnd.jpg').convert()
bg_end = pygame.image.load('bg_end.png').convert()


if __name__ == '__main__':
	main()