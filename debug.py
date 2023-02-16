
def debug(func):
    def _debug(*args, **kwargs):
        result = func(*args, **kwargs)
        print ("{} :\n(args :{}, kwargs :{}, result:{}, type:{}". format(func.__name__,
                                                                               args,
                                                                               kwargs,
                                                                               result,
                                                                               type(result) ))
        return result
    return _debug




