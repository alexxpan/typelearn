import curses 
from curses import wrapper

def main(stdscr):
    # initialize window 
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)

    text = "This is a test sentence."

    # split text into words for tracking
    temp_word_list = text.split()
    word_list = []
    for word in temp_word_list[:len(temp_word_list)-1]:
        word_list.append(word + " ")
    word_list.append(temp_word_list[-1])
        
    # initialize variables
    so_far = ""
    so_far_word = ""
    position = 0
    word_index = 0

    while True:
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

        stdscr.addstr(2, 0, "> ")
        c = stdscr.getch()

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

        if so_far_word == current_word:
            stdscr.clear()
            word_index += 1
            so_far_word = ""
        stdscr.addstr(6,0,str(position))


wrapper(main)
