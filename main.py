import pygame

import settings







stt = settings.Setting()

pygame.init()

win = pygame.display.set_mode(stt.win_size)
pygame.display.set_caption("Sudoku")
pygame.display.set_icon(pygame.image.load("images/sudoku.png"))

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
    
    pygame.display.flip()

if stt.save_data_to_file() != "":
    print ("Error. The settings file could not be saved. (settings.txt)")

pygame.quit


