import sys
import traceback
from tracestack.handler import ExceptionHandler, _get_ipython_handler


def pm(*args, **kwargs):
    """Post-mortem function that searches the last exception."""

    if hasattr(sys, "last_type"):
        einfo = (sys.last_type, sys.last_value, sys.last_traceback)
        handler = ExceptionHandler(*args, **kwargs)
        try:
            ipython_shell = get_ipython()
            ipython_shell.showtraceback()
            handler.handle_error(*einfo)
        except NameError:
            handler(*einfo)
    else:
        raise ValueError("no last exception")

def on(*args, **kwargs):
    """Install the tracestack exception handler as the system exception 
    handler."""

    try:
        ipython_shell = get_ipython()
        handler = ExceptionHandler(*args, **kwargs)

        def _get_ipython_handler(*args, **kwargs):
            def handle_ipython(shell, etype, value, tb, tb_offset=None):
                shell.showtraceback((etype, value, tb), tb_offset=tb_offset)
                handler.handle_error(etype, value, tb)
                return traceback.format_tb(tb)
            return handle_ipython

        ipython_shell.set_custom_exc((Exception,), 
                                     _get_ipython_handler(*args, **kwargs))
    except NameError:
        sys.excepthook = ExceptionHandler(*args, **kwargs)

def off():
    """Revert to the default exception handler."""

    try:
        ipython_shell = get_ipython()
        ipython_shell.set_custom_exc((), None)
    except NameError:
        sys.excepthook = sys.__excepthook__