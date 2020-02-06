import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable=False, defaults={}):
    def show_listing(s):
        for line_number, line_text in enumerate( s.split('\n'),1 ):
            print(f' {line_number: >3} {line_text.rstrip()}')

    # put your code here
    def unique(iterable):
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i
    if type(type_name) != str:
        raise SyntaxError('Type Name must be a string')
    if (not re.match('^([a-zA-Z])(\w)*$', type_name)) or keyword.iskeyword(type_name):
        raise SyntaxError('Type Name is does not start with a letter or it is a python keyword')
    if type(field_names) == list:
        for name in field_names:
            if (not re.match('^([a-zA-Z])(\w)*$', name)) or keyword.iskeyword(name):
                raise SyntaxError('Field Name does not start with a letter or it is a python keyword')
    elif type(field_names) == str:
        for name in unique(re.split(', *| |,',field_names)):
            if (not re.match('^([a-zA-Z])(\w)*$', name)) or keyword.iskeyword(name):
                raise SyntaxError('Field Name does not start with a letter or it is a python keyword')
    else: raise SyntaxError('Field Names must be a list or str')
    for k in defaults:
        if k not in field_names:
            raise SyntaxError(f'the key: {k} is not in the field names')
    field = [name for name in unique(re.split(', *| |,',field_names))] if type(field_names) == str else field_names
    field1 = []
    for k in ([name for name in unique(re.split(', *| |,',field_names))] if type(field_names) == str else field_names):
        if k in defaults:
            field1.append(f'{k}={defaults[k]}')
        else: field1.append(k)
    
    class_definition = '''\
class {type}:
    _fields = {fields}
    _mutable = {mutables}\n
    def __init__(self,'''.format(type= type_name, fields= field, mutables= mutable)
    for x in field1:
        class_definition += x + ''','''
    class_definition += '''):\n'''
    for x in field:
        class_definition += '''\
        self.''' + x + ''' = ''' + x + '''\n'''
    class_definition += '''\n\
    def __repr__(self):
        statement = '{type}('
        for x in self._fields:
            statement += x + '=' + str(self.__dict__[x]) + ','
        statement = statement[:len(statement) - 1]
        return statement + ')'\n
        '''.format(type= type_name)
    for x in field:
        class_definition += '''\n\
    def get_{param}(self):
        return self.{param}\n'''.format(param = x)
    
    class_definition += '''
    def __getitem__(self,index):
        if type(index) == int:
            if index < len(self._fields):
                return eval('self.get_' + str(self._fields[index]) + '()')
            else: raise IndexError('The index that you entered is out of range')
        elif type(index) == str:
            if index in self.__dict__:
                return self.__dict__[index]
            else: raise IndexError('The attribute that you wanted to get is not within this class')
        else: raise IndexError('The index you entered is an invalid type')
        
    def __eq__(self,right):
        if type(right) == type(self) :
            return all([self[name] == right[name] for name in self._fields])
        else: return False
    
    def _asdict(self):
        d = dict()
        for att in self._fields:
            d[att] = self[att]
        return d
        
    @staticmethod
    def _make(iterable):
        statement = '{type}('
        for x in iterable:
            statement += str(x) + ','
        return eval(statement + ')')
    
    def _replace(self,**kargs):
        for k in kargs:
            if k not in self.__dict__ :
                raise TypeError('The attribute that you are trying to replace is not an attribute of this class')
        if self._mutable == True:
            for key in kargs:
                self.__dict__[key] = kargs[key]
        else: 
            g = '{type}('
            for k in self.__dict__:
                if k in kargs:
                    g += str(kargs[k]) + ','
                else: g += str(self.__dict__[k]) + ','
            return eval(g + ')')
            
    def __setattr__(self, name, value): #check w suraj
        if not {mutables}:
            if name in self.__dict__:
                raise AttributeError('This attribute cannot be changed')
            else: self.__dict__[name] = value
        else: self.__dict__[name] = value'''.format(type= type_name, fields= field, mutables= mutable)
        
        
        
    # bind class_definition (used below) to the string constructed for the class


    # When debugging, uncomment following line to show source code for the class
    #show_listing(class_definition)
    
    # Execute this class_definition, a str, in a local name space; then bind the
    #   the source_code attribute to class_definition; after try/except return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )    
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):        
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test pnamedtuple below in script with Point = pnamedtuple('Point','x,y')
    Triple1    = pnamedtuple('Triple1', 'a b c')
    t1 = Triple1(1,2,3)
    print(t1._replace(a=2))
    #driver tests
    import driver
    driver.default_file_name = 'bscp3F19.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
