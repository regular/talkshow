def flatten_rect(r):
    ((x,y),(w,h)) = r
    return (x,y,w,h)

def rect_overlaps(r1, r2):
    # check if r1 is completely outside of r2
    # andreturn the inverse.
    ((x1,y1),(w1,h1)) = r1
    ((x2,y2),(w2,h2)) = r2
    return not ((x1<x2 and x1+w1 <= x2 or x1>=x2+w2) or (y1<y2 and y1+h1 <= y2 or y1>=y2+h2))

def clip_rect(r1, r2):
    if rect_overlaps(r1, r2):
        ((x1,y1),(w1,h1)) = r1
        ((x2,y2),(w2,h2)) = r2

        nx = max(x1, x2)
        ny = max(y1, y2)

        w = min(x1 + w1, x2 + w2) - nx
        h = min(y1 + h1, y2 + h2) - ny

        return ((nx, ny), (w, h))
    else:
        return ((0,0),(0,0))


##
# Regression Tests
##
import unittest
from test import test_support

class TestRectTools(unittest.TestCase):
    def test_flatten(self):
        assert flatten_rect(((1,2),(3,4))) == (1,2,3,4)
        
    def test_overlaps(self):
        assert rect_overlaps( ((1,1),(1,1)), ((1,1),(1,1)) ) == True
        assert rect_overlaps( ((1,1),(1,1)), ((2,1),(1,1)) ) == False
        assert rect_overlaps( ((1,1),(1,1)), ((1,2),(1,1)) ) == False
        assert rect_overlaps( ((1,1),(1,1)), ((0,1),(1,1)) ) == False
        assert rect_overlaps( ((1,1),(1,1)), ((1,0),(1,1)) ) == False
        assert rect_overlaps( ((1,1),(1,1)), ((0,1),(2,1)) ) == True
        assert rect_overlaps( ((1,1),(1,1)), ((1,0),(1,2)) ) == True
        assert rect_overlaps( ((1,1),(1,1)), ((0,0),(2,2)) ) == True
        assert rect_overlaps( ((10,10),(20,20)), ((5,5),(200,200)) ) == True
        assert rect_overlaps( ((5,5),(200,200)), ((10,10),(20,20)) ) == True
        assert rect_overlaps( ((0,0),(20,20)), ((5,5),(200,200)) ) == True
        assert rect_overlaps( ((5,5),(200,200)), ((0,0),(20,20)) ) == True
        assert rect_overlaps( ((0,0),(20,20)), ((25,5),(200,200)) ) == False
        assert rect_overlaps( ((0,0),(20,20)), ((25,25),(200,200)) ) == False
        assert rect_overlaps( ((25,5),(200,200)), ((0,0),(20,20)) ) == False
        assert rect_overlaps( ((25,25),(200,200)), ((0,0),(20,20)) ) == False

    def test_clip(self):
        assert clip_rect( ((25,5),(200,200)), ((0,0),(20,20)) ) == ((0,0),(0, 0))
        assert clip_rect( ((25,5),(200,200)), ((0,0),(30,30)) ) == ((25,5),(5, 25))
        assert clip_rect( ((1,1),(1,1)), ((1,1),(1,1)) ) == ((1,1),(1,1))
        assert clip_rect( ((100,100),(10,10)), ((10,10),(200,200)) ) == ((100,100),(10,10))
        assert clip_rect( ((0,0),(55,100)), ((45,0),(55,200)) ) == ((45,0),(10,100))

                
def test_main():
    test_support.run_unittest(
        TestRectTools,
        #... list other tests ...
    )

if __name__ == "__main__":
    test_main()
