import sys
from code import InteractiveConsole
from tracestack.handler import ExceptionHandler


class TracestackConsole(InteractiveConsole):
    """An interactive console for running code or REPLs while handling
    errors using the tracestack handler."""

    def __init__(self, *args, **kwargs):
        self.handler = ExceptionHandler(*args, **kwargs)
        kwargs.pop("engine")
        kwargs.pop("prompt")
        kwargs.pop("arguments")
        InteractiveConsole.__init__(self, *args, **kwargs)

    def showtraceback(self):
        InteractiveConsole.showtraceback(self)
        self.handler.handle_error(*sys.exc_info())

    def showsyntaxerror(self, filename=None):
        InteractiveConsole.showsyntaxerror(self, filename)
        self.handler.handle_error(*sys.exc_info())