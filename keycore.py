import os
import struct
import platform
import curses
import signal
import subprocess
from subprocess import call

screen = curses.initscr()
active_key_offset_x = 0
active_key_offset_y = 0
 
def get_terminal_size():
    current_os = platform.system()
    tuple_xy = None
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)
    return tuple_xy 

def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

def interrupt_handler(signum, frame):
    screen.move(active_key_offset_y, 0)
    screen.clrtoeol()
    screen.refresh()
    screen.addstr(active_key_offset_y, (sizex / 2) - 19, "Are you sure you want to quit? [Y/N]: ")
    
    key = ''
    while True:
        key = screen.getch()
        if key > 0:
            if key == ord('y') or key == ord('Y'):
                FNULL = open(os.devnull, 'w')
                call(['filetool.sh', '-b'], stdout=FNULL, stderr=subprocess.STDOUT)
                call(['exitcheck.sh', 'shutdown'], stdout=FNULL, stderr=subprocess.STDOUT)
            else:
                screen.addstr(active_key_offset_y, (sizex / 2) - 15, "Press a key to begin testing!")
                screen.refresh()
                break
 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)
    sizex, sizey = get_terminal_size()

    try:
        curses.curs_set(0)
    except:
        curses.curs_set(1)

    curses.cbreak()
    screen.keypad(1)

    title_offset_x = (sizex / 2) - 20
    title_offset_y = (sizey / 2) - 3

    screen.addstr(title_offset_y, title_offset_x, " __ _  ____  _  _  ___  __  ____  ____ ")
    screen.addstr(title_offset_y + 1, title_offset_x, "(  / )(  __)( \/ )/ __)/  \(  _ \(  __)")
    screen.addstr(title_offset_y + 2, title_offset_x, " )  (  ) _)  )  /( (__(  O ))   / ) _) ")
    screen.addstr(title_offset_y + 3, title_offset_x, "(__\_)(____)(__/  \___)\__/(__\_)(____)")
    screen.refresh()

    key = ''
    active_key_offset_x = (sizex / 2) - 13
    active_key_offset_y = title_offset_y + 5

    screen.addstr(active_key_offset_y, (sizex / 2) - 15, "Press a key to begin testing!")

    while True:
        key = screen.getch()
        screen.move(active_key_offset_y, 0)
        screen.clrtoeol()
        screen.refresh()

        if key > 0:
            screen.addstr(active_key_offset_y, active_key_offset_x, "You are pressing key {0}".format(key))

        screen.refresh()

    curses.endwin()