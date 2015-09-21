# Tracestack

Instantly search your Python error messages on the web.

## Features

* Integrate tracestack into your code in seconds, or run it from the command line
* You can automatically search every error, get prompted to search after each error, or just search your latest error.
* Compatible with Python 2 and 3
* Can search for answers on:
    * Google, limited to stackoverflow.com (default)
    * Google, searching the entire web
    * StackOverflow's own search engine

## Installation

    $ pip install tracestack
    
    >>> import tracestack

## Uses and Examples

Do a post-mortem autopsy of your last exception ...
    
    >>> 1 / 0
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
    
    >>> tracestack.pm()
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
    Searching this error message on Stack Overflow (using Google)...

... or catch all future exceptions ...

    >>> tracestack.on()
    >>> 1 / 0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
    Searching this error message on Stack Overflow (using Google)...

    >>> tracestack.off()

... or catch exceptions in only one function ...

    from tracestack import trace

    >>> @trace
    >>> def divide_by_zero():
    ...     1 / 0

... or in any Python script run from the command line ...

    $ tracestack manage.py runserver

... or in a read-evaluate-print loop ... 

    $ tracestack
    Python 2.7.6 (default, Sep  9 2014, 15:04:36) 
    [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (TracestackConsole)
    >>> 1 / 0
    

<img src="http://i.imgur.com/aEHs026.gif" />


## Options

    usage: tracestack [-h] [-p] [-e ENGINE] [SCRIPT] [ARGUMENTS [ARGUMENTS ...]]
    
    instantly search your Python error messages on the web
    
    positional arguments:
      SCRIPT                the Python script
      ARGUMENTS             any arguments to the script
    
    optional arguments:
      -h, --help            show this help message and exit
      -p, --prompt          prompt the user rather than immediately searching
      -e ENGINE, --engine ENGINE
                            the search engine to use:
                              'default': Google search limited to stackoverflow.com
                              'google': Google search of the full web
                              'stackoverflow': StackOverflow site search

In addition to being used on the command line, any of these arguments can be passed to the `pm`, `on`, and `trace` functions:
    
    >>> tracestack.on(prompt=True)
    >>> 1 / 0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
    Hit spacebar to search this error message on Stack Overflow (using Google): 

    >>> 1 / 0
    >>> tracestack.pm(engine="google")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
    Searching this error message on the web (using Google)...

    >>> @tracestack.trace(engine="stackoverflow")
    >>> def divide_by_zero():
    ...     1 / 0
    ...
    >>> divide_by_zero()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "tracestack/decorators.py", line 26, in wrapper
        result = func(*args, **kwargs)
      File "<stdin>", line 3, in divide_by_zero
    ZeroDivisionError: integer division or modulo by zero
    Searching this error message on Stack Overflow...

## Excellent Alternatives 

* [lukasschwab/Stackit](https://github.com/lukasschwab/stackit)
    * search and browse StackOverflow in the command line
    * pipe error messages directly into queries
* [gleitz/howdoi](https://github.com/gleitz/howdoi)
    * get programming answers to plaintext questions in the command line
    * works using inexplicable Jedi magic
* [SylvainDe/DidYouMean-Python](https://github.com/SylvainDe/DidYouMean-Python)
    * auto-suggests fixes to your errors based on common mistakes
    * also possibly magic
* [ajalt/fuckitpy](https://github.com/ajalt/fuckitpy)
    * makes sure your Python code runs "whether it has any right to or not"
    * please do not use this
* [dgrtwo/tracestack](https://github.com/dgrtwo/tracestack)
    * original tracestack package for the R language
    * written on a phone

