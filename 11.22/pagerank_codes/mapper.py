#!/usr/bin/env python

import sys

n=4
link=[[2,3,4],[3,4],[4],[2]]

for line in sys.stdin:
    line=line.strip()
    words=line.split()
    id=int(words[0])-1
    val=float(words[1])
    if len(link[id])==0:
        for i in range(n):
            print '%s\t%s'%(i+1,val/n)
    else:
        for twd in link[id]:
            print '%s\t%s'%(twd,val/len(link[id]))
    print '%s\t%s'%(id+1,0)
