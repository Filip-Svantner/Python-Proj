_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"

_columnTracker = [0,0,0,0,0]
key_pressed = None

import time
import sys
import random
from pynput import keyboard


def clear_the_terminal():
    sys.stdout.write("\033[2J\033[H")    # ANSI escape which clears the current terminal screen.
    sys.stdout.flush()


def build_clean_grid():
    """Reset the tetris grid to empty."""
    return [["  " for i in range(_ROWS)] for i in range(_COLUMNS)]


def drop_block(grid, column_number):
    """Given a column number, update the tetris grid to add a block to that column.
    Return the updated grid to the caller."""
    try:
        n = grid[column_number].index(_BLOCK)
        n = n - 1
    except:
        n = -1
    grid[column_number][n] = _BLOCK
    return grid


def display_grid(grid):
    """Display the current state of the tetris grid "vertically" up the screen. Remember: by default,
    the grid dispays across the screen, row-wise (which, usually, isn't what we want here)."""
    the_columns = tuple(range(0, _COLUMNS))
    the_rows = tuple(range(0, _ROWS))
    for r in the_rows:
        print("|", sep="", end="")
        for c in the_columns:
            print(grid[c][r], "|", sep="", end="")
        print()


def show_dropping_block(grid, column_number, columns_done):
    """Given a grid and a column to drop into, simulate a visual drop of a box."""
    global key_pressed

    for row in range(_ROWS - _columnTracker[column_number] -1):
        if key_pressed == "d":
            startIndex = column_number
            while True:
                if column_number >= 4:
                    column_number = startIndex
                    break
                
                column_number += 1

                if not columns_done[column_number]:
                    break

        if key_pressed == "a":
                        startIndex = column_number
                        while True:
                            if column_number <= 0:
                                column_number = startIndex
                                break

                            column_number -= 1

                            if not columns_done[column_number]:
                                break
            
        key_pressed = None
        
        grid[column_number][row] = _BLOCK
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_the_terminal()
        grid[column_number][row] = _BLANK
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_the_terminal()
    
    drop_block(grid,column_number)
    _columnTracker[column_number] += 1


def process_on_press(key):
    global key_pressed
    try:
        key_pressed = key.char
    except AttributeError:
        key_pressed = str(key)


def game_loop():
    g = build_clean_grid()
    display_grid(g)
    columnsDone = [False, False, False, False, False]
    loop = True

    listener = keyboard.Listener( on_press=process_on_press )
    listener.start()

    while loop:
        rand = random.randint(0,4)
        if(_columnTracker[rand] < 10):
            show_dropping_block(g,rand, columnsDone)
        else:
            columnsDone[rand] = True

        if all(columnsDone):
            loop = False
    display_grid(g)
    print("Game Over - Grid has been filled")
        

