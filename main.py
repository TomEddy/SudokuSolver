import math
import random
import time

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
    Img.save("testing.png", format='PNG', dpi=(200, 200))

    time.sleep(2)

    Img = Image.open("testing.png")

    sharp = ImageEnhance.Sharpness(Img)
    Img = sharp.enhance(2.0)
    size = Img.size
    # Img = Img.resize((round(size[0]*.25),round(size[1]*.25)))
    # size = ImgResized.size
    Img = Img.crop((round(.015 * size[0]), round(.015 * size[1]), round(.985 * size[0]), round(.985 * size[1])))
    size = Img.size

    # Converts image to grayscale
    Img = Img.convert('L')

    increments = round(size[0] / 9)
    midpoint = round((size[0] / 9) - (size[0] / 18))

    puzzle_list = []
    alternate = True
    alternate2 = True
    for k in range(9):
        # cropped = Img.crop((leftbound + (i * increments), leftbound + (k * increments), rightbound + (i * increments), rightbound+ (k * increments)))
        for i in range(9):

            leftbound = round(midpoint - ((21 / 32) * (size[0] / 9)) / 2)
            rightbound = round(midpoint + ((21 / 32) * (size[0] / 9)) / 2)
            cropped = Img.crop((leftbound + (i * increments), leftbound + (k * increments),
                                rightbound + (i * increments), rightbound + (k * increments)))
            extrema = cropped.getextrema()
            if extrema == (255, 255):
                # all white
                puzzle_list.append(0)
                print(puzzle_list)
            else:
                poss_list = []
                is_cont = True
                count = 0
                border_multiplier = 0
                while is_cont:
                    difference = random.randrange(round(((1 / 8) * (size[0] / 9))), round(((5 / 32) * (size[0] / 9))))
                    leftbound = round(midpoint - ((21 / 32) * (size[0] / 9)) + difference)
                    rightbound = round(midpoint + ((21 / 32) * (size[0] / 9)) - difference)
                    cropped = Img.crop((leftbound + (i * increments), leftbound + (k * increments),
                                        rightbound + (i * increments), rightbound + (k * increments)))
                    nobord_crop = ImageOps.crop(cropped, border=border_multiplier)
                    nobord_crop = ImageOps.expand(nobord_crop, border=2, fill='white')
                    nobord_crop = ImageOps.posterize(nobord_crop, 1)
                    output = pytesseract.image_to_string(nobord_crop, lang='eng',
                                                         config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                    if len(output) > 1:
                        poss_list.append(int(output[0]))
                    if count > 50:
                        border_multiplier = round(.1 * cropped.size[1])

                    if count > 120:
                        is_cont = False
                        puzzle_list.append('*')
                    elif count > 50 and len(poss_list) >= 5:
                        # nobord_crop.save('testing' + str(count) + '.jpg')
                        if poss_list.count(max(poss_list, key=poss_list.count)) >= math.floor(len(poss_list) * .7):
                            is_cont = False
                            puzzle_list.append(max(poss_list, key=poss_list.count))
                    elif len(poss_list) > 20:
                        if poss_list.count(max(poss_list, key=poss_list.count)) >= math.floor(len(poss_list) * .8):
                            is_cont = False
                            puzzle_list.append(max(poss_list, key=poss_list.count))
                    elif len(poss_list) > 5:
                        if poss_list.count(max(poss_list, key=poss_list.count)) >= math.floor(len(poss_list) * .9):
                            is_cont = False
                            puzzle_list.append(max(poss_list, key=poss_list.count))
                    count = count + 1
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
