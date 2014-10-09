.. title: Global mutable state - A dragon lies waiting
.. slug: global-mutable-state-a-dragon-lies-waiting
.. date: 2014-10-08 20:05:51 UTC+01:00
.. tags: python globals WSGI CGI
.. link: 
.. description: An article about global mutable state.
.. type: rest

======================================
Global mutable state - Dragons be here
======================================


Preface
-------

Commonly seen phrases:

  *"Global state is evil"*

  *"Avoid global module state!"*


Global state, and it's use, is a topic which every programmer will run into at some point.

Recently, I reviewed some Python_ code which involed the selection of random lines from a file,
and noticed that the code was written using a file pointer at as a global module variable.
(*The intention is to make this code available in a web application at some point*)


Scenario
--------
Given the following python module:


.. code-block:: python

    import random

    some_file = open('/usr/share/dict/words')
 
    def random_line():
        line = next(some_file)
        for (idx, next_line) in enumerate(some_file):
           if random.randrange(idx + 2):
	        continue
	   line = next_line
        return line

    print(random_line(a_ gfile))
    some_file.close()
 
This will run just fine, so long as its run in a dedicated python process.

However, when this code is executed concurrently in a threaded/multi-process environment
(e.g: under the Apache mod-wsgi module in either mpm or pre-fork),
then the program can crash with a segmentation fault.
An `example`_ would be when the number of threads per process is configured to be greater than 1 under
`mod-wsgi`_.

Global module variables are shared between threads.

This means it's not safe to access a global variable in a threaded Python program,
at least not without employing locking.

In this scenario, obviously the variable ``some_file`` has a pointer to the current position in file file.

A bits of history
----------------
In ancient times, scripts were executed as a separate, dedicated process as `CGI`_ scripts.
With the advent of embeded Python processes in webservers (e.g mod_python under Apache, and subsequently
mod-wsgi and the myriad other WSGI_ implementations), Python processes in webservers now do not execute a 
under a dedicated interpreter for each request, but rather employ what's know as a `sub interpeter`_.


Summary
-------
Generally, it best to *avoid use of global mutable module variables*.
 

.. _example: http://stackoverflow.com/questions/13171860/how-django-handles-simultaneous-requests-with-concurrency-over-global-variables
.. _mod-wsgi: https://code.google.com/p/modwsgi/
.. _CGI: http://en.wikipedia.org/wiki/Common_Gateway_Interface
.. _WSGI: http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
.. _`sub interpeter`: https://docs.python.org/2/c-api/init.html#sub-interpreter-support
