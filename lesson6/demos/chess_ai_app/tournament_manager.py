#!/usr/bin/env python3
"""
Tournament Manager for Chess LLM Arena
"""
import requests
import json
import time
import argparse

BASE_URL = "http://localhost:5000"

def create_tournament(players, rounds=1):
    """Create a tournament with specified players"""
    print(f"🏆 Creating tournament with {len(players)} players...")
    print(f"Players: {', '.join(players)}")
    
    all_games = []
    
    for round_num in range(rounds):
        print(f"\n🎯 Starting Round {round_num + 1}/{rounds}")
        
        # Create round-robin matches
        for i, white in enumerate(players):
            for j, black in enumerate(players):
                if i != j:
                    print(f"⚔️  Starting: {white} vs {black}")
                    
                    response = requests.post(f"{BASE_URL}/start_game", 
                                           json={
                                               "white_player": f"{white}-R{round_num+1}",
                                               "black_player": f"{black}-R{round_num+1}"
                                           })
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data['success']:
                            all_games.append(data['game_id'])
                            print(f"✅ Game started: {data['game_id'][:8]}")
                        else:
                            print(f"❌ Error: {data['error']}")
                    else:
                        print(f"❌ HTTP Error: {response.status_code}")
                    
                    time.sleep(1)  # Small delay between game starts
    
    return all_games

def monitor_tournament(duration=60):
    """Monitor tournament progress"""
    print(f"👀 Monitoring tournament for {duration} seconds...")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        response = requests.get(f"{BASE_URL}/leaderboard")
        
        if response.status_code == 200:
            leaderboard = response.json()
            
            print("\n" + "="*60)
            print("📊 LIVE LEADERBOARD")
            print("="*60)
            
            if leaderboard:
                # Sort by win rate
                sorted_players = sorted(leaderboard.items(), 
                                       key=lambda x: (x[1]['wins']/max(x[1]['games'], 1), x[1]['wins']), 
                                       reverse=True)
                
                print(f"{'Rank':<5} {'Player':<20} {'Games':<6} {'W':<4} {'L':<4} {'D':<4} {'Win%':<8}")
                print("-" * 60)
                
                for rank, (player, stats) in enumerate(sorted_players, 1):
                    win_rate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
                    print(f"{rank:<5} {player:<20} {stats['games']:<6} {stats['wins']:<4} {stats['losses']:<4} {stats['draws']:<4} {win_rate:<8.1f}")
            else:
                print("No games completed yet...")
        
        time.sleep(5)  # Update every 5 seconds
    
    print("\n🏁 Tournament monitoring completed!")

def quick_battle(player1="GPT-Alpha", player2="GPT-Beta"):
    """Start a quick battle between two players"""
    print(f"⚔️  Quick Battle: {player1} vs {player2}")
    
    response = requests.post(f"{BASE_URL}/start_game", 
                           json={
                               "white_player": player1,
                               "black_player": player2
                           })
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            game_id = data['game_id']
            print(f"✅ Battle started! Game ID: {game_id[:8]}")
            
            # Monitor the battle
            print("👀 Monitoring battle...")
            for i in range(30):  # Monitor for up to 30 iterations
                response = requests.get(f"{BASE_URL}/game/{game_id}")
                
                if response.status_code == 200:
                    game = response.json()
                    moves = len(game['moves'])
                    turn = game['current_turn']
                    status = game['status']
                    
                    print(f"Move {moves}: {turn.upper()} to play - Status: {status.upper()}")
                    
                    if status == 'finished':
                        result = game['result']
                        print(f"🎯 Battle finished! Result: {result.upper()}")
                        if result != 'draw':
                            winner = game['white_player'] if result == 'white' else game['black_player']
                            print(f"👑 Winner: {winner}")
                        break
                else:
                    print(f"❌ Error fetching game: {response.status_code}")
                    break
                
                time.sleep(2)  # Wait 2 seconds between checks
        else:
            print(f"❌ Error starting battle: {data['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chess LLM Tournament Manager')
    parser.add_argument('--mode', choices=['tournament', 'battle', 'monitor'], 
                       default='tournament', help='Mode to run')
    parser.add_argument('--players', nargs='+', 
                       default=['GPT-Magnus', 'GPT-Kasparov', 'GPT-Fischer', 'GPT-Tal'],
                       help='List of player names')
    parser.add_argument('--rounds', type=int, default=1, help='Number of rounds')
    parser.add_argument('--duration', type=int, default=60, help='Monitoring duration')
    parser.add_argument('--player1', default='GPT-Alpha', help='First player for battle')
    parser.add_argument('--player2', default='GPT-Beta', help='Second player for battle')
    
    args = parser.parse_args()
    
    print("🔥 Chess LLM Tournament Manager")
    print("=" * 50)
    
    if args.mode == 'tournament':
        games = create_tournament(args.players, args.rounds)
        print(f"\n🎮 Tournament created with {len(games)} games!")
        print("⏳ Waiting for games to start...")
        time.sleep(10)
        monitor_tournament(args.duration)
        
    elif args.mode == 'battle':
        quick_battle(args.player1, args.player2)
        
    elif args.mode == 'monitor':
        monitor_tournament(args.duration)
    
    print("\n✅ Tournament manager completed!")
    print("🌐 Visit http://localhost:5000 to see the live interface!")
