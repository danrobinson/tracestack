from __future__ import print_function
import sys, webbrowser, traceback
from tracestack.engines import GoogleEngine, StackEngine

try: 
    input = raw_input
except NameError: 
    pass

class ExceptionHandler(object):
    """When called, prompts the user to type s to search the error message"""

    def __init__(self, engine="default", skip=False, *args, **kwargs):
        if engine in ("default", "google"):
            self.engine = GoogleEngine(engine=engine, *args, **kwargs)
        elif engine == "stackoverflow":
            self.engine = StackEngine(*args, **kwargs)
        else:
            msg = "'%s' is not a valid engine option (choose between " + \
                  "'default', 'google', and 'stackoverflow')"
            raise ValueError(msg % engine)
        self.skip = skip

    def __call__(self, *einfo):
        einfo = einfo or sys.exc_info()
        self.print_traceback(*einfo)
        self.handle_error(*einfo)

    def print_traceback(self, *einfo):
        traceback.print_exception(*einfo)

    def handle_error(self, *einfo):
        error_string = self.get_error_string(*einfo)
        self.handle_string(error_string)

    def get_error_string(self, *einfo):
        (etype, evalue, tb) = einfo
        error_string = "{0} {1}".format(etype.__name__, 
                                evalue)
        return error_string

    def search(self, error_string):
        search_url = self.engine.search(error_string)
        webbrowser.open(search_url)

    def prompt(self):
        if self.skip:
            return True
        else:
            choice = input("Type s to search this error message on %s: " % self.engine.name())
            if choice == "s" or choice == "S":
                return True
            else:
                return False

    def handle_string(self, error_string):
        if self.prompt():
            self.search(error_string)
