from functools import wraps
from tracestack.handler import ExceptionHandler

def trace(*args, **kwargs):
    """Decorator that applies the tracestack exception handler to one function.
    Optionally takes the same arguments as the other functions.

    Usage:
    
    @trace
    def myFunction():
        ...

    @trace(mode="stackoverflow")
    def myFunction():
        ...
    """

    def decorator(func):
        """The decorator itself. The handler is built
        based on which arguments were passed to the 
        decorator factory, if any.  See below."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                handler()
        return wrapper

    if len(args) == 1 and callable(args[0]):
        # @tracestack was used as a decorator without arguments
        # return the decorated function
        handler = ExceptionHandler()
        return decorator(args[0])
    else:
        # @tracestack(...) was called with arguments
        # return a decorator based on those arguments
        handler = ExceptionHandler(*args, **kwargs)
        return decorator
