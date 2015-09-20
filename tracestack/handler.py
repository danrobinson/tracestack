from __future__ import print_function
import sys, webbrowser, traceback
from tracestack.engines import GoogleEngine, StackEngine
from tracestack.utils import getch

class ExceptionHandler(object):
    """Callable exception handler that can replace sys.__excepthook__."""

    def __init__(self, prompt=False, engine="default", *args, **kwargs):
        """Initializer takes same arguments as pm, enable, trace, etc.

        Args:
            prompt (bool) -- whether to prompt the user (default: False)
            engine (string) -- the search engine to use (default: "default")
                'default': Google limited to stackoverflow.com, 
                'google': full web search on Google, 
                'stackoverflow': StackOverflow site search
        """
        if engine in ("default", "google"):
            self.engine = GoogleEngine(engine=engine, *args, **kwargs)
        elif engine == "stackoverflow":
            self.engine = StackEngine(*args, **kwargs)
        else:
            msg = "'%s' is not a valid engine option (choose between " + \
                  "'default', 'google', and 'stackoverflow')"
            raise ValueError(msg % engine)
        self.prompt = prompt

    def __call__(self, *einfo):
        """Handles error.  Takes same three arguments as 
        sys.__excepthook__: type, value, traceback."""
        einfo = einfo or sys.exc_info()
        self._print_traceback(*einfo)
        self.handle_error(*einfo)

    def handle_error(self, *einfo):
        error_string = self._get_error_string(*einfo)
        self._handle_string(error_string)

    def _print_traceback(self, *einfo):
        traceback.print_exception(*einfo)

    def _get_error_string(self, *einfo):
        (etype, evalue, tb) = einfo
        error_string = traceback.format_exception_only(etype, evalue)[-1]
        return error_string

    def _search(self, error_string):
        search_url = self.engine.search(error_string)
        webbrowser.open(search_url)

    def _prompt(self):
        if self.prompt:
            print("Hit spacebar to search this error message on %s: " % self.engine.name(), end="")
            sys.stdout.flush()
            choice = getch()
            if choice == " ":
                return True
            else:
                return False
        else:
            print("Searching this error message on %s..." % self.engine.name())
            return True

    def _handle_string(self, error_string):
        if self._prompt():
            self._search(error_string)
