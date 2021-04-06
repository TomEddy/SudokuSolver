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
    row_count, col_count, index = (1 for j in range(3))
    rone, rtwo, rthree, rfour, rfive, rsix, rseven, reight, rnine, cone, ctwo, cthree, cfour, cfive, csix, cseven, ceight, cnine, sqr_indices, puzzle_array = (
    [] for i in range(20))
    # NOT DONE
    # Use these to maintain row/col information rather than repeated searches of entire puzzle.
    row_lists = [rone, rtwo, rthree, rfour, rfive, rsix, rseven, reight, rnine]
    col_lists = [cone, ctwo, cthree, cfour, cfive, csix, cseven, ceight, cnine]
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


# Method for printing out puzzle to terminal
def print_state_v2(puzzle_array):
    printer_count = 0
    for number in puzzle_array:
        print(number.value, end="")
        printer_count = printer_count + 1
        if printer_count == 9:
            printer_count = 0
            print()


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
