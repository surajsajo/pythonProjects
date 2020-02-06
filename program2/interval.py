import inspect
from math import sqrt


class Interval:
    def __init__(self,min,max,):
        self.min = min
        self.max = max
    
    @staticmethod
    def min_max(minimum,maximum=None):
        assert type(minimum) in [int,float], 'Minimum must be an int or float!'
        assert type(maximum) in [int,float] or maximum == None, 'Maximum must be an int or float!'
        if maximum != None:
            assert minimum <= maximum, 'Minimum value must be less than maximum value!'
        else: maximum = minimum
        return Interval(minimum,maximum)
    
    @staticmethod
    def mid_err(middle,error=0):
        assert type(middle) in [int,float], 'Middle value must be a numeric type!'
        assert type(error) in [int,float], 'Error value must be a numeric type!'
        assert error >= 0, 'Error value must not be negative!'
        return Interval.min_max(middle - error, middle + error)
    
    def best(self):
        if self.min != self.max:
            return ((self.max - self.min) / 2) + self.min
        else: return self.min
    
    def error(self):
        if self.min != self.max:
            return (abs(self.max) - abs(self.min)) / 2
        else: return (self.min) / 2
    
    def relative_error(self):
        return abs((self.error() / self.best()) * 100)
    
    def __repr__(self):
        return f'Interval({self.min},{self.max})'
    
    def __str__(self):
        return f'{self.best()}(+/-{self.error()})'
    
    def __bool__(self):
        if self.error() != 0 and self.min != self.max:
            return True
        else: return False
        
    def __pos__(self):
        return Interval(self.min, self.max)
    
    def __neg__(self):
        return Interval(-self.min, -self.max)
    
    def __add__(self,right):
        if type(right) == Interval:
            return Interval((self.min + right.min),(self.max + right.max))
        else: return Interval((self.min + right), (self.max + right))
        
    def __radd__(self,left):
        return Interval((self.min + left), (self.max + left))
        
    def __sub__(self,right):
        if type(right) == Interval:
            return Interval((self.min - right.max),(self.max - right.min))
        else: return Interval((self.min - right), (self.max - right))
        
    def __rsub__(self,left):
        if left - self.min < left - self.max:
            return Interval((left - self.min), (left - self.max))
        else: return Interval((left - self.max), (left - self.min))
    
    def __mul__(self, right):
        if type(right) not in (int, float, Interval):
            return NotImplemented
        if type(right) in (int, float):
            return Interval(self.min * right, self.max * right)
        else:
            lst = [self.min * right.min, self.min * right.max, self.max * right.min, self.max * right.max] 
            return Interval(min(lst), max(lst))
    
    def __rmul__(self, left):
        if type(left) not in (int, float):
            return NotImplemented
        return Interval(left * self.min, left * self.max)
    
    def __truediv__(self, right):
        if type(right) not in (int, float, Interval):
            return NotImplemented
        if type(right) in (int, float):
            return Interval(self.min / right, self.max / right)
        else:
            if right.min <= 0 <= right.max:
                raise ZeroDivisionError(f"{right.min} and {right.max} is between 0")
            lst = [self.min / right.min, self.min / right.max, self.max / right.min, self.max / right.max] 
            return Interval(min(lst), max(lst))
    
    def __rtruediv__(self, left):
        if type(left) not in (int, float):
            return NotImplemented
        if self.min <= 0 <= self.max:
            raise ZeroDivisionError(f"{self.min} and {self.max} is between 0")
        return Interval(left / self.max, left / self.min)
    
    def __pow__(self, right):
        if type(right) != int:
            return NotImplemented
        if right>= 0:
            return Interval(self.min ** right, self.max ** right)
        return Interval((1/self.max) ** -right, (1/self.min) ** -right)
    
    def __eq__(self, right):
        if type(right) not in (int, float, Interval):
            return NotImplemented
        if type(right) in (int, float):
            return self.min == right and self.max == right
        else:
            return self.min == right.min and self.max == right.max
    
    def __lt__(self, right):
        assert 'compare_mode' in Interval.__dict__
        assert Interval.compare_mode == "liberal" or Interval.compare_mode == "conservative"
        if Interval.compare_mode == 'liberal':
                if type(right) in (int, float):
                    return self.max > right
                else:
                    return self.max < right.max
        elif Interval.compare_mode == "conservative":
                if type(right) in (int, float):
                    return self.max < right
                else:
                    return self.max < right.min

        
    def __le__(self, right):
        assert 'compare_mode' in Interval.__dict__
        assert Interval.compare_mode == "liberal" or Interval.compare_mode == "conservative"
        if Interval.compare_mode == 'liberal':
            if type(right) in (int, float):
                return self.max >= right
            else:
                return self.max <= right.max
        elif Interval.compare_mode == "conservative":
            if type(right) in (int, float):
                return self.max <= right
            else:
                return self.max <= right.min
    
    def __abs__(self): #check w Suraj
        x = list()
        for b in range(int(self.min),int(self.max + 1)):
            x.append(b)
        b = list()
        for val in x:
            b.append(float(abs(val)))
        return Interval(min(b), max(b))
    
    def sqrt(self):
        if self.min < 0 or self.max < 0:
            raise ValueError("Cannot square root a negative")
        return Interval(sqrt(self.min), sqrt(self.max))
    
    def __setattr__(self, name, value): #check w suraj
        assert name not in self.__dict__, "It already is in dict"
        assert name == 'min' or name == 'max'
        self.__dict__[name] = value
    
if __name__ == '__main__':
    n = Interval.min_max(-3.0,-2.0)
    print(repr(abs(n)))
    """"g = Interval.mid_err(9.8,.05)
    print(repr(g))
    g = Interval.min_max(9.75,9.85)
    print(repr(g))
    d = Interval.mid_err(100,1)
    t = (d/(2*g)).sqrt()
    print(t,repr(t),t.relative_error())"""    

    import driver    
    driver.default_file_name = 'bscp22F19.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
