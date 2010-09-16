
import sys
import types


# Exception to use
class PrivateAttributeError(AttributeError):
    pass

# Check if the caller is legit at all levels... this can be improved
def check_caller(obj, level):
    frame = sys._getframe(level)
    cls = type(obj)

    # first of all, the instance has to be in the frame
    values = frame.f_locals.values()
    if obj not in values:
        raise PrivateAttributeError("Instance not in frame!")
    
    for attr, func in cls.__dict__.items():
        if not isinstance(func, types.FunctionType):
            continue
        code1 = func.func_code
        code2 = frame.f_code
        if code1 is code2:
            # we found the same code in a method,
            break
            # FIXME: have to find a way to check if it's an original
            # method and not added later
    else:
        # ops, ran out the loop... raise error
        raise PrivateAttributeError("caller not a method")


# Base Private attribute descriptor... not sure if it'll work with
# methods as is now
class Private(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls=None):
        check_caller(obj, 2)
        if self.name.startswith('_private_'):
            
        
        try:
            value = obj.__privdict__[self.name]
        except KeyError:
            raise AttributeError("Private attribute '%s' not set"%self.name)
        return value

    def __set__(self, obj, value):
        check_caller(obj, 2)
        obj.__privdict__[self.name] = value

    def __delete__(self, obj):
        check_caller(obj, 2)
        try:
            del obj.__privdict__[self.name] 
        except KeyError:
            raise AttributeError("Private attribute '%s' not set"%self.name)
            


# Now, some test code
class Test(object):
    foo = Private('foo')
    _private_foo = Private('_private_foo')
    bar = Private('bar')
    _private_var = Private('_private_bar')

    
    def __init__(self):
        self.foo = None
        self.bar = None
        self.wow = None

    def set_foo(self, value):
        self.foo = value
        self.bar = "and I am bar"

    def get_foo(self):
        return self.foo



def testit():
    o = Test()
    a = Test()

    # First, the obvious, the setter should work
    o.set_foo('I am foo in o')
    a.set_foo('I am foo in a')

    # and the getter too
    try:
        print "Testing getter: ",
        assert o.get_foo() == 'I am foo in o'
        assert a.get_foo() == 'I am foo in a'
        print 'OK'
    except PrivateAttributeError, msg:
        print 'FAIL', msg

    # And direct access should not
    try:
        print "Testing direct access to get: ",
        o.foo
        a.foo
        print 'ERROR'
    except PrivateAttributeError, msg:
        print 'OK'

    # for set neither
    try:
        print "Testing direct access to set: ",
        o.foo = 'I am not the original foo in o'
        a.foo = 'I am not the original foo in a'
        print 'ERROR'
    except PrivateAttributeError, msg:
        print 'OK'
  
    # it shouldn't work even with super class __getattribute__ method
    try:
        print "Testing with object.__getattribute__: ",
        assert object.__getattribute__(o, 'foo') == 'I am foo in o'
        assert object.__getattribute__(a, 'foo') == 'I am foo in a'
        print 'ERROR'
    except PrivateAttributeError, msg:
        print 'OK'

    # and __setattr__ neither
    try:
        print "Testing with object.__setattr__: ",
        object.__setattr__(o, 'foo', 'I am not the original foo in o')
        object.__setattr__(a, 'foo', 'I am not the original foo in a')
        print 'ERROR'
    except PrivateAttributeError, msg:
        print 'OK'

    # and it shouldn't work with __dict__ too
    try:
        print o.__dict__
        print "Testing with __dict__: ",
        assert o.__dict__['foo'] == 'I am foo in o'
        assert a.__dict__['foo'] == 'I am foo in a'
        print 'ERROR'
        # the foo descriptor is a class attribute, so should not
        # be accessible here
    except KeyError, msg:
        print 'OK'

    # Making it a bit harder... add my own getter dinamically
    def getfoo(self):
        return self.foo

    try:
        print "Testing with dinamically added getter: ",
        Test.getfoo = getfoo
        assert o.getfoo() == 'I am foo in o'
        #assert a.getfoo() == 'I am foo in a'
        print 'ERROR'
        # the foo descriptor is a class attribute, so should not
        # be accessible here
    except PrivateAttributeError, msg:
        print 'OK'

    # Now, testing the hard paths... suppose I know the implementation...
    try:
        print "Testing with __privdict__: ",
        assert o.__privdict__['foo'] == 'I am foo in o'
        assert a.__privdict__['foo'] == 'I am foo in a'
        print 'ERROR'
        # the foo descriptor is a class attribute, so should not
        # be accessible here
    except PrivateAttributeError, msg:
        print 'OK'

    # Now, testing the hard paths... suppose I know the implementation...
    try:
        print "Testing with object.__getattribute and __privdict__: ",
        assert object.__getattribute__(o.__privdict__, 'dic')['foo'] == 'I am foo in o'
        assert object.__getattribute__(a.__privdict__, 'dic')['foo'] == 'I am foo in a'
        print 'ERROR'
        # the foo descriptor is a class attribute, so should not
        # be accessible here
    except PrivateAttributeError, msg:
        print 'OK'





testit()
    
