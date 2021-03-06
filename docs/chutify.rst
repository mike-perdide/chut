Generate scripts
================

Chut allow you to generate some standalone scripts. Scripts will include chut
and docopts (and a few other modules if you want) encoded in base64.

How it works
-------------

..
    >>> import os, sys
    >>> import chut as ch
    >>> from chut import test
    >>> ch.rm('-Rf', 'dist/scripts').succeeded
    True
    >>> ch.env['PATH'] = 'bin:/bin:/usr/bin:' + os.path.dirname(sys.executable)

Write a file with a function in it::

    >>> ch.stdin(b'''
    ... import chut as ch
    ... @ch.console_script
    ... def my_script(arguments):
    ...     """Usage: %prog [-h]
    ...
    ...     -h, --help    Print this help
    ...     """
    ...     print('Hello world')
    ... ''') > 'myscript.py'
    ''

Then run chutify on it::

    >>> print(ch.chutify('myscript.py', combine_stderr=True))
    chmod +x dist/scripts/my-script

And check the result in ``dist/scripts``::

    >>> bool(test.x('dist/scripts/my-script'))
    True

    >>> print(ch.pipe('dist/scripts/my-script'))
    Hello world

    >>> print(ch.pipe('dist/scripts/my-script', '-h'))
    Usage: my-script [-h]
    <BLANKLINE>
    -h, --help    Print this help

..
    >>> if test.x('/usr/bin/python2.7'):
    ...   out = str(ch.pipe('python2.7', 'dist/scripts/my-script'))
    ...   assert out.succeeded, out.stderr
    >>> if test.x('/usr/bin/python3'):
    ...   out = str(ch.pipe('python3', 'dist/scripts/my-script'))
    ...   assert out.succeeded, out.stderr
    >>> ch.rm('-f myscript.*', shell=True).succeeded
    True

