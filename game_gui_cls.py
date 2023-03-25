import pygame
import settings_cls

class GameGUI():
    def __init__(self, screen_surface: object, settings_object: object):
        # self._win = pygame.display.set_mode()
        # self._stt = settings_cls.Setting()
        self._stt = settings_object
        self._win = screen_surface


    def show_table(self):
        win = self._win
        stt = self._stt
        # Load element image
        img = pygame.image.load("images/normal.png")
        img = pygame.transform.scale(img, (stt.element_width ,stt.element_height))
        rect = img.get_rect()
        # Draw board
        for x in range(0, stt.elements_in_game_x):
            for y in range(0, stt.elements_in_game_y):
                rect.x = stt.board_surface_pos_x + stt.element_width * x
                rect.y = stt.board_surface_pos_y + stt.element_height * y
                win.blit(img, rect)
        # Draw block delimiter lines
        # Define scale if the line should be moved slightly
        scale_x = 0
        scale_y = 0
        thickness = 2
        line_color = "green"
        # Draw vertical lines
        for x in range(0, stt.blocks_in_game_x + 1):
            start_x = stt.board_surface_pos_x + (stt.element_width * stt.elements_in_block_x) * x + scale_x
            start_y = stt.board_surface_pos_y
            end_x = start_x
            end_y = start_y + stt.board_surface_height
            pygame.draw.line(win, pygame.Color(line_color), (start_x, start_y), (end_x, end_y), thickness)
        # Draw horizontal lines
        for y in range(0, stt.blocks_in_game_y + 1):
            start_x = stt.board_surface_pos_x
            start_y = stt.board_surface_pos_y + (stt.element_height * stt.elements_in_block_y) * y + scale_y
            end_x = start_x + stt.board_surface_width
            end_y = start_y
            pygame.draw.line(win, pygame.Color(line_color), (start_x, start_y), (end_x, end_y), thickness)


