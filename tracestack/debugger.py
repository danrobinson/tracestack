import sys
from tracestack.handler import ExceptionHandler

def pm(*args, **kwargs):
    """Post-mortem function that searches the last exception."""

    if hasattr(sys, "last_type"):
        einfo = (sys.last_type, sys.last_value, sys.last_traceback)
        ExceptionHandler(*args, **kwargs)(*einfo)
    else:
        raise ValueError("no last exception")

def on(*args, **kwargs):
    """Install the tracestack exception handler as the system exception 
    handler."""

    sys.excepthook = ExceptionHandler(*args, **kwargs)

def off(*args, **kwargs):
    """Revert to the default exception handler."""

    sys.excepthook = sys.__excepthook__
