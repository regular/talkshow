import pyglet
import weakref

class NoCookie: pass

class DelayedCall:
    
    # In order to be able to cancel a scheduled function call
    # we need to make sure to pass a unique callable to pyglet's
    # scheduleXX() function. (in contrast to a single static function)
    # However, since we want to have automatic unscheduling when
    # a DelayedCall object gets out of scope, we cannot pass a strong
    # reference to our DelayedCall object to scheduleXXX() (pyglet would
    # keep its reference count from becoming zero)
    # That's why we construct a unique Identifier object that
    # simply forwards the scheduled call to a static method and passes
    # the *weak* reference to our instance we passed to scheduleXXX()
    # The static method _callme() acts like an instance method after having
    # resolved the weak reference.
    # THe Identifier instance can be used to cancel a specific instance
    # of DelayedCall 
    
    class Identifier:
        def __call__(self,delta,ref):
            DelayedCall._callme(ref)
            
    def __init__(self, func, delay, cookie = NoCookie, periodic = False):   
        assert delay != None
        assert delay == int(delay)
        
        self.periodic = periodic
        self.scheduled = False
        self.cookie = cookie
        self.identifier = DelayedCall.Identifier()
        
        if func:
            if periodic:
                if delay > 0:
                    pyglet.clock.schedule_interval(self.identifier, delay / 1000.0, weakref.ref(self))
                else:
                    pyglet.clock.schedule(self.identifier, weakref.ref(self))
            else:
                pyglet.clock.schedule_once(self.identifier, delay / 1000.0, weakref.ref(self))
            self.func = func
            self.scheduled = True
   
    @staticmethod    
    def _callme(ref):
        self = ref()
        if self == None:
            return
        
        if self.cookie == NoCookie:
            result = self.func()
        else:
            result = self.func(self.cookie)
        
        if not self.periodic:
            self.scheduled = False
        else:
            if result != True:
                self.cancel()
    
    def cancel(self):
        if self.scheduled:
            print "cancel!"
            pyglet.clock.unschedule(self.identifier)
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
        
class TestTwoCalls(TestDelayedCall):
    def callme(self, cookie):
        self.cookie = cookie
        
    def test_dc(self):
        self.cookie = None
        dc1 = DelayedCall(self.callme, 100, "huhu")
        dc2 = DelayedCall(self.window.close, 200)
        pyglet.app.run()
        assert self.cookie == "huhu"

class TestCancel1(TestDelayedCall):
    def dontcallme(self, cookie):
        print "DONT CALL ME I SAY!"
        self.cookie = cookie

    def test_dc(self):
        self.cookie = None
        dc1 = DelayedCall(self.dontcallme, 100, "huhu")
        dc2 = DelayedCall(self.window.close, 200)
        dc3 = DelayedCall(dc1.cancel, 50)
        pyglet.app.run()
        assert self.cookie == None
 
 
class TestCancel2(TestDelayedCall):
    def dontcallme(self, cookie):
        print "DONT CALL ME I SAY!"
        self.cookie = cookie

    def test_dc(self):
        self.cookie = None
        dc1 = DelayedCall(self.dontcallme, 100, "huhu")
        dc2 = DelayedCall(self.window.close, 200)
        dc1 = None
        pyglet.app.run()
        assert self.cookie == None
  
def test_main():
    test_support.run_unittest(
        TestDelayedCall,
        TestEveryFrame,
        TestPeriodic,
        TestTwoCalls,
        TestCancel1,
        TestCancel2
        #... list other tests ...
    )

if __name__ == "__main__":
    test_main()