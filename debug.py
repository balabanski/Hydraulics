
def debug(func):
    def _debug(*args, **kwargs):
        result = func(*args, **kwargs)
        print ("{} :\n\t(args :{}, \n\t kwargs :{}, \n\t result:{}, \n\t type:{}". format(func.__name__,
                                                                               args,
                                                                               kwargs,
                                                                               result,
                                                                               type(result) ))
        return result
    return _debug




