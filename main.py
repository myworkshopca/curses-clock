import curses
import datetime

# initialize colors.
def initcolors(bg_color=-1):

    # initialize the color pair
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
    #for i in range(0, 20):
        # pair number, foreground color, background color
        #curses.init_pair(i + 1, i, -1)
        curses.init_pair(i + 1, i, bg_color)
        #curses.init_pair(i + 1, i, 8)

# paint the welcome message.
def welcome_msg(stdscr, sh, sw):

    # set the start unit.
    sy = 5
    sx = 10

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
    initcolors()

    # get the screen size
    sh, sw = stdscr.getmaxyx()

    # paint welcome message.
    welcome_msg(stdscr, sh, sw)
    # paint the stopwatch.
            
    paint_stopwatch(stdscr, 7, 50, " ", curses.color_pair(3))

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
            paint_stopwatch(stdscr, 7, 50, str(stopwatch), curses.color_pair(3))

curses.wrapper(clock)
