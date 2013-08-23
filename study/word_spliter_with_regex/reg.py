#!usr/bin/python
# coding: utf-8
import re
import sys
import os
import profile

def split_word_file(filename):
    filedict = {}
    reg = re.compile('[a-zA-Z][a-zA-Z]*[a-zA-Z]')
    frontback = re.compile('([a-zA-Z])[a-zA-Z]*([a-zA-Z])')
    path = os.getcwd()
    try:
        f = open(filename, 'r')
        os.mkdir("%s/file" % path)
    except (IOError, OSError), e:
        print "error: %s" %e
    try:    
        while True:
            chunk = f.readline()
            if chunk:
                words = reg.findall(chunk) 
                for word in words:
                    match = frontback.match(word).group(1,2)
                    front = match[0]
                    back = match[1]
                    filename = "%s%s.txt" % (front, back)
                    if not filedict.has_key(filename):
                        filedict[filename] = open("file/%s" % filename, 'w')
                        filedict[filename].write("%s\n" % word)
                    else:
                        filedict[filename].write("%s\n" % word)
            else:
                break
        for k in filedict:
            filedict[k].close()

    finally:
        f.close()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        profile.run('split_word_file(sys.argv[1])')
    else:
        print "failed : wrong argument"
