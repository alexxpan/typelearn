import curses
from curses import wrapper

def main(stdscr):
    stdscr.resize(24, 80)
    y, x = stdscr.getmaxyx()
    stdscr.clear()
    while True:
        curses.use_default_colors()
        # Store the key value in the variable `c`
        c = stdscr.getch()
        # Clear the terminal
        stdscr.clear()
        if c == ord('a'):
            stdscr.addstr(str(y))
            stdscr.addstr("You pressed the 'a' key.")
        elif c == curses.KEY_UP:
            stdscr.addstr("You pressed the up arrow.")
        else:
            stdscr.addstr("This program doesn't know that key.....")

# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)

