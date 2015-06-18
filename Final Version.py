__author__ = 'Aaron Marquez'

from graphics import *
from random import randint
from time import clock

TILE_IMAGE = 'tile.gif'
FLAG_IMAGE = 'flag.gif'
MINE_IMAGE = 'mine.gif'
LOSE_IMAGE = 'lose.gif'
SMILEY_IMAGE = 'smiley.gif'
BLANK_CELL = 0
EXPOSED_CELL = 10
MINE_CELL = 13
MAX_ADJACENT_MINES = 8
WIDTH_OF_IMAGES = 32
HEIGHT_OF_IMAGES = 32
LEFT_OFFSET = 100
RIGHT_OFFSET = 100
TOP_OFFSET = 120
BOTTOM_OFFSET = LEFT_OFFSET // 2
X_OFFSET = LEFT_OFFSET
Y_OFFSET = TOP_OFFSET

win = GraphWin("Minesweeper", 1100, 700)

def create_minesweeper_matrix(rows, columns):
    minesweeper_matrix = []
    for i in range(rows):
        minesweeper_matrix.append([])
        for j in range(columns):
            minesweeper_matrix[i].append(0)
    return minesweeper_matrix

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(str(matrix[i][j]).rjust(4), end='')
        print()
    return None

def draw_the_grid(rows, columns):
    for i in range(rows):
        p1 = Point(LEFT_OFFSET, TOP_OFFSET + (WIDTH_OF_IMAGES * i))
        p2 = Point(LEFT_OFFSET + HEIGHT_OF_IMAGES, TOP_OFFSET + HEIGHT_OF_IMAGES + (WIDTH_OF_IMAGES * (i)))
        rect = Rectangle(p1, p2)
        rect.draw(win)
        for j in range(columns):
            p3 = Point(LEFT_OFFSET + (WIDTH_OF_IMAGES * j), TOP_OFFSET + (WIDTH_OF_IMAGES * i))
            p4 = Point(LEFT_OFFSET + HEIGHT_OF_IMAGES + (WIDTH_OF_IMAGES * (j)), TOP_OFFSET + HEIGHT_OF_IMAGES + (WIDTH_OF_IMAGES * i))
            recta = Rectangle(p3, p4)
            recta.draw(win)
    return None


def populate_with_mines(game_board_markers, number_of_mines):
    num_mines = 0
    while num_mines < number_of_mines:
        row = randint(0, len(game_board_markers) - 1)
        col = randint(0, len(game_board_markers[0]) - 1)
        if game_board_markers[row][col] != 13:
            game_board_markers[row][col] = MINE_CELL
            mine_image = Image(Point(LEFT_OFFSET + (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * col), TOP_OFFSET + \
                                     (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * row)), MINE_IMAGE)
            mine_image.draw(win)
            num_mines += 1
    return game_board_markers

def update_neighbor_count(game_board_markers, row, column):
    count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if 0 <= row + i <= (len(game_board_markers) - 1) and 0 <= column + j <= (len(game_board_markers[0]) - 1) and \
                            game_board_markers[row + i][column + j] == 13:
                count += 1
    if game_board_markers[row][column] == 13:
        count = 13
    return count


def add_mine_counts(game_board_markers):
    for i in range(len(game_board_markers)):
        for j in range(len(game_board_markers[i])):
            count = update_neighbor_count(game_board_markers, i, j)
            game_board_markers[i][j] = count
            if count != MINE_CELL and count != 0:
                center_of_text = Point(LEFT_OFFSET + (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * j), \
                                    TOP_OFFSET + (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * i))
                text_to_display = Text(center_of_text, count)
                text_to_display.setSize(10)
                text_to_display.setTextColor('black')
                text_to_display.draw(win)
    return game_board_markers


def draw_board_numbers(game_board_markers):
    for i in range(len(game_board_markers)):
        center_of_text = Point(LEFT_OFFSET - (WIDTH_OF_IMAGES/2), TOP_OFFSET + (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * i))
        text_to_display = Text(center_of_text, i)
        text_to_display.setSize(10)  # font size
        text_to_display.setTextColor('black')
        text_to_display.draw(win)
    for j in range(len(game_board_markers[0])):
        center_of_text = Point(LEFT_OFFSET + (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * j), TOP_OFFSET - (WIDTH_OF_IMAGES/2))
        text_to_display = Text(center_of_text, j)
        text_to_display.setSize(10)  # font size
        text_to_display.setTextColor('black')
        text_to_display.draw(win)
    return None

def draw_tiles(game_board_markers):
    game_board_images = []
    for i in range(len(game_board_markers)):
        game_board_images.append([])
        for j in range(len(game_board_markers[0])):
            tile_image = Image(Point(LEFT_OFFSET + (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * j), TOP_OFFSET + \
                                     (WIDTH_OF_IMAGES/2) + (WIDTH_OF_IMAGES * i)), TILE_IMAGE)
            tile_image.draw(win)
            game_board_images[i].append(tile_image)
    num_cols = len(game_board_markers[0])
    smiley_face = Image(Point(LEFT_OFFSET + (WIDTH_OF_IMAGES/2) * num_cols, TOP_OFFSET / 2), SMILEY_IMAGE)
    smiley_face.draw(win)
    return game_board_images


def convert_click_to_row_column(c_point, rows, columns):
    for i in range(rows):
        y_point = Y_OFFSET + (HEIGHT_OF_IMAGES * i)
        for j in range(columns):
            x_point = X_OFFSET + (WIDTH_OF_IMAGES * j)
            top_left = Point(x_point, y_point)
            bottom_right = Point(x_point + WIDTH_OF_IMAGES, y_point + HEIGHT_OF_IMAGES)
            if top_left.getX() <= c_point.getX() and bottom_right.getX() >= c_point.getX():
                if top_left.getY() <= c_point.getY() and bottom_right.getY() >= c_point.getY():
                    return i, j
    return None, None


def expose_all_mines(game_board_markers, game_board_images):
    for i in range(len(game_board_markers)):
        for j in range(len(game_board_markers[0])):
            if game_board_markers[i][j] == MINE_CELL:
                game_board_images[i][j].undraw()
        win.update()
    return None


def expose_empty_cells(game_board_markers, game_board_images, row, column):

    rows = len(game_board_markers)
    columns = len(game_board_markers[0])
    game_board_images[row][column].undraw()


    if row > 0 and game_board_markers[row-1][column] == 0:
        game_board_images[row-1][column].undraw()
    if row < rows-1 and game_board_markers[row+1][column] == 0:
        game_board_images[row+1][column].undraw()
    if column > 0 and game_board_markers[row][column-1] == 0:
        game_board_images[row][column-1].undraw()
    if column < columns-1 and game_board_markers[row][column+1] == 0:
        game_board_images[row][column+1].undraw()
    if row > 0 and column > 0 and game_board_markers[row-1][column-1] == 0:
        game_board_images[row-1][column-1].undraw()
    if row > 0 and column < columns-1 and game_board_markers[row-1][column+1] == 0:
        game_board_images[row-1][column+1].undraw()
    if row < rows-1 and column > 0 and game_board_markers[row+1][column-1] == 0:
        game_board_images[row+1][column-1].undraw()
    if row < rows-1 and column < columns-1 and game_board_markers[row+1][column+1] == 0:
        game_board_images[row+1][column+1].undraw()

    return None


def main():
    level = input("Enter a difficulty (Beginner, Intermediate, or Expert): ")
    if level == "Beginner":
        rows = 9
        columns = 9
        minesweeper_matrix = create_minesweeper_matrix(rows, columns)
        num_mines = 10
        new_matrix = populate_with_mines(minesweeper_matrix, num_mines)
        hi = add_mine_counts(new_matrix)
        print_matrix(hi)
        draw_board_numbers(new_matrix)
        draw_the_grid(9, 9)
        game_board_images = draw_tiles(new_matrix)
        win.update()
    if level == "Intermediate":
        rows = 16
        columns = 16
        minesweeper_matrix = create_minesweeper_matrix(rows, columns)
        num_mines = 40
        new_matrix = populate_with_mines(minesweeper_matrix, num_mines)
        hi = add_mine_counts(new_matrix)
        print_matrix(hi)
        draw_board_numbers(new_matrix)
        draw_the_grid(16, 16)
        game_board_images = draw_tiles(new_matrix)
        win.update()
    if level == "Expert":
        rows = 16
        columns = 30
        minesweeper_matrix = create_minesweeper_matrix(rows, columns)
        num_mines = 99
        new_matrix = populate_with_mines(minesweeper_matrix, num_mines)
        hi = add_mine_counts(new_matrix)
        print_matrix(hi)
        draw_board_numbers(new_matrix)
        draw_the_grid(16, 30)
        game_board_images = draw_tiles(new_matrix)
        win.update()
    while True:
        c_point = win.getMouse()
        row, column = convert_click_to_row_column(c_point, rows, columns)
        if row is None:
            continue
        elif new_matrix[row][column] == EXPOSED_CELL:
            continue
        elif new_matrix[row][column] == MINE_CELL:
            loss = Image(Point(LEFT_OFFSET + (WIDTH_OF_IMAGES/2) * columns, TOP_OFFSET / 2), LOSE_IMAGE)
            loss.draw(win)
            expose_all_mines(new_matrix, game_board_images)
            break
        elif new_matrix[row][column] >= 1 and new_matrix[row][column] <= rows - 1:
            game_board_images[row][column].undraw()
            new_matrix[row][column] = EXPOSED_CELL
            game_board_images[row][column] = None
        elif new_matrix[row][column] == 0:
            expose_empty_cells(new_matrix, game_board_images, row, column)
    win.getMouse()
    win.close()

main()