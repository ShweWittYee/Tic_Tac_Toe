"""Tic-Tac-Toe rules and reversible board operations."""
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
WINNING_LINES = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))


class TicTacToe:
    def __init__(self, board=None, current_player=None):
        self.board = list(board) if board is not None else [EMPTY] * 9
        if len(self.board) != 9 or any(cell not in (EMPTY, PLAYER_X, PLAYER_O) for cell in self.board):
            raise ValueError('Board must contain nine X, O or space cells.')
        self.current_player = current_player or (PLAYER_X if self.board.count(PLAYER_X) <= self.board.count(PLAYER_O) else PLAYER_O)
        if self.current_player not in (PLAYER_X, PLAYER_O):
            raise ValueError('Player must be X or O.')
        self._history = []

    def get_available_moves(self):
        return [pos for pos, cell in enumerate(self.board) if cell == EMPTY]

    def is_valid_move(self, pos):
        return type(pos) is int and 0 <= pos < 9 and self.board[pos] == EMPTY and not self.is_game_over()

    def make_move(self, pos, player=None):
        player = self.current_player if player is None else player
        if player not in (PLAYER_X, PLAYER_O) or not self.is_valid_move(pos):
            return False
        self._history.append((pos, self.current_player))
        self.board[pos] = player
        self.current_player = PLAYER_O if player == PLAYER_X else PLAYER_X
        return True

    def undo_move(self, pos):
        if type(pos) is not int or not 0 <= pos < 9:
            raise ValueError('Position must be an integer from 0 to 8.')
        if self.board[pos] == EMPTY:
            return
        if self._history and self._history[-1][0] != pos:
            raise ValueError('Undo moves in reverse order.')
        self.current_player = self._history.pop()[1] if self._history else self.board[pos]
        self.board[pos] = EMPTY

    def get_winning_line(self):
        return next((line for line in WINNING_LINES if self.board[line[0]] != EMPTY and all(self.board[pos] == self.board[line[0]] for pos in line)), None)

    def check_winner(self):
        line = self.get_winning_line()
        return self.board[line[0]] if line else None

    def is_draw(self):
        return EMPTY not in self.board and self.check_winner() is None

    def is_game_over(self):
        return self.check_winner() is not None or self.is_draw()
