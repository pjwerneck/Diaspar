

import inspect
import sys
import types
import unittest


class PrivateAttributeError(AttributeError):
    pass


def _check_caller(obj, level):
    frame = sys._getframe(level)
    cls = type(obj)

    values = frame.f_locals.values()
    if obj not in values:
        return False

    funcs = [func for func in cls.__dict__.values() if isinstance(func, types.FunctionType)]

    for func in funcs:
        code1 = func.func_code
        code2 = frame.f_code
        if code1 is code2:
            break
    else:
        return False
    return True


class Private(object):
    pass


class PrivateAttribute(Private):
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls=None):
        if not _check_caller(obj, 2):
            raise PrivateAttributeError("can only be used inside a method")
        try:
            value = obj.__privdict__[self.name]
        except KeyError:
            raise AttributeError("Private attribute '%s' not set"%self.name)
        return value

    def __set__(self, obj, value):
        if not _check_caller(obj, 2):
            raise PrivateAttributeError("can only be used inside a method")
        obj.__privdict__[self.name] = value

    def __delete__(self, obj):
        if not _check_caller(obj, 2):
            raise PrivateAttributeError("can only be used inside a method")
        try:
            del obj.__privdict__[self.name] 
        except KeyError:
            raise AttributeError("Private attribute '%s' not set"%self.name)


class PrivateMethod(Private):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if not _check_caller(obj, 2):
            raise PrivateAttributeError("can only be used inside a method")
        return types.MethodType(self.func, obj, cls)

    def __set__(self, obj, value):
        raise RuntimeError("You can't reasign a private method")

    def __delete__(self, obj):
        raise RuntimeError("You can't reasign a private method")
    
    
class PrivateDict(object):
    __slots__ = ['owner', '__privdict__']
    def __init__(self, owner):
        self.owner = owner
        self.__privdict__ = {}
        
    def __setitem__(self, key, value):
        if not _check_caller(self.owner, 3):
            raise PrivateAttributeError("Are you trying to break this?")
        self.__privdict__[key] = value
        
    def __getitem__(self, key):
        if not _check_caller(self.owner, 3):
            raise PrivateAttributeError("Are you trying to break this?")
        return self.__privdict__[key]

    def __getattribute__(self, attr):
        if not _check_caller(self, 2):
            raise PrivateAttributeError("Are you trying to break this?")
        return super(PrivateDict, self).__getattribute__(attr)

    def __setattribute__(self, attr):
        if not _check_caller(self, 2):
            raise PrivateAttributeError("Are you trying to break this?")
        return super(PrivateDict, self).__getattribute__(attr)
    

class MetaEnablePrivate(type):
    def __call__(cls, *args, **kwds):
        new = cls.__new__(cls, *args, **kwds)
        new.__privdict__ = PrivateDict(new)
        cls.__init__(new, *args, **kwds)
        return new


def private(*args):
    attrs = dict((name, PrivateAttribute(name)) for name in args)

    def _metaclass(name, bases, dict):
        dict.update(attrs)
        return MetaEnablePrivate(name, bases, dict)

    return _metaclass


# Now, some test code
class Test(object):
    __metaclass__ = private('foo', 'bar')
    
    def __init__(self, name):
        self.foo = None
        self.bar = None

        self.name = name
        self.wow = None

    def set_foo(self, value):
        self.foo = value
        self.bar = "and I am new bar in %s"%self.name

    def get_foo(self):
        return self.foo

    @PrivateMethod
    def meth(self):
        return 'I am supposed to be a private method'

    def call_meth(self):
        return self.meth()


class TestPrivateAttributes(unittest.TestCase):
    def setUp(self):
        self.obja = Test('a')
        self.objb = Test('b')
        self.obja.set_foo('I am foo in a')
        self.objb.set_foo('I am foo in b')

    def testGettersSetters(self):
        # get original
        self.assertEqual(self.obja.get_foo(), 'I am foo in a')
        self.assertEqual(self.objb.get_foo(), 'I am foo in b')
        # set
        self.obja.set_foo('I am new foo in a')
        self.objb.set_foo('I am new foo in b')
        # check if it really got set
        self.assertEqual(self.obja.get_foo(), 'I am new foo in a')
        self.assertEqual(self.objb.get_foo(), 'I am new foo in b')        

    def testBreakDirectGet(self):
        self.assertRaises(PrivateAttributeError, getattr, self.obja, 'foo')
        self.assertRaises(PrivateAttributeError, getattr, self.obja, 'bar')
        self.assertEqual(self.obja.wow, None)
        self.assertRaises(PrivateAttributeError, getattr, self.objb, 'foo')
        self.assertRaises(PrivateAttributeError, getattr, self.objb, 'bar')
        self.assertEqual(self.objb.wow, None)

    def testBreakDirectSet(self):
        self.assertRaises(PrivateAttributeError, setattr, self.obja, 'foo', '')
        self.assertRaises(PrivateAttributeError, setattr, self.obja, 'bar', '')
        self.obja.wow = ''
        self.assertRaises(PrivateAttributeError, setattr, self.objb, 'foo', '')
        self.assertRaises(PrivateAttributeError, setattr, self.objb, 'bar', '')
        self.objb.wow = ''

    def testWithObjectGetattribute(self):
        self.assertRaises(PrivateAttributeError, object.__getattribute__,
                          self.obja, 'foo')
        self.assertRaises(PrivateAttributeError, object.__getattribute__,
                          self.obja, 'bar')
        self.assertRaises(PrivateAttributeError, object.__getattribute__,
                          self.objb, 'foo')
        self.assertRaises(PrivateAttributeError, object.__getattribute__,
                          self.objb, 'bar')

    def testWithObjectSetattr(self):
        self.assertRaises(PrivateAttributeError, object.__setattr__,
                          self.obja, 'foo', '')
        self.assertRaises(PrivateAttributeError, object.__setattr__,
                          self.obja, 'bar', '')
        self.assertRaises(PrivateAttributeError, object.__setattr__,
                          self.objb, 'foo', '')
        self.assertRaises(PrivateAttributeError, object.__setattr__,
                          self.objb, 'bar', '')

    def testWithObjectPrivdict(self):
        self.assertRaises(PrivateAttributeError, lambda :self.obja.__privdict__['foo'])
        self.assertRaises(PrivateAttributeError, lambda :self.obja.__privdict__['bar'])
        self.assertRaises(PrivateAttributeError, lambda :self.objb.__privdict__['foo'])
        self.assertRaises(PrivateAttributeError, lambda :self.objb.__privdict__['bar'])



if __name__ == '__main__':
    unittest.main()
    
