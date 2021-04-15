import random

import pytesseract
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps

import solve
import util

# Version 2 methods and classes denoted with v2 appended. Taking a more OO approach
# to solving this issue as it will simplify solving method overall. Making square objects created on parse.
if __name__ == '__main__':

    # !Testing for image recognition!
    Img = Image.open("SudokuPicture2.jpg")
    size = Img.size
    sharp = ImageEnhance.Sharpness(Img)
    Img = sharp.enhance(2.0)

    # ImgResized = Img.resize((round(size[0]*5),round(size[1]*5)))
    # size = ImgResized.size
    Img = Img.crop((round(.01 * size[0]), round(.01 * size[1]), round(.99 * size[0]), round(.99 * size[1])))
    increments = round(size[0] / 9)
    midpoint = round((size[0] / 9) - (size[0] / 18))

    puzzle_list = []
    alternate = True
    alternate2 = True
    for k in range(9):
        # cropped = Img.crop((leftbound + (i * increments), leftbound + (k * increments), rightbound + (i * increments), rightbound+ (k * increments)))
        for i in range(9):
            poss_list = []
            for j in range(30):
                if j == 0:
                    difference = 0
                else:
                    difference = random.randrange(round(((1 / 8) * (size[0] / 9))), round(((1 / 4) * (size[0] / 9))))
                leftbound = round(midpoint - ((3 / 4) * (size[0] / 9)) + difference)
                rightbound = round(midpoint + ((3 / 4) * (size[0] / 9)) - difference)
                cropped = Img.crop((leftbound + (i * increments), leftbound + (k * increments),
                                    rightbound + (i * increments), rightbound + (k * increments)))
                nobord_crop = ImageOps.expand(cropped, border=-(round(.005 * size[0])), fill='white')
                output = pytesseract.image_to_string(nobord_crop, lang='eng', \
                                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                # nobord_crop.save('testing'+str(i)+str(j)+'.jpg')
                if len(output) > 1:
                    poss_list.append(int(output[0]))
                elif alternate:
                    alternate = False
                elif alternate2:
                    alternate2 = False
                else:
                    poss_list.append(0)
                    alternate = True
                    alternate2 = True

            if len(poss_list) == 0:
                puzzle_list.append(0)
            else:
                puzzle_list.append(max(poss_list, key=poss_list.count))
            print(puzzle_list)
        puzzle_list.append('newline')
    print(puzzle_list)
    # !Testing for image recognition!

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
