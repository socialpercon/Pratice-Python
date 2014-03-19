#!usr/bin/python
# coding: utf-8
import re
import sys
import os
import collections
import ConfigParser

def split_word_file(filename):
    filedict = {}
    config = ConfigParser.RawConfigParser()
    config.read('reg.ini')
    reg_ex = config.get('Section', "reg")
    frontback_ex = config.get('Section', "frontback")
    cnt = collections.Counter()
    reg = re.compile(reg_ex)
    frontback = re.compile(frontback_ex)
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
                cnt[word] += 1
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

    print cnt.most_common(10)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        split_word_file(sys.argv[1])
    else:
        print "failed : wrong argument"
