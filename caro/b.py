import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)


BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
	global DISPLAYSURF, FPSCLOCK
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	mousex = 0
	mousey = 0
	pygame.display.set_caption('caro')
	mainboard = getRandomizedBoard()
	revealedBoxes = generateRevealedBoxesData(False)
	firstSelection = None
	DISPLAYSURF.fill(BGCOLOR)
	startGameAnimation(mainboard)
	while True:
		mouseClick = False
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(mainboard,revealedBoxes)
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClick = True
		boxx,boxy = getBoxAtPixel(mousex,mousey)
		if boxx != None and boxy != None:
			if not revealedBoxes[boxx][boxy]:
				drawHightlightBox(boxx,boxy)
			if not revealedBoxes[boxx][boxy] and mouseClick:
				revealBoxesAnimation(mainboard,[(boxx,boxy)])
				revealedBoxes[boxx][boxy]=True
				if firstSelection == None:
					firstSelection = (boxx,boxy)
				else:
					icon1shape, icon1color = getShapeAndColor(mainboard,firstSelection[0],firstSelection[1])
					icon2shape, icon2color = getShapeAndColor(mainboard,boxx,boxy)
					if icon1shape != icon2shape or icon1color != icon2color:
						pygame.time.wait(1000)
						coverBoxesAnimation(mainboard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
						revealedBoxes[firstSelection[0]][firstSelection[1]] = False
						revealedBoxes[boxx][boxy] = False
					elif hasWon(revealedBoxes): # check if all pairs found
						gameWonAnimation(mainboard)
						pygame.time.wait(2000)

						# Reset the board
						mainboard = getRandomizedBoard()
						revealedBoxes = generateRevealedBoxesData(False)

						# Show the fully unrevealed board for a second.
						drawBoard(mainboard, revealedBoxes)
						pygame.display.update()
						pygame.time.wait(1000)

						# Replay the start game animation.
						startGameAnimation(mainboard)
					firstSelection = None
			pygame.display.update()
			FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
	result = []
	for i in range(BOARDWIDTH):
		result.append([val]*BOARDWIDTH)
	return result

def getRandomizedBoard():
	icons = []
	for color in ALLCOLORS:
		for shape in ALLSHAPES:
			icons.append((shape,color))
	random.shuffle(icons)
	iconsUsed = int(BOARDWIDTH*BOARDHEIGHT/2)
	icons = icons[:iconsUsed]*2
	random.shuffle(icons)

	board = []
	for x in range(BOARDWIDTH):
		colum = []
		for y in range(BOARDHEIGHT):
			colum.append(icons[0])
			del icons[0]
		board.append(colum)
	return board

def splitIntoGroupsOf(groupSize, theList):
	result = []
	for i in range(0, len(theList), groupSize):
		result.append(theList[i:i + groupSize])
	return result

def leftTopCoordsOfBox(boxx,boxy):
	left = boxx*(BOXSIZE + GAPSIZE) + XMARGIN
	top = boxy*(BOXSIZE + GAPSIZE) + YMARGIN
	return (left, top)

def getBoxAtPixel(x,y):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left, top = leftTopCoordsOfBox(boxx,boxy)
			boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
			if boxRect.collidepoint(x,y):
				return (boxx,boxy)
	return (None,None)

def drawHightlightBox(boxx,boxy):
	left, top = leftTopCoordsOfBox(boxx,boxy)
	pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR,(left-5,top-5,BOXSIZE+10,BOXSIZE+10),4)

def getShapeAndColor(board,boxx,boxy):
	return board[boxx][boxy][0], board[boxx][boxy][1]

def drawIcon(shape, color, boxx, boxy):
 	quarter = int(BOXSIZE * 0.25) # syntactic sugar
 	half =    int(BOXSIZE * 0.5)  # syntactic sugar
 	left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
 	# Draw the shapes
 	if shape == DONUT:
 		pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
 		pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
 	elif shape == SQUARE:
 		pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
 	elif shape == DIAMOND:
 		pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
 	elif shape == LINES:
 		for i in range(0, BOXSIZE, 4):
 			pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
 			pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
 	elif shape == OVAL:
 		pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

def drawBoard(board,revealedBoxes):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left,top = leftTopCoordsOfBox(boxx,boxy)
			if not revealedBoxes[boxx][boxy]:
				pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
			else:
				shape, color = getShapeAndColor(board,boxx,boxy)
				drawIcon(shape,color,boxx,boxy)


def drawBoxCover(board,boxes,coverage):
	for box in boxes:
		left,top=leftTopCoordsOfBox(box[0],box[1])
		shape, color =  getShapeAndColor(board,box[0],box[1])
		pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
		drawIcon(shape,color,box[0],box[1])
		if coverage > 0:
			pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,coverage,BOXSIZE))
	pygame.display.update()
	FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board,boxestoReveal):
	for coverage in range(BOXSIZE,(-REVEALSPEED)-1,-REVEALSPEED):
		drawBoxCover(board,boxestoReveal,coverage)

def coverBoxesAnimation(board,boxestoCover):
	for coverage in range(0,BOXSIZE+REVEALSPEED,REVEALSPEED):
		drawBoxCover(board,boxestoCover,coverage)

def startGameAnimation(board):
	coveredBoxes = generateRevealedBoxesData(False)
	boxes = []
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			boxes.append((x, y))
	random.shuffle(boxes)
	boxGroups = splitIntoGroupsOf(8, boxes)

	drawBoard(board, coveredBoxes)
	for boxGroup in boxGroups:
		revealBoxesAnimation(board, boxGroup)
		coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
	coveredBoxes = generateRevealedBoxesData(True)
	color1 = LIGHTBGCOLOR
	color2 = BGCOLOR

	for i in range(13):
		color1, color2 = color2, color1
		DISPLAYSURF.fill(color1)
		drawBoard(board, coveredBoxes)
		pygame.display.update()
		pygame.time.wait(300)


def hasWon(revealedBoxes):
	for i in revealedBoxes:
		if False in i:
			return False # return False if any boxes are covered.
	return True

if __name__ == '__main__':
	main()

