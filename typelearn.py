import curses 
from curses import wrapper
import time
import praw
import random

# initiate a Reddit instance, return a list of (title, url) tuples to choose text from
def generateRedditText():
    reddit = praw.Reddit(client_id='ShnOH4X_5CuPmA',
                         client_secret='2Pi7dfAvjf58uZ7Vt0-eZ4sZ4WA',
                         user_agent='mac:typelearn:v1 (by /u/BigYamini)')
    subreddit_list = [reddit.subreddit('news'),
                      reddit.subreddit('worldnews'),
                      reddit.subreddit('futurology'),
                      reddit.subreddit('politics')]
    tuple_list = []
    for subreddit in subreddit_list:
        for submission in subreddit.hot(limit=15):
            submission_title, submission_url = submission.title, submission.url
            # change curly quotes to straight quotes
            submission_title = submission_title.replace("’","'").replace("‘","'").replace('“','"').replace('”','"')
            submission_url = submission_url.replace("’","'").replace("‘","'").replace('“','"').replace('”','"')
            tuple_list.append((submission_title, submission_url))
    return tuple_list
            

# returns a random text string and its source for the user to type, from the input list
def getText(tuple_list):
    return random.choice(tuple_list)

# split a text string into a word list for tracking
def splitText(text):
    temp_word_list = text.split()
    word_list = []
    for word in temp_word_list[:len(temp_word_list)-1]:
        word_list.append(word + " ")
    word_list.append(temp_word_list[-1])
    return word_list

# display text on screen, with the user's current position highlighted
def displayText(stdscr, text, position, y, x):

    # highlight first character if at the start
    if position == 0:
        stdscr.addstr(0, 0, text[0], curses.A_STANDOUT)
        stdscr.addstr(0, position+1, text[position+1:])
    # highlight last character if past the end
    elif position >= len(text):
        stdscr.addstr(0, 0, text[:len(text)-1])
        stdscr.addstr(position // x, (len(text)-1) % x, text[len(text)-1], curses.A_STANDOUT)
    # highlight the next character to type
    else: 
        stdscr.addstr(0, 0, text[:position])
        stdscr.addstr(position // x, position % x, text[position], curses.A_STANDOUT)
        stdscr.addstr((position+1) // x, (position+1) % x, text[position+1:])

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
    curses.init_pair(4, curses.COLOR_BLUE, -1)

    # generate text for the user to type
    tuple_list = generateRedditText()
    text, source = getText(tuple_list)
    word_list = splitText(text)
        
    # initialize variables
    so_far = ""
    so_far_word = ""
    position = 0
    word_index = 0
    start_time = None
    quit = False
    y, x = stdscr.getmaxyx()

    while True:
        displayText(stdscr, text, position, y, x)
       
        # handle screen resizes
        if curses.is_term_resized(y, x):
            stdscr.clear()
            y, x = stdscr.getmaxyx()
            displayText(stdscr, text, position, y, x)
       
        if quit:
            break

        stdscr.addstr((len(text) // x) + 2, 0, "> ")
        if start_time is None:
            stdscr.addstr((len(text) // x) + 4, 0, "Start typing to begin. Hit ESC to quit.", curses.A_BOLD)

        c = stdscr.getch()

        # quit on ESC
        if c == 27 or quit:
            break

        # start a timer after the first key is pressed
        if c < 256 and start_time is None:
            stdscr.clear() 
            start_time = time.time()

        # detect and handle 'delete' key
        if c == 127:
            if len(so_far_word) > 0:
                so_far = so_far[:-1]
                so_far_word = so_far_word[:-1]
                stdscr.clear()

        # handle user character input
        elif c < 256 and c != 10:
            so_far += chr(c)
            so_far_word += chr(c)

        position = len(so_far)

        # keep track of the current word the user is typing
        current_word = word_list[word_index]
        # display red if typo
        if so_far_word != current_word[:len(so_far_word)]:
            stdscr.addstr((len(text) // x) + 2, 2, so_far_word, curses.color_pair(2))
        # otherwise, green
        else:
            stdscr.addstr((len(text) // x) + 2, 2, so_far_word, curses.color_pair(1))

        # clear the input section when words are typed correctly
        if so_far_word == current_word and word_index < len(word_list) - 1:
            stdscr.clear()
            word_index += 1
            so_far_word = ""

        # detect when the text is finished being typed        
        if so_far == text:
            end_time = time.time()
            # calculate and display wpm and source
            wpm = calculateWPM(text, start_time, end_time)
            stdscr.addstr((len(text) // x) + 2, 2, "WPM: ", curses.A_BOLD)
            stdscr.addstr((len(text) // x) + 2, 7, str(wpm), curses.color_pair(3))
            stdscr.addstr((len(text) // x) + 4, 0, "Press Enter to continue playing or 'r' to redo. Hit ESC to quit.", curses.A_BOLD)
            stdscr.addstr((len(text) // x) + 6, 0, "Source: ", curses.A_BOLD)
            stdscr.addstr((len(text) // x) + 6, 8, source, curses.color_pair(4))
            # reset the game
            valid_option = False
            while True:
                d = stdscr.getch()
                # ESC (27) pressed
                if d == 27:
                    quit = True
                    break
                # enter key (10) or 'r' key (114) pressed
                elif d == 10 or d == 114:
                    if d == 10:
                        text, source = getText(tuple_list)
                        word_list = splitText(text)
                    # re-initialize variables and clear screen
                    stdscr.clear()
                    so_far = ""
                    so_far_word = ""
                    position = 0
                    word_index = 0
                    start_time = None
                    done = False
                    quit = False
                    y, x = stdscr.getmaxyx()
                    break

wrapper(main)
