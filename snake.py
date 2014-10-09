import itertools, time, random
from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red, blue
from collections import namedtuple
from random import randint

Point = namedtuple("Point",["x","y"])

MAX_FPS = 10
time_per_frame = 1. / MAX_FPS
#isDead = False

class FrameCounter(object):
    def __init__(self):
        self.render_times = []
        self.dt = .5
    def frame(self):
        self.render_times.append(time.time())
    def fps(self):
        now = time.time()
        while self.render_times and self.render_times[0] < now - self.dt:
            self.render_times.pop(0)
        return len(self.render_times) / max(self.dt, now - self.render_times[0] if self.render_times else self.dt)

class SnakeGame(object):
    def __init__(self, width, height):
        self.snake_segments = [Point(x=10, y=10), Point(x=10, y=11), Point(x=10, y=12)]
        self.apple = Point(x=13, y=10)
        self.width = width
        self.height = height
        self.direction = Point(x=1, y=0)
        self.isDead = False
        self.snake_length = 3
    def render(self):
        a = FSArray(self.height, self.width)
        # Border
        for i in range(0, self.width):
            a[0, i] = bold('*')
            a[self.height - 1, i] = bold('*')
        for j in range(0, self.height):
            a[j, 0] = bold('*')
            a[j, self.width - 1] = bold('*')
        # Add an apple!
        self.create_apple(a)
        # If not dead, add snake to screen
        if not self.isDead:
            for seg in self.snake_segments:
                a[seg.y, seg.x] = blue('X')
            a[self.apple.y, self.apple.x] = red('Q')
            return a
        else:
            a = self.deathSequence(a)
            return a

    def move(self):
    	new_x = self.snake_segments[0].x + self.direction.x
    	new_y = self.snake_segments[0].y + self.direction.y
    	if new_x == 0 or new_x == self.width or new_y == 0 or new_y == self.height:
    		self.isDead = True
        elif Point(new_x, new_y) in self.snake_segments:
            self.isDead = True
    	else:
            self.snake_segments.insert(0, Point(new_x, new_y))
            if Point(new_x, new_y) == self.apple:
                self.apple = None
                self.snake_length += 1
            else:
                self.snake_segments.pop(self.snake_length)
    def create_apple(self, a):
        if self.apple is None:
            self.apple = Point(x = randint(1, self.width - 2), y = randint(1, self.height - 2))
            while self.apple in self.snake_segments:
                self.apple = Point(x = randint(1, self.width - 2), y = randint(1, self.height - 2))
    def deathSequence(self, a):
        a[10, 10] = red('X')
        a[10, 14] = red('X')
        a[12, 10] = red('_')
        a[12, 11] = red('_')
        a[12, 12] = red('_')
        a[12, 13] = red('_')
        a[12, 14] = red('_')
        return a

def main():
    counter = FrameCounter()
    with FullscreenWindow() as window:
    	# Why don't we see this? 
        print('Press escape to exit')
        game = SnakeGame(window.width, window.height)
        with Input() as input_generator:
            c = None
            last_c = '<DOWN>'
            for framenum in itertools.count(0):

                a = game.render() # insert death boolean
                window.render_to_terminal(a)

                t0 = time.time()
                while True:
                    t = time.time()
                    # This tells you how long you're willing to wait before you just move the snake along
                    # equal to time_per_frame
                    temp_c = input_generator.send(max(0, t - (t0 + time_per_frame)))                    
                    if temp_c is not None:
                        c = temp_c
                    if c is None:
                        pass
                    elif c == '<ESC>':
                        return
                    elif c == '<UP>' and last_c != '<DOWN>':
                        game.direction = Point(x=0, y=-1)
                        last_c = '<UP>'
                    elif c == '<DOWN>' and last_c != '<UP>':
                        game.direction = Point(x=0, y=1)
                        last_c = '<DOWN>'
                    elif c == '<LEFT>' and last_c != '<RIGHT>':
                        game.direction = Point(x=-1, y=0)
                        last_c = '<LEFT>'
                    elif c == '<RIGHT>' and last_c != '<LEFT>':
                        game.direction = Point(x=1, y=0)
                        last_c = '<RIGHT>'
                    c = None
                    if time_per_frame < t - t0:
                        break

                #fps = 'FPS: %.1f' % counter.fps()
                #a[0:1, 0:len(fps)] = [fps]

                game.move()

                #counter.frame()
                

if __name__ == '__main__':
    main()
