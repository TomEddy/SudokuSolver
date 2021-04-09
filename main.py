import solve
import util

# Version 2 methods and classes denoted with v2 appended. Taking a more OO approach
# to solving this issue as it will simplify solving method overall. Making square objects created on parse.
if __name__ == '__main__':
    # Parsing the puzzle from text file
    puzzle_array, row_lists, col_lists = util.parse_text_v2('SudokuPuzzleHard')
    loop_breaker = 0
    continue_bool = True

    print(f'Parsing the following puzzle.')
    util.print_state_v2(puzzle_array)

    # CHANGE NEEDED
    # While loop will incorporate guessing if puzzle is unable to ba logically solved.
    while continue_bool and loop_breaker <= 65:
        solve.solve_puzzle_check_row_col(puzzle_array, row_lists, col_lists)
        loop_breaker = loop_breaker + 1
        # For now we will have the computer make a guess at this point. This is where more advanced solving
        # techniques can be added in the future.

    print("Puzzle complete?")
    print(util.puzzle_check_v2(puzzle_array))
    util.print_state_v2(puzzle_array)
