import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # To begin, by binding the class attribute to True means checking can occur
    #   (but only when self._checking_on is bound to True too)
    checking_on  = True
  
    # For checking the decorated function, bind self._checking_on as True too
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        def listCheck():
            assert type(value) == list, f'{param} failed annotation check (wrongtype): value = {value}\n\
             was type {type(value)}, but it should be type list'
            if len(annot) == 1:
                if all([type(g) == type for g in annot]):
                    for val in value:
                        assert isinstance(val,annot[0]), f'{param} failed annotation check (wrong type): value = {val}\n\
                        was type {type(val)}, but should be type {annot[0]}'
                else: 
                    for x in annot:
                        if type(x) == type:
                            self.check(param,type(x),value)
                            for g in value:
                                for f in g:
                                    self.check(param,x[0],f)
                        else:
                            for g in value:
                                self.check(param,x,g)
            else:
                assert len(value) == len(annot), f'{param} failed annotation check (wrong number of elements): value = {value}\n\
                annotation had {len(annot)} elements {annot}' 
                for val in value:
                    assert isinstance(val,annot[value.index(val)]), f'{param} failed annotation check (wrong type): value = {val}\n\
                    was type {type(val)}, but should be type {annot[value.index(val)]}'
                    
        def dictCheck():
            assert type(value) == dict, f'{param} failed annotation check (wrongtype): value = {value}\n\
             was type {type(value)}, but it should be type dict'
            self.check(param,type(annot),value)
            for x in annot:
                for g in value:
                    self.check(param,x,g)
                    self.check(param,annot[x],value[g])
                    
        def tupleCheck():
            assert type(value) == tuple, f'{param} failed annotation check (wrongtype): value = {value}\n\
             was type {type(value)}, but it should be type tuple'
            self.check(param,type(annot),value)
            if len(annot) == 1:
                for x in annot:
                    for g in value:
                        self.check(param,x,g)
                        self.check(param,x,value[value.index(g)])
            else: 
                for x in annot:
                        for g in value:
                            if annot.index(x) == value.index(g):
                                self.check(param,x,g)
        def setCheck():
            assert type(value) == set, f'{param} failed annotation check (wrongtype): value = {value}\n\
             was type {type(value)}, but it should be type set'
            self.check(param,type(annot),value)
            assert len(annot) == 1, f'{param} annotation inconsistency: set should have 1 value but had {len(annot)}\n\
            annotation = {annot}'
            for x in annot:
                for g in value:
                    self.check(param,x,g) 
        
        def frozenCheck():
            assert type(value) == frozenset, f'{param} failed annotation check (wrongtype): value = {value}\n\
             was type {type(value)}, but it should be type frozenset'
            self.check(param,type(annot),value)
            assert len(annot) == 1, f'{param} annotation inconsistency: set should have 1 value but had {len(annot)}\n\
            annotation = {annot}'
            for x in annot:
                for g in value:
                    self.check(param,x,g) 
            
        def funcCheck():
            assert len(inspect.signature(annot).parameters) == 1, f'{param} annotation inconsistency: predicate should have 1 parameter but had {len(inspect.signature(annot).parameters)}\n\
            predicate = {annot}'
            try:
                assert annot(value) == True, f'{param} failed annotations check: value = {value}\n\
                predicate = {annot}'
            except:
                raise AssertionError('NEED ERROR MESSAGE')
                    
                  
        # To begin, get check's function annotation and compare it to its arguments
        if type(annot) == type:
            assert isinstance(value,annot), f'{param} failed annotation check (wrong type): value = {value}\n\
             was type {type(value)} but it should be type {annot}'
        elif type(annot) == list:
            listCheck()
        elif type(annot) == dict:
            dictCheck()
        elif type(annot) == tuple:
            tupleCheck()
        elif type(annot) == set:
            setCheck()
        elif type(annot) == frozenset:
            frozenCheck()
        elif inspect.isfunction(annot):
            funcCheck()
        elif type(annot) == str:
            pass
        else: 
            try:
                annot.__check_annotation__(self.check,param,value,check_history)
            except AttributeError:
                raise AssertionError('ERROR MESSAGE')
        
            
         
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return an ordereddict of the parameter/argument bindings: it's a special
        #   kind of dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if Check_Annotation.checking_on and self._checking_on:
            try:
                # Check the annotation for each of the parameters that is annotated
                for annot in self._f.__annotations__:
                    for param in param_arg_bindings():
                        if self._f.__annotations__[annot] != None and param == annot:
                            self.check(param,self._f.__annotations__[param],param_arg_bindings()[param])
                    if annot == 'return':
                        assert isinstance(self._f(*args,**kargs),self._f.__annotations__[annot]), f'{annot} failed annotation check (wrong type): value = {self._f(*args,**kargs)}\n\
                         was type {type(self._f(*args,**kargs))} but it should be type {self._f.__annotations__[annot]}'
                return self._f(*args, **kargs)
                    
                # Compute/remember the value of the decorated function
                
                # If 'return' is in the annotation, check it
                
                # Return the decorated answer
                
                #remove after adding real code in try/except
                
            # On first AssertionError, print the source lines of the function and reraise 
            except AssertionError:
                """print(80*'-')
                for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
                    print(l.rstrip())
                print(80*'-')"""
                raise
        else: return self._f(*args, **kargs)




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4F19.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
