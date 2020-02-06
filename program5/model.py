import controller, sys
import model   # Pass a reference to this model module to update calls in update_all

#Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special   import Special


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running     = False
cycle_count = 0
simultons = set()
button = None


#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running,cycle_count,simultons,button
    running     = False
    cycle_count = 0
    simultons   = set()
    button = None

#start running the simulation
def start():
    global running
    running = True


#stop running the simulation (freezing it)
def stop():
    global running
    running = False 
  


#tep just one update in the simulation
def step ():
    if running:
        update_all()
        stop()
    else:
        start()
        update_all()
        stop()
    
            
    


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global button
    button = kind


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    if button == 'Remove':
        g = set(simultons)
        for f in g:
            if f.contains([x,y]):
                remove(f)
    elif button != None:
        add(eval(f'{button}({x},{y})'))
    
            


#add simulton s to the simulation
def add(s):
    simultons.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    simultons.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    g = set()
    for x in simultons:
        if p(x):
            g.add(x)
    return g


#call update \(pass model as its argument\) for every simulton in the simulation
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count
    if running:
        cycle_count += 1
        g = set(simultons)
        for x in g:
            x.update(model)

#delete every simulton from the canvas in the simulation; then call display on each
#  simulton being simulated to add it back to the canvas, possibly in a new location, to
#  animate it; also, update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    
    for x in simultons:
        x.display(controller.the_canvas)
    
    controller.the_progress.config(text=str(cycle_count)+" cycles/" + str(len(simultons))+" simultons")
