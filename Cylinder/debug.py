

def debug(func):
    def _debug(*args, **kwargs):
        result = func(*args, **kwargs)
        print ("{}(args :{}, kwargs :{})". format(func.__name__,args, kwargs ))
        return result
    return _debug






