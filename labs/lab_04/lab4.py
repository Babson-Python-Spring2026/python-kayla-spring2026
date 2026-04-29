import random


MINE = "💣"
HIDDEN = "♦"


def get_valid_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))

            if min_value <= value <= max_value:
                return value

            print(f"Please enter a number between {min_value} and {max_value}.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def count_adjacent_mines(mine_locations, row, col, height, width):
    count = 0

    for row_change in [-1, 0, 1]:
        for col_change in [-1, 0, 1]:

            if row_change == 0 and col_change == 0:
                continue

            neighbor_row = row + row_change
            neighbor_col = col + col_change

            if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
                if (neighbor_row, neighbor_col) in mine_locations:
                    count += 1

    return count


def create_board(height, width, num_mines):
    mine_locations = set()

    while len(mine_locations) < num_mines:
        row = random.randint(0, height - 1)
        col = random.randint(0, width - 1)
        mine_locations.add((row, col))

    board = []

    for row in range(height):
        board_row = []

        for col in range(width):
            if (row, col) in mine_locations:
                board_row.append(MINE)
            else:
                board_row.append(
                    count_adjacent_mines(mine_locations, row, col, height, width)
                )

        board.append(board_row)

    return board, mine_locations


def print_board(board, dug_locations, height, width, reveal=False):
    print()
    print("     " + "   ".join(str(col) for col in range(width)))
    print("   +" + "---+" * width)

    for row in range(height):
        row_display = f"{row:2} |"

        for col in range(width):
            if reveal or (row, col) in dug_locations:
                value = board[row][col]
                display = " " if value == 0 else str(value)
            else:
                display = HIDDEN

            row_display += f" {display} |"

        print(row_display)
        print("   +" + "---+" * width)


def setup_game():
    height = get_valid_input("Board height / rows, 2-10: ", 2, 10)
    width = get_valid_input("Board width / columns, 2-10: ", 2, 10)

    max_mines = height * width - 1
    num_mines = get_valid_input(f"Number of mines, 1-{max_mines}: ", 1, max_mines)

    board, mine_locations = create_board(height, width, num_mines)

    dug_locations = set()
    game_over = False
    won = False
    lost = False

    return height, width, num_mines, mine_locations, board, dug_locations, game_over, won, lost


def get_move(height, width, dug_locations):
    while True:
        over = get_valid_input(
            f"How many over would you like to dig? 0-{width - 1}: ",
            0,
            width - 1
        )

        down = get_valid_input(
            f"How many down would you like to dig? 0-{height - 1}: ",
            0,
            height - 1
        )

        row = down
        col = over

        if (row, col) in dug_locations:
            print("You already dug that spot. Choose another location.")
        else:
            return row, col


def check_win(dug_locations, height, width, num_mines):
    safe_cells = height * width - num_mines
    return len(dug_locations) == safe_cells


def reveal_neighbors(board, dug_locations, row, col, height, width):
    if (row, col) in dug_locations:
        return

    dug_locations.add((row, col))

    if board[row][col] != 0:
        return

    for row_change in [-1, 0, 1]:
        for col_change in [-1, 0, 1]:

            if row_change == 0 and col_change == 0:
                continue

            neighbor_row = row + row_change
            neighbor_col = col + col_change

            if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
                reveal_neighbors(
                    board,
                    dug_locations,
                    neighbor_row,
                    neighbor_col,
                    height,
                    width
                )


def dig(board, dug_locations, row, col, height, width):
    if board[row][col] == MINE:
        return True

    if board[row][col] == 0:
        reveal_neighbors(board, dug_locations, row, col, height, width)
    else:
        dug_locations.add((row, col))

    return False


def play_game():
    height, width, num_mines, mine_locations, board, dug_locations, game_over, won, lost = setup_game()

    print_board(board, dug_locations, height, width)

    while not game_over:
        row, col = get_move(height, width, dug_locations)

        lost = dig(board, dug_locations, row, col, height, width)

        if lost:
            game_over = True
            print_board(board, dug_locations, height, width, reveal=True)
            print("You have hit a mine. Try Again")

        else:
            won = check_win(dug_locations, height, width, num_mines)

            if won:
                game_over = True
                print_board(board, dug_locations, height, width, reveal=True)
                print("Congratulations! You won.")

            else:
                print_board(board, dug_locations, height, width)


def main():
    while True:
        play_game()

        while True:
            again = input("Play again? (yes/no): ").strip().lower()

            if again in ("yes", "no"):
                break

            print("Please enter 'yes' or 'no'.")

        if again == "no":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()