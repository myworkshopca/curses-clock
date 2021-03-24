import curses
import datetime

def clock(stdscr):

    # set 0 to hide the cursor.
    curses.curs_set(0)
    # set up this to make the while loop work.
    stdscr.nodelay(1)
    # timeout is using millisecond (ms) as unit
    stdscr.timeout(50)

    stopwatch = 0
    counting = False
    start = datetime.datetime.now()

    stdscr.addstr(0, 0, "press any key to start and stop!")

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
            stdscr.addstr(3, 0, str(stopwatch))

curses.wrapper(clock)
