# encoding: utf-8

from __future__ import unicode_literals

from timeit import Timer

from marrow.tags.html5 import *
from hscribe.template import template
from marrow.tags.html5 import table, tr, td


table_ = [dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10) for x in range(1000)]


def bigtable1():
    return table[
            (tr[
                (td[c] for c in row)
            ] for row in table_)
        ]


def bigtable3():
    return table[
            (tr[
                (td[c] for c in row)
            ] for row in table_)
        ]


@template
def bigtable2(t, d):
    with d.table():
        for row in table_:
            with d.tr():
                for c in row.values():
                    d.td(c)


n = 10
duration = Timer("list(r.render())", "from __main__ import bigtable1; r = bigtable1()").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration
print "Timeit (Bigtable Cached Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("unicode(r)", "from __main__ import bigtable1; r = bigtable1()").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration
print "Timeit (Bigtable Cached Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("list(r().render())", "from __main__ import bigtable3; r = bigtable3").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration
print "Timeit (Bigtable Regen Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("unicode(r())", "from __main__ import bigtable3; r = bigtable3").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration
print "Timeit (Bigtable3 Regen Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)

duration = Timer("r().render()", "from __main__ import bigtable2; r = bigtable2").timeit(n)
timeper = duration / float(n) * 1000
genper = float(n) / duration
print "Timeit (Fletcher Bigtable): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
