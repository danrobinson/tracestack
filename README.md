# Tracestack
Instantly search your Python error messages on the web

## Features

* Integrate it into your code in seconds, or run it from the command line
* Post-mortem mode
* REPL mode
* Compatible with Python 2 and 3
* Can search for answers on:
 * Google, limited to stackoverflow.com (default)
 * The entire web (via Google)
 * StackOverflow's own search engine

## Installation

Install using pip:

    pip install git+git://github.com/danrobinson/tracestack.git

## Uses and Examples

Do a post-mortem autopsy of your last exception ...

    >>> tracestack.pm()
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
    Type s to search this error message on Stack Overflow (using Google):

... or catch all future exceptions ...

    tracestack.enable()
    ...
    # buggy code here
    ...
    # tracestack.disable()

... or in any Python script run from the command line ...

    $ tracestack manage.py runserver

... or in a read-evaluate-print-loop ... 

    $ tracestack
    Python 2.7.6 (default, Sep  9 2014, 15:04:36) 
    [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (TracestackConsole)
    >>> 

... or in only one function . . .

    from tracestack import trace

    @trace
    def buggy_function():
        # ... buggy code ...

## Options

    usage: tracestack [-h] [-s] [-e ENGINE] [SCRIPT] [ARGUMENTS [ARGUMENTS ...]]
    
    instantly search your Python error messages on the web
    
    positional arguments:
      SCRIPT                the Python script
      ARGUMENTS             any arguments to the script
    
    optional arguments:
      -h, --help            show this help message and exit
      -s, --skip            skip the prompt and immediately search each exception
      -e ENGINE, --engine ENGINE
                            the search engine to use:
                              'default': Google limited to stackoverflow.com, 
                              'google': full web on Google, 
                              'stackoverflow': StackOverflow site search

In addition to being used on the command line, any of these arguments can be passed to the `pm`, `enable`, and `trace` functions:
    
    tracestack.pm(skip=True)
    # will immediately run search based on the last exception

    tracestack.enable(engine="google")
    # future exceptions will prompt a search of the entire web
    
    tracestack.trace(engine="stackoverflow")
    def buggy_function():
         """exceptions raised by this function will prompt 
         a search directly on stackoverflow.com """
         ...

## Excellent Alternatives 

* [lukasschwab/Stackit](https://github.com/lukasschwab/stackit)
 * search and browse StackOverflow in the command line
 * pipe error messages directly into queries
* [gleitz/howdoi](https://github.com/gleitz/howdoi)
 * get programming answers to plaintext questions in the command line
 * works via insane Jedi magic
* [dgrtwo/tracestack](https://github.com/dgrtwo/tracestack)
 * original tracestack package for R programs
 * written on a phone

