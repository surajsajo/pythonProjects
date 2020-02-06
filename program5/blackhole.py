# Black_Hole is singly derived from Simulton, updating by finding+removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    radius = 10
    def __init__(self,x,y,width=20,height=20):
        Simulton.__init__(self, x, y, width, height)
    
    def contains(self, xy):
        return self.distance([xy[0],xy[1]]) < Black_Hole.radius
    
    def update(self,model):
        eaten = set()
        for x in model.find(lambda x : isinstance(x, Prey)):
            if self.contains([x.get_location()[0],x.get_location()[1]]):
                eaten.add(x)
                model.remove(x)
        return eaten
    
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-self.get_dimension()[0]/2      , self.get_location()[1]-self.get_dimension()[1]/2,
                                self.get_location()[0]+self.get_dimension()[0]/2, self.get_location()[1]+self.get_dimension()[1]/2,
                                fill='#000000')
    

    
    