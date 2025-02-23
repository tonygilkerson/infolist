import sys
import tty
import termios

# read a single character on a unix system
# https://exceptionshub.com/python-read-a-single-character-from-the-user.html
def read_unix(count: int):
    fd = sys.stdin.fileno()

    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(count)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch