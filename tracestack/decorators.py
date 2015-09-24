import sys
from functools import wraps
import tracestack

def trace(*args, **kwargs):
    """Decorator that applies the tracestack exception handler to one function.
    Optionally takes the same arguments as the other functions.

    Examples:
    
    @tracestack.trace
    def buggy_function():
        ...

    @tracestack.trace(prompt=True)
    def buggy_function():
        ...

    """

    def decorator(func):
        """The decorator itself."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracestack.on(*handler_args, **handler_kwargs)
            result = func(*args, **kwargs)
            tracestack.off()
            return result
        return wrapper

    if len(args) == 1 and callable(args[0]):
        # @tracestack was used as a decorator without arguments.
        # Return the decorated function.
        handler_args = []
        handler_kwargs = {}
        return decorator(args[0])
    else:
        # @tracestack(...) was called with arguments.
        # Return a decorator based on those arguments.
        handler_args = args
        handler_kwargs = kwargs
        return decorator