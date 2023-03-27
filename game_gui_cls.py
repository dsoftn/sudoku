import pygame

import settings_cls
import game_logic_cls
import pygameButton


class GameGUI():
    """Everything related to the graphical user interface (GUI) is done here.
    """
    def __init__(self, screen_surface: pygame.Surface, settings_object: settings_cls.Setting):
        # self._win = pygame.display.set_mode()
        # self._stt = settings_cls.Setting()
        self._logic = game_logic_cls.SudokuGameLogic(settings_object)
        self._stt = settings_object
        self._win = screen_surface
        self._show_correct = False  # Shows user is entries correct
        self._sudoku_solved = False  # Indicates is sudoku solved by user
        pygame.font.init()
        self._stt.board_font_size, self._font_width, self._font_height = self._find_font_size_for_board()
        # Define buttons
        self.btn_size9x9 = pygameButton.Button(self._win, (720, 30), 70, 40, "9x9", font_size=28)
        self.btn_size6x6 = pygameButton.Button(self._win, (640, 30), 70, 40, "6x6", font_size=28)
        self.btn_new_game = pygameButton.Button(self._win, (10, 30), 200, 50, self._stt.lang("new_game"), font_size=46, bg_color="green")
        self.btn_check_sudoku = pygameButton.Button(self._win, (300, 755), 200, 40, self._stt.lang("check_sudoku"), font_size=36, bg_color="green")

    def update_gui(self):
        # Find font size
        self._stt.board_font_size, self._font_width, self._font_height = self._find_font_size_for_board()
        # Create new game
        if not self._logic.active_game:
            self._logic.start_new_game()
        # Show Table
        self.show_table(self._show_correct)
        # Show sudoku in table
        self.show_sudoku()
        self.draw_gui()
        if self.btn_new_game.mouse_click:
            self.start_new_game()
            self.btn_new_game.mouse_click = False
            self._sudoku_solved = False
        if self.btn_size6x6.mouse_click:
            self._stt.game_size = 6
            self.start_new_game()
            self.btn_size6x6.mouse_click = False
            self._sudoku_solved = False
        if self.btn_size9x9.mouse_click:
            self._stt.game_size = 9
            self.start_new_game()
            self.btn_size9x9.mouse_click = False
            self._sudoku_solved = False
        if self.btn_check_sudoku.mouse_click:
            self._logic.analyze_user_input()
            self._show_correct = True
            self.btn_check_sudoku.mouse_click = False

    def start_new_game(self):
        self._logic.active_game = False
        self._logic.start_new_game()

    def draw_gui(self):
        img_title = pygame.image.load("images/title.png")
        img_title = pygame.transform.scale(img_title, (240, 70))
        rect_title = img_title.get_rect()
        rect_title.x = 280
        rect_title.y = 25
        img_zoom_out = pygame.image.load("images/zoom_out.png")
        img_zoom_out = pygame.transform.scale(img_zoom_out, (50, 50))
        rect_zoom_out = img_zoom_out.get_rect()
        rect_zoom_out.x = 740
        rect_zoom_out.y = 150
        self._win.blit(img_title, rect_title)
        self._win.blit(img_zoom_out, rect_zoom_out)

        # Buttons
        self.btn_new_game.draw_button()
        self.btn_size6x6.draw_button()
        self.btn_size9x9.draw_button()
        self.btn_check_sudoku.draw_button()

        # If user is solved sudoku 
        if self._sudoku_solved:
            font = pygame.font.SysFont("Comic Sans MS", 40)
            text = font.render(self._stt.lang("user_solved_msg"), 1, "light green")
            self._win.blit(text, (100, 95))
            img_end = pygame.image.load("images/end.png")
            img_end = pygame.transform.scale(img_end, (100, 200))
            rect_end = img_title.get_rect()
            rect_end.x = 5
            rect_end.y = 250
            self._win.blit(img_end, rect_end)


    def mouse_event_handler(self, event):
        mouse_pos = pygame.mouse.get_pos()
        x_mouse = mouse_pos[0]
        y_mouse = mouse_pos[1]
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x_mouse > self._stt.board_surface_pos_x and x_mouse < self._stt.board_surface_pos_x + self._stt.board_surface_width:
                if y_mouse > self._stt.board_surface_pos_y and y_mouse < self._stt.board_surface_pos_y + self._stt.board_surface_height:
                    x_mouse = x_mouse - self._stt.board_surface_pos_x
                    y_mouse = y_mouse - self._stt.board_surface_pos_y
                    self._stt.selection_x = int(x_mouse / self._stt.element_width)
                    self._stt.selection_y = int(y_mouse / self._stt.element_height)
            if x_mouse > 739 and x_mouse < 791 and y_mouse > 149 and y_mouse < 191:
                self._stt.game_surface_zoom_level += 1

        # Events for buttons
        self.btn_new_game.event_handler(event)
        self.btn_size6x6.event_handler(event)
        self.btn_size9x9.event_handler(event)
        self.btn_check_sudoku.event_handler(event)
                


    def key_event_handler(self, keys):
        if keys[pygame.K_0] or keys[pygame.K_DELETE]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 0)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_1]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 1)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_2]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 2)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_3]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 3)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_4]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 4)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_5]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 5)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_6]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 6)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_7]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 7)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_8]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 8)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_9]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 9)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()

        if keys[pygame.KSCAN_SPACE]:
            self._logic.analyze_user_input()
            self._show_correct = True
    
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
        table = self._logic.board
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
                if _selection_x == x and _selection_y == y and not self._show_correct:
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
        table = logic.board
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

