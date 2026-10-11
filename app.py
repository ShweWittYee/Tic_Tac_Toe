"""Flask controls: board rules and AI decisions stay in Python."""
import json
import os
import secrets
from flask import Flask, Response, jsonify, render_template, request, session, stream_with_context
from agent import RandomAgent, HeuristicAgent, MinimaxAgent, simulate_match
from game import TicTacToe

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
AGENTS = {'random': RandomAgent, 'heuristic': HeuristicAgent, 'minimax': MinimaxAgent}


def new_state(mode='human', x_agent='minimax', o_agent='minimax', human='X'):
    return dict(board=[' '] * 9, current_player='X', mode=mode,
                x_agent=x_agent, o_agent=o_agent, human=human, decision=None)


def load_game():
    state = session.get('game') or new_state()
    return state, TicTacToe(state['board'], state['current_player'])


def is_ai_turn(state, game):
    return state['mode'] == 'ai' or (state['mode'] == 'human' and game.current_player != state['human'])


def response_state(state, game):
    state['board'] = game.board.copy()
    state['current_player'] = game.current_player
    session['game'] = state
    finished = game.is_game_over()
    winner = game.check_winner()
    ai_turn = is_ai_turn(state, game) and not finished
    return dict(**state, winner=winner, winning_line=game.get_winning_line(),
                game_over=finished, ai_turn=ai_turn,
                legal_moves=game.get_available_moves() if not finished else [],
                can_play=not finished and not ai_turn,
                status=f'{winner} wins!' if winner else 'It is a draw.' if finished else
                       f'{game.current_player} to move' + (' · AI turn' if ai_turn else ' · choose a square'))


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/api/state')
def get_state():
    return jsonify(response_state(*load_game()))


@app.post('/api/new')
def reset():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Send a JSON object.'), 400
    mode, x_agent, o_agent, human = (data.get('mode', 'human'), data.get('x_agent', 'minimax'),
                                   data.get('o_agent', 'minimax'), data.get('human', 'X'))
    if (not all(isinstance(value, str) for value in (mode, x_agent, o_agent, human))
            or mode not in ('human', 'local', 'ai') or x_agent not in AGENTS
            or o_agent not in AGENTS or human not in ('X', 'O')):
        return jsonify(error='Invalid game configuration.'), 400
    return jsonify(response_state(new_state(mode, x_agent, o_agent, human), TicTacToe()))


@app.post('/api/move')
def move():
    state, game = load_game()
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Send a JSON object.'), 400
    if is_ai_turn(state, game) or not game.make_move(data.get('pos')):
        return jsonify(error='That move is not allowed.'), 400
    return jsonify(response_state(state, game))


@app.post('/api/step')
def step():
    state, game = load_game()
    if game.is_game_over() or not is_ai_turn(state, game):
        return jsonify(error='There is no AI turn to play.'), 400
    player = game.current_player
    kind = state['x_agent'] if player == 'X' else state['o_agent']
    agent = AGENTS[kind](player)
    pos = agent.get_move(game)
    state['decision'] = dict(player=player, kind=kind, selected_move=pos, **agent.statistics())
    game.make_move(pos)
    return jsonify(response_state(state, game))


@app.get('/api/simulate')
def benchmark():
    x_kind, o_kind = request.args.get('x', 'minimax'), request.args.get('o', 'random')
    try:
        count = int(request.args.get('games', '50'))
    except ValueError:
        return jsonify(error='Games must be an integer.'), 400
    if x_kind not in AGENTS or o_kind not in AGENTS or not 1 <= count <= 500:
        return jsonify(error='Choose valid agents and 1–500 games.'), 400

    @stream_with_context
    def stream():
        x_agent, o_agent = AGENTS[x_kind]('X'), AGENTS[o_kind]('O')
        totals = dict(agent1_wins=0, agent2_wins=0, draws=0, games_played=0)
        for index in range(count):
            result = simulate_match(x_agent, o_agent, 1)
            for key in totals:
                totals[key] += result[key]
            played = index + 1
            payload = dict(totals, total=count,
                           agent1_win_rate=round(totals['agent1_wins'] / played * 100, 2),
                           agent2_win_rate=round(totals['agent2_wins'] / played * 100, 2),
                           draw_rate=round(totals['draws'] / played * 100, 2))
            yield 'data: ' + json.dumps(payload) + '\n\n'
        yield 'event: done\ndata: {}\n\n'
    return Response(stream(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
