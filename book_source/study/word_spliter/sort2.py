#!usr/bin/python
# coding: utf-8
import sys
import operator



if __name__ == "__main__":

    try:
        f = open('./data.txt', 'r')
    except IOError, e:
        print "error"
    
    try:    
        wdict = {}
        for s in f:
            b = s.split(' ')
            
        for word in b:
            w = word.strip()
            if w == '':
                continue
            else:
                try:
                    wdict[w] = wdict[w] +1
                except KeyError:
                    wdict[w] = 1
                
        sorted_dict = sorted(wdict.iteritems(), key = operator.itemgetter(1))
        for i in range(-4,-1):
            print sorted_dict[i]
    finally:
        f.close()
