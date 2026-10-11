"""Random, priority heuristic, and depth-scored alpha-beta agents."""
import random
from time import perf_counter
from game import TicTacToe, PLAYER_X, PLAYER_O


class Agent:
    def __init__(self, player):
        if player not in (PLAYER_X, PLAYER_O):
            raise ValueError('Player must be X or O.')
        self.player = self.symbol = player
        self.opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
        self.reset_stats()

    def reset_stats(self):
        self.nodes_visited = 0
        self.cutoffs = 0
        self.candidate_scores = {}
        self.elapsed_ms = 0

    def get_move(self, game):
        raise NotImplementedError

    def choose_move(self, game):
        return self.get_move(game)

    def statistics(self):
        return dict(nodes_visited=self.nodes_visited, cutoffs=self.cutoffs,
                    candidate_scores=self.candidate_scores, elapsed_ms=round(self.elapsed_ms, 2))


class RandomAgent(Agent):
    def get_move(self, game):
        self.reset_stats()
        if game.is_game_over():
            return None
        moves = game.get_available_moves()
        # Candidate scoring disabled for RandomAgent.
        # self.candidate_scores = {move: round(1 / len(moves), 3) for move in moves}
        return random.choice(moves)


class HeuristicAgent(Agent):
    def find_winning_move(self, game, player):
        for move in game.get_available_moves():
            game.make_move(move, player)
            try:
                self.nodes_visited += 1
                wins = game.check_winner() == player
            finally:
                game.undo_move(move)
            if wins:
                return move
        return None

    def get_move(self, game):
        self.reset_stats()
        if game.is_game_over():
            return None
        start = perf_counter()
        # Candidate scoring disabled for HeuristicAgent.
        # for move in game.get_available_moves():
        #     # Priority ranks, rather than minimax utilities.
        #     score = 3 if move == 4 else 2 if move in (0, 2, 6, 8) else 1
        #     for player, priority in ((self.opponent, 4), (self.player, 5)):
        #         game.make_move(move, player)
        #         try:
        #             self.nodes_visited += 1
        #             if game.check_winner() == player:
        #                 score = priority
        #         finally:
        #             game.undo_move(move)
        #     self.candidate_scores[move] = score
        # best = max(self.candidate_scores.values())
        # move = random.choice([move for move, score in self.candidate_scores.items() if score == best])

        # Apply the priority rules directly, without computing scores.
        move = self.find_winning_move(game, self.player)
        if move is None:
            move = self.find_winning_move(game, self.opponent)
        if move is None:
            available = game.get_available_moves()
            if 4 in available:
                move = 4
            else:
                corners = [pos for pos in (0, 2, 6, 8) if pos in available]
                move = random.choice(corners or available)
        self.elapsed_ms = (perf_counter() - start) * 1000
        return move


class MinimaxAgent(Agent):
    def __init__(self, player, use_alpha_beta=True):
        super().__init__(player)
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, game):
        self.reset_stats()
        if game.is_game_over():
            return None
        start = perf_counter()
        best_score, best_move = float('-inf'), None
        for move in game.get_available_moves():
            game.make_move(move, self.player)
            try:
                # Fresh windows give exact scores for every candidate.
                score = self.minimax(game, 0, False, float('-inf'), float('inf'))
            finally:
                game.undo_move(move)
            self.candidate_scores[move] = score
            if score > best_score:
                best_score, best_move = score, move
        self.elapsed_ms = (perf_counter() - start) * 1000
        return best_move

    def minimax(self, game, depth, maximizing, alpha=float('-inf'), beta=float('inf')):
        self.nodes_visited += 1
        winner = game.check_winner()
        if winner == self.player:
            return 10 - depth
        if winner == self.opponent:
            return depth - 10
        if game.is_draw():
            return 0
        best = float('-inf') if maximizing else float('inf')
        player = self.player if maximizing else self.opponent
        for move in game.get_available_moves():
            game.make_move(move, player)
            try:
                score = self.minimax(game, depth + 1, not maximizing, alpha, beta)
            finally:
                game.undo_move(move)
            if maximizing:
                best = max(best, score)
                alpha = max(alpha, best)
            else:
                best = min(best, score)
                beta = min(beta, best)
            if self.use_alpha_beta and alpha >= beta:
                self.cutoffs += 1
                break
        return best


def simulate_match(agent1, agent2, num_games=100, progress_callback=None):
    """Keep agents' assigned symbols; report cumulative results after each game."""
    if type(num_games) is not int or num_games < 1:
        raise ValueError('num_games must be a positive integer.')
    if agent1.player == agent2.player:
        raise ValueError('Match agents must use different symbols.')
    agents = {agent1.player: agent1, agent2.player: agent2}
    result = dict(agent1_wins=0, agent2_wins=0, draws=0, games_played=0,
                  agent1_win_rate=0, agent2_win_rate=0, draw_rate=0)
    for _ in range(num_games):
        game = TicTacToe()
        while not game.is_game_over():
            move = agents[game.current_player].get_move(game)
            if not game.make_move(move):
                raise ValueError('Agent returned an illegal move.')
        winner = game.check_winner()
        key = 'draws' if winner is None else 'agent1_wins' if winner == agent1.player else 'agent2_wins'
        result[key] += 1
        result['games_played'] += 1
        for count, rate in (('agent1_wins', 'agent1_win_rate'), ('agent2_wins', 'agent2_win_rate'), ('draws', 'draw_rate')):
            result[rate] = round(result[count] / result['games_played'] * 100, 2)
        if progress_callback:
            progress_callback(dict(result))
    return result
