import sys
from tracestack.handler import ExceptionHandler

def pm(*args, **kwargs):
    """Post-mortem function that searches the last exception."""

    einfo = sys.exc_info()
    if einfo[0]:
        ExceptionHandler(*args, **kwargs)(*einfo)
    else:
        raise ValueError("no last exception")

def enable(*args, **kwargs):
    """Install the tracestack exception handler as the system exception 
    handler."""

    sys.excepthook = ExceptionHandler(*args, **kwargs)

def disable(*args, **kwargs):
    """Revert to the default exception handler."""

    sys.excepthook = sys.__excepthook__

