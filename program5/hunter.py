# Hunter is doubly-derived from the Mobile_Simulton and Pulsator classes:
#   updating/displaying like its Pulsator base, but also moving (either in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):
    dis = 200
    def __init__(self,x,y):
        Pulsator.__init__(self, x, y)
        Mobile_Simulton.__init__(self, x, y, width=20, height=20, angle=1, speed=5)
        Mobile_Simulton.randomize_angle(self)
        
    def update(self, model):
        Pulsator.update(self, model)
        g = model.find(lambda x : isinstance(x, Prey))
        for f in g:
            if self.distance(f.get_location()) <= self.dis:
                y = f.get_location()[1] - self.get_location()[1]
                x = f.get_location()[0] - self.get_location()[0]
                angle = atan2(y,x)
                self.set_angle(angle)
        self.move()