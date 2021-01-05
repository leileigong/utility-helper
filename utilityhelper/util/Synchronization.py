"""
from Thinking in Python, Bruce Eckel
http://python-3-patterns-idioms-test.readthedocs.org/en/latest/Observer.html

(c) Copyright 2008, Creative Commons Attribution-Share Alike 3.0.

Simple emulation of Java's 'synchronized'
keyword, from Peter Norvig.
"""
import functools
from threading import RLock

def synchronized(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            self.mutex.acquire()
            return method(self, *args, **kwargs)
        finally:
            self.mutex.release()
    return wrapper


def synchronized2(method):

    def f(*args, **kwargs):
        self = args[0]
        self.mutex.acquire()
        # print(method.__name__, 'acquired')
        try:
            return method(*args, **kwargs)
        finally:
            self.mutex.release()
            # print(method.__name__, 'released')
    return f


def synchronize(klass, names=None):
    """Synchronize methods in the given class.
    Only synchronize the methods whose names are
    given, or all methods if names=None."""
    if type(names) == type(''):
        names = names.split()
    for (name, val) in list(klass.__dict__.items()):
        if callable(val) and name != '__init__' and \
                (names is None or name in names):
            # print("synchronizing", name)
            setattr(klass, name, synchronized(val))


class Synchronization(object):
    # You can create your own self.mutex, or inherit from this class:

    def __init__(self):
        self.mutex = RLock()
