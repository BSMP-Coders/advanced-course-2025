from flask import Flask, request, jsonify, render_template_string
from markupsafe import Markup
from openai import AzureOpenAI
import os
import dotenv
import chess
import chess.pgn
import json
import threading
import time
from datetime import datetime
import uuid

# Load environment variables
dotenv.load_dotenv()

AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_NAME = "gpt-35-turbo"

app = Flask(__name__)

openai_client = AzureOpenAI(
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT,
    api_version="2024-05-01-preview",
)

# Global game state
games = {}
tournaments = {}
leaderboard = {}
active_games = []

class ChessGame:
    def __init__(self, game_id, white_player, black_player):
        self.id = game_id
        self.board = chess.Board()
        self.white_player = white_player
        self.black_player = black_player
        self.moves = []
        self.status = "active"
        self.result = None
        self.start_time = datetime.now()
        self.current_turn = "white"
        
    def make_move(self, move_str):
        try:
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.moves.append(move_str)
                self.current_turn = "black" if self.current_turn == "white" else "white"
                
                # Check game status
                if self.board.is_checkmate():
                    self.status = "finished"
                    self.result = "white" if self.board.turn == chess.BLACK else "black"
                elif self.board.is_stalemate() or self.board.is_insufficient_material():
                    self.status = "finished"
                    self.result = "draw"
                    
                return True
            return False
        except:
            return False
    
    def get_fen(self):
        return self.board.fen()
    
    def get_legal_moves(self):
        return [move.uci() for move in self.board.legal_moves]

def get_llm_move(game, player_name):
    """Get a chess move from the LLM"""
    board_fen = game.get_fen()
    legal_moves = game.get_legal_moves()
    
    # Create a detailed prompt for the LLM
    prompt = f"""You are playing chess as {player_name}. It's your turn.
    
Current board position (FEN): {board_fen}
Legal moves available: {', '.join(legal_moves)}

You are playing as {'White' if game.current_turn == 'white' else 'Black'}.

Please respond with ONLY the move in UCI format (e.g., e2e4, g1f3, etc.).
Choose a good strategic move from the legal moves list.
Do not include any explanation, just the move."""

    try:
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a chess grandmaster. Always respond with only a valid UCI move."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.7
        )
        
        move = response.choices[0].message.content.strip()
        
        # Validate the move
        if move in legal_moves:
            return move
        else:
            # If invalid, pick a random legal move
            import random
            return random.choice(legal_moves)
            
    except Exception as e:
        print(f"Error getting LLM move: {e}")
        # Return a random legal move as fallback
        import random
        return random.choice(legal_moves)

def play_game_auto(game_id):
    """Auto-play a game between two LLMs"""
    game = games[game_id]
    
    while game.status == "active":
        current_player = game.white_player if game.current_turn == "white" else game.black_player
        
        # Get move from LLM
        move = get_llm_move(game, current_player)
        
        # Make the move
        if game.make_move(move):
            print(f"Game {game_id}: {current_player} played {move}")
            time.sleep(1)  # Small delay between moves
        else:
            print(f"Invalid move {move} by {current_player}")
            break
    
    # Update leaderboard
    if game.result:
        if game.result == "white":
            update_leaderboard(game.white_player, "win")
            update_leaderboard(game.black_player, "loss")
        elif game.result == "black":
            update_leaderboard(game.black_player, "win")
            update_leaderboard(game.white_player, "loss")
        else:
            update_leaderboard(game.white_player, "draw")
            update_leaderboard(game.black_player, "draw")

def update_leaderboard(player, result):
    """Update player stats in leaderboard"""
    if player not in leaderboard:
        leaderboard[player] = {"wins": 0, "losses": 0, "draws": 0, "games": 0}
    
    leaderboard[player]["games"] += 1
    if result == "win":
        leaderboard[player]["wins"] += 1
    elif result == "loss":
        leaderboard[player]["losses"] += 1
    else:
        leaderboard[player]["draws"] += 1

# HTML Templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess LLM Arena</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3em;
            margin: 0;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .nav {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .nav button {
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .nav button:hover {
            transform: scale(1.05);
        }
        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .game-card {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        .game-card h3 {
            margin-top: 0;
            color: #FFD700;
        }
        .chess-board {
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
            background: #8B4513;
            border: 5px solid #654321;
            border-radius: 10px;
            font-family: monospace;
            font-size: 12px;
        }
        .board-row {
            display: flex;
        }
        .board-cell {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: #333;
        }
        .light { background: #F0D9B5; }
        .dark { background: #B58863; }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }
        .leaderboard {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        }
        .leaderboard table {
            width: 100%;
            border-collapse: collapse;
        }
        .leaderboard th, .leaderboard td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        }
        .leaderboard th {
            background: rgba(255, 255, 255, 0.1);
            color: #FFD700;
        }
        .status-active { color: #4ECDC4; }
        .status-finished { color: #FF6B6B; }
        .move-list {
            max-height: 200px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
        }
    </style>
    <script>
        function refreshPage() {
            location.reload();
        }
        
        function startNewGame() {
            const white = document.getElementById('white_player').value;
            const black = document.getElementById('black_player').value;
            
            fetch('/start_game', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({white_player: white, black_player: black})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Game started! Game ID: ' + data.game_id);
                    refreshPage();
                } else {
                    alert('Error starting game: ' + data.error);
                }
            });
        }
        
        // Auto-refresh every 5 seconds
        setInterval(refreshPage, 5000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>♟️ Chess LLM Arena ♟️</h1>
            <p>Watch AI models battle it out on the chessboard!</p>
        </div>
        
        <div class="nav">
            <button onclick="refreshPage()">🔄 Refresh</button>
            <button onclick="startNewGame()">🎮 New Game</button>
        </div>
        
        <div class="game-grid">
            <div class="game-card">
                <h3>🎯 Start New Game</h3>
                <div class="form-group">
                    <label>White Player (LLM):</label>
                    <input type="text" id="white_player" value="GPT-White" placeholder="Enter white player name">
                </div>
                <div class="form-group">
                    <label>Black Player (LLM):</label>
                    <input type="text" id="black_player" value="GPT-Black" placeholder="Enter black player name">
                </div>
                <button onclick="startNewGame()" style="width: 100%; padding: 15px; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border: none; border-radius: 10px; color: white; font-weight: bold; cursor: pointer;">
                    🚀 Start Battle!
                </button>
            </div>
            
            {% for game_id, game in games.items() %}
            <div class="game-card">
                <h3>⚔️ Game {{ game_id[:8] }}</h3>
                <p><strong>White:</strong> {{ game.white_player }}</p>
                <p><strong>Black:</strong> {{ game.black_player }}</p>
                <p><strong>Status:</strong> <span class="status-{{ game.status }}">{{ game.status.upper() }}</span></p>
                <p><strong>Turn:</strong> {{ game.current_turn.upper() }}</p>
                {% if game.result %}
                <p><strong>Result:</strong> {{ game.result.upper() }}</p>
                {% endif %}
                <p><strong>Moves:</strong> {{ game.moves|length }}</p>
                
                <div class="move-list">
                    {% for move in game.moves[-10:] %}
                    <div>{{ loop.index0 + 1 + (game.moves|length - 10 if game.moves|length > 10 else 0) }}. {{ move }}</div>
                    {% endfor %}
                </div>
                
                <div class="chess-board">
                    {{ render_board(game.board)|safe }}
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="leaderboard">
            <h2>🏆 Leaderboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Games</th>
                        <th>Wins</th>
                        <th>Losses</th>
                        <th>Draws</th>
                        <th>Win Rate</th>
                    </tr>
                </thead>
                <tbody>
                    {% for player, stats in leaderboard.items() %}
                    <tr>
                        <td>{{ player }}</td>
                        <td>{{ stats.games }}</td>
                        <td>{{ stats.wins }}</td>
                        <td>{{ stats.losses }}</td>
                        <td>{{ stats.draws }}</td>
                        <td>{{ "%.1f%%" % (stats.wins / stats.games * 100 if stats.games > 0 else 0) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

def render_board(board):
    """Render a simple ASCII chess board"""
    piece_symbols = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }
    
    board_html = ""
    for rank in range(7, -1, -1):  # Start from rank 8 down to 1
        board_html += '<div class="board-row">'
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            piece_char = piece_symbols.get(piece.symbol(), ' ') if piece else '&nbsp;'
            
            # Determine square color
            square_color = "light" if (file + rank) % 2 == 0 else "dark"
            
            board_html += f'<div class="board-cell {square_color}">{piece_char}</div>'
        board_html += '</div>'
    
    return Markup(board_html)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, games=games, leaderboard=leaderboard, render_board=render_board)

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        data = request.get_json()
        white_player = data.get('white_player', 'GPT-White')
        black_player = data.get('black_player', 'GPT-Black')
        
        game_id = str(uuid.uuid4())
        game = ChessGame(game_id, white_player, black_player)
        games[game_id] = game
        
        # Start the game in a separate thread
        game_thread = threading.Thread(target=play_game_auto, args=(game_id,))
        game_thread.daemon = True
        game_thread.start()
        
        return jsonify({'success': True, 'game_id': game_id})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/game/<game_id>')
def get_game(game_id):
    if game_id in games:
        game = games[game_id]
        return jsonify({
            'id': game.id,
            'white_player': game.white_player,
            'black_player': game.black_player,
            'status': game.status,
            'current_turn': game.current_turn,
            'result': game.result,
            'moves': game.moves,
            'fen': game.get_fen()
        })
    return jsonify({'error': 'Game not found'}), 404

@app.route('/leaderboard')
def get_leaderboard():
    return jsonify(leaderboard)

@app.route('/tournament', methods=['POST'])
def start_tournament():
    try:
        data = request.get_json()
        players = data.get('players', ['GPT-1', 'GPT-2', 'GPT-3', 'GPT-4'])
        
        tournament_id = str(uuid.uuid4())
        tournament_games = []
        
        # Create round-robin tournament
        for i, white in enumerate(players):
            for j, black in enumerate(players):
                if i != j:
                    game_id = str(uuid.uuid4())
                    game = ChessGame(game_id, white, black)
                    games[game_id] = game
                    tournament_games.append(game_id)
                    
                    # Start each game
                    game_thread = threading.Thread(target=play_game_auto, args=(game_id,))
                    game_thread.daemon = True
                    game_thread.start()
        
        tournaments[tournament_id] = {
            'id': tournament_id,
            'players': players,
            'games': tournament_games,
            'start_time': datetime.now().isoformat()
        }
        
        return jsonify({'success': True, 'tournament_id': tournament_id, 'games': len(tournament_games)})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
