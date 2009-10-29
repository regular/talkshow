import math
import pyglet
import string
import wrappers
from pyglet.gl import *

def getCapVertexCount(segment_count):
    return segment_count*2 + 3
    
def getCapIndexCount(segment_count):
    return segment_count * (3 * 3)

def setVertex(vb, vi, x, y, z, color, alpha):
    vb.vertices[vi*3:vi*3+3] = [x, y, z]
    vb.colors[vi*4:vi*4+4] = [color[0], color[1], color[2], alpha]

def createCap(angle, ox, oy, segment_count, radius, outer_radius, vb, ib, vi, ii, color, alpha):
    first_vi = vi

    a = angle
    x = math.cos(a) * radius + ox
    y = math.sin(a) * radius + oy
    xo = math.cos(a) * outer_radius + ox
    yo = math.sin(a) * outer_radius + oy

    z = 0

    setVertex(vb, vi+0, ox, oy, z, color, alpha)
    setVertex(vb, vi+1, x, y, z, color, alpha)
    setVertex(vb, vi+2, xo, yo, z, color, 0)
    
    vi += 3
    
    for i in range(segment_count):
        a = angle + math.pi / 2.0 / segment_count * (i + 1)
        x = math.cos(a) * radius + ox
        y = math.sin(a) * radius + oy
        
        xo = math.cos(a) * outer_radius + ox
        yo = math.sin(a) * outer_radius + oy
    
        setVertex(vb, vi, x, y, z, color, alpha)
        setVertex(vb, vi+1, xo, yo, z, color, 0)
        
        ib[ii+0] = first_vi
        ib[ii+1] = vi - 2
        ib[ii+2] = vi
        
        ib[ii+3] = vi - 2 
        ib[ii+4] = vi - 1
        ib[ii+5] = vi + 1
        
        ib[ii+6] = vi - 2 
        ib[ii+7] = vi + 1
        ib[ii+8] = vi
        
        vi += 2
        ii += 9

    return (vi, ii)

class RoundRect(wrappers.Visible):
    RADIUS = 10
    OUTER_RADIUS = 13
    SEGMENT_COUNT = 8
    
    def __init__(self, parent, name, x, y, w, h, radius=RADIUS, outer_radius=OUTER_RADIUS, color="#ff6e00"):                                     
        wrappers.Visible.__init__(self, parent, name, x,y,w,h)
                                     
        vertex_count = 4 * getCapVertexCount(self.SEGMENT_COUNT)
        index_count = 7 * 2 * 3 + 4 * getCapIndexCount(self.SEGMENT_COUNT)
        
        self.mesh = pyglet.graphics.vertex_list_indexed(vertex_count, [0]*index_count, "v3f", "c4B") 
                   
        self.color = (   # NOTE: r and b are swapped            
            string.atoi(color[5:7], 16),
            string.atoi(color[3:5], 16),
            string.atoi(color[1:3], 16)
        )
                
        self.radius = radius
        self.outer_radius = outer_radius
                
        self._reconstruct()

    def draw(self):
        if self.extent != self.current_extent:
            self._reconstruct()

        glMatrixMode(gl.GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x, self.y + self.h, 0);
        self.mesh.draw(pyglet.gl.GL_TRIANGLES)
        glPopMatrix()
                     
    def _reconstruct(self):
        self.current_extent = self.extent        
        self._fillBuffers(0, 0)

    def _fillBuffers(self, x, y):
        segment_count = self.SEGMENT_COUNT
        radius = self.radius
        outer_radius = self.outer_radius
        color = self.color
        alpha = 255

        vb = self.mesh
        ib = self.mesh.indices
    
        vi = 0
        ii = 0

        angle = 0
        
        # upper left
        vi_ul = vi
        ox = x + outer_radius
        oy = y + outer_radius
        vi, ii = createCap(math.pi , ox, oy, segment_count, radius, outer_radius, vb, ib, vi, ii, color, alpha)
                
        # lower left
        vi_ll = vi
        oy = y + self.h - outer_radius 
        ox = x + outer_radius   
        vi, ii = createCap(math.pi / 2, ox, oy, segment_count, radius, outer_radius, vb, ib, vi, ii, color, alpha)
        ve_ll = vi
        
        # connecting upper left with lower left        
        ib[ii+0:ii+2*2*3] = [  
                        vi_ul+1, vi_ll-2, vi_ll+1, 
                        vi_ul+1, vi_ll+1, ve_ll-2,

                        vi_ul+2, vi_ul+1, ve_ll-2, 
                        vi_ul+2, ve_ll-2, ve_ll-1
        ]
        
        ii += 2*2*3
                
        # upper right
        vi_ur = vi
        ox = x + self.w - outer_radius
        oy = y + outer_radius
        vi, ii = createCap(math.pi + math.pi/2 , ox, oy, segment_count, radius, outer_radius, vb, ib, vi, ii, color, alpha)
                
        # lower right
        vi_lr = vi
        oy = y + self.h - outer_radius             
        vi, ii = createCap(math.pi / 2  -    math.pi/2, ox, oy, segment_count, radius, outer_radius, vb, ib, vi, ii, color, alpha)
        ve_lr = vi
        
        # connecting upper right with lower right
        ib[ii+0:ii+2*2*3] = [  
                        vi_ur+1, vi_lr-2, vi_lr+1, 
                        vi_ur+1, vi_lr+1, ve_lr-2,
                        
                        vi_lr-2, vi_lr-1, vi_lr+2, 
                        vi_lr-2, vi_lr+2, vi_lr+1
        ]
        
        ii += 2*2*3
        
        # connecting upper left with upper right
        ib[ii+0:ii+3*2*3] = [  
                        vi_ll-2, vi_ur+2, vi_ur+1, 
                        vi_ll-2, vi_ur+2,vi_ll-1,
                        
        # connecting lower left with lower right

                        vi_ll+2, vi_ll+1, ve_lr-1, 
                        vi_ll+1,ve_lr-1,ve_lr-2,
                        
        # filling the center (opaque)
        
                        vi_ll-2, vi_ur+1,ve_lr-2,
                        vi_ll-2,  vi_ll+1 ,ve_lr-2,
                        
        ]
            