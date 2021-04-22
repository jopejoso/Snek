from pynput.keyboard import Key, Listener
import sys
from time import sleep
import os
from enum import Enum
from random import randint

class Dir(Enum):
    IDLE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Global direction of dot
DIR = Dir.IDLE
DEBUG = False

def disable_input():
    os.system("stty -echo")

def enable_input():
    os.system("stty echo")


def on_press(key):
    global DIR
    global DEBUG
    # Select dot direction on key press
    if key is Key.up:
        DIR = Dir.UP
    elif key is Key.down:
        DIR = Dir.DOWN
    elif key is Key.left:
        DIR = Dir.LEFT
    elif key is Key.right:
        DIR = Dir.RIGHT

    if DEBUG:
        print('{} -> {}'.format(key, DIR))
        sys.stdout.flush()

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False


def round(num, _min, _max):
    if num < _min:
        return _min
    elif num > _max:
        return _max
    return num


def clearAll():
    #os.system('clear')
    # Nasty hack for fast console clear
    sys.stdout.write(chr(27) + "[1;1H" + chr(27) + "[2J");

class FieldSize:

    def to1D(self, x:int, y:int):
        return y * self.size + x

    def __init__(self, size:int=50):
        self.size = size
        self.max1D = self.to1D(size-1, size-1)

    def x(self, num:int):
        return int( num % self.size )

    def y(self, num:int):
        return int( num / self.size )

    def xy(self, num:int):
        return self.x(num), self.y(num)

    def _in(self, ax:int):
        return ax >= 0 and ax < self.size

    def isIn(self, x:int, y:int):
        return self._in(x) and self._in(y)
        


class Snake:
    def __init__(self, fieldSize:FieldSize, initDir:Dir=Dir.RIGHT, points=None):
        if points is None:
            points = list()
            num = int(fieldSize.size / 3)
            mid = int(fieldSize.size / 2)
            x = 0
            for y in range(mid + num, mid, - 1):
                points.append(fieldSize.to1D(x, y))
        self.fieldSize = fieldSize
        self.direction = initDir
        self.plist = points
        self.pset = set(points)
        self.oposite = {Dir.UP:Dir.DOWN, Dir.DOWN:Dir.UP, Dir.LEFT:Dir.RIGHT, Dir.RIGHT:Dir.LEFT}

    def _eat(self, x:int, y:int):
        p = self.fieldSize.to1D(x, y)
        self.plist.append(p)
        self.pset.add(p)

    def _move(self, x:int, y:int, food:bool):
        self._eat(x, y)
        if not food:
            pfirst = self.plist.pop(0)
            self.pset.remove(pfirst)

    def containsPoints(self, x:int, y:int):
        p = self.fieldSize.to1D(x, y)
        return p in self.pset

    def containsPoint(self, p:int):
        return p in self.pset

    def next(self):
        head = self.plist[-1]
        x, y = self.fieldSize.xy(head)
        if self.direction is Dir.UP:
            y -= 1
        elif self.direction is Dir.DOWN:
            y += 1
        elif self.direction is Dir.LEFT:
            x -= 1
        elif self.direction is Dir.RIGHT:
            x += 1
        return x, y

    def isValid(self, x:int, y:int):
        return self.fieldSize.isIn(x, y) and not self.containsPoints(x, y)

    def move(self, food:bool):
        x, y = self.next()
        if self.isValid(x, y):
            self._move(x, y, food)
            return True
        else:
            return False

    def setDir(self, direction:Dir):
        if direction is not Dir.IDLE and self.oposite[direction] is not self.direction:
            self.direction = direction


class Field:
    def _define_empty_field_str(self):
        m = self.fieldSize.size
        topBot = '+' + ( '-' * m ) + '+'
        empties = '|' + ( self.cempty * m ) + '|'
        self.emptyTemplate = topBot + '\n' + ((empties + '\n') * m) + topBot

    def _new_food(self, foodcnt:int=1):
        cnt = 0
        while cnt < foodcnt:
            f = randint(0, self.fieldSize.max1D)
            if f not in self.food and not self.snake.containsPoint(f):
                self.food.add(f)
                cnt += 1

    def _change_food(self, old):
        self.food.remove(old)
        self._new_food()

    def __init__(self, size:int=50, foodcnt:int=1, cfood='*', csnake='+', cshead='o', cempty=' '):
        self.cfood = cfood
        self.csnake = csnake
        self.cshead = cshead
        self.cempty = cempty
        self.fieldSize = FieldSize(size)
        self.printFieldSize = FieldSize(size + 3) # Added characters: '|', '|', '\n'
        self.snake = Snake(self.fieldSize)
        self.ongoing = True
        self._define_empty_field_str()
        self.food = set()
        self._new_food(foodcnt=foodcnt)

    def move(self, direction:Dir):
        if not self.ongoing:
            return self.ongoing
        self.snake.setDir(direction)
        x, y = self.snake.next()
        p = self.fieldSize.to1D(x, y)
        isfood = p in self.food
        self.ongoing = self.snake.move(isfood)
        if isfood:
            self._change_food(p)
        return self.ongoing
    
    def _get_print_point(self, field_point:int):
        x, y = self.fieldSize.xy(field_point)
        return self.printFieldSize.to1D(x + 1, y + 1)

    def printState(self):
        clearAll()

        string_list = list(self.emptyTemplate)

        # Food
        for f in self.food:
            pf = self._get_print_point(f)
            string_list[pf] = self.cfood
        # Snake body
        for s in self.snake.plist:
            ps = self._get_print_point(s)
            string_list[ps] = self.csnake
        # Snake head
        h = self.snake.plist[-1]
        ps = self._get_print_point(s)
        string_list[ps] = self.cshead

        print(''.join(string_list))
        sys.stdout.flush()
        

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


if __name__ == '__main__':
    disable_input()

    speed = Speed.S4
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    field = Field(25)

    while True:
        field.printState()
        if DEBUG:
            print('{}'.format(DIR))
            sys.stdout.flush()
        game_on = field.move(DIR)
        if not game_on or not listener.running:
            break
        sleep(speed.value)

    enable_input()

    print("Snek done :)")
    sleep(1.0)

