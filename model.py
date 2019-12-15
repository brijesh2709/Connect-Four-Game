import collections


NONE = 0
RED = 1
YELLOW = 2



BOARD_COLUMNS = 7
BOARD_ROWS = 6


GameState = collections.namedtuple('GameState', ['board', 'turn'])


class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass


class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass


def new_game() -> GameState:
    '''
    Returns a GameState representing a brand new game in which no
    moves have been made yet.
    '''
    return GameState(board = _new_game_board(), turn = RED)



def drop(game_state: GameState, column_number: int) -> GameState:
    _require_valid_column_number(column_number)
    _require_game_not_over(game_state)

    empty_row = _find_bottom_empty_row_in_column(game_state.board, column_number)

    if empty_row == -1:
        raise InvalidMoveError()

    else:
        new_board = _copy_game_board(game_state.board)
        new_board[column_number][empty_row] = game_state.turn
        new_turn = _opposite_turn(game_state.turn)
        return GameState(board = new_board, turn = new_turn)



def pop(game_state: GameState, column_number: int) -> GameState:

    _require_valid_column_number(column_number)
    _require_game_not_over(game_state)

    if game_state.turn == game_state.board[column_number][BOARD_ROWS - 1]:
        new_board = _copy_game_board(game_state.board)

        for row in range(BOARD_ROWS - 1, -1, -1):
            new_board[column_number][row] = new_board[column_number][row - 1]

        new_board[column_number][row] = NONE

        new_turn = _opposite_turn(game_state.turn)

        return GameState(board = new_board, turn = new_turn)

    else:
        raise InvalidMoveError()



def winner(game_state: GameState) -> int:
    '''
    Determines the winning player in the given game state, if any.
    If the red player has won, RED is returned; if the yellow player
    has won, YELLOW is returned; if no player has won yet, NONE is
    returned.
    '''
    winner = NONE
    
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS):
            if _winning_sequence_begins_at(game_state.board, col, row):
                if winner == NONE:
                    winner = game_state.board[col][row]
                elif winner != game_state.board[col][row]:

                    return _opposite_turn(game_state.turn)

    return winner
    

def _new_game_board() -> [[int]]:

    board = []

    for col in range(BOARD_COLUMNS):
        board.append([])
        for row in range(BOARD_ROWS):
            board[-1].append(NONE)

    return board



def _copy_game_board(board: [[int]]) -> [[int]]:
    '''Copies the given game board'''
    board_copy = []

    for col in range(BOARD_COLUMNS):
        board_copy.append([])
        for row in range(BOARD_ROWS):
            board_copy[-1].append(board[col][row])

    return board_copy



def _find_bottom_empty_row_in_column(board: [[int]], column_number: int) -> int:

    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[column_number][i] == NONE:
            return i

    return -1



def _opposite_turn(turn: str) -> str:
        if turn == RED:
        return YELLOW
    else:
        return RED



def _winning_sequence_begins_at(board: [[int]], col: int, row: int) -> bool:

    return _four_in_a_row(board, col, row, 0, 1) \
            or _four_in_a_row(board, col, row, 1, 1) \
            or _four_in_a_row(board, col, row, 1, 0) \
            or _four_in_a_row(board, col, row, 1, -1) \
            or _four_in_a_row(board, col, row, 0, -1) \
            or _four_in_a_row(board, col, row, -1, -1) \
            or _four_in_a_row(board, col, row, -1, 0) \
            or _four_in_a_row(board, col, row, -1, 1)
    


def _four_in_a_row(board: [[int]], col: int, row: int, coldelta: int, rowdelta: int) -> bool:
    '''
    Returns True if a winning sequence of pieces appears on the board
    beginning in the given column and row and extending in a direction
    specified by the coldelta and rowdelta
    '''
    start_cell = board[col][row]

    if start_cell == NONE:
        return False
    else:
        for i in range(1, 4):
            if not _is_valid_column_number(col + coldelta * i) \
                    or not _is_valid_row_number(row + rowdelta * i) \
                    or board[col + coldelta *i][row + rowdelta * i] != start_cell:
                return False
        return True
    


def _require_valid_column_number(column_number: int) -> None:
    if type(column_number) != int or not _is_valid_column_number(column_number):
        raise ValueError('column_number must be int between 0 and {}'.format(BOARD_COLUMNS - 1))



def _require_game_not_over(game_state: GameState) -> None:
    if winner(game_state) != NONE:
        raise GameOverError()



def _is_valid_column_number(column_number: int) -> bool:
    return 0 <= column_number < BOARD_COLUMNS



def _is_valid_row_number(row_number: int) -> bool:

    return 0 <= row_number < BOARD_ROWS
