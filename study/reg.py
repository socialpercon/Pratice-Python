#!usr/bin/python
# coding: utf-8
import re
import sys



if __name__ == "__main__":
    filename = sys.argv[1]
    wdict = {}
    filedict = {}
    reg = re.compile('[a-zA-Z][a-zA-Z]*[a-zA-Z]')
    frontback = re.compile('([a-zA-Z])[a-zA-Z]*([a-zA-Z])')
    try:
        f = open(filename, 'r')
    except IOError, e:
        print "error: %s" %e
    try:    
        wdict = {}
        while True:
            chunk = f.readline()
            if chunk:
                word = re.findall('[a-zA-Z][a-zA-Z]*[a-zA-Z]',chunk) 
                for i in word:
                    match = re.search('([a-zA-Z])[a-zA-Z]*([a-zA-Z])', i).group()
                    front = match[0]
                    back = match[1]
                    filename = "%s%s.txt" % (front, back)
                    if not filedict.has_key(filename):
                        filedict[filename] = open("file/%s.txt" %i, 'w')
                        filedict[filename].write("%s\n" % i)
                    else:
                        filedict[filename].write("%s\n" % i)
            else:
                break
    finally:
        f.close()
