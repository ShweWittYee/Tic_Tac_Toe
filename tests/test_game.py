import os
import sys
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def get_game_module():
    try:
        import game
        return game
    except ImportError as e:
        pytest.fail(f"Could not import game.py: {e}")


@pytest.mark.weight(5)
@pytest.mark.number("1.2")
def test_board_initialization_and_moves():
    """Verify TicTacToe board initialization and move mechanics"""
    gmod = get_game_module()
    TicTacToe = getattr(gmod, 'TicTacToe', None)
    PLAYER_X = getattr(gmod, 'PLAYER_X', 'X')
    PLAYER_O = getattr(gmod, 'PLAYER_O', 'O')
    EMPTY = getattr(gmod, 'EMPTY', ' ')
    assert TicTacToe is not None, "TicTacToe class not found in game.py"

    game = TicTacToe()
    assert len(game.board) == 9
    assert all(c == EMPTY for c in game.board)
    assert len(game.get_available_moves()) == 9
    assert game.current_player == PLAYER_X

    # Make move 4 (center)
    assert game.is_valid_move(4) is True
    success = game.make_move(4)
    assert success is True
    assert game.board[4] == PLAYER_X
    assert game.current_player == PLAYER_O
    assert 4 not in game.get_available_moves()
    assert len(game.get_available_moves()) == 8

    # Invalid move on occupied square
    assert game.is_valid_move(4) is False
    assert game.make_move(4) is False

    # Undo move
    game.undo_move(4)
    assert game.board[4] == EMPTY
    assert game.current_player == PLAYER_X
    assert len(game.get_available_moves()) == 9


@pytest.mark.weight(5)
@pytest.mark.number("1.3")
def test_winning_and_draw_conditions():
    """Verify row, column, diagonal win detection and draw states"""
    gmod = get_game_module()
    TicTacToe = getattr(gmod, 'TicTacToe', None)
    PLAYER_X = getattr(gmod, 'PLAYER_X', 'X')
    PLAYER_O = getattr(gmod, 'PLAYER_O', 'O')
    EMPTY = getattr(gmod, 'EMPTY', ' ')
    assert TicTacToe is not None, "TicTacToe class not found in game.py"

    # 1. Row win
    row_win_board = [
        PLAYER_X, PLAYER_X, PLAYER_X,
        PLAYER_O, PLAYER_O, EMPTY,
        EMPTY,    EMPTY,    EMPTY
    ]
    g1 = TicTacToe(board=row_win_board)
    assert g1.check_winner() == PLAYER_X
    assert g1.get_winning_line() == (0, 1, 2)
    assert g1.is_game_over() is True

    # 2. Column win
    col_win_board = [
        PLAYER_O, PLAYER_X, EMPTY,
        PLAYER_O, PLAYER_X, EMPTY,
        PLAYER_O, EMPTY,    PLAYER_X
    ]
    g2 = TicTacToe(board=col_win_board)
    assert g2.check_winner() == PLAYER_O
    assert g2.get_winning_line() == (0, 3, 6)
    assert g2.is_game_over() is True

    # 3. Diagonal win
    diag_win_board = [
        PLAYER_X, PLAYER_O, EMPTY,
        PLAYER_O, PLAYER_X, EMPTY,
        EMPTY,    EMPTY,    PLAYER_X
    ]
    g3 = TicTacToe(board=diag_win_board)
    assert g3.check_winner() == PLAYER_X
    assert g3.get_winning_line() == (0, 4, 8)

    # 4. Draw board
    draw_board = [
        PLAYER_X, PLAYER_O, PLAYER_X,
        PLAYER_X, PLAYER_O, PLAYER_O,
        PLAYER_O, PLAYER_X, PLAYER_X
    ]
    g4 = TicTacToe(board=draw_board)
    assert g4.check_winner() is None
    assert g4.is_draw() is True
    assert g4.is_game_over() is True
