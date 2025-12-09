import sqlite3
from datetime import datetime

class GameDatabase:
    def __init__(self, db_name='game_stats.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_wins INTEGER DEFAULT 0,
                computer_wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                total_games INTEGER DEFAULT 0,
                last_updated TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_choice TEXT,
                computer_choice TEXT,
                result TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if total_games column exists, if not add it
        cursor.execute("PRAGMA table_info(game_stats)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'total_games' not in columns:
            cursor.execute('ALTER TABLE game_stats ADD COLUMN total_games INTEGER DEFAULT 0')
            # Update existing records
            cursor.execute('''
                UPDATE game_stats 
                SET total_games = player_wins + computer_wins + draws
            ''')
        
        # Initialize stats if table is empty
        cursor.execute('SELECT COUNT(*) FROM game_stats')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO game_stats (player_wins, computer_wins, draws, total_games, last_updated)
                VALUES (0, 0, 0, 0, ?)
            ''', (datetime.now(),))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get current game statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT player_wins, computer_wins, draws, total_games FROM game_stats WHERE id = 1')
        stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'player_wins': stats[0],
            'computer_wins': stats[1],
            'draws': stats[2],
            'total_games': stats[3]
        }
    
    def update_stats(self, result):
        """Update statistics based on game result"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if result == 'player':
            cursor.execute('''
                UPDATE game_stats 
                SET player_wins = player_wins + 1, 
                    total_games = total_games + 1,
                    last_updated = ?
                WHERE id = 1
            ''', (datetime.now(),))
        elif result == 'computer':
            cursor.execute('''
                UPDATE game_stats 
                SET computer_wins = computer_wins + 1, 
                    total_games = total_games + 1,
                    last_updated = ?
                WHERE id = 1
            ''', (datetime.now(),))
        else:  # draw
            cursor.execute('''
                UPDATE game_stats 
                SET draws = draws + 1, 
                    total_games = total_games + 1,
                    last_updated = ?
                WHERE id = 1
            ''', (datetime.now(),))
        
        conn.commit()
        conn.close()
    
    def add_game_history(self, player_choice, computer_choice, result):
        """Add a game to history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO game_history (player_choice, computer_choice, result)
            VALUES (?, ?, ?)
        ''', (player_choice, computer_choice, result))
        
        conn.commit()
        conn.close()
    
    def reset_stats(self):
        """Reset all statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE game_stats 
            SET player_wins = 0, computer_wins = 0, draws = 0, total_games = 0, last_updated = ?
            WHERE id = 1
        ''', (datetime.now(),))
        
        cursor.execute('DELETE FROM game_history')
        
        conn.commit()
        conn.close()
