import solve
import util

# Version 2 methods and classes denoted with v2 appended. Taking a more OO approach
# to solving this issue as it will simplify solving method overall. Making square objects created on parse.
if __name__ == '__main__':
    # Parsing the puzzle from text file
    puzzle_array, row_lists, col_lists = util.parse_text_v2('SudokuPuzzleExpert')
    loop_breaker = 0
    continue_bool = True

    print(f'Parsing the following puzzle.')
    util.print_state_v2(puzzle_array)

    # While loop will incorporate guessing if puzzle is unable to ba logically solved.
    solve.solve_puzzle_check_row_col(puzzle_array, row_lists, col_lists)
    save_state = util.clone_puzzle(puzzle_array)
    row_list_save = util.clone(row_lists)
    col_list_save = util.clone(col_lists)
    while not util.puzzle_check_v2(puzzle_array):
        puzzle_array = util.clone_puzzle(save_state)
        row_lists = util.clone(row_list_save)
        col_lists = util.clone(col_list_save)
        puzzle_array, row_lists, col_lists = solve.time_to_guess(puzzle_array, save_state, row_lists, row_list_save,
                                                                 col_lists, col_list_save)
    print("Puzzle complete?")
    print(util.puzzle_check_v2(puzzle_array))
    util.print_state_v2(puzzle_array)
