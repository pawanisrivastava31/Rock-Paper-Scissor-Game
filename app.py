from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
import os
from database import GameDatabase

app = Flask(__name__)
CORS(app)

# Initialize database
db = GameDatabase()

CHOICES = ['rock', 'paper', 'scissors']

# Add this route to serve the frontend
@app.route('/')
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, path)

def determine_winner(player_choice, computer_choice):
    """Determine the winner of the game"""
    if player_choice == computer_choice:
        return 'draw'
    
    winning_combinations = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    
    if winning_combinations[player_choice] == computer_choice:
        return 'player'
    else:
        return 'computer'

@app.route('/api/play', methods=['POST'])
def play():
    """Handle a game round"""
    data = request.get_json()
    player_choice = data.get('choice', '').lower()
    
    if player_choice not in CHOICES:
        return jsonify({'error': 'Invalid choice'}), 400
    
    computer_choice = random.choice(CHOICES)
    result = determine_winner(player_choice, computer_choice)
    
    db.update_stats(result)
    db.add_game_history(player_choice, computer_choice, result)
    
    stats = db.get_stats()
    
    return jsonify({
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result,
        'stats': stats
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current statistics"""
    stats = db.get_stats()
    return jsonify(stats)

@app.route('/api/reset', methods=['POST'])
def reset_stats():
    """Reset all statistics"""
    db.reset_stats()
    stats = db.get_stats()
    return jsonify({
        'message': 'Statistics reset successfully',
        'stats': stats
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
