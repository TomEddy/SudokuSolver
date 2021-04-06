# Version 2 methods and classes denoted with v2 appended. Taking a more OO approach
# to solving this issue as it will simplify solving method overall. Making square objects created on parse.
class Sudoku_square_v2:
    def __init__(self, value, row, col, square, index):
        self.value = value
        self.row = row
        self.col = col
        self.square = square
        self.index = index
        self.possible = list([1, 2, 3, 4, 5, 6, 7, 8, 9])


# Parsing puzzle and creating square objects containing the following: value in square,
# row square is in, col square is in,same sqr indices, index for square
def parse_text_v2(name):
    puzzle_array = []
    row_count = 1
    col_count = 1
    index = 1
    sqr_indices = []
    with open(name, encoding='utf8') as f:
        for line in f:
            for char in line:
                if char != '\n':
                    if 1 <= row_count <= 3:
                        if 1 <= col_count <= 3:
                            sqr_indices = [1, 2, 3, 10, 11, 12, 19, 20, 21]
                        elif 4 <= col_count <= 6:
                            sqr_indices = [4, 5, 6, 13, 14, 15, 22, 23, 24]
                        elif 7 <= col_count <= 9:
                            sqr_indices = [7, 8, 9, 16, 17, 18, 25, 26, 27]
                        else:
                            print('Square check failed')
                    elif 4 <= row_count <= 6:
                        if 1 <= col_count <= 3:
                            sqr_indices = [28, 29, 30, 37, 38, 39, 46, 47, 48]
                        elif 4 <= col_count <= 6:
                            sqr_indices = [31, 32, 33, 40, 41, 42, 49, 50, 51]
                        elif 7 <= col_count <= 9:
                            sqr_indices = [34, 35, 36, 43, 44, 45, 52, 53, 54]
                        else:
                            print('Square check failed')
                    elif 7 <= row_count <= 9:
                        if 1 <= col_count <= 3:
                            sqr_indices = [55, 56, 57, 64, 65, 66, 73, 74, 75]
                        elif 4 <= col_count <= 6:
                            sqr_indices = [58, 59, 60, 67, 68, 69, 76, 77, 78]
                        elif 7 <= col_count <= 9:
                            sqr_indices = [61, 62, 63, 70, 71, 72, 79, 80, 81]
                        else:
                            print('Square check failed')
                    else:
                        print('Square check failed')
                    s_name = Sudoku_square_v2(int(char), row_count, col_count, sqr_indices, index)
                    puzzle_array.append(s_name)
                    index = index + 1
                    col_count = col_count + 1
                    if col_count == 10:
                        col_count = col_count - 9
            row_count = row_count + 1
    return puzzle_array


# This will check for cols or rows close to full and fill them if possible
def solve_puzzle_check_row_col(puzzle_array):
    filled_rows = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    filled_cols = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(puzzle_array)):
        if puzzle_array[i].value != 0:
            filled_cols[puzzle_array[i].col - 1] = filled_cols[puzzle_array[i].col - 1] + 1
            filled_rows[puzzle_array[i].row - 1] = filled_rows[puzzle_array[i].row - 1] + 1
    current_row = 1
    current_col = 1
    possible_indicies = []
    for pos_row in filled_rows:
        if pos_row != 9:
            for j in range(len(puzzle_array)):
                if puzzle_array[j].row == current_row and puzzle_array[j].value == 0:
                    possible_indicies.append(j + 1)

            for pos_ind_select in possible_indicies:
                for pos_values in puzzle_array[pos_ind_select - 1].possible:
                    count_of_value = 0
                    for pos_ind_full in possible_indicies:
                        if puzzle_array[pos_ind_full - 1].possible.count(pos_values) == 1:
                            count_of_value = count_of_value + 1
                    if count_of_value == 1:
                        puzzle_array[pos_ind_select - 1].value = pos_values
                        return True
        current_row = current_row + 1
        possible_indicies.clear()

    for pos_col in filled_cols:
        if pos_col != 9:
            for j in range(len(puzzle_array)):
                if puzzle_array[j].col == current_col and puzzle_array[j].value == 0:
                    possible_indicies.append(j + 1)
            for pos_ind_select in possible_indicies:
                for pos_values in puzzle_array[pos_ind_select - 1].possible:
                    count_of_value = 0
                    for pos_ind_full in possible_indicies:
                        if puzzle_array[pos_ind_full - 1].possible.count(pos_values) == 1:
                            count_of_value = count_of_value + 1
                    if count_of_value == 1:
                        puzzle_array[pos_ind_select - 1].value = pos_values
                        return True
        current_col = current_col + 1
        possible_indicies.clear()
    return False


# Method for making steps towards solving puzzle earch run attempts to change one value in puzzle.
def solve_puzzle_v2(puzzle_array):
    for i in range(len(puzzle_array)):
        # This list of possibilities are the numbers that could possibly be
        # placed in square
        possible = puzzle_array[i].possible
        rows_to_check = []
        cols_to_check = []
        only_remaining = False
        # Checking if the space is empty
        if puzzle_array[i].value == 0:
            sqr_number = puzzle_array[i].square
            for index in sqr_number:
                if possible.count(puzzle_array[index - 1].value) == 1:
                    possible.remove(puzzle_array[index - 1].value)
                    if len(possible) == 1:
                        puzzle_array[i].value = possible[0]
                        only_remaining = True
            for sqr in puzzle_array:
                if possible.count(sqr.value) == 1 and (
                        sqr.row == puzzle_array[i].row or sqr.col == puzzle_array[i].col):
                    possible.remove(sqr.value)
                    if len(possible) == 1:
                        puzzle_array[i].value = possible[0]
                        only_remaining = True
                if sqr.row != puzzle_array[i].row and sqr.square == puzzle_array[i].square and rows_to_check.count(
                        sqr.row) == 0:
                    rows_to_check.append(sqr.row)
                if sqr.col != puzzle_array[i].col and sqr.square == puzzle_array[i].square and cols_to_check.count(
                        sqr.col) == 0:
                    cols_to_check.append(sqr.col)
            for k in possible:
                b = is_change_okay_v2(cols_to_check, rows_to_check, k, puzzle_array, i)
                if b:
                    puzzle_array[i].value = k
                    return True
            if only_remaining:
                return True
    return False


# Method for verifying if change should be made
def is_change_okay_v2(cols, rows, num, puzzle, index):
    rows_cleared = []
    cols_cleared = []
    square_indices = []
    square_indices_to_remove = []
    for sqr in puzzle:
        if rows.count(sqr.row) == 1 and sqr.value == num:
            rows_cleared.append(sqr.row)
        if cols.count(sqr.col) == 1 and sqr.value == num:
            cols_cleared.append(sqr.col)
    for sqr in puzzle[index].square:
        square_indices.append(sqr)
    for same_sqr in square_indices:
        if rows_cleared.count(puzzle[same_sqr - 1].row) == 1 or cols_cleared.count(puzzle[same_sqr - 1].col) == 1 or \
                puzzle[same_sqr - 1].value != 0:
            square_indices_to_remove.append(same_sqr)
    for sqr_remove in square_indices_to_remove:
        square_indices.remove(sqr_remove)
    if len(square_indices) == 1:
        return True
    return False


# Method for verifying that puzzle is solved. Needed for program to understand if guess was successful.
def puzzle_check_v2(puzzle_array):
    total_row = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_col = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for sqr in puzzle_array:
        total_row[sqr.row - 1] = total_row[sqr.row - 1] + sqr.value
        total_col[sqr.col - 1] = total_col[sqr.col - 1] + sqr.value
    if total_row.count(45) == 9 and total_col.count(45) == 9:
        return True
    else:
        return False


# Method for printing out puzzle to terminal
def print_state_v2(puzzle_array):
    printer_count = 0
    for number in puzzle_array:
        print(number.value, end="")
        printer_count = printer_count + 1
        if printer_count == 9:
            printer_count = 0
            print()


if __name__ == '__main__':
    # Parsing the puzzle from text file
    puzzleArray = parse_text_v2('SudokuPuzzleMedium2')
    count = 0
    loop_breaker = 0
    guess_loop_breaker = 0
    continue_bool = True
    guess_bool = True

    print(f'Parsing the following puzzle.')
    print_state_v2(puzzleArray)

    while guess_bool and guess_loop_breaker <= 65:
        while continue_bool and loop_breaker <= 65:
            while continue_bool and count <= 65:
                continue_bool = solve_puzzle_v2(puzzleArray)
                count = count + 1
            loop_breaker = loop_breaker + 1
            continue_bool = solve_puzzle_check_row_col(puzzleArray)
        # For now we will have the computer make a guess at this point. This is where more advanced solving techniques can be added in the future.
        guess_loop_breaker = guess_loop_breaker + 1

    print(str(count) + " pass through")
    print("Puzzle complete?")
    print(puzzle_check_v2(puzzleArray))
    print_state_v2(puzzleArray)
