import random
import string
from models.word import Word
from database.db import db


# utils/game_generator.py
import random
import string

def generate_game_grid(level_id):
    level_config = {
        1: {'grid_size': 8, 'word_count': 6},
        2: {'grid_size': 10, 'word_count': 9},
        3: {'grid_size': 12, 'word_count': 12}
    }
    config = level_config.get(level_id, level_config[1])
    size = config['grid_size']

    # Get real words from DB
    words = Word.query.filter(
        db.func.length(Word.word) <= size
    ).order_by(db.func.random()).limit(config['word_count']).all()

    word_list = [w.word.upper() for w in words]
    grid = [[' ' for _ in range(size)] for _ in range(size)]

    # Place words horizontally (simple & reliable)
    for word in word_list:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            row = random.randint(0, size - 1)
            col = random.randint(0, size - len(word))
            can_place = all(grid[row][col + i] in (' ', word[i]) for i in range(len(word)))
            if can_place:
                for i, letter in enumerate(word):
                    grid[row][col + i] = letter
                placed = True
            attempts += 1

    # Fill empty cells
    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return {
        'grid': grid,
        'words': word_list
    }

def can_place_word(grid, word, row, col, direction, grid_size):
    # Implementation for checking if word can be placed
    pass


def place_word(grid, word, row, col, direction):
    # Implementation for placing word in grid
    pass