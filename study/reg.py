#!usr/bin/python
# coding: utf-8

import sys

class FileHandler:
    def __init__(self):
        self.filedict = {}
    
    def setfile(self, filename, filedes):
        if not self.filedict.has_key(filename):
            self.filedict[filename] = filedes


class Parser:
    def __init__(self, filename):
        wdict = {}
        try:
            f = open(filename, 'r')
        except IOError, e:
            print "error: %s" %e
        
    def parer(

if __name__ == "__main__":
    filename = sys.argv[1]
    
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
