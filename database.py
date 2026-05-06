import sqlite3
from datetime import datetime

# ref: https://docs.python.org/3/library/sqlite3.html

DATABASE_FILE = "player.db"


def init_database():
    # Create tables if they don't exist
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE,
                  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Game scores table
    c.execute('''CREATE TABLE IF NOT EXISTS game_scores
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  list_name TEXT,
                  score INTEGER,
                  total INTEGER,
                  percentage INTEGER,
                  date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()


def create_user(username):
    #Create a new user, return user_id
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        # User already exists
        conn.close()
        return get_user_id(username)


def get_user_id(username):
    # Get user_id from username
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0]
    return None


def save_score(username, list_name, score, total):
    # Save a game score to the database
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Get or create user
    user_id = get_user_id(username)
    if not user_id:
        user_id = create_user(username)

    # Calculate percentage
    percentage = int((score / total) * 100) if total > 0 else 0

    # Insert score
    c.execute('''INSERT INTO game_scores 
                 (user_id, list_name, score, total, percentage) 
                 VALUES (?, ?, ?, ?, ?)''',
              (user_id, list_name, score, total, percentage))

    conn.commit()
    conn.close()

    print(f"✓ Score saved for {username}")


def get_user_stats(username):
    # Get all scores for a specific user
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    user_id = get_user_id(username)
    if not user_id:
        conn.close()
        return []

    c.execute('''SELECT list_name, score, total, percentage, date_played 
                 FROM game_scores 
                 WHERE user_id = ? 
                 ORDER BY date_played DESC''', (user_id,))

    results = c.fetchall()
    conn.close()
    return results


def get_leaderboard(list_name):
    # Get top scores for a specific word list
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute('''SELECT users.username, game_scores.score, game_scores.total, game_scores.percentage
                 FROM game_scores
                 JOIN users ON game_scores.user_id = users.id
                 WHERE game_scores.list_name = ?
                 ORDER BY game_scores.percentage DESC, game_scores.score DESC
                 LIMIT 10''', (list_name,))

    results = c.fetchall()
    conn.close()
    return results


def get_all_leaderboard():
    # Get top scores across all lists
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute('''SELECT users.username, 
                        SUM(game_scores.score) as total_score,
                        SUM(game_scores.total) as total_words,
                        ROUND(AVG(game_scores.percentage), 1) as avg_percentage
                 FROM game_scores
                 JOIN users ON game_scores.user_id = users.id
                 GROUP BY users.username
                 ORDER BY avg_percentage DESC, total_score DESC
                 LIMIT 10''')

    results = c.fetchall()
    conn.close()
    return results


def display_user_stats(username):
    # Display user's game history
    stats = get_user_stats(username)

    if not stats:
        print(f"No scores found for {username}")
        return

    print(f"\n{'=' * 60}")
    print(f"📊 STATS FOR {username.upper()}")
    print(f"{'=' * 60}")
    print(f"{'List':<20} {'Score':<10} {'Percentage':<12} {'Date':<15}")
    print(f"{'-' * 60}")

    for list_name, score, total, percentage, date_played in stats:
        print(f"{list_name:<20} {score}/{total:<8} {percentage}%{'':<8} {date_played[:10]}")

    print(f"{'=' * 60}\n")


def display_leaderboard(list_name=None):
    # Display leaderboard
    if list_name:
        results = get_leaderboard(list_name)
        title = f"LEADERBOARD - {list_name.upper()}"
    else:
        results = get_all_leaderboard()
        title = "OVERALL LEADERBOARD"

    if not results:
        print(f"No scores yet for {title}")
        return

    print(f"\n{'=' * 60}")
    print(f"🏆 {title}")
    print(f"{'=' * 60}")

    if list_name:
        print(f"{'Rank':<6} {'Player':<20} {'Score':<12} {'Percentage':<12}")
        print(f"{'-' * 60}")
        for i, (username, score, total, percentage) in enumerate(results, 1):
            print(f"{i:<6} {username:<20} {score}/{total:<10} {percentage}%")
    else:
        print(f"{'Rank':<6} {'Player':<20} {'Avg %':<12} {'Total Score':<12}")
        print(f"{'-' * 60}")
        for i, (username, total_score, total_words, avg_percentage) in enumerate(results, 1):
            print(f"{i:<6} {username:<20} {avg_percentage}%{'':<8} {total_score}/{total_words}")

    print(f"{'=' * 60}\n")