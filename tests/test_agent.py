import os
import sys
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def get_modules():
    try:
        import game
        import agent
        return game, agent
    except ImportError as e:
        pytest.fail(f"Could not import game or agent module: {e}")


@pytest.mark.weight(5)
@pytest.mark.number("1.4")
def test_heuristic_agent_logic():
    """Verify Heuristic Agent takes immediate wins and blocks opponent wins"""
    gmod, amod = get_modules()
    TicTacToe = getattr(gmod, 'TicTacToe', None)
    PLAYER_X = getattr(gmod, 'PLAYER_X', 'X')
    PLAYER_O = getattr(gmod, 'PLAYER_O', 'O')
    EMPTY = getattr(gmod, 'EMPTY', ' ')
    HeuristicAgent = getattr(amod, 'HeuristicAgent', None)
    
    assert TicTacToe is not None and HeuristicAgent is not None, "TicTacToe or HeuristicAgent not found"

    agent_o = HeuristicAgent(player=PLAYER_O)

    # 1. Immediate win scenario for O at position 2
    # Board: O O _ | X X _ | _ _ _
    board_win = [
        PLAYER_O, PLAYER_O, EMPTY,
        PLAYER_X, PLAYER_X, EMPTY,
        EMPTY,    EMPTY,    EMPTY
    ]
    g_win = TicTacToe(board=board_win, current_player=PLAYER_O)
    move = agent_o.get_move(g_win)
    assert move == 2, f"Heuristic agent should have chosen winning move 2, got {move}"

    # 2. Immediate block scenario: X is threatening win at position 2
    # Board: X X _ | O _ _ | _ _ _
    board_block = [
        PLAYER_X, PLAYER_X, EMPTY,
        PLAYER_O, EMPTY,    EMPTY,
        EMPTY,    EMPTY,    EMPTY
    ]
    g_block = TicTacToe(board=board_block, current_player=PLAYER_O)
    move = agent_o.get_move(g_block)
    assert move == 2, f"Heuristic agent should have blocked move at 2, got {move}"


@pytest.mark.weight(15)
@pytest.mark.number("1.5")
def test_minimax_unbeatable_and_optimal():
    """Verify Minimax Agent makes optimal moves and is mathematically unbeatable"""
    gmod, amod = get_modules()
    TicTacToe = getattr(gmod, 'TicTacToe', None)
    PLAYER_X = getattr(gmod, 'PLAYER_X', 'X')
    PLAYER_O = getattr(gmod, 'PLAYER_O', 'O')
    EMPTY = getattr(gmod, 'EMPTY', ' ')
    RandomAgent = getattr(amod, 'RandomAgent', None)
    MinimaxAgent = getattr(amod, 'MinimaxAgent', None)
    simulate_match = getattr(amod, 'simulate_match', None)

    assert MinimaxAgent is not None and RandomAgent is not None and simulate_match is not None, "Agent functions/classes not found in agent.py"

    minimax_o = MinimaxAgent(player=PLAYER_O, use_alpha_beta=True)

    # 1. Immediate Win Priority
    board_win = [
        PLAYER_O, PLAYER_O, EMPTY,
        PLAYER_X, PLAYER_X, EMPTY,
        EMPTY,    EMPTY,    EMPTY
    ]
    g_win = TicTacToe(board=board_win, current_player=PLAYER_O)
    assert minimax_o.get_move(g_win) == 2

    # 2. Immediate Block Priority
    board_block = [
        PLAYER_X, PLAYER_X, EMPTY,
        PLAYER_O, EMPTY,    EMPTY,
        EMPTY,    EMPTY,    EMPTY
    ]
    g_block = TicTacToe(board=board_block, current_player=PLAYER_O)
    assert minimax_o.get_move(g_block) == 2

    # 3. Simulate 50 matches against RandomAgent: Minimax MUST NEVER LOSE
    random_agent = RandomAgent(player=PLAYER_X)
    results = simulate_match(agent1=minimax_o, agent2=random_agent, num_games=50)

    # agent2 (RandomAgent) wins must be strictly 0
    assert results["agent2_wins"] == 0, (
        f"Minimax Agent lost {results['agent2_wins']} games to Random Agent! "
        "Minimax must be strictly unbeatable."
    )
    print(f"Minimax vs Random simulation passed: {results['agent1_wins']} wins, {results['draws']} draws, 0 losses.")
