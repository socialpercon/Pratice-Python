import os
import sys
import time

def main() :
	interval = int(sys.argv[1])
	zipName  = sys.argv[2]
	program  = sys.argv[3]

	print interval , zipName, program

	while 1 :
			cmd = """mce job -list | grep "%s" | awk '{print $2}'""" % program
			cid = os.popen(cmd).read(1000).strip()

			cmd = "mce job -kill %s" % cid
			os.system(cmd)
			print cmd

			cmd = "mce job -run %s %s" % (zipName , program)
			os.system(cmd)
			print cmd

			print "sleep ... %s" % interval
			time.sleep(interval)


if __name__ == "__main__" :
	main()
