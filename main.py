import solve
import util

# Version 2 methods and classes denoted with v2 appended. Taking a more OO approach
# to solving this issue as it will simplify solving method overall. Making square objects created on parse.
if __name__ == '__main__':
    # Parsing the puzzle from text file
    puzzleArray = util.parse_text_v2('SudokuPuzzleMedium2')
    count = 0
    loop_breaker = 0
    guess_loop_breaker = 0
    continue_bool = True
    guess_bool = True

    print(f'Parsing the following puzzle.')
    util.print_state_v2(puzzleArray)

    while guess_bool and guess_loop_breaker <= 65:
        while continue_bool and loop_breaker <= 65:
            while continue_bool and count <= 65:
                continue_bool = solve.solve_puzzle_v2(puzzleArray)
                count = count + 1
            loop_breaker = loop_breaker + 1
            continue_bool = solve.solve_puzzle_check_row_col(puzzleArray)
        # For now we will have the computer make a guess at this point. This is where more advanced solving techniques can be added in the future.
        guess_loop_breaker = guess_loop_breaker + 1

    print(str(count) + " pass through")
    print("Puzzle complete?")
    print(util.puzzle_check_v2(puzzleArray))
    util.print_state_v2(puzzleArray)
