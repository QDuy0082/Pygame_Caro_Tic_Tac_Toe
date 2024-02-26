import pygame, sys, pygame_gui
from pygame.locals import *
pygame.init()

Clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1000,700))
pygame.display.set_caption('khai dep trai')
DISPLAYSURF.fill((0,0,0))

MANAGER = pygame_gui.UIManager((1000,700))
TEXTINPUT = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((100,275),(900,50)),manager=MANAGER,object_id= "#main_text_entry")

WHITE = (255,255,255)

while True:
	UI_REFRESH_RATE = Clock.tick(60)/1000
	DISPLAYSURF.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
			show_text(event.text)

		MANAGER.process_events(event)

	MANAGER.update(UI_REFRESH_RATE)
	DISPLAYSURF.fill(WHITE)
	MANAGER.draw_ui(DISPLAYSURF)


	pygame.display.update()