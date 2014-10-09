"""Demonstration of why gloabal mutable state is bad.

When running in a threaded/multi-process environement,
such as mod-wsgi,apache, or a wsgi server, or simply a threaded application
(such as plone/zope2, global mutable state is not safe.

Running this script that uses a global file pointer:

  while true; do python globfptest.py global ;if [ $? -ne 0 ]; then break; sleep 0.2; fi; done

will always segfault.

Using a local file pointer:

  while true; do python globfptest.py local ;if [ $? -ne 0 ]; then break; sleep 0.2; fi; done

Will run forever.

"""
import random
import threading


gfp = open('test.txt')


def readline_gfp():
    global gfp
    pos = gfp.tell()
    gfp.seek(0)
    line = next(gfp)
    for i, next_line in enumerate(gfp):
        pos = gfp.tell()
        if random.randrange(i + 2):
            continue
        line = next_line        
        print 'LOOP:', pos, line
    return pos, line


def readline_lfp():
    with open('test.txt') as fp:
        pos = fp.tell()
        line = next(fp)
        for i, next_line in enumerate(fp):
            if random.randrange(i + 2):
                continue
            line = next_line
            pos = fp.tell()
            print 'LOOP:', pos, line
    return pos, line


def make_thread_test(func, nthreads=10, cleanup=None):
    threads = []
    for i in range(nthreads):
        t = threading.Thread(target=func, name='Thread %i' % i)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    if cleanup:
        cleanup()


def test_gfp():
    make_thread_test(readline_gfp, cleanup=gfp.close)


def test_lfp():
    make_thread_test(readline_lfp)


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if 'global' in args:
        test_gfp()
    elif 'local' in args:
        test_lfp()
    else:
        print __doc__
        print "Specify 'local' or 'global' as a tset to run"
        sys.exit(1)

