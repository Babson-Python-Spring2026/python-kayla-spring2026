"""
Homework: Reading Code with State / Transitions / Invariants (Tic-Tac-Toe)

This program brute-forces tic-tac-toe WITHOUT recursion.

What it actually counts:
- It explores all possible games where X starts and players alternate.
- The search STOPS as soon as someone wins (a terminal state).
- It also records full boards that end in a tie.
- It tracks UNIQUE *terminal* boards “up to symmetry” (rotations + reflections),
  meaning rotated/flipped versions are treated as the same terminal board.

YOUR TASKS:

RULE:  Do not change any executable code (no reformatting logic, no renaming variables, no moving lines). 
       Only add/replace comments and docstrings.
       
1) Define STATE for this program.
the state is the collection of variables that change as the program runs.
   - What variables change as the program runs?
   - board, unique_seen, full_boards, x_wins_on_full_board, draws_on_full_board, x_wins, o_wins, ties)

2) Explain where TRANSITIONS happen.
transitions happen when the state changes
   - Where does the state change? (where in the code, which functions)
   -a move is placed on the board
   -a move is undone
   -a terminal board is recorded and ounters are incremented
   -unique boards are stored in unique_seen

3) Identify 4 INVARIANTS.
   - What properties remain true as the program runs (and what checks enforce them).
   - For instance: has_winner() is a check; the invariant is “we do not continue exploring after a win.”
    1. Players alternate turns. This is enforced by the fixed nested loop structure.
    2. A cell is never overwritten while occupied. Each move checks: if board[i] == ' '.
    3. The board always contains only 'X', 'O', or ' '. All assignments enforce this.
    4. Exploration stops once someone wins. should_continue() checks has_winner() before deeper loops.

4) For every function that says ''' TODO ''', replace that docstring with a real explanation
   of what the function does (1-4 sentences).

5) Add inline comments anywhere you see "# TODO" explaining what that code block is doing.

6) DO NOT USE AI. Write 5-8 sentences explaining one non-obvious part (choose one):  
   (a) symmetry logic (what makes a board unique), 
   (b) why we undo moves, 
   (c) why standard_form() produces uniqueness
   
    The program explores every possible sequence of moves using nested loops,
    but it only keeps a single board object in memory. When a move is placed,
    the board changes. After exploring all possibilities that
    start with that move, the program must restore the board to its previous
    state so other move sequences can be explored. This is why each move is
    followed by an "undo" statement that resets the square back to ' '. Without
    undoing the move, later branches of the search would incorrectly inherit
    previous moves and produce invalid boards. This technique is similar to
    backtracking: we try a move, explore everything that follows it, then
    revert the state so the next possibility starts from the correct board.
    Undoing moves ensures that at the start of each loop iteration the board
    exactly represents the game state after the previous moves only.
   
7) The output from the program is two print statements:
       127872
       138 81792 46080 91 44 3

    explain what each number represents.

    First number:
    127872
    This is the number of games that reached a full 9-move board before the
    search stopped.

    Second line:
    138 81792 46080 91 44 3

    138: number of UNIQUE terminal boards after removing rotations/reflections  
    81792: number of full boards where X wins on the final move  
    46080: number of full boards that end in a draw  
    91: unique terminal boards where X wins  
    44: unique terminal boards where O wins  
    3: unique terminal boards that are ties


Submission:
- Update this file with your answers. Commit and sync

"""

# ----------------------------
# Global running totals (STATE)
# ----------------------------

unique_seen = []             # TODO: this list stores representations of terminal boards. each board is converted to its standard form so that rotations and refelctions count as the same board
board = [' '] * 9            # TODO: this is a flat list representation of the tic tac toe board. the board is mutated as moves are played and then undone, so other moves can be explored

full_boards = 0              # TODO: Counts how many games reached a full board before stopping.
x_wins_on_full_board = 0     # TODO: Counts full boards where X wins on the final move. 
draws_on_full_board = 0      # TODO: Counts full boards that ended in a draw.

x_wins = 0                   # TODO: counts unique terminal boards where X wins.
o_wins = 0                   # TODO: counts unique terminal boards where O wins.
ties = 0                     # TODO: counts unique terminal boards that are ties.


# ----------------------------
# Board representation helpers
# ----------------------------

def to_grid(flat_board: list[str]) -> list[list[str]]:
    ''' converts the flat 1 dimensoinal board list into a 3x3 grid. this makes it easier to perform rotations and reflections when computing board symmetries '''
    grid = []
    for row in range(3):
        row_vals = []
        for col in range(3):
            row_vals.append(flat_board[row * 3 + col])
        grid.append(row_vals)
    return grid


def rotate_clockwise(grid: list[list[str]]) -> list[list[str]]:
    ''' returns a new grid representing the input grid rotated 90 degrees clockwise. this is used to generate symmetric versions of a board when computing a canonical representation '''
    rotated = [[' '] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            rotated[c][2 - r] = grid[r][c]
    return rotated


def flip_vertical(grid: list[list[str]]) -> list[list[str]]:
    ''' returns a vertically flipped version of the grid. the top and bottom rows are swapped, producing a mirror reflection '''
    return [grid[2], grid[1], grid[0]]


def standard_form(flat_board: list[str]) -> list[list[str]]:
    ''' compute a canonical representation of the board under symmetry. all 8 symmetric versions of the board are generated, and the smallest one is returned. this allows equivalent boards to be treated as identical '''
    grid = to_grid(flat_board)
    flipped = flip_vertical(grid)

    variants = []
    for _ in range(4):
        variants.append(grid)
        variants.append(flipped)
        grid = rotate_clockwise(grid)
        flipped = rotate_clockwise(flipped)

    return min(variants)


def record_unique_board(flat_board: list[str]) -> None:
    ''' records a terminal board only if its canonical form has not been seen. this prevents counting rotated or reflected versions of the same board multiple times. '''
    global x_wins, o_wins, ties

    rep = standard_form(flat_board)

    # TODO: prevents symmetric boards from being double counted. 
    if rep not in unique_seen:
        unique_seen.append(rep)

        # TODO: This updates counts for unique *terminal* boards. determines whether a player won, lost, or tie and update counts.
        winner = who_won(flat_board)
        if winner == 'X':
            x_wins += 1
        elif winner == 'O':
            o_wins += 1
        else:
            ties += 1


# ----------------------------
# Game logic
# ----------------------------

def has_winner(flat_board: list[str]) -> bool:
    ''' checks whether either player has three in a row on the board. returns True if a winning line is found, otherwise False. '''
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [6, 4, 2],             # diagonals
    ]

    for line in winning_lines:
        score = 0
        for idx in line:
            if flat_board[idx] == 'X':
                score += 10
            elif flat_board[idx] == 'O':
                score -= 10
        if abs(score) == 30:
            return True

    return False


def who_won(flat_board: list[str]) -> str:
    ''' determines which player won the game. return 'X', 'O', or 'TIE''''
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [6, 4, 2],             # diagonals
    ]

    for line in winning_lines:
        score = 0
        for idx in line:
            if flat_board[idx] == 'X':
                score += 10
            elif flat_board[idx] == 'O':
                score -= 10

        if score == 30:
            return 'X'
        elif score == -30:
            return 'O'

    return 'TIE'


def should_continue(flat_board: list[str], move_number: int) -> bool:
    ''' determines whether the search should continue exploring deeper moves. if a player has already won, the game is a terminal state and the board is recorded before stopping further. '''
    # TODO: if someone has already won, the game is over and we stop exploring
    if has_winner(flat_board):
        record_unique_board(flat_board)
        return False
    return True


def record_full_board(flat_board: list[str]) -> None:
    ''' handles the terminal case where all 9 moves have been played. records the board, increments full board counters, and determines whether the result was a win for X or a draw '''
    global full_boards, x_wins_on_full_board, draws_on_full_board

    # TODO: This is a terminal state because the board is full (9 moves).
    record_unique_board(flat_board)
    full_boards += 1

    # TODO: On a full board, either X has won (last move) or it is a draw.
    if has_winner(flat_board):
        x_wins_on_full_board += 1
    else:
        draws_on_full_board += 1


# ----------------------------
# Brute force search (9 nested loops)
# ----------------------------

# TODO: transitions occur whenever we place a move on the board
# TODO: (board[i] = 'X' or 'O') and whenever we undo it. (board[i] = ' ') after exploring deeper possibilities

# Move 1: X
for x1 in range(9):
    board[x1] = 'X'
    if should_continue(board, 1):

        # Move 2: O
        for o1 in range(9):
            if board[o1] == ' ':
                board[o1] = 'O'
                if should_continue(board, 2):

                    # Move 3: X
                    for x2 in range(9):
                        if board[x2] == ' ':
                            board[x2] = 'X'
                            if should_continue(board, 3):

                                # Move 4: O
                                for o2 in range(9):
                                    if board[o2] == ' ':
                                        board[o2] = 'O'
                                        if should_continue(board, 4):

                                            # Move 5: X
                                            for x3 in range(9):
                                                if board[x3] == ' ':
                                                    board[x3] = 'X'
                                                    if should_continue(board, 5):

                                                        # Move 6: O
                                                        for o3 in range(9):
                                                            if board[o3] == ' ':
                                                                board[o3] = 'O'
                                                                if should_continue(board, 6):

                                                                    # Move 7: X
                                                                    for x4 in range(9):
                                                                        if board[x4] == ' ':
                                                                            board[x4] = 'X'
                                                                            if should_continue(board, 7):

                                                                                # Move 8: O
                                                                                for o4 in range(9):
                                                                                    if board[o4] == ' ':
                                                                                        board[o4] = 'O'
                                                                                        if should_continue(board, 8):

                                                                                            # Move 9: X
                                                                                            for x5 in range(9):
                                                                                                if board[x5] == ' ':
                                                                                                    board[x5] = 'X'

                                                                                                    # Full board reached (terminal)
                                                                                                    record_full_board(board)

                                                                                                    # undo move 9
                                                                                                    board[x5] = ' '

                                                                                        # undo move 8
                                                                                        board[o4] = ' '

                                                                            # undo move 7
                                                                            board[x4] = ' '

                                                                # undo move 6
                                                                board[o3] = ' '

                                                    # undo move 5
                                                    board[x3] = ' '

                                        # undo move 4
                                        board[o2] = ' '

                            # undo move 3
                            board[x2] = ' '

                # undo move 2
                board[o1] = ' '

    # undo move 1
    board[x1] = ' '


print(full_boards)
print(len(unique_seen), x_wins_on_full_board, draws_on_full_board, x_wins, o_wins, ties)
