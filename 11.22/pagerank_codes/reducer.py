#!/usr/bin/env python

from operator import itemgetter
import sys

current_id=None
current_val=0
id=None
n=4
a=0.85
offset=(1-a)/n
for line in sys.stdin:
    line=line.strip()
    id,val=line.split('\t', 1)
    val=float(val)
    if current_id == id:
        current_val += val*a
    else:
        if current_id:
            print '%s\t%s' % (current_id,current_val+offset)
        current_val=val*a
        current_id=id

if current_id == id:
    print '%s\t%s' % (current_id,current_val+offset)

