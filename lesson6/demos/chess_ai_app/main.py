from flask import Flask, request, jsonify, render_template_string, send_file, redirect, url_for
from markupsafe import Markup
from openai import AzureOpenAI
import os
import dotenv
import chess
import chess.pgn
import json
import threading
import time
import requests
import uuid
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()

AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
TTS_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_BSMP24")
TTS_KEY = os.getenv("AZURE_OPENAI_API_KEY_BSMP24")
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

# Demo game data - Famous game: Morphy vs Count Isouard and Duke of Brunswick (1858)
DEMO_GAME = {
    "id": "demo_game_morphy_1858",
    "white_player": "GPT-Morphy",
    "black_player": "GPT-Duke",
    "moves": [
        {"move": "e4", "san": "e4", "player": "white", "time": "2024-01-15 10:00:00"},
        {"move": "e5", "san": "e5", "player": "black", "time": "2024-01-15 10:00:05"},
        {"move": "Nf3", "san": "Nf3", "player": "white", "time": "2024-01-15 10:00:10"},
        {"move": "d6", "san": "d6", "player": "black", "time": "2024-01-15 10:00:15"},
        {"move": "d4", "san": "d4", "player": "white", "time": "2024-01-15 10:00:20"},
        {"move": "Bg4", "san": "Bg4", "player": "black", "time": "2024-01-15 10:00:25"},
        {"move": "dxe5", "san": "dxe5", "player": "white", "time": "2024-01-15 10:00:30"},
        {"move": "Bxf3", "san": "Bxf3", "player": "black", "time": "2024-01-15 10:00:35"},
        {"move": "Qxf3", "san": "Qxf3", "player": "white", "time": "2024-01-15 10:00:40"},
        {"move": "dxe5", "san": "dxe5", "player": "black", "time": "2024-01-15 10:00:45"},
        {"move": "Bc4", "san": "Bc4", "player": "white", "time": "2024-01-15 10:00:50"},
        {"move": "Nf6", "san": "Nf6", "player": "black", "time": "2024-01-15 10:00:55"},
        {"move": "Qb3", "san": "Qb3", "player": "white", "time": "2024-01-15 10:01:00"},
        {"move": "Qe7", "san": "Qe7", "player": "black", "time": "2024-01-15 10:01:05"},
        {"move": "Nc3", "san": "Nc3", "player": "white", "time": "2024-01-15 10:01:10"},
        {"move": "c6", "san": "c6", "player": "black", "time": "2024-01-15 10:01:15"},
        {"move": "Bg5", "san": "Bg5", "player": "white", "time": "2024-01-15 10:01:20"},
        {"move": "b5", "san": "b5", "player": "black", "time": "2024-01-15 10:01:25"},
        {"move": "Nxb5", "san": "Nxb5", "player": "white", "time": "2024-01-15 10:01:30"},
        {"move": "cxb5", "san": "cxb5", "player": "black", "time": "2024-01-15 10:01:35"},
        {"move": "Bxb5+", "san": "Bxb5+", "player": "white", "time": "2024-01-15 10:01:40"},
        {"move": "Nbd7", "san": "Nbd7", "player": "black", "time": "2024-01-15 10:01:45"},
        {"move": "O-O-O", "san": "O-O-O", "player": "white", "time": "2024-01-15 10:01:50"},
        {"move": "Rd8", "san": "Rd8", "player": "black", "time": "2024-01-15 10:01:55"},
        {"move": "Rxd7", "san": "Rxd7", "player": "white", "time": "2024-01-15 10:02:00"},
        {"move": "Rxd7", "san": "Rxd7", "player": "black", "time": "2024-01-15 10:02:05"},
        {"move": "Rd1", "san": "Rd1", "player": "white", "time": "2024-01-15 10:02:10"},
        {"move": "Qe6", "san": "Qe6", "player": "black", "time": "2024-01-15 10:02:15"},
        {"move": "Bxd7+", "san": "Bxd7+", "player": "white", "time": "2024-01-15 10:02:20"},
        {"move": "Nxd7", "san": "Nxd7", "player": "black", "time": "2024-01-15 10:02:25"},
        {"move": "Qb8+", "san": "Qb8+", "player": "white", "time": "2024-01-15 10:02:30"},
        {"move": "Nxb8", "san": "Nxb8", "player": "black", "time": "2024-01-15 10:02:35"},
        {"move": "Rd8#", "san": "Rd8#", "player": "white", "time": "2024-01-15 10:02:40"}
    ],
    "result": "1-0",
    "status": "completed",
    "winner": "GPT-Morphy",
    "game_type": "Demo Match",
    "start_time": "2024-01-15 10:00:00",
    "end_time": "2024-01-15 10:02:40"
}

# Initialize demo game in leaderboard
def initialize_demo_leaderboard():
    """Add demo game results to leaderboard"""
    if "GPT-Morphy" not in leaderboard:
        leaderboard["GPT-Morphy"] = {"wins": 1, "losses": 0, "draws": 0, "games": 1}
    if "GPT-Duke" not in leaderboard:
        leaderboard["GPT-Duke"] = {"wins": 0, "losses": 1, "draws": 0, "games": 1}

# Initialize demo data
initialize_demo_leaderboard()

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
    
    # Different AI personalities
    personalities = {
        "GPT-Aggressive": "I play aggressively, looking for tactical opportunities and attacks.",
        "GPT-Defensive": "I prioritize piece safety and solid positional play.",
        "GPT-Balanced": "I balance tactical and positional considerations."
    }
    
    personality = personalities.get(player_name, "I play solid, strategic chess.")
    
    prompt = f"""You are playing chess as {player_name}. {personality}
    
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

def generate_commentary(game_data):
    """Generate exciting sports commentary for a chess game"""
    moves_summary = ", ".join([f"{i+1}. {move['san']}" for i, move in enumerate(game_data['moves'][:10])])
    
    prompt = f"""
    You are an exciting sports commentator for a chess match between {game_data['white_player']} and {game_data['black_player']}. 
    
    The game ended with {game_data['winner']} winning. Key moves included: {moves_summary}
    
    Create an exciting 30-second sports commentary recap of this chess match. Make it dramatic and engaging like a sports highlight reel.
    Include:
    - Dramatic opening
    - Key tactical moments
    - The decisive winning sequence
    - Victory celebration
    
    Keep it under 200 words and make it sound like a real sports broadcaster covering an epic chess battle!
    """
    
    try:
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an enthusiastic sports commentator specializing in chess matches."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"What an incredible match between {game_data['white_player']} and {game_data['black_player']}! After an intense battle, {game_data['winner']} emerged victorious with brilliant tactical play!"

def generate_audio_commentary(text, filename="commentary.mp3"):
    """Generate audio commentary using Azure TTS"""
    if not TTS_ENDPOINT or not TTS_KEY:
        return None
        
    url = f"{TTS_ENDPOINT}/openai/deployments/tts/audio/speech?api-version=2024-02-15-preview"
    headers = {
        "api-key": TTS_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "tts",
        "input": text,
        "voice": "onyx"  # Deep, dramatic voice for sports commentary
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            return filename
        else:
            print(f"TTS request failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"TTS error: {e}")
        return None

def render_chess_board(board, highlight_squares=None):
    """Render a chess board as HTML"""
    if highlight_squares is None:
        highlight_squares = []
    
    pieces = {
        'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
        'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
    }
    
    html = '<table class="chess-board">'
    
    for rank in range(8):
        html += '<tr>'
        for file in range(8):
            square = chess.square(file, 7-rank)
            piece = board.piece_at(square)
            piece_symbol = pieces.get(piece.symbol(), '') if piece else ''
            
            square_color = 'light' if (rank + file) % 2 == 0 else 'dark'
            highlight_class = ' highlight' if square in highlight_squares else ''
            
            html += f'<td class="square {square_color}{highlight_class}">{piece_symbol}</td>'
        html += '</tr>'
    
    html += '</table>'
    return Markup(html)

def render_board(board):
    """Render a simple ASCII chess board for main page"""
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

# HTML Templates
MAIN_HTML_TEMPLATE = """
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
            text-decoration: none;
        }
        .nav button:hover {
            transform: scale(1.05);
        }
        .nav a {
            text-decoration: none;
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
        .game-card.demo {
            border: 2px solid #FFD700;
            background: rgba(255, 215, 0, 0.2);
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
        .status-completed { color: #FFD700; }
        .move-list {
            max-height: 200px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
        }
        .demo-badge {
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: black;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }
        .replay-btn {
            background: linear-gradient(45deg, #9C27B0, #BA68C8);
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
        }
        .replay-btn:hover {
            transform: scale(1.05);
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
        
        function startTournament() {
            const players = ['GPT-Aggressive', 'GPT-Defensive', 'GPT-Balanced', 'GPT-Tactical'];
            
            fetch('/tournament', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({players: players})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Tournament started! ' + data.games + ' games created');
                    refreshPage();
                } else {
                    alert('Error starting tournament: ' + data.error);
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
            <button onclick="startTournament()">🏆 Tournament</button>
            <a href="/demo_replay"><button>🎬 Demo Replay</button></a>
        </div>
        
        <div class="game-grid">
            <div class="game-card">
                <h3>🎯 Start New Game</h3>
                <div class="form-group">
                    <label>White Player (LLM):</label>
                    <select id="white_player">
                        <option value="GPT-Aggressive">GPT-Aggressive</option>
                        <option value="GPT-Defensive">GPT-Defensive</option>
                        <option value="GPT-Balanced">GPT-Balanced</option>
                        <option value="GPT-Tactical">GPT-Tactical</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Black Player (LLM):</label>
                    <select id="black_player">
                        <option value="GPT-Defensive">GPT-Defensive</option>
                        <option value="GPT-Aggressive">GPT-Aggressive</option>
                        <option value="GPT-Balanced">GPT-Balanced</option>
                        <option value="GPT-Tactical">GPT-Tactical</option>
                    </select>
                </div>
                <button onclick="startNewGame()" style="width: 100%; padding: 15px; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border: none; border-radius: 10px; color: white; font-weight: bold; cursor: pointer;">
                    🚀 Start Battle!
                </button>
            </div>
            
            <!-- Demo Game Card -->
            <div class="game-card demo">
                <h3>🎬 Demo: The Opera Game <span class="demo-badge">HISTORIC</span></h3>
                <p><strong>White:</strong> {{ demo_game.white_player }}</p>
                <p><strong>Black:</strong> {{ demo_game.black_player }}</p>
                <p><strong>Status:</strong> <span class="status-{{ demo_game.status }}">{{ demo_game.status.upper() }}</span></p>
                <p><strong>Result:</strong> {{ demo_game.result }} - {{ demo_game.winner }} Wins!</p>
                <p><strong>Moves:</strong> {{ demo_game.moves|length }}</p>
                <p><strong>Type:</strong> {{ demo_game.game_type }}</p>
                
                <div class="move-list">
                    {% for move in demo_game.moves[-10:] %}
                    <div>{{ loop.index0 + 1 + (demo_game.moves|length - 10 if demo_game.moves|length > 10 else 0) }}. {{ move.san }}</div>
                    {% endfor %}
                </div>
                
                <a href="/demo_replay" class="replay-btn">🎥 Watch Full Replay</a>
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
                        <td>{{ player }} {% if player == 'GPT-Morphy' or player == 'GPT-Duke' %}<span class="demo-badge">DEMO</span>{% endif %}</td>
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

DEMO_REPLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess LLM Arena - Demo Replay</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .title {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #fff, #ffeb3b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
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
            text-decoration: none;
        }
        
        .nav button:hover {
            transform: scale(1.05);
        }
        
        .nav a {
            text-decoration: none;
        }
        
        .game-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
        }
        
        .player-card {
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            min-width: 150px;
        }
        
        .winner {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
        }
        
        .game-result {
            text-align: center;
            font-size: 1.5em;
            margin: 20px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chess-board {
            border: 3px solid #333;
            border-collapse: collapse;
            margin: 0 auto;
            background: #f0d9b5;
        }
        
        .chess-board td {
            width: 60px;
            height: 60px;
            text-align: center;
            vertical-align: middle;
            font-size: 2em;
            border: 1px solid #333;
            position: relative;
        }
        
        .chess-board .light {
            background-color: #f0d9b5;
        }
        
        .chess-board .dark {
            background-color: #b58863;
        }
        
        .moves-panel {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .move-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 12px;
            margin: 5px 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .move-item:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateX(5px);
        }
        
        .move-number {
            font-weight: bold;
            color: #ffeb3b;
        }
        
        .commentary-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .commentary-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .audio-controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .play-btn {
            background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .play-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        .commentary-text {
            font-size: 1.1em;
            line-height: 1.6;
            background: rgba(0, 0, 0, 0.2);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #ffeb3b;
        }
        
        .replay-controls {
            text-align: center;
            margin-top: 30px;
        }
        
        .replay-btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            color: white;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 0 10px;
        }
        
        .replay-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #ffeb3b;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        @keyframes highlight {
            0%, 100% { background-color: rgba(255, 235, 59, 0.3); }
            50% { background-color: rgba(255, 235, 59, 0.6); }
        }
        
        .highlight {
            animation: highlight 1s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">♟️ Chess LLM Arena</h1>
            <p class="subtitle">Epic Battle Replay: The Opera Game Reimagined</p>
        </div>
        
        <div class="nav">
            <a href="/"><button>🏠 Home</button></a>
            <button onclick="window.location.reload()">🔄 Refresh</button>
            <button onclick="generateNewCommentary()">🎤 New Commentary</button>
        </div>
        
        <div class="game-info">
            <div class="player-card">
                <h3>🤖 {{ game.white_player }}</h3>
                <p>Playing White</p>
            </div>
            <div class="game-result">
                <strong>{{ game.result }}</strong><br>
                <span style="font-size: 0.8em;">{{ game.winner }} Wins!</span>
            </div>
            <div class="player-card winner">
                <h3>🏆 {{ game.black_player }}</h3>
                <p>Playing Black</p>
            </div>
        </div>
        
        <div class="main-content">
            <div class="board-section">
                <h3 style="text-align: center; margin-bottom: 20px;">Final Position</h3>
                {{ board_html }}
            </div>
            
            <div class="moves-panel">
                <h3>Game Moves</h3>
                {% for move in game.moves %}
                <div class="move-item">
                    <span class="move-number">{{ loop.index }}.</span>
                    <span>{{ move.san }}</span>
                    <span style="font-size: 0.8em; opacity: 0.7;">{{ move.player }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="commentary-section">
            <div class="commentary-header">
                <h3>🎙️ Live Commentary</h3>
                <div class="audio-controls">
                    {% if audio_file %}
                    <button class="play-btn" onclick="playCommentary()">🔊 Play Commentary</button>
                    <audio id="commentary-audio" src="/audio/{{ audio_file }}" style="display: none;"></audio>
                    {% endif %}
                    <button class="play-btn" onclick="generateNewCommentary()" style="background: linear-gradient(45deg, #9C27B0, #BA68C8); margin-left: 10px;">🎤 Generate New Commentary</button>
                </div>
            </div>
            <div class="commentary-text" id="commentary-text">
                {{ commentary }}
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{{ game.moves|length }}</div>
                <div class="stat-label">Total Moves</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">2:40</div>
                <div class="stat-label">Game Duration</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ game.game_type }}</div>
                <div class="stat-label">Match Type</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">Checkmate</div>
                <div class="stat-label">Game End</div>
            </div>
        </div>
        
        <div class="replay-controls">
            <button class="replay-btn" onclick="window.location.reload()">🔄 Watch Again</button>
            <button class="replay-btn" onclick="window.location.href='/'">🏠 Back to Arena</button>
            <button class="replay-btn" onclick="alert('Feature coming soon!')">📊 Full Analysis</button>
        </div>
    </div>
    
    <script>
        function playCommentary() {
            const audio = document.getElementById('commentary-audio');
            if (audio) {
                audio.play();
            }
        }
        
        function generateNewCommentary() {
            const button = event.target;
            const originalText = button.textContent;
            button.textContent = '🎤 Generating...';
            button.disabled = true;
            
            fetch('/generate_commentary')
                .then(response => response.json())
                .then(data => {
                    // Update commentary text
                    document.getElementById('commentary-text').textContent = data.commentary;
                    
                    // Update audio if available
                    if (data.audio_file) {
                        const audio = document.getElementById('commentary-audio');
                        if (audio) {
                            audio.src = '/audio/' + data.audio_file;
                        }
                    }
                    
                    button.textContent = originalText;
                    button.disabled = false;
                })
                .catch(error => {
                    console.error('Error generating commentary:', error);
                    button.textContent = originalText;
                    button.disabled = false;
                });
        }
        
        // Add some interactive effects
        document.querySelectorAll('.move-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                item.style.background = 'rgba(255, 235, 59, 0.3)';
                setTimeout(() => {
                    item.style.background = 'rgba(255, 255, 255, 0.1)';
                }, 500);
            });
        });
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return render_template_string(MAIN_HTML_TEMPLATE, 
                                games=games, 
                                leaderboard=leaderboard, 
                                render_board=render_board,
                                demo_game=DEMO_GAME)

@app.route('/demo_replay')
def demo_replay():
    """Demo replay page with commentary"""
    
    # Use default commentary text for demo
    default_commentary = """
    Ladies and gentlemen, what an absolutely SPECTACULAR display of chess mastery! 
    GPT-Morphy comes out swinging with the classic King's Pawn opening, and GPT-Duke responds in kind. 
    But watch this - Morphy's knight to f3 sets up a tactical storm that's about to shake the very foundations of this match!
    
    The tension builds as pieces clash in the center, but it's Morphy's brilliant bishop sacrifice that turns the tide! 
    With surgical precision, the white pieces coordinate like a well-oiled machine. 
    And THERE IT IS! The devastating queen sacrifice followed by that thunderous rook checkmate on d8! 
    
    CHECKMATE! What a performance! GPT-Morphy has delivered a masterpiece that would make the chess immortals weep with joy!
    """
    
    # Check if demo_commentary.mp3 exists, otherwise set to None
    audio_file = "demo_commentary.mp3" if os.path.exists("demo_commentary.mp3") else None
    
    # Reconstruct the game board at the final position
    board = chess.Board()
    for move_data in DEMO_GAME['moves']:
        try:
            move = board.parse_san(move_data['san'])
            board.push(move)
        except:
            pass
    
    final_board_html = render_chess_board(board)
    
    return render_template_string(DEMO_REPLAY_TEMPLATE, 
                                game=DEMO_GAME, 
                                board_html=final_board_html,
                                commentary=default_commentary,
                                audio_file=audio_file)

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
        players = data.get('players', ['GPT-Aggressive', 'GPT-Defensive', 'GPT-Balanced', 'GPT-Tactical'])
        
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
                    
                    # Start each game with a small delay
                    def delayed_start(gid):
                        time.sleep(i * 2)  # Stagger game starts
                        play_game_auto(gid)
                    
                    game_thread = threading.Thread(target=delayed_start, args=(game_id,))
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

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve audio files"""
    try:
        return send_file(filename, as_attachment=False)
    except:
        return "Audio file not found", 404

@app.route('/generate_commentary')
def generate_new_commentary():
    """Generate new commentary for the demo game"""
    commentary_text = generate_commentary(DEMO_GAME)
    audio_file = generate_audio_commentary(commentary_text, "demo_commentary.mp3")
    
    return jsonify({
        'commentary': commentary_text,
        'audio_file': audio_file
    })

if __name__ == '__main__':
    print("🏆 Chess LLM Arena - Full Application Starting...")
    print("🏠 Main Arena available at: http://localhost:5000")
    print("🎬 Demo replay available at: http://localhost:5000/demo_replay")
    print("🎙️ Commentary system ready!")
    print("🎯 Features: Live games, tournaments, demo replay, leaderboard")
    app.run(debug=True, host='0.0.0.0', port=5000)
