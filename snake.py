import itertools, time, random
from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red, blue

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
        self.snake_segments = [(10, 10), (10, 11), (10, 12)]
        self.width = width
        self.height = height
        self.direction = (1, 0)
        self.isDead = False
    def render(self):
        a = FSArray(self.height, self.width)
        # Border
        for i in range(0, self.width):
            a[i, 0] = bold('*')
            a[i, self.height] = bold('*')
        for j in range(0, self.height):
            a[0, j] = bold('*')
            a[self.width, j] = bold('*')
        # If not dead, add snake to screen
        if not self.isDead:
            for seg in self.snake_segments:
                a[seg[0],seg[1]] = blue('X')
            return a
        else:
            a = self.deathSequence(a)
            return a
    def move(self):
    	new_x = self.snake_segments[0][0] + self.direction[0]
    	new_y = self.snake_segments[0][1] + self.direction[1]
    	if new_x == 0 or new_x == self.width or new_y == 0 or new_y == self.height:
    		self.isDead = True
        elif (new_x, new_y) in self.snake_segments:
            self.isDead = True
    	else:
        	self.snake_segments.insert(0, (new_x, new_y))
        	self.snake_segments.pop(3)
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
                        game.direction = (-1, 0)
                        last_c = '<UP>'
                    elif c == '<DOWN>' and last_c != '<UP>':
                        game.direction = (1, 0)
                        last_c = '<DOWN>'
                    elif c == '<LEFT>' and last_c != '<RIGHT>':
                        game.direction = (0, -1)
                        last_c = '<LEFT>'
                    elif c == '<RIGHT>' and last_c != '<LEFT>':
                        game.direction = (0, 1)
                        last_c = '<RIGHT>'
                    c = None
                    if time_per_frame < t - t0:
                        break

                #fps = 'FPS: %.1f' % counter.fps()
                #a[0:1, 0:len(fps)] = [fps]

                game.move()
                a = game.render() # insert death boolean
                window.render_to_terminal(a)
                #counter.frame()
                

if __name__ == '__main__':
    main()
