# encoding: utf-8

from __future__ import unicode_literals

from timeit import Timer
from marrow.tags.html5 import *
from hscribe.template import template


page = html [
        head [ title [ 'Welcome!' ] ],
        flush, # allow the browser to start downloading static resources early
        body ( class_ = "nav-home" ) [
                p [
                        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                    ],
                flush, # pretend that this next div takes a long time to generate
                div [ 'foo' ]
            ]
    ]


@template
def bigtable2(t, d):
    with d.html():
        with d.head():
            d.title('Welcome!')
        with d.body(class_="nav-home"):
            d.p('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
            d.div('foo')



n = 50000
duration = Timer("list(page.render())", "from __main__ import page").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Please wait..."
print "Timeit (Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("unicode(page)", "from __main__ import page").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Timeit (Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("bigtable2().render()", "from __main__ import bigtable2").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Timeit (Fletcher Page): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
