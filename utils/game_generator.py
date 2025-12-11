import random
import string
from models.word import Word
from database.db import db

def generate_game_grid(level_id):
    # 1. Define Directions
    DIR_HORIZONTAL = (0, 1)
    DIR_VERTICAL   = (1, 0)
    DIR_DIAGONAL   = (1, 1)
    
    DIR_H_REVERSE  = (0, -1)
    DIR_V_REVERSE  = (-1, 0)
    DIR_D_REVERSE  = (-1, -1)
    
    DIR_D_BL_TR    = (-1, 1)
    DIR_D_TL_BR    = (1, -1)

    # 2. Configuration per level
    level_config = {
        1: {
            'grid_size': 8, 
            'word_count': 6, 
            'difficulty': 'easy',
            'directions': [DIR_HORIZONTAL, DIR_VERTICAL, DIR_DIAGONAL] 
        },
        2: {
            'grid_size': 10, 
            'word_count': 9, 
            'difficulty': 'medium',
            'directions': [
                DIR_HORIZONTAL, DIR_VERTICAL, DIR_DIAGONAL,
                DIR_H_REVERSE, DIR_V_REVERSE
            ] 
        },
        3: {
            'grid_size': 12, 
            'word_count': 12, 
            'difficulty': 'hard',
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

    # 3. Fetch Words logic
    words_query = []

    # --- NEW LOGIC FOR HARD LEVEL ---
    if level_id == 3:
        # Hard Level: Mix of 4 Easy, 4 Medium, 4 Hard
        # This makes it harder because short words are easily lost in a large grid
        
        # 1. Fetch 4 Easy
        easy_words = Word.query.filter(
            Word.difficulty == 'easy',
            db.func.length(Word.word) <= size
        ).order_by(db.func.random()).limit(3).all()

        # 2. Fetch 4 Medium
        medium_words = Word.query.filter(
            Word.difficulty == 'medium',
            db.func.length(Word.word) <= size
        ).order_by(db.func.random()).limit(3).all()

        # 3. Fetch 4 Hard
        hard_words = Word.query.filter(
            Word.difficulty == 'hard',
            db.func.length(Word.word) <= size
        ).order_by(db.func.random()).limit(6).all()

        # Combine and Shuffle
        words_query = easy_words + medium_words + hard_words
        random.shuffle(words_query)

        # Safety Fallback: If DB is empty, fill with random words
        if len(words_query) < 12:
            remaining = 12 - len(words_query)
            filler = Word.query.filter(db.func.length(Word.word) <= size)\
                .order_by(db.func.random()).limit(remaining).all()
            words_query.extend(filler)

    else:
        # --- STANDARD LOGIC FOR EASY/MEDIUM ---
        words_query = Word.query.filter(
            Word.difficulty == difficulty_level,
            db.func.length(Word.word) <= size
        ).order_by(db.func.random()).limit(config['word_count'] + 5).all()
        
        # Fallback
        if len(words_query) < config['word_count']:
            remaining = config['word_count'] - len(words_query)
            fallback_words = Word.query.filter(
                Word.difficulty != difficulty_level, 
                db.func.length(Word.word) <= size
            ).order_by(db.func.random()).limit(remaining).all()
            words_query.extend(fallback_words)

    # Extract uppercase strings
    candidate_words = [w.word.upper() for w in words_query]
    
    # Initialize empty grid
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    placed_words = []

    # 4. Place Words (Exhaustive Shuffle Method)
    for word in candidate_words:
        if len(placed_words) >= config['word_count']:
            break

        # Generate ALL possible positions (row, col, direction)
        possible_placements = []
        for d in allowed_directions:
            for r in range(size):
                for c in range(size):
                    possible_placements.append((r, c, d))
        
        # Shuffle for true randomness
        random.shuffle(possible_placements)

        # Try placements until one fits
        for r, c, d in possible_placements:
            if can_place_word(grid, word, r, c, d, size):
                place_word(grid, word, r, c, d)
                placed_words.append(word)
                break 

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
    
    end_row = row + (len(word) - 1) * dr
    end_col = col + (len(word) - 1) * dc
    
    if not (0 <= end_row < size and 0 <= end_col < size):
        return False
        
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