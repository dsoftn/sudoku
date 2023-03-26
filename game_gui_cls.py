import pygame
import settings_cls
import game_logic_cls


class GameGUI():
    """Everything related to the graphical user interface (GUI) is done here.
    """
    def __init__(self, screen_surface: object, settings_object: object):
        # self._win = pygame.display.set_mode()
        # self._stt = settings_cls.Setting()
        self._logic = game_logic_cls.SudokuGameLogic(settings_object)
        self._stt = settings_object
        self._win = screen_surface
        pygame.font.init()
        self._stt.board_font_size, self._font_width, self._font_height = self._find_font_size_for_board()

    def show_table(self, show_correct: bool = False):
        win = self._win
        stt = self._stt
        # Load element image
        img = None
        img_normal = pygame.image.load("images/normal.png")
        img_normal = pygame.transform.scale(img_normal, (stt.element_width ,stt.element_height))
        img_empty = pygame.image.load("images/empty.png")
        img_empty = pygame.transform.scale(img_empty, (stt.element_width ,stt.element_height))
        img_correct = pygame.image.load("images/correct.png")
        img_correct = pygame.transform.scale(img_correct, (stt.element_width ,stt.element_height))
        img_wrong = pygame.image.load("images/wrong.png")
        img_wrong = pygame.transform.scale(img_wrong, (stt.element_width ,stt.element_height))
        img_selection = pygame.image.load("images/selection.png")
        img_selection = pygame.transform.scale(img_selection, (stt.element_width ,stt.element_height))
        img_selection_predefined = pygame.image.load("images/selection_predefined.png")
        img_selection_predefined = pygame.transform.scale(img_selection_predefined, (stt.element_width ,stt.element_height))
        rect = img_normal.get_rect()
        # Get table from logic
        table = self._logic._new_board()
        # Get selection position
        _selection_x = stt.selection_x
        _selection_y = stt.selection_y
        # Draw board
        for x in range(0, stt.elements_in_game_x):
            for y in range(0, stt.elements_in_game_y):
                rect.x = stt.board_surface_pos_x + stt.element_width * x
                rect.y = stt.board_surface_pos_y + stt.element_height * y
                element = table[y][x]
                # Color element
                if element[1]:
                    img = img_normal
                else:
                    if show_correct:
                        if element[2]:
                            if element[3]:
                                img = img_correct
                            else:
                                img = img_wrong
                        else:
                            img = img_empty
                    else:
                        img = img_empty
                # Check if selected
                if _selection_x == x and _selection_y == y:
                    if element[1]:
                        img = img_selection_predefined
                    else:
                        img = img_selection
                # Draw on screen
                win.blit(img, rect)
                # Draw rectangle in selected element
                if _selection_x == x and _selection_y == y:
                    rect_x = stt.board_surface_pos_x + stt.element_width * x + stt.element_width / 7
                    rect_y = stt.board_surface_pos_y + stt.element_height * y  + stt.element_height / 7
                    rect_w = stt.element_width * 5 / 7
                    rect_h = stt.element_height * 5 / 7
                    pygame.draw.rect(win, "#000000", pygame.Rect((rect_x, rect_y, rect_w, rect_h)), 2)

        # Draw block delimiter lines
        # Define scale if the line should be moved slightly
        scale_x = 0
        scale_y = 0
        thickness = 4
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

    def show_sudoku(self):
        win = self._win
        stt = self._stt
        logic = self._logic
        table = logic._new_board()
        font = pygame.font.SysFont(stt.board_font_name, stt.board_font_size)
        for x in range(0, stt.elements_in_game_x):
            for y in range(0, stt.elements_in_game_y):
                value_set = table[y][x]
                value = str(value_set[0])
                if value_set[1] or value_set[2]:
                    text = font.render(value, 1, self._stt.board_font_color)
                    element_pos_x = stt.board_surface_pos_x + stt.element_width * x
                    element_pos_y = stt.board_surface_pos_y + stt.element_height * y
                    pos_x = element_pos_x + (stt.element_width - self._font_width) / 2
                    pos_y = element_pos_y + (stt.element_height - self._font_height) / 2
                    win.blit(text, (pos_x, pos_y))



    def _find_font_size_for_board(self) -> int:
        max_height = int(self._stt.element_height * 2 / 3)
        font_size = 0
        for size in range(10, 220):
            font = pygame.font.SysFont(self._stt.board_font_name, size)
            text = font.render("8", 1, self._stt.board_font_color)
            height = text.get_height()
            width = text.get_width()
            if height > max_height:
                font_size = size - 1
                break
            font_height = height
            font_width = width
        if font_size == 0:
            font_size = 120
        return font_size, font_width, font_height

