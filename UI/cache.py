# cache.py

import sqlite3
import pickle
from game import Game

# Global cache for nodes, shared between both AIs
node_cache = {}


def save_node(node, db_path='current_game.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS nodes (board_hash TEXT PRIMARY KEY, node BLOB)''')

    board_hash = str(hash(tuple(map(tuple, node.board))))
    serialized_node = pickle.dumps(node)

    cur.execute('''INSERT OR REPLACE INTO nodes (board_hash, node) VALUES (?, ?)''', (board_hash, serialized_node))
    conn.commit()
    conn.close()


def load_node(board, db_path='current_game.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    board_hash = str(hash(tuple(map(tuple, board))))
    cur.execute('SELECT node FROM nodes WHERE board_hash=?', (board_hash,))
    result = cur.fetchone()

    conn.close()
    if result:
        return pickle.loads(result[0])
    return None


def get_node(board, db_path='current_game.db'):
    # First, try getting the regular board hash
    board_hash = Game.GetBoardHash(board)

    # Check if the board hash is in cache
    if board_hash in node_cache:
        return node_cache[board_hash]

    # Try loading from the database
    node = load_node(board, db_path)
    if node:
        node_cache[board_hash] = node  # Add to cache if found
        return node

    # If not found, try getting the mirrored board hash
    mirrored_board_hash = Game.GetMirroredBoardHash(board)

    # Check if the mirrored board hash is in cache
    if mirrored_board_hash in node_cache:
        return node_cache[mirrored_board_hash]

    # Try loading the mirrored board from the database
    node = load_node(board, db_path)
    if node:
        node_cache[mirrored_board_hash] = node  # Add to cache if found
        return node

    # If neither the original nor the mirrored board is found, return None
    return None


def create_new_node(node, db_path='current_game.db'):
    # First, check if the node already exists by calling get_node
    board = node.board
    existing_node = get_node(board, db_path)

    if existing_node:
        return existing_node  # If the node already exists, return it

    # Add the new node to the cache using the board hash
    board_hash = Game.GetBoardHash(board)
    node_cache[board_hash] = node

    # Optionally save the new node to the database
    save_node(node, db_path)

    return node

