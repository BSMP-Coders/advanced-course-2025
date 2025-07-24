#!/usr/bin/env python3
"""
Test script for the Chess LLM Arena
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_start_game():
    """Test starting a single game"""
    print("🎮 Starting a new game...")
    
    response = requests.post(f"{BASE_URL}/start_game", 
                           json={
                               "white_player": "GPT-Alpha",
                               "black_player": "GPT-Beta"
                           })
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ Game started successfully! Game ID: {data['game_id']}")
            return data['game_id']
        else:
            print(f"❌ Error starting game: {data['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    return None

def test_tournament():
    """Test starting a tournament"""
    print("🏆 Starting a tournament...")
    
    players = ["GPT-Magnus", "GPT-Kasparov", "GPT-Fischer", "GPT-Tal"]
    
    response = requests.post(f"{BASE_URL}/tournament", 
                           json={"players": players})
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ Tournament started! Tournament ID: {data['tournament_id']}")
            print(f"📊 Total games: {data['games']}")
            return data['tournament_id']
        else:
            print(f"❌ Error starting tournament: {data['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    return None

def get_leaderboard():
    """Get current leaderboard"""
    print("📊 Fetching leaderboard...")
    
    response = requests.get(f"{BASE_URL}/leaderboard")
    
    if response.status_code == 200:
        leaderboard = response.json()
        print("\n🏆 Current Leaderboard:")
        print("-" * 50)
        print(f"{'Player':<15} {'Games':<6} {'Wins':<5} {'Losses':<7} {'Draws':<6} {'Win Rate':<8}")
        print("-" * 50)
        
        for player, stats in leaderboard.items():
            win_rate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
            print(f"{player:<15} {stats['games']:<6} {stats['wins']:<5} {stats['losses']:<7} {stats['draws']:<6} {win_rate:<8.1f}%")
    else:
        print(f"❌ HTTP Error: {response.status_code}")

def monitor_game(game_id):
    """Monitor a specific game"""
    print(f"👀 Monitoring game {game_id}...")
    
    for i in range(10):  # Monitor for 10 iterations
        response = requests.get(f"{BASE_URL}/game/{game_id}")
        
        if response.status_code == 200:
            game = response.json()
            print(f"Move {len(game['moves'])}: {game['current_turn']} to play - Status: {game['status']}")
            
            if game['status'] == 'finished':
                print(f"🎯 Game finished! Result: {game['result']}")
                break
        else:
            print(f"❌ Error fetching game: {response.status_code}")
            break
        
        time.sleep(2)  # Wait 2 seconds between checks

if __name__ == "__main__":
    print("🔥 Chess LLM Arena Test Suite")
    print("=" * 40)
    
    # Test starting a single game
    game_id = test_start_game()
    
    if game_id:
        print("\n⏳ Waiting 5 seconds before monitoring...")
        time.sleep(5)
        monitor_game(game_id)
    
    print("\n" + "=" * 40)
    
    # Test starting a tournament
    tournament_id = test_tournament()
    
    if tournament_id:
        print("\n⏳ Waiting 10 seconds for games to progress...")
        time.sleep(10)
        get_leaderboard()
    
    print("\n✅ Test suite completed!")
    print("🌐 Visit http://localhost:5000 to see the live interface!")
