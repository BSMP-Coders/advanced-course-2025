from flask import Flask, request, jsonify, render_template_string, send_file
from markupsafe import Markup
from openai import AzureOpenAI
import os
import dotenv
import chess
import chess.pgn
import json
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

# Demo game data - Famous game: Morphy vs Count Isouard and Duke of Brunswick (1858)
DEMO_GAME = {
    "id": "demo_game_1",
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

@app.route('/')
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
    import os
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
    
    template = """
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
                <button class="replay-btn" onclick="alert('Feature coming soon!')">📊 Full Analysis</button>
                <button class="replay-btn" onclick="alert('Feature coming soon!')">🏆 More Matches</button>
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
    
    return render_template_string(template, 
                                game=DEMO_GAME, 
                                board_html=final_board_html,
                                commentary=default_commentary,
                                audio_file=audio_file)

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
    print("🏆 Chess LLM Arena Demo Starting...")
    print("📺 Demo replay available at: http://localhost:5000")
    print("🎙️ Commentary system ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)
