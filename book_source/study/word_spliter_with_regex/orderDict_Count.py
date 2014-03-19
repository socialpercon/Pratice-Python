#!usr/bin/python
# coding: utf-8
import re
import sys
import os
import collections

def split_word_file(filename):
    filedict = {}
    cnt = {} 
    reg = re.compile('[a-zA-Z][a-zA-Z]*[a-zA-Z]')
    frontback = re.compile('([a-zA-Z])[a-zA-Z]*([a-zA-Z])')
    path = os.getcwd()
    try:
        f = open(filename, 'r')
        os.mkdir("%s/file" % path)
    except (IOError, OSError), e:
        print "error: %s" %e
    try:    
        for chunk in f:
            words = reg.findall(chunk) 
            for word in words:
                if cnt.has_key(word):
                    cnt[word] += 1
                else:
                    cnt[word] = 1
                match = frontback.match(word).group(1,2)
                front = match[0]
                back = match[1]
                filename = "%s%s.txt" % (front, back)
                if not filedict.has_key(filename):
                    filedict[filename] = open("file/%s" % filename, 'w')
                    filedict[filename].write("%s\n" % word)
                else:
                    filedict[filename].write("%s\n" % word)
        for k in filedict:
            filedict[k].close()
    finally:
        f.close()

    collections.deque(collections.OrderedDict(sorted(cnt.items(), key = lambda t:t[1])), 10)
    dic=collections.OrderedDict(sorted(cnt.items(), key = lambda t:t[1]))
    print dic.items()[0:10]
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        split_word_file(sys.argv[1])
    else:
        print "failed : wrong argument"
