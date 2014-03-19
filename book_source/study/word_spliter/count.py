#!usr/bin/python
# coding: utf-8

import sys



if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
    except IOError, e:
        print "error"
    
    try:    
        wdict = {}
        for s in f.readlines():
            b = s.split(' ')
            for word in b:
                w = word.strip()
                try:
                    wdict[w] = wdict[w] +1
                except KeyError:
                    wdict[w] = 1
        for k in wdict:
            print k, wdict[k]

    finally:
        f.close()
