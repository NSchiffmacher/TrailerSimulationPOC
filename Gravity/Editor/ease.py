import math
import matplotlib.pyplot as plt
import numpy as np
import time


class EaseInOut:
    def __init__(self, start_time, anim_length, from_value, to_value):
        self.start_time = start_time
        self.length = anim_length
        self.from_value = from_value
        self.to_value = to_value

        self.a = 0.001
        self.prop = 0.98
        self.offset = math.log(1/(1-self.prop))

        self.start_time = time.time()
        self.done = False

        self.i = 0

    def eval(self, t):
        dt = t - self.start_time
        if dt > self.length:
            self.done = True
            print(self.i)
            return self.to_value

        raw_val = 0
        x = self.translate(dt, 0, self.length, 0, 2*self.offset/self.a)
        if dt <= self.length / 2:
            raw_val = math.exp(self.a * x - self.offset)-1
        else:
            raw_val = 1 - math.exp(-self.a * x + self.offset)

        self.i += 1
        return self.translate(raw_val, -self.prop, self.prop, self.from_value, self.to_value)

        
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)


if __name__ == '__main__':
    ease = EaseInOut(50,0,-500)

    xs = np.linspace(0,50,1000)
    ys = []
    for i in range(len(xs)):
        ys.append(ease.eval(xs[i]))
    plt.plot(xs, ys)
    plt.show()