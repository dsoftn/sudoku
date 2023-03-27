import random
import settings_cls


class SudokuGameLogic():
    """Creates a sudoku table and determines the number of empty fields depending on
    the level of the game.

    _board is list size X * Y
    Board cell = [  value (int): Value of cell (1-4, 1-6 or 1-9)
                    predefined (bool): If true, it is shown on board
                    edited (bool): If true, user entered data in cell
                    correct (bool): If true, user data is correct ]
    _board_solved (list):
        list with only numbers

    """
    def __init__(self, setting_object: settings_cls.Setting):
        self._stt = setting_object
        self.active_game = False  # Indicates that game is created
        self._board = []  # Game board
        self._solved_board = []  # Solved board, contains just numbers

    def start_new_game(self):
        """Starts new game.
            - Creates empty table
            - Populates table with predefinded values
        """
        self.active_game = True
        is_solved = False
        while not is_solved:
            self._create_empty_board()
            self._create_new_sudoku()
            self._empty_user_cells()
            is_solved = self._solve_sudoku()


    def analyze_user_input(self):
        for y in range(0, self._stt.elements_in_game_y):
            for x in range(0, self._stt.elements_in_game_x):
                cell = self._board[y][x]
                if not cell[1]:
                    allowed = self._available_vals(x, y)
                    if cell[0] not in allowed:
                        self._board[y][x][3] = False
                    else:
                        self._board[y][x][3] = True

    def check_sudoku_is_user_solved(self) -> bool:
        solved = True
        for y in range(0, self._stt.elements_in_game_y):
            if not solved:
                break
            for x in range(0, self._stt.elements_in_game_x):
                cell = self._board[y][x]
                if cell[0] == 0:
                    solved = False
                    break
                allowed = self._available_vals(x, y)
                if len(allowed) == 1:
                    if allowed[0] != cell[0]:
                        solved = False
                        break
                else:
                    solved = False
                    break
        return solved

    def _create_empty_board(self):
        elements_x = self._stt.elements_in_game_x
        elements_y = self._stt.elements_in_game_y
        self._board = []
        for y in range(0, elements_y):
            x_list = []
            for x in range(0, elements_x):
                x_list.append([0, False, False, False])
            self._board.append(x_list)

    def _get_cell_val(self, x: int, y: int) -> int:
        return self._board[y][x][0]
    
    def _set_cell_val(self, x: int, y: int, value: int, predefinded: bool = False, edited: bool = False, correct: bool = False):
        self._board[y][x] = [value, predefinded, edited, correct]

    def set_cell_val(self, x: int, y: int, value: int):
        cell = self._board[y][x]
        if value == 0:
            edited = False
        else:
            edited = True
        if not cell[1]:
            self._board[y][x] = [value, False, edited, cell[3]]

    def _available_vals(self, x: int, y: int) -> list:
        # Save old value and put 0 in cell
        old_val = self._board[y][x][0]
        self._board[y][x][0] = 0
        # Find x occupied values
        vals_x = [v[0] for v in self._board[y] if v[0] != 0]
        # Find y occupied values
        vals_y = [v[x][0] for v in self._board if v[x][0] != 0]
        # Find block occupied values
        vals_b = []
        start_pos_x = int(x / self._stt.elements_in_block_x) * self._stt.elements_in_block_x
        start_pos_y = int(y / self._stt.elements_in_block_y) * self._stt.elements_in_block_y
        for pos_y in range(start_pos_y, start_pos_y + self._stt.elements_in_block_y):
            for pos_x in range(start_pos_x, start_pos_x + self._stt.elements_in_block_x):
                if self._board[pos_y][pos_x][0] != 0:
                    vals_b.append(self._board[pos_y][pos_x][0])
        # Make all_v list with all allowed values
        all_v = []
        for i in range(1, self._stt.block_size + 1):
            all_v.append(i)
        # Remove all existing values ​​from the list
        all_v = [v for v in all_v if v not in vals_x]
        all_v = [v for v in all_v if v not in vals_y]
        all_v = [v for v in all_v if v not in vals_b]
        # Return the old value to the cell
        self._board[y][x][0] = old_val
        # Return a list of available values
        return all_v

    def _create_new_sudoku(self):
        stt = self._stt
        # Build Sudoku
        """ Rules for creating Sudoku:
        Create a blank 9x9 board.
        Fill the first row randomly with numbers from 1 to 9.
        Fill the second row so that the numbers in it are not repeated in the 
            same column or the same 3x3 region as the numbers in the first row.
        Continue filling in the remaining rows in the same way,
            using Sudoku rules to ensure that no number is repeated in 
            the same row, column or 3x3 region.
        """
        count = 0
        start_over = False
        sudoku_found = False
        for i in range(99):
            if sudoku_found:
                if self._is_sudoku_valid():
                    break
                else:
                    sudoku_found = False
            while count < 40:
                for y in range(0, stt.elements_in_game_y):
                    if start_over:
                        break
                    for x in range(0, stt.elements_in_game_x):
                        if start_over:
                            break
                        allowed_list = self._available_vals(x, y)
                        if allowed_list:
                            index = random.randint(0, len(allowed_list) - 1)
                            self._set_cell_val(x, y, allowed_list[index], predefinded=True)
                            # print (allowed_list, " NUMBER: ", allowed_list[index], " AT ", x, y)
                        else:
                            # print ("STOP: ", x, y, allowed_list)
                            start_over = True
                if start_over:
                    start_over = False
                else:
                    sudoku_found = True
                    break
                count += 1
        # Copy board to self._solved_board
        self._solved_board = []
        for y in range(0, stt.elements_in_game_y):
            for x in range(0, stt.elements_in_game_x):
                self._solved_board.append(self._board[x][y][0])
       
    def _empty_user_cells(self):
        stt = self._stt        
        # Counts number of added predefined cells
        count = 0
        # Maximum of predefined cells
        user_cells_count  = stt.elements_in_game_x * stt.elements_in_game_y
        user_cells_count = int(user_cells_count * stt.game_level * stt.level_points / 100)
        while count < user_cells_count:
            x = random.randint(0, stt.elements_in_game_x - 1)
            y = random.randint(0, stt.elements_in_game_y - 1)
            if self._get_cell_val(x, y) != 0:
                self._set_cell_val(x, y, 0, False, False, False)
                count += 1
        
    def _solve_sudoku(self):
        stt = self._stt
        # Backup original table
        table = []
        for y in range(0, stt.elements_in_game_y):
            for x in range(0, stt.elements_in_game_x):
                table.append(self._board[y][x][0])
        # Track if sudoku is solved
        is_solved = False
        # Track is there improve, if not exit while loop and return false
        has_improved = True
        while has_improved:
            has_improved = False
            # Walk through all cells
            for y in range(0, stt.elements_in_game_y):
                for x in range(0, stt.elements_in_game_x):
                    if self._board[y][x][1]:
                        continue
                    # Check is there cell with only 1 solution
                    solutions = self._available_vals(x,y)
                    if len(solutions) == 1:
                        self._set_cell_val(x, y, solutions[0])
                        has_improved = True
                    # Check is there unique value for this cell in row, col or block
                    # Check row
                    if not has_improved:
                        values = []
                        for x1 in range(0, stt.elements_in_game_x):
                            if x != x1:
                                if self._get_cell_val(x1, y) == 0:
                                    values = values + self._available_vals(x1, y)
                        for solution in solutions:
                            if solution not in values:
                                self._set_cell_val(x, y, solution)
                                has_improved = True
                                break
                    # Check column
                    if not has_improved:
                        values = []
                        for y1 in range(0, stt.elements_in_game_y):
                            if y != y1:
                                if self._get_cell_val(x, y1) == 0:
                                    values = values + self._available_vals(x, y1)
                        for solution in solutions:
                            if solution not in values:
                                self._set_cell_val(x, y, solution)
                                has_improved = True
                                break
                    # Check block
                    if not has_improved:
                        values = self._find_all_block_values_for_solve_sudoku(x, y)
                        for solution in solutions:
                            if solution not in values:
                                self._set_cell_val(x, y, solution)
                                has_improved = True
                                break
            is_solved = self._is_sudoku_valid()
            if is_solved:
                break
        # Restore original table
        count = 0
        for y in range(0, stt.elements_in_game_y):
            for x in range(0, stt.elements_in_game_x):
                self._board[y][x][0] = table[count]
                count += 1
        return is_solved
        
    def _find_all_block_values_for_solve_sudoku(self, x: int, y: int) -> list:
        # Find block occupied values
        vals_b = []
        start_pos_x = int(x / self._stt.elements_in_block_x) * self._stt.elements_in_block_x
        start_pos_y = int(y / self._stt.elements_in_block_y) * self._stt.elements_in_block_y
        for pos_y in range(start_pos_y, start_pos_y + self._stt.elements_in_block_y):
            for pos_x in range(start_pos_x, start_pos_x + self._stt.elements_in_block_x):
                if self._board[pos_y][pos_x][0] == 0 and pos_y != y and pos_x != x:
                    vals_b = vals_b + self._available_vals(pos_x, pos_y)
        return vals_b


    def _is_sudoku_valid(self):
        result = True
        for y in range(0, self._stt.elements_in_block_y):
            for x in range(0, self._stt.elements_in_block_x):
                cell = self._get_cell_val(x, y)
                vals = self._available_vals(x, y)
                if cell == 0:
                    result = False
                if vals:
                    if cell != vals[0]:
                        result = False
                else:
                    result = False
        return result



    @property
    def board(self) -> list:
        return self._board



