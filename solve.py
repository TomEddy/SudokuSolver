# Method for making steps towards solving puzzle each run attempts to change one value in puzzle.
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
