from utils import *
from pynput.keyboard import Key, Listener

# Global Keys used
PAUSE_KEY = Key.space
EXIT_KEY = Key.esc

# Global direction of snake
DIR = Dir.IDLE
PAUSED_DIR = Dir.IDLE


def _is_char_key(key, char):
    return hasattr(key, 'char') and key.char == char


def snake_on_press(key):
    global DIR, PAUSED_DIR
    # Select direction on key press
    if key is Key.up or _is_char_key(key, 'w'):
        DIR = Dir.UP
    elif key is Key.down or _is_char_key(key, 's'):
        DIR = Dir.DOWN
    elif key is Key.left or _is_char_key(key, 'a'):
        DIR = Dir.LEFT
    elif key is Key.right or _is_char_key(key, 'd'):
        DIR = Dir.RIGHT
    elif key is PAUSE_KEY:
        if DIR is Dir.STOP:
            # Unpause
            DIR = PAUSED_DIR
            PAUSED_DIR = Dir.STOP
        else:
            # Pause
            PAUSED_DIR = DIR
            DIR = Dir.STOP


def on_release(key):
    global EXIT_KEY
    if key == EXIT_KEY:
        # Stop listener
        return False


def global_direction():
    global DIR
    return DIR


def get_snek_listener():
    return Listener(on_press=snake_on_press, on_release=on_release)
