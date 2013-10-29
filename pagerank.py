#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Original version(ruby): http://snippets.dzone.com/posts/show/3284
"""
M = 0x100000000 # modulo for unsigned int 32bit(4byte)

class GooglePageRank:
	def __init__(self, uri):
		self.uri = uri
		self.iurl = "info:%s" % uri

	def m1(self, a, b, c, d):
		return (((a + (M - b) + (M - c)) % M) ^ (d % M)) % M # mix/power mod

	def i2c(self, i):
		return [i & 0xff, i>>8 & 0xff, i>>16 & 0xff, i>>24 & 0xff]

	def c2i(self, s, k=0):
		try:
			try: c0 = ord(s[k])
			except: c0 = 0
			try: c1 = ord(s[k+1])
			except: c1 = 0
			try: c2 = ord(s[k+2])
			except: c2 = 0
			try: c3 = ord(s[k+3])
			except: c3 = 0
			c2i = ((c3*0x100+c2)*0x100+c1)*0x100+c0
		except:
			c2i = 0
		return c2i

	def mix(self, a, b, c):
		a %= M; b %= M; c %= M
		a = self.m1(a, b, c, c>>13); b = self.m1(b, c, a, a<< 8); c = self.m1(c, a, b, b>>13)
		a = self.m1(a, b, c, c>>12); b = self.m1(b, c, a, a<<16); c = self.m1(c, a, b, b>> 5)
		a = self.m1(a, b, c, c>> 3); b = self.m1(b, c, a, a<<10); c = self.m1(c, a, b, b>>15)
		return [a, b, c]

	def old_cn(self, iurl = None):
		if not iurl:
			iurl = self.iurl
		a = 0x9E3779B9; b = 0x9E3779B9; c = 0xE6359A60
		size = len(iurl)
		k = 0
		while size >= k+12:
			a += self.c2i(iurl, k); b += self.c2i(iurl, k+4); c += self.c2i(iurl, k+8)
			a, b, c = self.mix(a, b, c)
			k += 12
		a += self.c2i(iurl, k)
		b += self.c2i(iurl, k+4)
		c += (self.c2i(iurl, k+8) << 8) + size
		a, b, c = self.mix(a, b, c)
		return c

	def cn(self):
		ch = self.old_cn()
		ch = ((ch / 7) << 2) | ((ch - (ch / 13) * 13) & 7)
		new_url = ""
		for ii in range(20):
			for i in self.i2c(ch):
				new_url += chr(i)
			ch -=9
		return int("6%s" % self.old_cn(new_url))
	
	def request_uri(self):
		from urllib import quote
		uri = "http://toolbarqueries.google.com/search?client=navclient-auto&hl=en&ch=%s&ie=UTF-8&oe=UTF-8&features=Rank&q=info:%s"
		cn = self.cn()
		quoted_uri = quote(self.uri, safe="")
		return uri % (cn, quoted_uri)

	def page_rank(self, uri=None):
		if not uri:
			uri = self.uri
		else:
			self.uri = uri
		uri = self.request_uri()
		from urllib2 import urlopen
		doc = urlopen(uri)
		return int(doc.read().split(":")[2])


def Main(cmdoptions, cmdargs):
	
	print GooglePageRank(cmdargs[0]).page_rank()

	return 0



if __name__ == "__main__":
	import os, optparse
	cmdparser = optparse.OptionParser(usage="%prog [options] <uri>")
	cmdparser.add_option("-v", "--verbose", dest="is_verbose", default=False, action="store_true",
							help="Show verbose messages. (disabled by default)")
	cmdparser.add_option("-o", "--output-file", dest="output_file", default=None,
							help="Output file name (None)")
	(cmdoptions, cmdargs) = cmdparser.parse_args()
	
	os._exit(Main(cmdoptions, cmdargs))


