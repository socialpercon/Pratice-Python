import sys

try:
    raise Exception

except Exception, e:
    import traceback
    print "exception: {0}, {1}".format(sys.exc_info()[2].tb_lineno, traceback.format_exc)
