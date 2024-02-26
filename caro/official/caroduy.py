import pygame, sys, cv2, numpy
from pygame.locals import *
from pygame import mixer 
from PIL import Image, ImageSequence
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
table_exit_width = 16*(GAPSIZE+BOXSIZE)
table_exit_heigth = 10*(GAPSIZE+BOXSIZE)

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = 30
YMARGIN = 100
XMARGINWIN = int((WINDOWWIDTH - BOARDWINWIDTH*(BOXSIZE+GAPSIZE))/2)
YMARGINWIN = 200


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

RECT_COLOR = '#6666FF'
BGCOLOR = LIGHTBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = YELLOW
color_table = WHITE

X = 'x'
O = 'o'
RECT = 'rect'

ALLCOLORS = (RED, BLUE)
ALLSHAPES = (X,O)
win = []
arr_pos = []

color_active = Color('lightskyblue3')
color_passive = (255,0,255)
color_win = YELLOW
clicked = False
exit = False


# assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."



class Gamestate():
	def __init__(self):
		self.state = 'intro'

	def intro(self):
		global scroll
		for i in range (0, til):
			DISPLAYSURF.blit(bg,(i*bg_width+scroll,0))

		theme_img.draw(DISPLAYSURF)
		start_btn_bf_img.draw(DISPLAYSURF)

		pos = pygame.mouse.get_pos()
		if start_btn_bf_img.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				start_btn_at_img.draw(DISPLAYSURF)
				pygame.display.update()
				pygame.time.wait(200)
				self.state = 'mid'

		scroll -= 0.5
		if abs(scroll) > bg_width:
			scroll =0
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		pygame.display.update()

	def mid(self):
		global scroll
		for i in range (0, til):
			DISPLAYSURF.blit(bg,(i*bg_width+scroll,0))


		button_next_bf_img.draw(DISPLAYSURF)

		pos = pygame.mouse.get_pos()
		if button_next_bf_img.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				button_next_at_img.draw(DISPLAYSURF)
				pygame.display.update()
				pygame.time.wait(200)
				self.state = 'main_game'

		scroll -= 0.5
		if abs(scroll) > bg_width:
			scroll =0
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			TEXT_1.text_event(event)
			TEXT_2.text_event(event)

		TEXT_1.draw()
		TEXT_2.draw()


		pygame.display.update()

	def main_game(self):
		global mousex, mousey, count, win, arr_pos, clicked, text, text_rect, counter
		mixer.music.stop()
		mouseClick = False
		DISPLAYSURF.blit(bgnd,(0,0))
		return_button_bf_img.draw(DISPLAYSURF)

		pos = pygame.mouse.get_pos()
		if return_button_bf_img.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
				return_button_at_img.draw(DISPLAYSURF)
				pygame.display.update()
				if len(arr_pos)>0:
					count-=1
					mainboard[arr_pos[count][0]][arr_pos[count][1]] = RECT
					markedBoxes[arr_pos[count][0]][arr_pos[count][1]] = False
					arr_pos.pop()
					clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False

		pygame.draw.rect(DISPLAYSURF,BLACK,(XMARGIN-GAPSIZE, YMARGIN-GAPSIZE, BOARDWIDTH*(BOXSIZE+GAPSIZE)+GAPSIZE, BOARDHEIGHT*(BOXSIZE+GAPSIZE)+GAPSIZE))
		#drawArcCv2(DISPLAYSURF,BLUE,(30,30),100,10,360)
		drawBoard(mainboard, markedBoxes)
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClick = True
			if event.type == timer_event:
				counter -= 1
				text = font.render(str(counter), True, '#803945')
				text_rect = text.get_rect(center = (XMARGIN+22*(BOXSIZE+GAPSIZE)+160,YMARGIN+15*(BOXSIZE+GAPSIZE)+50))
				if counter == 0:
					text = font.render("Time out!", True, (0,128,0)) 
					text_rect = text.get_rect(center = (XMARGIN+22*(BOXSIZE+GAPSIZE)+160,YMARGIN+15*(BOXSIZE+GAPSIZE)+50))
					DISPLAYSURF.blit(text, text_rect)
					pygame.display.update()
					pygame.time.wait(2000)				
					self.state='end'
		DISPLAYSURF.blit(text, text_rect)
		if counter > 5: color = BLACK
		elif counter > 0: 
			warning_sound.play()
			color = RED
		if counter > 0: drawArcCv2(DISPLAYSURF, color, (XMARGIN+22*(BOXSIZE+GAPSIZE)+160,YMARGIN+15*(BOXSIZE+GAPSIZE)+50), 60, 9, -360*counter/60)
		TEXT_1.draw_main(RECT_TEXT_1)
		TEXT_2.draw_main(RECT_TEXT_2)
		#pygame.draw.rect(DISPLAYSURF, GRAY, RECT_CLOCK)




		boxx,boxy = getBoxAtPixel(mousex,mousey)
		if boxx != None and boxy != None:
			drawHightlightBox(boxx,boxy,mainboard,markedBoxes,HIGHLIGHTCOLOR,2)
			if not markedBoxes[boxx][boxy] and mouseClick:
				if count >= 0:
					counter = 60
					text = font.render(str(counter), True, '#803945')
					text_rect = text.get_rect(center = (XMARGIN+22*(BOXSIZE+GAPSIZE)+160,YMARGIN+15*(BOXSIZE+GAPSIZE)+50))
					mainboard[boxx][boxy] = ALLSHAPES[count % 2]
					button_sound.play()
					drawIcon(ALLSHAPES[count % 2],boxx,boxy,0,0)
					markedBoxes[boxx][boxy]=True
					arr_pos.append([boxx,boxy])
					if checkwin(mainboard,boxx,boxy,ALLSHAPES[count % 2]) == 1:
						print("win")
						for i in range(5):
							drawHightlightBox(win[i][0],win[i][1],mainboard,markedBoxes,color_win,0)
							pygame.display.update()
						pygame.time.wait(3000)
						self.state = 'end'
				if counter > 0: 
					count += 1
			if counter == 0: 
				count = -1
				
		pygame.display.update()


	def end(self):
		global scroll,win,mainboard,markedBoxes, exit, count, arr_pos, currentFrame, counter
		# for i in range (0, til):
		# 	DISPLAYSURF.blit(bg_win,(i*bg_width+scroll,0))
		# scroll -= 0.5
		# if abs(scroll) > bg_width:
		# 	scroll =0
		DISPLAYSURF.blit(bg_end,(0,0))
		victory_sound.play()
		winner_font_1 = pygame.font.SysFont('ALGERIAN',90)
		winner_font_2 = pygame.font.SysFont('Cambria Math',120,True)
		winner_text_1 = winner_font_1.render("THE WINNER IS", True, BLACK)
		if ALLSHAPES[(count+1) % 2]=='x':
			winner_text_2 = winner_font_2.render(f"{TEXT_1.text}", True, BLACK)
		else:
			winner_text_2 = winner_font_2.render(f"{TEXT_2.text}", True, BLACK)
		winner_text_1_rect = winner_text_1.get_rect(center=(WINDOWWIDTH/2,200))
		winner_text_2_rect = winner_text_2.get_rect(center=(WINDOWWIDTH/2,350))
		DISPLAYSURF.blit(winner_text_1,winner_text_1_rect)
		DISPLAYSURF.blit(winner_text_2,winner_text_2_rect)

		#drawBoardWin(mainboard,markedBoxes,BOARDWINWIDTH,BOARDWINHEIGHT,win[0][0],min(win[0][1],win[4][1]))
		rect = gifFrameList[currentFrame].get_rect(center = (250, 250))
		DISPLAYSURF.blit(gifFrameList[currentFrame], rect)
		rect = gifFrameList[currentFrame].get_rect(center = (750, 250))
		DISPLAYSURF.blit(gifFrameList[currentFrame], rect)
		currentFrame = (currentFrame + 1) % len(gifFrameList)

		exit_button_bf_img.draw(DISPLAYSURF)
		button_replay_bf_img.draw(DISPLAYSURF)
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
				win = []
				arr_pos = []
				mainboard = getBoard()
				markedBoxes = generateMarkedBoxesData(False)
				count=0
				counter=60
				TEXT_1.reset_text()
				TEXT_2.reset_text()
				self.state = 'intro'

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
		if self.state == 'main_game':
			self.main_game()
		if self.state == 'end':
			self.end()

def main():
	global DISPLAYSURF, FPSCLOCK, input_rect
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF.fill(BGCOLOR)
	game_state = Gamestate()

	while True:
		game_state.state_manager()
		FPSCLOCK.tick(FPS)
		

def generateMarkedBoxesData(val):
	result = []
	for i in range(BOARDWIDTH):
		result.append([val]*BOARDHEIGHT)
	return result


def getBoard():
	board = []
	for i in range(BOARDWIDTH):
		board.append([RECT]*BOARDHEIGHT)
	return board



def leftTopCoordsOfBox(boxx,boxy):
	left = boxx*(BOXSIZE + GAPSIZE) + XMARGIN
	top = boxy*(BOXSIZE + GAPSIZE) + YMARGIN
	return (left, top)

def leftTopCoordsOfBoxWin(boxx,boxy):
	left = boxx*(BOXSIZE + GAPSIZE) + XMARGINWIN
	top = boxy*(BOXSIZE + GAPSIZE) + YMARGINWIN
	return (left, top)

def getBoxAtPixel(x,y):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left, top = leftTopCoordsOfBox(boxx,boxy)
			boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
			if boxRect.collidepoint(x,y):
				return (boxx,boxy)
	return (None,None)

def getShapeAndColor(board, boxx, boxy):
	return board[boxx][boxy]

def drawHightlightBox(boxx,boxy,board,revealedBoxes,color,elevation):
	left, top = leftTopCoordsOfBox(boxx,boxy)
	pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
	pygame.draw.rect(DISPLAYSURF,color,(left+elevation,top+elevation,BOXSIZE-2*elevation,BOXSIZE-2*elevation))
	if revealedBoxes[boxx][boxy]:
		shape = getShapeAndColor(board,boxx,boxy)
		drawIcon(shape,boxx,boxy,elevation,0)

def drawHightlightBoxWin(boxx,boxy,shape,color,pos_x,pos_y):
	left, top = leftTopCoordsOfBoxWin(boxx,boxy)
	pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
	pygame.draw.rect(DISPLAYSURF,color,(left,top,BOXSIZE,BOXSIZE))
	drawIcon(shape,boxx,boxy,0,1)

def drawBoard(board,revealedBoxes):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left,top = leftTopCoordsOfBox(boxx,boxy)
			if not revealedBoxes[boxx][boxy]:
				pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
			else:
				pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
				shape = getShapeAndColor(board,boxx,boxy)
				drawIcon(shape,boxx,boxy,0,0)

def drawBoardWin(board,revealedBoxes,width,height,pos_x,pos_y):
	global win
	for boxx in range(width):
		for boxy in range(height):
			left,top = leftTopCoordsOfBoxWin(boxx,boxy)
			if not revealedBoxes[pos_x+boxx][pos_y+boxy]:
				pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
			else:
				pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
				shape = getShapeAndColor(board,boxx+pos_x,boxy+pos_y)
				drawIcon(shape,boxx,boxy,0,1)
				if [boxx+pos_x,boxy+pos_y] in win:
					drawHightlightBoxWin(boxx,boxy,shape,color_win,pos_x,pos_y)

def draw_line_round_corners_polygon(surf, p1, p2, c, w):
	p1v = pygame.math.Vector2(p1)
	p2v = pygame.math.Vector2(p2)
	lv = (p2v - p1v).normalize()
	lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
	pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
	pygame.draw.polygon(surf, c, pts)
	pygame.draw.circle(surf, c, p1, round(w / 2))
	pygame.draw.circle(surf, c, p2, round(w / 2))

def drawIcon(shape, boxx, boxy, elevation, win):
	half = int(BOXSIZE * 0.5)
	if win==1:
		left, top = leftTopCoordsOfBoxWin(boxx, boxy)
	else:
		left, top = leftTopCoordsOfBox(boxx,boxy)

 	#pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
	if shape == O:
		pygame.draw.circle(DISPLAYSURF, BLUE, (left + half, top + half), half - elevation - 3,4)
	elif shape == X:
		draw_line_round_corners_polygon(DISPLAYSURF, (left + ICONSIZE + elevation, top + ICONSIZE + elevation), (left + BOXSIZE - ICONSIZE - elevation - 1, top + BOXSIZE - ICONSIZE - elevation - 1),RED,5)
		draw_line_round_corners_polygon(DISPLAYSURF, (left + ICONSIZE + elevation, top + BOXSIZE - ICONSIZE - elevation - 1), (left + BOXSIZE - ICONSIZE - elevation - 1, top + ICONSIZE + elevation), RED,5)

def checkwin(board,x,y,shape):
	#check row
	global win
	d = 0
	for i in range(BOARDWIDTH):
		if board[i][y]==shape:
			d+=1
			if d==5:
				if i-4 > 0 and i < BOARDWIDTH-1 and board[i-5][y] == board[i+1][y] and board[i-5][y] != shape and board[i-5][y] in ALLSHAPES:
					d = 0
				else:
					for j in range(i-4,i+1):
						win.append([j,y])
					return 1
		else:
			d=0

	#check column
	d=0
	for i in range(BOARDHEIGHT):
		if board[x][i] == shape:
			d+=1
			if d==5:
				if i-4 > 0 and i < BOARDHEIGHT-1 and board[x][i-5] == board[x][i+1] and board[x][i-5] != shape and board[x][i-5] in ALLSHAPES:
					d = 0
				else:
					for j in range(i-4,i+1):
						win.append([x,j])
					return 1
		else:
			d=0

	#check diagonal
	min_left_top = min(x,y)
	min_right_bottom = min(BOARDWIDTH - x-1, BOARDHEIGHT - y-1)
	min_left_bottom = min(x,BOARDHEIGHT-y-1)
	min_right_top = min(BOARDWIDTH - x-1, y)
	#left
	d=0
	x_axis = x - min_left_top
	y_axis = y - min_left_top
	for i in range(min_left_top+min_right_bottom+1):
		if board[x_axis+i][y_axis+i] == shape:
			d+=1
			if d== 5:
				
				if i-4 > 0 and  i < min_left_top+min_right_bottom and board[x_axis+i-5][y_axis+i-5] == board[x_axis+i+1][y_axis+i+1] and board[x_axis+i-5][y_axis+i-5] != shape and board[x_axis+i-5][y_axis+i-5] in ALLSHAPES:
					d = 0
				else:
					for j in range(i-4,i+1):
						win.append([x_axis+j,y_axis+j])
					return 1
		else:
			d=0
	#right
	d=0
	x_axis = x - min_left_bottom
	y_axis = y + min_left_bottom
	for i in range(min_left_bottom+min_right_top+1):
		if board[x_axis+i][y_axis-i] == shape:
			d+=1
			if d == 5:
				if i-4 > 0 and  i < min_left_bottom+min_right_top and board[x_axis+i-5][y_axis-(i-5)] == board[x_axis+i+1][y_axis-(i+1)] and board[x_axis+i-5][y_axis-(i-5)] != shape and board[x_axis+i-5][y_axis-(i-5)] in ALLSHAPES:
					d = 0
				else:
					for j in range(i-4,i+1):
						win.append([x_axis+j,y_axis-j])
					return 1
		else:
			d=0
	return 0

def drawArcCv2(surf, color, center, radius, width, end_angle):
	circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
	circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
		(radius-width//2, radius-width//2), 0, 0, end_angle, (*color, 255), width, lineType=cv2.LINE_AA) 
	circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
	surf.blit(circle_surface, circle_surface.get_rect(center = center))

def display_text(surface, text, pos, font, color):
	collection = [word.split(' ') for word in text.splitlines()]
	space = font.size(' ')[0]
	x,y = pos
	for lines in collection:
		for words in lines:
			word_surface = font.render(words, True, color)
			word_width , word_height = word_surface.get_size()
			if x + word_width >= table_exit_width + int((WINDOWWIDTH - table_exit_width)/2):
				x = pos[0]
				y += word_height
			surface.blit(word_surface, (x,y))
			x += word_width + space
		x = pos[0]
		y += word_height		

def draw_table_exit():
	global exit, scroll
	for i in range (0, til):
		DISPLAYSURF.blit(bg_win,(i*bg_width+scroll,0))
	scroll -= 0.5
	if abs(scroll) > bg_width:
		scroll =0
	pygame.draw.rect(DISPLAYSURF,color_table,RECT_TABLE_EXIT)
	text = "Ban co chac thoat khoi chuong trinh hay khong?"
	display_text(DISPLAYSURF,text,(int((WINDOWWIDTH - table_exit_width)/2)+40,int((WINDOWHEIGHT - table_exit_heigth)/2)+50),base_font,BLACK)
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

def pilImageToSurface(pilImage):
	mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
	return pygame.image.fromstring(data, size, mode).convert_alpha()

def loadGIF(filename):
	pilImage = Image.open(filename)
	frames = []
	if pilImage.format == 'GIF' and pilImage.is_animated:
		for frame in ImageSequence.Iterator(pilImage):
			pygameImage = pilImageToSurface(frame.convert('RGBA'))
			frames.append(pygameImage)
	else:
		frames.append(pilImageToSurface(pilImage))
	return frames
				

# class BUTTON():
# 	def __init__(self,text,width,height,pos,elevation):
# 		self.pressed = False
# 		self.elevation = elevation
# 		self.dynamic_elevation = elevation
# 		self.original_y_pos = pos[1]

# 		self.top_rect = pygame.Rect(pos,(width,height))   #
# 		self.top_color = '#475F77'

# 		self.bottom_rect = pygame.Rect(pos,(width,elevation))   #
# 		self.bottom_color = '#354B5E'

# 		self.text_surface = gui_font.render(text,True,'#FFFFFF')	 #
# 		self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)  #

# 	def draw(self):
# 		self.top_rect.y = self.original_y_pos - self.dynamic_elevation   #
# 		self.text_rect.center = self.top_rect.center	#

# 		self.bottom_rect.midtop = self.top_rect.midtop
# 		self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

# 		pygame.draw.rect(DISPLAYSURF,self.bottom_color,self.bottom_rect,border_radius = 12)
# 		pygame.draw.rect(DISPLAYSURF,self.top_color,self.top_rect,border_radius = 12)
# 		DISPLAYSURF.blit(self.text_surface,self.text_rect)
# 		self.check_click()

# 	def check_click(self):
# 		mouse_pos = pygame.mouse.get_pos()
# 		if self.top_rect.collidepoint(mouse_pos):
# 			self.top_color = '#D74B4B'
# 			if pygame.mouse.get_pressed()[0]:
# 				self.dynamic_elevation = 0
# 				self.pressed = True
# 			else:
# 				if self.pressed == True:
# 					print('Click')
# 					self.pressed = False
# 				self.dynamic_elevation = self.elevation
# 		else:
# 			self.top_color = '#475F77'
# 		return self.pressed



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
		self.rect_text = pygame.Rect(pos,(width,height))
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

	def draw(self):
		if self.active:
			self.color = Color('#00CC66')
		else:
			self.color = RECT_COLOR

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

	def reset_text(self):
		self.rect_text.x = self.pos_original[0]
		self.rect_text.y = self.pos_original[1]
		self.text = ''



DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
mousex = 0
mousey = 0
count = 0
save_boxx = 0
save_boxy = 0
pygame.display.set_caption('caro')
mainboard = getBoard()
markedBoxes = generateMarkedBoxesData(False)

# gui_font = pygame.font.Font(None,70)

base_font = pygame.font.SysFont("Cambria Math",32)

TEXT_1 = text(140,46,(338,260),320)
TEXT_2 = text(140,46,(338,380),320)

RECT_CLOCK = pygame.Rect(XMARGIN+22*(BOXSIZE+GAPSIZE),YMARGIN-(BOXSIZE+GAPSIZE),100,100)
RECT_TEXT_1 = (XMARGIN+22*(BOXSIZE+GAPSIZE),YMARGIN+4*(BOXSIZE+GAPSIZE))
RECT_TEXT_2 = (XMARGIN+22*(BOXSIZE+GAPSIZE),YMARGIN+10*(BOXSIZE+GAPSIZE))
RECT_TABLE_EXIT = pygame.Rect(int((WINDOWWIDTH - table_exit_width)/2),int((WINDOWHEIGHT - table_exit_heigth)/2),table_exit_width,table_exit_heigth)





bg = pygame.image.load('bg.jpg').convert()
theme_img = pygame.image.load('theme.png').convert_alpha()
theme_img = Button(150, 80, theme_img, 0.65)
button_sound = pygame.mixer.Sound('button-25.wav')
warning_sound = pygame.mixer.Sound('warning.wav')
victory_sound = pygame.mixer.Sound('Victory_sound.wav')
#button intro
start_btn_bf = pygame.image.load('start_btn_bf.png').convert_alpha()
start_btn_at = pygame.image.load('start_btn_at.png').convert_alpha()
start_btn_at_img = Button(int((WINDOWWIDTH - start_btn_at.get_width())/2)+1,int(2*WINDOWHEIGHT/3)+3, start_btn_at, 1)
start_btn_bf_img = Button(int((WINDOWWIDTH - start_btn_bf.get_width())/2),int(2*WINDOWHEIGHT/3), start_btn_bf, 1)

#button mid
button_next_bf = pygame.image.load('button_next_bf.png').convert_alpha()
button_next_at = pygame.image.load('button_next_at.png').convert_alpha()
button_next_bf_img = Button(int((WINDOWWIDTH - button_next_bf.get_width())/2),int(5*WINDOWHEIGHT/7),button_next_bf,1)
button_next_at_img = Button(int((WINDOWWIDTH - button_next_at.get_width())/2),int(5*WINDOWHEIGHT/7)+3,button_next_at,1)


#button main_game
return_button = pygame.image.load('return_button.png').convert_alpha()
return_button_bf_img = Button(30,30,return_button,0.15)
return_button_at_img = Button(32,32,return_button,0.12)

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


bg_width =  bg.get_width()
scroll = 0
til = math.ceil(WINDOWWIDTH/bg_width)+1
mixer.music.load('Bgmusic.wav')
mixer.music.play(-1)
font = pygame.font.SysFont(None, 70)
counter = 60
text = font.render(str(counter), True, '#803945')
text_rect = text.get_rect(center = (XMARGIN+22*(BOXSIZE+GAPSIZE)+160,YMARGIN+15*(BOXSIZE+GAPSIZE)+50))
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)
bg_win = pygame.image.load('bg_win.jpg').convert()
win_sound = pygame.mixer.Sound('button-25.wav')
gifFrameList = loadGIF("my_gif.gif")
currentFrame = 0
bgnd = pygame.image.load('bgnd.jpg').convert()
bg_end = pygame.image.load('bg_end.png').convert()


if __name__ == '__main__':
	main()