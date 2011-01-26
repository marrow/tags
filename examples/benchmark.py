import sys
from timeit import Timer
from marrow.tags.html5 import *


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

table_ = [dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)] * 1000
def bigtable(table_): return table (indent=False) [ [(tr [ [(td [ str(i) ]) for i in row.values()] ]) for row in table_ ] ]

print repr(page)
print
print [i for i in page.render('ascii')]
print
print unicode(page)

n = 100000
duration = Timer("[i for i in page.render('ascii')]", "from __main__ import page").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Please wait..."
print "Timeit (Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("unicode(page)", "from __main__ import page").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Timeit (Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

n = 10
duration = Timer("[i for i in table__.render('ascii')]", "from __main__ import bigtable, table_; table__ = bigtable(table_)").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Timeit (Bigtable Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

n = 10
duration = Timer("unicode(table__).encode('ascii')", "from __main__ import bigtable, table_; table__ = bigtable(table_)").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration

print "Timeit (Bigtable Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
