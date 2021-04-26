import sys
import os
from enum import Enum


def disable_input():
    os.system("stty -echo")


def enable_input():
    os.system("stty echo")


class Speed(Enum):
    S0 = 0.3
    S1 = 0.25
    S2 = 0.20
    S3 = 0.15
    S4 = 0.1
    S5 = 0.08
    S6 = 0.06
    S7 = 0.05
    S8 = 0.035
    S9 = 0.025


class Dir(Enum):
    IDLE = 0
    STOP = 1
    UP = 2
    DOWN = 3
    LEFT = 4
    RIGHT = 5


def clear_all():
    # Nasty hack for fast console clear
    sys.stdout.write(chr(27) + "[1;1H" + chr(27) + "[2J")


def clean_console_action(action):
    try:
        disable_input()
        action()
    except Exception:
        enable_input()
        return
    enable_input()
