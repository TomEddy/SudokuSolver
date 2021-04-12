import random

import util


# Current method for guessing. This does not give preference to indices that have a lower chance of failure or
# provides most information when correct. This is currently totally random and should be improved in the future.
def time_to_guess(puzzle_array, save_state, row_lists, row_list_save, col_lists, col_list_save):
    if util.puzzle_check_v2(puzzle_array):
        return
    solve_puzzle_check_row_col(puzzle_array, row_lists, col_lists)
    # Finding where to guess. Choosing place with least chance of being wrong
    possible_ind = []
    for sqr in puzzle_array:
        if sqr.value == 0 and len(sqr.possible) > 0:
            possible_ind.append(sqr.index)

    if len(possible_ind) > 0:
        ran_ind = random.choice(possible_ind)
        ran_pos = random.choice(puzzle_array[ran_ind - 1].possible)
        puzzle_array[ran_ind - 1].value = ran_pos
        row_lists[puzzle_array[ran_ind - 1].row - 1].append(ran_pos)
        col_lists[puzzle_array[ran_ind - 1].col - 1].append(ran_pos)
        time_to_guess(puzzle_array, save_state, row_lists, row_list_save, col_lists, col_list_save)
    return puzzle_array, row_lists, col_lists


# This will check for cols or rows close to full and fill them if possible after recursively calling other method.
def solve_puzzle_check_row_col(puzzle_array, row_lists, col_lists):
    # Calling recursive solver which will attempt to replace as many number as possible with standard method
    solve_puzzle_v2(puzzle_array, row_lists, col_lists)
    filled_rows = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    filled_cols = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(puzzle_array)):
        if puzzle_array[i].value != 0:
            filled_cols[puzzle_array[i].col - 1] = filled_cols[puzzle_array[i].col - 1] + 1
            filled_rows[puzzle_array[i].row - 1] = filled_rows[puzzle_array[i].row - 1] + 1
    current_row = 1
    current_col = 1
    possible_indices = []
    for pos_row in filled_rows:
        if pos_row != 9:
            for j in range(len(puzzle_array)):
                if puzzle_array[j].row == current_row and puzzle_array[j].value == 0:
                    possible_indices.append(j + 1)
            for pos_ind_select in possible_indices:
                for pos_values in puzzle_array[pos_ind_select - 1].possible:
                    count_of_value = 0
                    for pos_ind_full in possible_indices:
                        if puzzle_array[pos_ind_full - 1].possible.count(pos_values) == 1:
                            count_of_value = count_of_value + 1
                    if count_of_value == 1:
                        puzzle_array[pos_ind_select - 1].value = pos_values
                        return solve_puzzle_check_row_col(puzzle_array, row_lists, col_lists)
        current_row = current_row + 1
        possible_indices.clear()

    for pos_col in filled_cols:
        if pos_col != 9:
            for j in range(len(puzzle_array)):
                if puzzle_array[j].col == current_col and puzzle_array[j].value == 0:
                    possible_indices.append(j + 1)
            for pos_ind_select in possible_indices:
                for pos_values in puzzle_array[pos_ind_select - 1].possible:
                    count_of_value = 0
                    for pos_ind_full in possible_indices:
                        if puzzle_array[pos_ind_full - 1].possible.count(pos_values) == 1:
                            count_of_value = count_of_value + 1
                    if count_of_value == 1:
                        puzzle_array[pos_ind_select - 1].value = pos_values
                        return solve_puzzle_check_row_col(puzzle_array, row_lists, col_lists)
        current_col = current_col + 1
        possible_indices.clear()
    return


# Method for making steps towards solving puzzle each run attempts to change one value in puzzle.
def solve_puzzle_v2(puzzle_array, row_lists, col_lists):
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
                        row_lists[puzzle_array[i].row - 1].append(possible[0])
                        col_lists[puzzle_array[i].col - 1].append(possible[0])
                        only_remaining = True
            for sqr in puzzle_array:
                if possible.count(sqr.value) == 1 and (
                        sqr.row == puzzle_array[i].row or sqr.col == puzzle_array[i].col):
                    possible.remove(sqr.value)
                    if len(possible) == 1:
                        puzzle_array[i].value = possible[0]
                        row_lists[puzzle_array[i].row - 1].append(possible[0])
                        col_lists[puzzle_array[i].col - 1].append(possible[0])
                        only_remaining = True
                if sqr.row != puzzle_array[i].row and sqr.square == puzzle_array[i].square and rows_to_check.count(
                        sqr.row) == 0:
                    rows_to_check.append(sqr.row)
                if sqr.col != puzzle_array[i].col and sqr.square == puzzle_array[i].square and cols_to_check.count(
                        sqr.col) == 0:
                    cols_to_check.append(sqr.col)

            for pos_nums in possible:
                can_change = is_change_okay_v2(cols_to_check, rows_to_check, pos_nums, puzzle_array, i, row_lists,
                                               col_lists)
                if can_change:
                    puzzle_array[i].value = pos_nums
                    row_lists[puzzle_array[i].row - 1].append(pos_nums)
                    col_lists[puzzle_array[i].col - 1].append(pos_nums)
                    return solve_puzzle_v2(puzzle_array, row_lists, col_lists)
            if only_remaining:
                return solve_puzzle_v2(puzzle_array, row_lists, col_lists)
    return


# Method for verifying if change should be made based on rules of Sudoku
# cols_to_check : The columns within the square that need to be checked for presence of num
# rows_to_check : The rows within the square that need to be checked for presence of num
# num : The number that we are verifying if it can be placed in the puzzle at index
# puzzle : The list of Sudoku_Square_v2 objects
# index : The index of the space in puzzle in question
def is_change_okay_v2(cols_to_check, rows_to_check, num, puzzle, index, row_lists, col_lists):
    # square_indices : List used to store all the index locations for particular Sudoku square
    square_indices = []
    for sqr in puzzle[index].square:
        square_indices.append(sqr)

    # rows_cleared : List used to store rows in which do contain the desired number. We want to see this match with
    # input list rows.
    rows_cleared = []
    # cols_cleared : List used to store cols in which do contain the desired number. We want to see this match with
    # input list cols.
    cols_cleared = []

    for nums in range(len(row_lists)):
        if rows_to_check.count(nums) == 1 and row_lists[nums - 1].count(num) == 1:
            rows_cleared.append(nums)
        if cols_to_check.count(nums) == 1 and col_lists[nums - 1].count(num) == 1:
            cols_cleared.append(nums)
    # square_indices_to_remove : This is the list of index locations that have been cleared either by being in a row
    # which has been cleared, a column that has been cleared or by containing a none zero number. We want to see the
    # intersection between this and available spaces in square to be all but one index. This would mean that the one
    # remaining index is the only place in which the number in question can go.
    square_indices_to_remove = []
    for same_sqr in square_indices:
        if rows_cleared.count(puzzle[same_sqr - 1].row) == 1 or cols_cleared.count(puzzle[same_sqr - 1].col) == 1 or \
                puzzle[same_sqr - 1].value != 0:
            square_indices_to_remove.append(same_sqr)
    for sqr_remove in square_indices_to_remove:
        square_indices.remove(sqr_remove)
    if len(square_indices) == 1:
        return True
    return False
