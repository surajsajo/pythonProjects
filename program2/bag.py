from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self,iterable=[]):
        self.bag = defaultdict(set)
        for item in iterable:
            if item in self.bag:
                self.bag[item] += 1
            else: self.bag[item] = 1
    
    def __repr__(self):
        letters = list()
        for letter in self.bag:
            for k in range(self.bag[letter]):
                letters.append(letter)
        return f'Bag({letters})'
    
    def __str__(self):
        letters = list()
        for letter in self.bag:
            letters.append(f'{letter}[{self.bag[letter]}]')
        letters = tuple(letters)
        return f'Bag{letters}'
    
    def __len__(self):
        return sum(self.bag.values())
    
    def unique(self):
        return len(self.bag)
    
    def  __contains__(self,arg):
        if arg in self.bag:
            return True
        else: return False
        
    def count(self,arg):
        if arg in self.bag:
            return self.bag[arg]
        else: return 0
     
    def add(self,arg):
        if arg not in self.bag:
            self.bag[arg] = 1
        else: self.bag[arg] += 1
    
    def __add__(self,right):
        if type(right) != Bag :
            return NotImplemented('Both objects that you are adding have to be Bag objects!')
        iterable = list()
        for letter in self.bag:
            for _ in range(self.bag[letter]):
                iterable.append(letter)
        newBag = Bag(iterable)
        for letter in right.bag:
            if letter not in newBag.bag:
                newBag.bag[letter] = right.bag[letter]
            else: newBag.bag[letter] += right.bag[letter]
        return newBag
    
    def remove(self,arg):
        if arg in self.bag:
            self.bag[arg] -= 1
            if self.bag[arg] == 0:
                self.bag.pop(arg)
        else: raise ValueError(f'{arg} is not a value in the bag!') 
    
    def __eq__(self,right):
        if type(right) != Bag:
            return False
        else:
            if self.bag == right.bag:
                return True
            else: return False
    
    def __ne__(self,right):
        if type(right) != Bag:
            return True
        if self.bag == right.bag:
            return False
        else: return True
        
    def __iter__(self):
        def gen(bin):
            for key in bin:
                for _ in range(bin[key]):
                    yield key
        return (gen(dict(self.bag)))




if __name__ == '__main__':
    #Put your own test code here to test Bag before doing bsc tests
    b = Bag(['d','a','b','d','c','b','d'])
    print(str(b))

    print('Start simple testing')

    import driver
    driver.default_file_name = 'bscp21F19.txt'
#     driver.default_show_exception =True
#     driver.default_show_exception_message =True
#     driver.default_show_traceback =True
    driver.driver()
