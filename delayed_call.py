import pyglet

class NoCookie: pass

class DelayedCall:        
    def __init__(self, func, delay, cookie = NoCookie, periodic = False):   
        self.periodic = periodic
        self.scheduled = False
        if func:
            if periodic:
                if delay > 0:
                    pyglet.clock.schedule_interval(self._callme, delay / 1000.0, cookie)
                else:
                    pyglet.clock.schedule(self._callme, cookie)
            else:
                pyglet.clock.schedule_once(self._callme, delay / 1000.0, cookie)
            self.func = func
            self.scheduled = True
   
    def _callme(self, delta, cookie):
        if cookie == NoCookie:
            result = self.func()
        else:
            result = self.func(cookie)
        
        if not self.periodic:
            self.scheduled = False
        else:
            if result != True:
                self.cancel()
        
    def cancel(self):
        if self.scheduled:
            pyglet.clock.unschedule(self._callme)
        self.scheduled = False
    
    def __del__(self):
        self.cancel()


class PeriodicCall(DelayedCall):        
    def __init__(self, func, delay, cookie = NoCookie):
        DelayedCall.__init__(self, func, delay, cookie, periodic=True)

##
# Regression Tests
##
import unittest
from test import test_support

class TestDelayedCall(unittest.TestCase):
    def setUp(self):
        self.window = pyglet.window.Window()
         
    def tearDown(self):
        pass

    def callme(self, cookie):
        self.cookie = cookie
        self.window.close()

    def test_dc(self):
        self.cookie = None
        dc = DelayedCall(self.callme, 1000, "hello")
        pyglet.app.run()
        assert self.cookie == "hello"

class TestEveryFrame(TestDelayedCall):
    def countdown(self):
        self.counter -=1
        if self.counter == 0:
            self.window.close()
        return self.counter > 0
        
    def test_dc(self):
        self.counter=100
        dc = PeriodicCall(self.countdown, 0)
        pyglet.app.run()
        assert self.counter == 0
    

class TestPeriodic(TestDelayedCall):
    def countdown(self):
        self.counter -=1
        if self.counter == 0:
            self.window.close()
        return self.counter > 0

    def test_dc(self):
        self.counter=3
        dc = PeriodicCall(self.countdown, 1000)
        pyglet.app.run()
        assert self.counter == 0
        
def test_main():
    test_support.run_unittest(
        TestDelayedCall,
        TestEveryFrame,
        TestPeriodic
        #... list other tests ...
    )

if __name__ == "__main__":
    test_main()