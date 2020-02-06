# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole


class Pulsator(Black_Hole): 
    counter = 0
    
    def __init__(self,x,y):
        Black_Hole.__init__(self, x, y)
        self.counter = 0
        
    def update(self,model):
        self.counter += 1
        if self.counter == 30:
            if self.get_dimension()[0] == 1:
                model.remove(self)
            else: 
                self.counter = 0
                self.set_dimension(self.get_dimension()[0] - 1, self.get_dimension()[1] - 1)
        g = Black_Hole.update(self, model)
        for _ in g:
            self.change_dimension(1,1)
            self.counter = 0
        return g
            
    
    
