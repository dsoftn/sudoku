class SudokuGameLogic():
    """Creates a sudoku table and determines the number of empty fields depending on
    the level of the game.

    Board is list size X * Y
    Board cell = [  value (int): Value of cell (1-4, 1-6 or 1-9)
                    predefined (bool): If true, it is shown on board
                    edited (bool): If true, user entered data in cell
                    correct (bool): If true, user data is correct ]
    """
    def __init__(self, setting_object: object):
        self._stt = setting_object
        self.active_game = False  # Indicates that game is created
        self._board = []  # Game board

    def start_game(self):
        self.active_game = True

    def _new_board(self):
        elements_x = self._stt.elements_in_game_x
        elements_y = self._stt.elements_in_game_y
        self._board = []
        for y in range(0, elements_y):
            x_list = []
            for x in range(0, elements_x):
                x_list.append([0, True, False, False])
            self._board.append(x_list)

        # Za potrebe testiranja
        self._board[1][2] = [5,False,True, False]

        return self._board