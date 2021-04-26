from time import sleep
from keyshandler import *
from random import randint
import argparse


class FieldSize:

    def to1D(self, x: int, y: int):
        return y * self.size + x

    def __init__(self, size: int = 50):
        self.size = size
        self.max1D = self.to1D(size - 1, size - 1)

    def x(self, num: int):
        return int(num % self.size)

    def y(self, num: int):
        return int(num / self.size)

    def xy(self, num: int):
        return self.x(num), self.y(num)

    def _in(self, ax: int):
        return 0 <= ax < self.size

    def isIn(self, x: int, y: int):
        return self._in(x) and self._in(y)


class Snake:
    def __init__(self, fieldSize: FieldSize, initDir: Dir = Dir.RIGHT, points=None):
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
        self.oppositeDir = {Dir.UP: Dir.DOWN, Dir.DOWN: Dir.UP, Dir.LEFT: Dir.RIGHT, Dir.RIGHT: Dir.LEFT}

    def _eat(self, x: int, y: int):
        p = self.fieldSize.to1D(x, y)
        self.plist.append(p)
        self.pset.add(p)

    def _move(self, x: int, y: int, food: bool):
        self._eat(x, y)
        if not food:
            pfirst = self.plist.pop(0)
            self.pset.remove(pfirst)

    def containsPoints(self, x: int, y: int):
        p = self.fieldSize.to1D(x, y)
        return p in self.pset

    def containsPoint(self, p: int):
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

    def isValid(self, x: int, y: int):
        return self.fieldSize.isIn(x, y) and not self.containsPoints(x, y)

    def move(self, food: bool):
        x, y = self.next()
        if self.isValid(x, y):
            self._move(x, y, food)
            return True
        else:
            return False

    def setDir(self, direction: Dir):
        if direction is not Dir.IDLE and self.oppositeDir[direction] is not self.direction:
            self.direction = direction

    def size(self):
        return len(self.plist)


class Field:
    def _define_empty_field_str(self):
        m = self.fieldSize.size
        topBot = '+' + ('-' * m) + '+'
        empties = '|' + (self.cempty * m) + '|'
        self.emptyTemplate = topBot + '\n' + ((empties + '\n') * m) + topBot

    def _new_food(self, foodcnt: int = 1):
        cnt = 0
        while cnt < foodcnt:
            f = randint(0, self.fieldSize.max1D)
            if f not in self.food and not self.snake.containsPoint(f):
                self.food.add(f)
                cnt += 1

    def _change_food(self, old):
        self.food.remove(old)
        self._new_food()

    def __init__(self, size: int = 50, foodcnt: int = 1, cfood='*', csnake='+', cshead='o', cempty=' '):
        self.cfood = cfood
        self.csnake = csnake
        self.cshead = cshead
        self.cempty = cempty
        self.fieldSize = FieldSize(size)
        self.printFieldSize = FieldSize(size + 3)  # Added characters: '|', '|', '\n'
        self.snake = Snake(self.fieldSize)
        self.ongoing = True
        self._define_empty_field_str()
        self.food = set()
        self._new_food(foodcnt=foodcnt)

    def move(self, direction: Dir):
        if not self.ongoing or direction is Dir.STOP:
            return self.ongoing
        self.snake.setDir(direction)
        x, y = self.snake.next()
        p = self.fieldSize.to1D(x, y)
        isfood = p in self.food
        self.ongoing = self.snake.move(isfood)
        if isfood:
            self._change_food(p)
        return self.ongoing

    def _get_print_point(self, field_point: int):
        x, y = self.fieldSize.xy(field_point)
        return self.printFieldSize.to1D(x + 1, y + 1)

    def __str__(self):
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
        ph = self._get_print_point(h)
        string_list[ph] = self.cshead
        return ''.join(string_list)


class Game:
    def __init__(self, speed=Speed.S4, size=25):
        self.field = Field(size)
        self.listener = get_snek_listener()
        self.speed = speed

    def start_msg(self):
        size = self.field.fieldSize.size + 2
        str_list = [' ASCII Snake ', ' Pause: <Space> ', ' Exit: <Esc> ', ' Score: {:>3} '.format(str(self.field.snake.size()))]
        max_size = max([len(s) for s in str_list])
        before = int((size - max_size) / 2) if max_size < size else 0
        ret_list = ['=' * size]
        for s in str_list:
            ret_list.append('-' * before + s + '-' * max(0, size - len(s) - before))
        ret_list.append('=' * size)
        return '\n'.join(ret_list) + '\n'

    def play(self):
        self.listener.start()

        def _play():
            while True:
                clear_all()
                print(self.start_msg())
                print(self.field)
                sys.stdout.flush()
                game_on = self.field.move(global_direction())
                if not game_on or not self.listener.running:
                    break
                sleep(self.speed.value)

        clean_console_action(_play)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple ASCII snake game')
    parser.add_argument('-s', metavar='N', type=int, help='size of the snake')
    args = parser.parse_args()
    fsize = args.s if args.s is not None else 20
    game = Game(size=fsize)
    game.play()
