import pygame
import os

import settings_cls
import game_gui_cls


class SudokuGame():
    """This is where the flow of the game and interaction with the user is controlled.

    Module: game_gui_cls
        Takes care of game display and user interface display.
    Module: settings_cls
        Manages the 'settings.txt' file and obtains all the data required for
        the correct display of the game and the user interface.
    Module: game_logic_cls
        Creates a sudoku table and determines the number of empty fields depending on
        the level of the game.
    """
    def __init__(self):
        pygame.display.set_caption(stt.lang("win_title"))
        if os.path.isfile(os.curdir+"/images/sudoku.png"):
            pygame.display.set_icon(pygame.image.load("images/sudoku.png"))
        
        self.gui = game_gui_cls.GameGUI(win, stt)

    def show_table(self):
        self.gui.update_gui()

    def event_handler(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            self.gui.key_event_handler(keys)
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            self.gui.mouse_event_handler(event)
        
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            self.gui._show_correct = False
            if keys[pygame.K_UP]:
                stt.selection_y -= 1
            elif keys[pygame.K_DOWN]:
                stt.selection_y += 1
            elif keys[pygame.K_LEFT]:
                stt.selection_x -= 1
            elif keys[pygame.K_RIGHT]:
                stt.selection_x += 1
            elif keys[pygame.K_PAGEUP]:
                stt.game_surface_zoom_level += 1
            elif keys[pygame.K_PAGEDOWN]:
                stt.game_surface_zoom_level -= 1



stt = settings_cls.Setting()
pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode(stt.win_size)
pygame.key.set_repeat(500, 50)
game = SudokuGame()

run = True
while run:
    clock.tick(30)
    win.fill(stt.win_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        game.event_handler(event)
        


    game.show_table()
    pygame.display.flip()

if stt.save_data_to_file() != "":
    print ("Error. The settings file could not be saved. (settings.txt)")

pygame.quit


