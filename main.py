import curses
import datetime

def init_colors(bg_color=-1):
    """initialize colors. return a set of colors in a dictionary.
    Parameters
    ----------
    bg_color number:
      the id for background color
    Return
    ------
    colors dict:
      a set of colors in a dictionary object.
    """

    # initialize the color pair
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
    #for i in range(0, 20):
        # pair number, foreground color, background color
        #curses.init_pair(i + 1, i, -1)
        curses.init_pair(i + 1, i, bg_color)
        #curses.init_pair(i + 1, i, 8)

    return {
        "grey": curses.color_pair(9), # grey
        "yellow": curses.color_pair(12), # yellow
        "blue": curses.color_pair(13), # blue
        "lightblue": curses.color_pair(22), # blue
        "green": curses.color_pair(48), # Green
        "red": curses.color_pair(10), # red
    }

# paint the welcome message.
def welcome_msg(stdscr, sy, sx):
    """Paint the welcome message from the starting y and x axis.
    Parameters
    ----------
    sy number:
      the starting unit's y axis
    sx number:
      the starting unit's x axis
    """

    stdscr.addstr(sy, sx, "Welcome to Curses colck!", curses.color_pair(12))
    stdscr.addstr(sy + 2, sx, "' ': Start/Pause/Resume stopwatch")
    stdscr.addstr(sy + 3, sx, "'r': Reset stopwatch")
    stdscr.addstr(sy + 4, sx, "'q': Quit")

    vertical_divider(stdscr, sy, sx + 35, 20, curses.color_pair(22))

# paint the vertical divider
def vertical_divider(stdscr, sy, sx, length, color):

    for y in range(sy, sy + length):
        # 9616 - ▐
        stdscr.addstr(y, sx, chr(9616), color)

# paint stopwatch
def paint_stopwatch(stdscr, sy, sx, time, color):

    stdscr.addstr(sy, sx, ' ' * 20)
    stdscr.addstr(sy, sx, 'Stopwatch: {0}'.format(time), color)

def clock(stdscr):

    # initialize colors.
    colors = init_colors()

    # get the screen size
    sh, sw = stdscr.getmaxyx()

    # calculate the starting unit.
    # ul: upper left
    uly, ulx = 2, 10

    # paint welcome message.
    welcome_msg(stdscr, uly, ulx)
    # paint the stopwatch.
            
    paint_stopwatch(stdscr, uly + 2, 50, "0.0", colors['green'])

    # set 0 to hide the cursor.
    curses.curs_set(0)
    # set up this to make the while loop work.
    stdscr.nodelay(1)
    # timeout is using millisecond (ms) as unit
    stdscr.timeout(50)

    stopwatch = 0
    counting = False
    start = datetime.datetime.now()

    while True:

        # hold to wait for user's input.
        # the getch() will return -1 if timeout!
        userkey = stdscr.getch()

        if userkey in [27, 113, 81]:
            # user pressed ESC, q or Q
            break;
        elif userkey >= 0:
            # user press any other key.
            # greater or eaqual to 0 to make sure this is not timeout
            if counting:
                # turn off counting
                counting = False
                # reset stopwatch.
                stopwatch = 0
            else:
                # turn on counting.
                counting = True
                if stopwatch == 0:
                    # this is start.
                    start = datetime.datetime.now()
                    #stopwatch = (datetime.datetime.now() - start).seconds

        if counting:
            stopwatch = (datetime.datetime.now() - start).seconds
            paint_stopwatch(stdscr, uly + 2, 50, str(stopwatch), colors['green'])

curses.wrapper(clock)
