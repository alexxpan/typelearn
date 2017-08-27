import curses 
from curses import wrapper
import time

# return a random text string for the user to type
def getText():
    return "This is a test sentence."

# split a text string into a word list for tracking
def splitText(text):
    temp_word_list = text.split()
    word_list = []
    for word in temp_word_list[:len(temp_word_list)-1]:
        word_list.append(word + " ")
    word_list.append(temp_word_list[-1])
    return word_list

# display text on screen, with the user's current position highlighted
def displayText(stdscr, text, position):
    # highlight first character if at the start
    if position == 0:
        stdscr.addstr(0, position, text[0], curses.A_STANDOUT)
        stdscr.addstr(0, position+1, text[position+1:])
    # highlight last character if past the end
    elif position >= len(text):
        stdscr.addstr(0, 0, text[:len(text)-1])
        stdscr.addstr(0, len(text)-1, text[len(text)-1], curses.A_STANDOUT)
    # highlight the next character to type
    else: 
        stdscr.addstr(0, 0, text[:position])
        stdscr.addstr(0, position, text[position], curses.A_STANDOUT)
        stdscr.addstr(0, position+1, text[position+1:])

def calculateWPM(text, start, end):
    time_elapsed = end - start
    char_per_sec = float(len(text)) / time_elapsed
    wpm = (char_per_sec / 5.0) * 60
    return wpm

def main(stdscr):
    # initialize window 
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)

    text = getText()
    word_list = splitText(text)
        
    # initialize variables
    so_far = ""
    so_far_word = ""
    position = 0
    word_index = 0
    start_time = None
    quit = False

    while True:
        displayText(stdscr, text, position)

        if quit:
            break

        stdscr.addstr(2, 0, "> ")
        if start_time is None:
            stdscr.addstr(4, 0, "Start typing to begin. Hit ESC to quit.", curses.A_BOLD)

        c = stdscr.getch()

        # quit on ESC
        if c == 27 or quit:
            break

        # start a timer after the first key is pressed
        if c is not None and start_time is None:
            stdscr.clear() 
            start_time = time.time()

        # detect and handle 'delete' key
        if c == 127:
            if len(so_far_word) > 0:
                so_far = so_far[:-1]
                so_far_word = so_far_word[:-1]
                stdscr.clear()

        # handle user character input
        elif c < 256:
            so_far += chr(c)
            so_far_word += chr(c)

        position = len(so_far)

        # keep track of the current word the user is typing
        current_word = word_list[word_index]
        # display red if typo
        if so_far_word != current_word[:len(so_far_word)]:
            stdscr.addstr(2, 2, so_far_word, curses.color_pair(2))
        # otherwise, green
        else:
            stdscr.addstr(2, 2, so_far_word, curses.color_pair(1))

        # clear the input section when words are typed correctly
        if so_far_word == current_word and word_index < len(word_list) - 1:
            stdscr.clear()
            word_index += 1
            so_far_word = ""

        # detect when the text is finished being typed        
        if so_far == text:
            end_time = time.time()
            # calculate and display wpm
            wpm = calculateWPM(text, start_time, end_time)
            stdscr.addstr(2, 2, "WPM: ", curses.A_BOLD)
            stdscr.addstr(2, 7, str(wpm), curses.color_pair(3))
            stdscr.addstr(4, 0, "Press enter to continue playing or 'r' to redo. Hit ESC to quit.", curses.A_BOLD)
            # reset the game
            valid_option = False
            while not valid_option:
                d = stdscr.getch()
                # ESC (27) pressed
                if d == 27:
                    quit = True
                    break
                # enter key (13) or 'r' key (114) pressed
                elif d == 13 or d == 114:
                    if d == 114:
                        text = getText()
                    # re-initialize variables and clear screen
                    stdscr.clear()
                    so_far = ""
                    so_far_word = ""
                    position = 0
                    word_index = 0
                    start_time = None
                    done = False
                    quit = False
                    break

                        
            



wrapper(main)
