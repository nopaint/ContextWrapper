

class SampleClass(object):
    def __init__(self):
        pass

    def __getattr__(self, name):
        print "called SampleClass.__getattr__ with {}".format(name)

    def aMethod(self, singlearg, arglist):
        pass


class ContextWrapper(object):
    def __init__(self, wrapClass, *args):
        self.__wrapClass__ = wrapClass
        self.__wrapObj__ = None
        self.__wrapInitArgs__ = args

    def __methods__(self): pass

    def __members__(self): pass

    def __methodwrapper__(self, methodname, *args, **kwargs):
        if self.__wrapObj__ == None:
            while True:
                with self.__wrapClass__(self.__wrapInitArgs__) as wrapObj:
                    callMethod = wrapObj.getattr(self.__wrapClass__,
                                                 methodname)
                    yield callMethod(args, kwargs)


    def __getattr__(self, name):
        # if the name being invoked doesn't exist on this class and
        # does exist on wrapClass, we need to return a wrapper
        # function that calls __methodwrapper_ with the methodname
        print "called {}.{} with {}".format(self.__class__, '__getattr__', name)
        if not hasattr(self, name):
            print "no attr named {}".format(name)
            return_method = lambda x : self.__methodwrapper__(name, x)
            print "returning {}".format(return_method)
            return return_method
        return getattr(self, name)

