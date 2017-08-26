import curses
from curses import wrapper

def getOutput(source):
    if source == "test":
        return "This is a test sentence for the typing game."

def main(stdscr):
    curses.use_default_colors()
    stdscr.clear()
    stdscr.resize(24, 80)
    stdscr.box()
    stdscr.nodelay(True)

    status = "home"

    while status != "exit":

        c = stdscr.keypad(1)

        if c == curses.KEY_RESIZE:
            stdscr.clear()
            stdscr.resize(24, 80)
            stdscr.box()

        # home menu
        if status == "home":
            stdscr.clear()
            stdscr.box()

            stdscr.addstr(7, 20, "Welcome to Alex Pan's terminal game!")
            stdscr.addstr(9, 20, "1. Start a Game")
            stdscr.addstr(10, 20, "2. Game Rules")
            stdscr.addstr(11, 20, "3. About the Game")
            stdscr.addstr(12, 20, "4. Quit")
            
            if c == ord('1'):
                status = "start"
            elif c == ord('4'):
                status = "quit"

        
        # start menu
        if status == "start":
            stdscr.clear()
            stdscr.box()

            stdscr.addstr(7, 20, "Select a source to type from:")
            stdscr.addstr(9, 20, "1. Test")
            stdscr.addstr(10, 20, "2. Twitter")
            stdscr.addstr(11, 20, "3. The New York Times")

            if c == ord('1'):
                status = "play"
                source = "test"

        # quit menu
        if status == "quit":
            stdscr.clear()
            stdscr.box()

            stdscr.addstr(7, 20, "Are you sure you want to quit? (y/n)")
            if c == ord('y') or c == ord('Y'):
                status = "exit"
            elif c == ord('n') or c == ord('N'):
                status = "home"
                stdscr.refresh()

        # play menu
        if status == "play":
            stdscr.clear()
            stdscr.box()

            output = getOutput(source)
            stdscr.addstr(0, 0, output)

# turns on cbreak, turns off echo, enables keypad, initializes colors
wrapper(main)
