"""
This Special Simulton is a mini neon green variation of the Black_Hole simulton 
starts off moving in a circular shape at a speed of 5 if it is not bouncing on a 
wall and if it is then it moves along the wall or it bounces really far across the 
canvas. 

As it eats more prey, it increases it's speed and starts moving in a bigger circle
and the circle gets bigger and bigger as the speed increases and once it hits the wall
with a high speed it bounces all over the canvas. 
"""


from mobilesimulton import Mobile_Simulton
from blackhole import Black_Hole
from math import pi


class Special(Black_Hole, Mobile_Simulton):

    def __init__(self,x,y):
        Black_Hole.__init__(self, x, y,width=10,height=10)
        Mobile_Simulton.__init__(self, x, y, width=15, height=15, angle=0, speed=5)
        
    def update(self, model):
        g = Black_Hole.update(self, model)
        self.set_angle(self.get_angle() + (pi / 2))
        if len(g) != 0:
            self.set_speed(self.get_speed() + 3)
        self.move()
        
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-self.get_dimension()[0]      , self.get_location()[1]-self.get_dimension()[1],
                                self.get_location()[0]+self.get_dimension()[0], self.get_location()[1]+self.get_dimension()[1],
                                fill='#00FF00')