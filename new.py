import curses 
from curses import wrapper

def main(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    #curses.echo()

    text = "This is a test sentence."
    temp_word_list = text.split()
    word_list = []
    for word in temp_word_list[:len(temp_word_list)-1]:
        word_list.append(word + " ")
    word_list.append(temp_word_list[-1])
        
    so_far = ""
    so_far_word = ""
    position = 0
    word_index = 0

    while True:
        if position == 0:
            stdscr.addstr(0, position, text[0], curses.A_STANDOUT)
            stdscr.addstr(0, position+1, text[position+1:])
        else:
            stdscr.addstr(0, 0, text[:position])
            stdscr.addstr(0, position, text[position], curses.A_STANDOUT)
            stdscr.addstr(0, position+1, text[position+1:])

        c = stdscr.getch()
        if c == 127:
            if len(so_far_word) > 0:
                so_far = so_far[:-1]
                so_far_word = so_far_word[:-1]
                stdscr.clear()
        elif len(chr(c)) == 1:
            so_far += chr(c)
            so_far_word += chr(c)
        position = len(so_far)
        stdscr.addstr(1, 0, so_far_word, curses.color_pair(1))

        current_word = word_list[word_index]
        if so_far_word == current_word:
            stdscr.clear()
            word_index += 1
            so_far_word = ""
        stdscr.addstr(5,0,str(word_index))

wrapper(main)
