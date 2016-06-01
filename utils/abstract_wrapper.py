def abstract(func):

    def wrapper(self, *args, **kwargs):
        msg = 'Method %r not implemented in class %r.' % (func.__name__, self.__class__)
        raise NotImplementedError(msg)

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper