import weakref

LOOP = 1
SMOOTH = 2
PING_PONG = 4

T = 0

def now():
    return T

class AnimatedProperty:
    properties = {}

    @staticmethod
    def animate(owner, name, startvalue, endvalue, delay, duration=0, flags = 0):
        #if not hasattr(owner, name):
        #    print "HA?",owner
        #    dir(owner)
        #    raise Exception("Property to animate does not exist: " + name)
        
        funcs = []
        if flags & PING_PONG and flags & LOOP:
            funcs.append(lambda x: x-int(x) if not int(x)%2 else 1.0 - (x-int(x)))
        elif flags & LOOP:
            funcs.append(lambda x: x-int(x))
        if flags & SMOOTH:
            funcs.append(lambda x: (x*x) * (3.0-(2.0*x)))
            
        ap = (now(), weakref.ref(owner), startvalue, endvalue, delay, duration, funcs, flags & LOOP)
        AnimatedProperty.properties[(id(owner), name)] = ap
    
    @staticmethod
    def tick():
        pending = {}
        for k, ap in AnimatedProperty.properties.items():
            _id, name = k
            starttime, owner, \
            startvalue, endvalue, delay, duration, \
            funcs, loop = ap
            owner = owner()
            keep = True
            if owner:
                elapsed = (now() - starttime)
                elapsed -= delay
                if elapsed >= 0:
                    if duration > 0:
                        x = elapsed / float(duration)
                        if x >= 1.0 and not loop:
                            x = 1.0
                            keep = False
                    else:
                        x = 1.0
                        keep = False
                    for f in funcs:
                        x = f(x)
                    x = (endvalue - startvalue) *x + startvalue
                    setattr(owner, name, x)
            else:
                keep = False
            
            if keep:
                pending[k] = ap
        AnimatedProperty.properties = pending
                
#
# Regression Tests
##
import unittest
from test import test_support

class TestAnimatedProperty(unittest.TestCase):
    values = []
    
    def setValue(self, v):
        self.values.append((T,  int(v)))
        
    def getValue(self):
        return 0.0
    animateMe = property(getValue, setValue)
    
    def test_delay(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 100, 1000)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()
        
        assert self.values == [(1000, 100)]
        
    def test_linear(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 100, 500, 1000)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values == [(500, 0), (600, 10), (700, 20), (800, 30), (900, 40), (1000, 50), (1100, 60), (1200, 70), (1300, 80), (1400, 90), (1500, 100)]


    def test_smooth(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 1000, 0, 1000, flags = SMOOTH)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values ==  [(0, 0), (100, 28), (200, 104), (300, 216), (400, 352), (500, 500), (600, 648), (700, 783), (800, 896), (900, 972), (1000, 1000)]
 
 
    def test_loop(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 1000, 0, 1000, flags = LOOP)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values == [(0, 0), (100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600), (700, 700), (800, 800), (900, 900), (1000, 0), (1100, 100), (1200, 199), (1300, 300), (1400, 399), (1500, 500), (1600, 600), (1700, 700), (1800, 800), (1900, 899)]

    def test_ping_pong(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 1000, 0, 1000, flags = LOOP|PING_PONG)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values == [(0, 0), (100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600), (700, 700), (800, 800), (900, 900), (1000, 1000), (1100, 899), (1200, 800), (1300, 700), (1400, 600), (1500, 500), (1600, 399), (1700, 300), (1800, 199), (1900, 100)]

    def test_smooth_ping_pong(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 1000, 0, 1000, flags = LOOP|PING_PONG|SMOOTH)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values == [(0, 0), (100, 28), (200, 104), (300, 216), (400, 352), (500, 500), (600, 648), (700, 783), (800, 896), (900, 972), (1000, 1000), (1100, 972), (1200, 896), (1300, 783), (1400, 648), (1500, 500), (1600, 351), (1700, 216), (1800, 103), (1900, 28)]


    def test_smooth_loop(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 1000, 0, 1000, flags = LOOP|SMOOTH)
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values == [(0, 0), (100, 28), (200, 104), (300, 216), (400, 352), (500, 500), (600, 648), (700, 783), (800, 896), (900, 972), (1000, 0), (1100, 28), (1200, 103), (1300, 216), (1400, 351), (1500, 500), (1600, 648), (1700, 783), (1800, 896), (1900, 972)]

    def test_cancel(self):
        self.values = []
        global T
        T = 0
        AnimatedProperty.animate(self, "animateMe", 0, 1000, 0, 1000)
        AnimatedProperty.animate(self, "animateMe", 0, 0, 0)
        
        for t in range(20):
            T = t * 100
            AnimatedProperty.tick()

        assert self.values == [(0, 0)]

        
def test_main():
    test_support.run_unittest(
        TestAnimatedProperty
        #... list other tests ...
    )

if __name__ == "__main__":
    test_main()