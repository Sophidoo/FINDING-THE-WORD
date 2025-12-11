import random
import string
from models.word import Word
from database.db import db

def generate_game_grid(level_id):
    # 1. Define Directions (Row Change, Col Change)
    DIR_HORIZONTAL = (0, 1)   # Right
    DIR_VERTICAL   = (1, 0)   # Down
    DIR_DIAGONAL   = (1, 1)   # Down-Right
    
    DIR_H_REVERSE  = (0, -1)  # Left
    DIR_V_REVERSE  = (-1, 0)  # Up
    DIR_D_REVERSE  = (-1, -1) # Up-Left
    
    DIR_D_BL_TR    = (-1, 1)  # Up-Right
    DIR_D_TL_BR    = (1, -1)  # Down-Left

    # 2. Configuration per level
    level_config = {
        1: {
            'grid_size': 8, 
            'word_count': 6, 
            'difficulty': 'easy',
            # Easy: Horizontal, Vertical, Diagonal
            'directions': [DIR_HORIZONTAL, DIR_VERTICAL, DIR_DIAGONAL] 
        },
        2: {
            'grid_size': 10, 
            'word_count': 9, 
            'difficulty': 'medium',
            # Medium: Easy + Reverse H/V
            'directions': [
                DIR_HORIZONTAL, DIR_VERTICAL, DIR_DIAGONAL,
                DIR_H_REVERSE, DIR_V_REVERSE
            ] 
        },
        3: {
            'grid_size': 12, 
            'word_count': 12, 
            'difficulty': 'hard',
            # Hard: Chaos (All 8 directions)
            'directions': [
                DIR_HORIZONTAL, DIR_VERTICAL, DIR_DIAGONAL,
                DIR_H_REVERSE, DIR_V_REVERSE, DIR_D_REVERSE,
                DIR_D_BL_TR, DIR_D_TL_BR
            ] 
        }
    }
    
    config = level_config.get(level_id, level_config[1])
    size = config['grid_size']
    difficulty_level = config['difficulty']
    allowed_directions = config['directions']

    # 3. Fetch Words (Strictly filtered by Difficulty)
    words_query = Word.query.filter(
        Word.difficulty == difficulty_level,
        db.func.length(Word.word) <= size
    ).order_by(db.func.random()).limit(config['word_count'] + 5).all()
    
    # Fallback if DB is empty for that difficulty
    if len(words_query) < config['word_count']:
        remaining = config['word_count'] - len(words_query)
        fallback_words = Word.query.filter(
            Word.difficulty != difficulty_level, 
            db.func.length(Word.word) <= size
        ).order_by(db.func.random()).limit(remaining).all()
        words_query.extend(fallback_words)

    candidate_words = [w.word.upper() for w in words_query]
    
    # Initialize empty grid
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    placed_words = []

    # 4. Place Words (Exhaustive Shuffle Method)
    for word in candidate_words:
        if len(placed_words) >= config['word_count']:
            break

        # A. Generate ALL possible positions (row, col, direction)
        possible_placements = []
        for d in allowed_directions:
            for r in range(size):
                for c in range(size):
                    possible_placements.append((r, c, d))
        
        # B. Shuffle them to ensure true randomness
        random.shuffle(possible_placements)

        # C. Try placements until one fits
        for r, c, d in possible_placements:
            if can_place_word(grid, word, r, c, d, size):
                place_word(grid, word, r, c, d)
                placed_words.append(word)
                break # Word placed, move to next word

    # 5. Fill Empty Cells
    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return {
        'grid': grid,
        'words': placed_words
    }

def can_place_word(grid, word, row, col, direction, size):
    """Checks if a word fits in the grid at the given position and direction."""
    dr, dc = direction
    
    # Check boundaries
    end_row = row + (len(word) - 1) * dr
    end_col = col + (len(word) - 1) * dc
    
    if not (0 <= end_row < size and 0 <= end_col < size):
        return False
        
    # Check collisions
    for i in range(len(word)):
        r, c = row + i * dr, col + i * dc
        if grid[r][c] != ' ' and grid[r][c] != word[i]:
            return False
            
    return True

def place_word(grid, word, row, col, direction):
    """Writes the word into the grid."""
    dr, dc = direction
    for i, letter in enumerate(word):
        grid[row + i * dr][col + i * dc] = letter