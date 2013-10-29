import ConfigParser 
import os

config = ConfigParser.ConfigParser() 
PATH = os.path.dirname( os.path.abspath( __file__ ) )
print PATH
config.read("%s/mce.ini" % PATH) 
try : PORT = config.get("SECTION","PORT")
except : PORT = 6060
print PORT 
try : IP = config.get("SECTION","IP") 
except : IP = "127.0.0.1"
print IP
