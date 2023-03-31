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
        self.btn_size9x9 = pygameButton.Button(self._win, (int(720 * self._stt.win_scale_x), int(30 * self._stt.win_scale_y)), int(70 * self._stt.win_scale_x), int(40 * self._stt.win_scale_y), "9x9", font_size=int(28 * self._stt.win_scale_x))
        self.btn_size6x6 = pygameButton.Button(self._win, (int(640 * self._stt.win_scale_x), int(30 * self._stt.win_scale_y)), int(70 * self._stt.win_scale_x), int(40 * self._stt.win_scale_y), "6x6", font_size=int(28 * self._stt.win_scale_x))
        self.btn_new_game = pygameButton.Button(self._win, (int(10 * self._stt.win_scale_x), int(30 * self._stt.win_scale_y)), int(200 * self._stt.win_scale_x), int(50 * self._stt.win_scale_y), self._stt.lang("new_game"), font_size=int(46 * self._stt.win_scale_x), bg_color="green")
        self.btn_check_sudoku = pygameButton.Button(self._win, (int(300 * self._stt.win_scale_x), int(755 * self._stt.win_scale_y)), int(200 * self._stt.win_scale_x), int(40 * self._stt.win_scale_y), self._stt.lang("check_sudoku"), font_size=int(36 * self._stt.win_scale_x), bg_color="green")
        self.btn_help = pygameButton.Button(self._win, (int(505 * self._stt.win_scale_x), int(755 * self._stt.win_scale_y)), int(290 * self._stt.win_scale_x), int(40 * self._stt.win_scale_y), self._stt.lang("hint"), font_size=int(28 * self._stt.win_scale_x), bg_color="#FF0000", fg_color="#000066")

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
        if self.btn_help.mouse_click:
            self._logic.analyze_user_input()
            self.show_hint()
            self._logic.analyze_user_input()
            self._show_correct = True
            self.btn_help.mouse_click = False
        if self._sudoku_solved:
            self._logic.analyze_user_input()
            self._show_correct = True

    def start_new_game(self):
        self._logic.active_game = False
        self._logic.start_new_game()

    def draw_gui(self):
        # Draw title image
        img_title = pygame.image.load("images/title.png")
        img_title = pygame.transform.scale(img_title, (240, 70))
        rect_title = img_title.get_rect()
        rect_title.x = int(280 * self._stt.win_scale_x)
        rect_title.y = int(25 * self._stt.win_scale_y)
        self._win.blit(img_title, rect_title)
        # Draw board cell selection
        img_set0 = pygame.image.load("images/set0/correct.png")
        img_set0 = pygame.transform.scale(img_set0, (60, 60))
        rect_set0 = img_set0.get_rect()
        rect_set0.x = int(20 * self._stt.win_scale_x)
        rect_set0.y = int(440 * self._stt.win_scale_y)
        self._win.blit(img_set0, rect_set0)
        img_set1 = pygame.image.load("images/set1/correct.png")
        img_set1 = pygame.transform.scale(img_set1, (60, 60))
        rect_set1 = img_set1.get_rect()
        rect_set1.x = int(20 * self._stt.win_scale_x)
        rect_set1.y = int(510 * self._stt.win_scale_y)
        self._win.blit(img_set1, rect_set1)
        img_set2 = pygame.image.load("images/set2/correct.png")
        img_set2 = pygame.transform.scale(img_set2, (60, 60))
        rect_set2 = img_set2.get_rect()
        rect_set2.x = int(20 * self._stt.win_scale_x)
        rect_set2.y = int(580 * self._stt.win_scale_y)
        self._win.blit(img_set2, rect_set2)
        img_set3 = pygame.image.load("images/set3/correct.png")
        img_set3 = pygame.transform.scale(img_set3, (60, 60))
        rect_set3 = img_set0.get_rect()
        rect_set3.x = int(20 * self._stt.win_scale_x)
        rect_set3.y = int(650 * self._stt.win_scale_y)
        self._win.blit(img_set3, rect_set3)
        # Draw national flags for language change
        img_srbija = pygame.image.load("images/flag_serbia.png")
        img_srbija = pygame.transform.scale(img_srbija, (40, 20))
        rect_srbija = img_srbija.get_rect()
        rect_srbija.x = 70
        rect_srbija.y = int(770 * self._stt.win_scale_y)
        self._win.blit(img_srbija, rect_srbija)
        img_uk = pygame.image.load("images/flag_uk.png")
        img_uk = pygame.transform.scale(img_uk, (40, 20))
        rect_uk = img_uk.get_rect()
        rect_uk.x = 20
        rect_uk.y = int(770 * self._stt.win_scale_y)
        self._win.blit(img_uk, rect_uk)
        # Zoom out button
        img_zoom_out = pygame.image.load("images/zoom_out.png")
        img_zoom_out = pygame.transform.scale(img_zoom_out, (50, 50))
        rect_zoom_out = img_zoom_out.get_rect()
        rect_zoom_out.x = int(740 * self._stt.win_scale_x)
        rect_zoom_out.y = int(150 * self._stt.win_scale_y)
        self._win.blit(img_zoom_out, rect_zoom_out)
        # Buttons
        self.btn_new_game.draw_button()
        self.btn_new_game.caption = self._stt.lang("new_game")
        self.btn_size6x6.draw_button()
        self.btn_size9x9.draw_button()
        self.btn_check_sudoku.draw_button()
        self.btn_check_sudoku.caption = self._stt.lang("check_sudoku")
        if self._show_correct:
            self.btn_help.draw_button()
        self.btn_help.caption = self._stt.lang("hint")
        # Level
        font = pygame.font.SysFont("Comic Sans MS", 40)
        text = font.render(self._stt.lang("level_msg"), 1, "blue")
        self._win.blit(text, (int(710 * self._stt.win_scale_x), int(400 * self._stt.win_scale_y)))
        font = pygame.font.SysFont("Comic Sans MS", 60)
        if self._stt.game_level == 1:
            color = "green"
        elif self._stt.game_level == 2:
            color = "#B2FF66"
        elif self._stt.game_level == 3:
            color = "yellow"
        elif self._stt.game_level == 4:
            color = "#AE4343"
        elif self._stt.game_level == 5:
            color = "red"
        text = font.render(str(self._stt.game_level), 1, color)
        self._win.blit(text, (int(735 * self._stt.win_scale_x), int(440 * self._stt.win_scale_y)))
        img_level_up = pygame.image.load("images/level_up.png")
        img_level_up = pygame.transform.scale(img_level_up, (60, 60))
        rect_level_up = img_zoom_out.get_rect()
        rect_level_up.x = int(720 * self._stt.win_scale_x)
        rect_level_up.y = int(330 * self._stt.win_scale_y)
        self._win.blit(img_level_up, rect_level_up)
        img_level_down = pygame.image.load("images/level_down.png")
        img_level_down = pygame.transform.scale(img_level_down, (60, 60))
        rect_level_down = img_zoom_out.get_rect()
        rect_level_down.x = int(720 * self._stt.win_scale_x)
        rect_level_down.y = int(530 * self._stt.win_scale_y)
        self._win.blit(img_level_down, rect_level_down)
        # If user is solved sudoku 
        if self._sudoku_solved:
            font = pygame.font.SysFont("Comic Sans MS", 40)
            text = font.render(self._stt.lang("user_solved_msg"), 1, "light green")
            self._win.blit(text, (int(100 * self._stt.win_scale_x), int(95 * self._stt.win_scale_y)))
            img_end = pygame.image.load("images/end.png")
            img_end = pygame.transform.scale(img_end, (100, 200))
            rect_end = img_title.get_rect()
            rect_end.x = int(5 * self._stt.win_scale_x)
            rect_end.y = int(250 * self._stt.win_scale_y)
            self._win.blit(img_end, rect_end)

    def mouse_event_handler(self, event):
        mouse_pos = pygame.mouse.get_pos()
        x_mouse = mouse_pos[0]
        y_mouse = mouse_pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change selected cell
            if x_mouse > self._stt.board_surface_pos_x and x_mouse < self._stt.board_surface_pos_x + self._stt.board_surface_width:
                if y_mouse > self._stt.board_surface_pos_y and y_mouse < self._stt.board_surface_pos_y + self._stt.board_surface_height:
                    x_mouse_cell = x_mouse - self._stt.board_surface_pos_x
                    y_mouse_cell = y_mouse - self._stt.board_surface_pos_y
                    self._stt.selection_x = int(x_mouse_cell / self._stt.element_width)
                    self._stt.selection_y = int(y_mouse_cell / self._stt.element_height)
            # Zoom clicked
            if x_mouse > int(739 * self._stt.win_scale_x) and x_mouse < int(791 * self._stt.win_scale_x) and y_mouse > int(149 * self._stt.win_scale_y) and y_mouse < int(191 * self._stt.win_scale_y):
                self._stt.game_surface_zoom_level += 1
            # Level UP clicked
            if x_mouse > int(719 * self._stt.win_scale_x) and x_mouse < int(781 * self._stt.win_scale_x) and y_mouse > int(329 * self._stt.win_scale_y) and y_mouse < int(391 * self._stt.win_scale_y):
                old_level = self._stt.game_level
                self._stt.game_level += 1
                if old_level != self._stt.game_level:
                    self.start_new_game()
                    self._sudoku_solved = False
            # Level DOWN clicked
            if x_mouse > int(719 * self._stt.win_scale_x) and x_mouse < int(781 * self._stt.win_scale_x) and y_mouse > int(529 * self._stt.win_scale_y) and y_mouse < int(591 * self._stt.win_scale_y):
                old_level = self._stt.game_level
                self._stt.game_level -= 1
                if old_level != self._stt.game_level:
                    self.start_new_game()
                    self._sudoku_solved = False
            # English flag clicked
            if x_mouse > int(19 * self._stt.win_scale_x) and x_mouse < int(61 * self._stt.win_scale_x) and y_mouse > int(769 * self._stt.win_scale_y) and y_mouse < int(791 * self._stt.win_scale_y):
                self._stt.language = 0
                pygame.display.set_caption(self._stt.lang("win_title"))
            # Serbian flag clicked
            if x_mouse > int(69 * self._stt.win_scale_x) and x_mouse < int(111 * self._stt.win_scale_x) and y_mouse > int(769 * self._stt.win_scale_y) and y_mouse < int(791 * self._stt.win_scale_y):
                self._stt.language = 1
                pygame.display.set_caption(self._stt.lang("win_title"))
            # Change cell buttons clicked
            if x_mouse > int(19 * self._stt.win_scale_x) and x_mouse < int(81 * self._stt.win_scale_x) and y_mouse > int(439 * self._stt.win_scale_y) and y_mouse < int(501 * self._stt.win_scale_y):
                self._stt.buttons_image_folder = "images/set0/"
            if x_mouse > int(19 * self._stt.win_scale_x) and x_mouse < int(81 * self._stt.win_scale_x) and y_mouse > int(509 * self._stt.win_scale_y) and y_mouse < int(571 * self._stt.win_scale_y):
                self._stt.buttons_image_folder = "images/set1/"
            if x_mouse > int(19 * self._stt.win_scale_x) and x_mouse < int(81 * self._stt.win_scale_x) and y_mouse > int(579 * self._stt.win_scale_y) and y_mouse < int(641 * self._stt.win_scale_y):
                self._stt.buttons_image_folder = "images/set2/"
            if x_mouse > int(19 * self._stt.win_scale_x) and x_mouse < int(81 * self._stt.win_scale_x) and y_mouse > int(649 * self._stt.win_scale_y) and y_mouse < int(711 * self._stt.win_scale_y):
                self._stt.buttons_image_folder = "images/set3/"
        # Events for buttons
        self.btn_new_game.event_handler(event)
        self.btn_size6x6.event_handler(event)
        self.btn_size9x9.event_handler(event)
        self.btn_check_sudoku.event_handler(event)
        if self._show_correct:
            self.btn_help.event_handler(event)
                
    def key_event_handler(self, keys):
        keys = pygame.key.get_pressed()
        self._show_correct = False
        # Arrow key pressed
        if keys[pygame.K_UP]:
            self._stt.selection_y -= 1
        elif keys[pygame.K_DOWN]:
            self._stt.selection_y += 1
        elif keys[pygame.K_LEFT]:
            self._stt.selection_x -= 1
        elif keys[pygame.K_RIGHT]:
            self._stt.selection_x += 1
        elif keys[pygame.K_PAGEUP]:
            self._stt.game_surface_zoom_level += 1
        elif keys[pygame.K_PAGEDOWN]:
            self._stt.game_surface_zoom_level -= 1
        # Number pressed
        if keys[pygame.K_0] or keys[pygame.K_DELETE] or keys[pygame.K_KP_0]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 0)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_1] or keys[pygame.K_KP_1]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 1)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_2] or keys[pygame.K_KP_2]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 2)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_3] or keys[pygame.K_KP_3]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 3)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_4] or keys[pygame.K_KP_4]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 4)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_5] or keys[pygame.K_KP_5]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 5)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_6] or keys[pygame.K_KP_6]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 6)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_7] or keys[pygame.K_KP_7]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 7)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_8] or keys[pygame.K_KP_8]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 8)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        elif keys[pygame.K_9] or keys[pygame.K_KP_9]:
            self._logic.set_cell_val(self._stt.selection_x, self._stt.selection_y, 9)
            self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
        # Spacebar pressed
        if keys[pygame.K_SPACE]:
            self._logic.analyze_user_input()
            self._show_correct = True
    
    def show_hint(self):
        stt = self._stt
        wait_ms = stt.hint_animation_speed
        cell = self._logic.user_hint()
        # If cell not found abort function
        if not cell:
            return
        cell_x = cell[0]
        cell_y = cell[1]
        cell_val = cell[2]
        # Go to cell
        while stt.selection_x != cell_x or stt.selection_y != cell_y:
            pygame.time.wait(wait_ms)
            if abs(cell_x - stt.selection_x) > abs(cell_y - stt.selection_y):
                if stt.selection_x < cell_x:
                    stt.selection_x += 1
                elif stt.selection_x > cell_x:
                    stt.selection_x -= 1
            else:
                if stt.selection_y < cell_y:
                    stt.selection_y += 1
                elif stt.selection_y > cell_y:
                    stt.selection_y -= 1
            self.show_table(show_correct=True)
            self.show_sudoku()
            self.draw_gui()
            pygame.display.flip()
        # Write correct value into cell
        pygame.time.wait(wait_ms)
        self._logic.set_cell_val(cell_x, cell_y, cell_val)
        self._sudoku_solved = self._logic.check_sudoku_is_user_solved()
    
    def show_table(self, show_correct: bool = False):
        win = self._win
        stt = self._stt
        # Load element image
        png_folder = stt.buttons_image_folder
        img = None
        img_normal = pygame.image.load(png_folder + "normal.png")
        img_normal = pygame.transform.scale(img_normal, (stt.element_width ,stt.element_height))
        img_empty = pygame.image.load(png_folder + "empty.png")
        img_empty = pygame.transform.scale(img_empty, (stt.element_width ,stt.element_height))
        img_correct = pygame.image.load(png_folder + "correct.png")
        img_correct = pygame.transform.scale(img_correct, (stt.element_width ,stt.element_height))
        img_wrong = pygame.image.load(png_folder + "wrong.png")
        img_wrong = pygame.transform.scale(img_wrong, (stt.element_width ,stt.element_height))
        img_selection = pygame.image.load(png_folder + "selection.png")
        img_selection = pygame.transform.scale(img_selection, (stt.element_width ,stt.element_height))
        img_selection_predefined = pygame.image.load(png_folder + "selection_predefined.png")
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
                    pygame.draw.rect(win, stt._selection_rectangle_color, pygame.Rect((rect_x, rect_y, rect_w, rect_h)), stt._selection_rectangle_thicknes)
        # Draw block delimiter lines
        # Define scale if the line should be moved slightly
        scale_x = stt.scale_delimiter_lines_x
        scale_y = stt.scale_delimiter_lines_y
        thickness = stt.delimiter_line_thicknes
        line_color = stt.delimiter_line_color
        # Draw vertical lines
        for x in range(0, stt.blocks_in_game_x + 1):
            start_x = stt.board_surface_pos_x + (stt.element_width * stt.elements_in_block_x) * x + scale_x
            start_y = stt.board_surface_pos_y + scale_y
            end_x = start_x
            end_y = start_y + stt.board_surface_height
            pygame.draw.line(win, pygame.Color(line_color), (start_x, start_y), (end_x, end_y), thickness)
        # Draw horizontal lines
        for y in range(0, stt.blocks_in_game_y + 1):
            start_x = stt.board_surface_pos_x + scale_x
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

