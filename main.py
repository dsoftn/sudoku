import pygame
import os

import settings_cls
import game_gui_cls


class SudokuGame():
    def __init__(self):
        pygame.display.set_caption(stt.lang("win_title"))
        if os.path.isfile(os.curdir+"/images/sudoku.png"):
            pygame.display.set_icon(pygame.image.load("images/sudoku.png"))
        
        self.gui = game_gui_cls.GameGUI(win, stt)
        

    def show_table(self):
        self.gui.show_table()



stt = settings_cls.Setting()
pygame.init()

win = pygame.display.set_mode(stt.win_size)
game = SudokuGame()

run = True
while run:
    win.fill(stt.win_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
    game.show_table()
    pygame.display.flip()

if stt.save_data_to_file() != "":
    print ("Error. The settings file could not be saved. (settings.txt)")

pygame.quit


