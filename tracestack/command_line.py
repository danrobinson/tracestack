from __future__ import print_function
import sys
import os
import runpy
import traceback
import contextlib
import argparse
from tracestack.handler import ExceptionHandler
from tracestack.console import TracestackConsole

def run():
    """Runs the script provided by the arguments, using the 
    tracestack exception handler.
    """
    parser = _build_parser()
    args = vars(parser.parse_args())
    print(args)
    script = args.pop("script")
    handler = ExceptionHandler(**args)
    if script:
        # set up the system variables
        sys.argv = sys.argv[1:]
        sys.path[0] = os.path.dirname(os.path.abspath(script))
        try:
            runpy.run_path(script, run_name="__main__")
        except:
            einfo = sys.exc_info()
            _print_clean_traceback(einfo)
            handler.handle_error(*einfo)
    else:
        # no additional arguments were given; run the REPL loop
        console = TracestackConsole(**args)
        console.interact()

def _build_parser():
    """Returns the argument parser (which is built using argparse)."""
    
    parser = argparse.ArgumentParser(description='instantly search your ' + \
                                                 'Python error messages on' + \
                                                 ' the web',
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('script', metavar='SCRIPT', type=str, nargs='?',
                        help='the Python script')
    parser.add_argument('arguments', metavar='ARGUMENTS', type=str, nargs='*',
                        help='any arguments to the script')
    parser.add_argument('-s', '--skip', help='skip the prompt and immediately search each exception',
                        action='store_true')
    parser.add_argument('-e', 
                        '--engine', 
                        help="""the search engine to use:
  'default': Google limited to stackoverflow.com, 
  'google': full web search on Google, 
  'stackoverflow': StackOverflow site search""", 
                        default="default", 
                        choices=['default', 'google', 'stackoverflow'], 
                        metavar="ENGINE",
                        type=str)
    return parser

def _print_clean_traceback(einfo):
    """Print the traceback, without showing all the overhead added by tracestack."""

    extracted = traceback.extract_tb(einfo[2])
    if extracted[-1][0] in ('trace', 'runpy.py'):
        # the error call is coming from inside the house
        # this shouldn't happen, but if it does, do the default behavior
        sys.__excepthook__(sys.exc_info)
        print("inside the house")
    else:
        # remove the traceback levels that relate to runpy or trace
        extracted = [level for level in 
                     extracted if 
                     os.path.basename(level[0]) not in ('command_line.py', 'runpy.py')]
        extracted = traceback.format_list(extracted)
        # print as if it were a normal traceback
        print("Traceback (most recent call last):", file=sys.stderr)
        for level in extracted:
            print(level, end="", file=sys.stderr)
        for line in traceback.format_exception_only(einfo[0], einfo[1]):
            print(line, end="", file=sys.stderr)
