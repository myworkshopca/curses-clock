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
        "purple": curses.color_pair(56), # purple
    }

# paint the welcome message.
def welcome_msg(stdscr, sy, sx, color_dict):
    """Paint the welcome message from the starting y and x axis.
    Parameters
    ----------
    sy number:
      the starting unit's y axis
    sx number:
      the starting unit's x axis
    """

    stdscr.addstr(sy, sx, "Welcome to Curses Clock!", color_dict['yellow'])
    stdscr.addstr(sy + 2, sx, "' ': Start/Pause/Resume stopwatch")
    stdscr.addstr(sy + 3, sx, "'r': Reset stopwatch")
    stdscr.addstr(sy + 4, sx, "'q': Quit")

    vertical_divider(stdscr, sy, sx + 35, 20, color_dict)

# paint the vertical divider
def vertical_divider(stdscr, sy, sx, length, color_dict):

    for y in range(sy, sy + length):
        # 9616 - ▐
        stdscr.addstr(y, sx, chr(9616), color_dict['lightblue'])

# paint stopwatch
def paint_stopwatch(stdscr, sy, sx, delta, color_dict):

    stdscr.addstr(sy, sx, ' ' * 20)
    # we will paint the seconds and 1 / 10 second
    msg = 'Stopwatch: {0}.{1}'.format(delta.seconds, delta.microseconds // 100000)
    stdscr.addstr(sy, sx, msg, color_dict['green'])

# paint time.
def paint_time(stdscr, sy, sx, color_dict, time_zone="GMT"):

    stdscr.addstr(sy, sx, "Greenwich Mean Time (GMT)", color_dict['red'])
    stdscr.addstr(sy + 1, sx, ' ' * 20)
    now = datetime.datetime.now()
    stdscr.addstr(sy + 1, sx, str(now), color_dict['purple']);

def clock(stdscr):

    # initialize colors.
    colors = init_colors()

    # get the screen size
    sh, sw = stdscr.getmaxyx()

    # calculate the starting unit.
    # ul: upper left
    uly, ulx = 2, 10

    # paint welcome message.
    welcome_msg(stdscr, uly, ulx, colors)

    # set 0 to hide the cursor.
    curses.curs_set(0)
    # set up this to make the while loop work.
    stdscr.nodelay(1)
    # timeout is using millisecond (ms) as unit
    stdscr.timeout(100)

    # set to start from 0 delta.
    stopwatch = datetime.timedelta()
    counting = False
    start = datetime.datetime.now()
    # paint the stopwatch.
    paint_stopwatch(stdscr, uly + 2, 50, stopwatch, colors)

    while True:

        # hold to wait for user's input.
        # the getch() will return -1 if timeout!
        userkey = stdscr.getch()

        if userkey in [27, ord('q')]:
            # user pressed ESC, q
            break;
        elif userkey == ord(' '):
            # user press white space: start, pause ore resume the stopwatch.
            if counting:
                # turn off counting
                counting = False
                # reset stopwatch
                stopwatch += datetime.datetime.now() - start
            else:
                # turn on counting.
                counting = True
                # set the start.
                start = datetime.datetime.now()
        elif userkey == ord('r'):
            # reset the stopwatch.
            stopwatch = datetime.timedelta()
            counting = False
            start = datetime.datetime.now()
            # paint the stopwatch.
            paint_stopwatch(stdscr, uly + 2, 50, stopwatch, colors)

        if counting:
            paint_stopwatch(stdscr, uly + 2, 50,
                    stopwatch + (datetime.datetime.now() - start), colors)

        # paint current time
        paint_time(stdscr, uly + 4, 50, colors)

curses.wrapper(clock)
