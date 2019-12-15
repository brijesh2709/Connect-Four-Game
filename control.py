'''We import the model that is connect four and run the control.'''
import connectfour as cf

pop = False
size = 80

class control():
    '''This class deals as an interface between view and model.'''
    def __init__(self):
        '''In this method we define variables.'''
        self.board = cf._new_game_board()
        self.winner = 0
        self.columns_position = []
        self.turn = 1
        self.columns = cf.BOARD_COLUMNS
        self.rows = cf.BOARD_ROWS
        self.get_columns_position()

    def game_action(self, x, y):
        """Function to check user action to the board"""
        if y // cf.BOARD_ROWS > size:
            # Check if user select pop
            pop = True
        else:
            pop = False
        for i in range(len(self.columns_position)):
            # Check which column did the user select.
            j, k = self.columns_position[i]
            if j <= x <= k:
                self.action(i, pop)

    def change_board_size(self, col, row):
        '''If the user wants custom board, This method changes user board
        size for the user.'''
        cf.BOARD_COLUMNS = col
        cf.BOARD_ROWS = row
        self.columns = col
        self.rows = row
        self.board = cf._new_game_board()
        self.get_columns_position()

    def get_columns_position(self):
        """Function that get columns position by the size of the board"""
        self.columns_position = []
        for i in range(cf.BOARD_COLUMNS):
            self.columns_position.append((size * i, size * (i + 1)))

    def action(self, col, pop):
        """Function that change game board with user action."""
        if pop:
            try:
                # try to pop if the column if able to
                self.board, self.turn = cf.pop(self, col)
            except cf.InvalidMoveError:
                pass
                # if not able to just drop
                self.board, self.turn = cf.drop(self, col)
        else:
            try:
                self.board, self.turn = cf.drop(self, col)
            except cf.InvalidMoveError:
                pass
        # After each move check winner.
        self.winner = cf.winner(self)
