# typelearn

Typelearn is a terminal-based productivity game. It is designed to improve typing speed while staying up-tp-date with current events and learning new information.

It generates text to type using the praw Reddit API (https://praw.readthedocs.io/en/latest/index.html). Submission titles and urls are pulled from the 'hot' section of the following subreddits:
  - r/news
  - r/worldnews
  - r/futurology
  - r/politics
  
WPM is calculated by using the typical formula of assuming an average word length of 5. It takes the number of characters typed per second, divides it by 5, and multiplies it by 60.

To play, download the typelearn.py file. Navigate to the file in your terminal, and start the script by running 'python typelearn.py'. That's it!

*Note: Requires external dependencies. Make sure you have 'pip', a python package manager. This can be downloaded via Homebrew or any other package management system. Run 'pip install praw' in terminal to download the required libraries.

*Note: Optimized for mac usage.
