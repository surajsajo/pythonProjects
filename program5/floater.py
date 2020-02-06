# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage



from prey import Prey
import math,random


class Floater(Prey): 
    radius = 5
    def __init__(self,x,y,width=10,height=10,angle=1,speed=5):
        Prey.__init__(self, x, y, width, height,angle,speed)
        Prey.randomize_angle(self)
    
    def update(self,model): 
        g = random.random()      
        if g % 0.3 == g or g % 0.3 == 0:
            s = random.uniform(-0.5,0.5)
            if 3 <= self.get_speed() + s:
                if self.get_speed() + s <= 7:
                    s = self.get_speed() + s
                else: s = 7  
            else: s = 3
            a = random.uniform(-0.5,0.5)
            if -2 * math.pi <= self.get_angle() + a:
                if self.get_angle() + a <= 2 * math.pi:
                    a = self.get_angle() + a
                else: a = 2 * math.pi
            else: a = -2 * math.pi
            self.set_velocity(s, a)
        self.move()
        
    
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-Floater.radius      , self.get_location()[1]-Floater.radius,
                                self.get_location()[0]+Floater.radius, self.get_location()[1]+Floater.radius,
                                fill='#ff0000')
