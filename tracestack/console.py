import sys
from code import InteractiveConsole
from tracestack.handler import ExceptionHandler


class TracestackConsole(InteractiveConsole):
    """An interactive console for running code or REPL loops that handle
    errors using the tracestack handler."""

    def __init__(self, *args, **kwargs):
        self.handler = ExceptionHandler(*args, **kwargs)
        kwargs.pop("engine")
        kwargs.pop("skip")
        kwargs.pop("script")
        kwargs.pop("arguments")
        InteractiveConsole.__init__(self, *args, **kwargs)

    def showtraceback(self):
        InteractiveConsole.showtraceback(self)
        self.handler.handle_error(*sys.exc_info())
