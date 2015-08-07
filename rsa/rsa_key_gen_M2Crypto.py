import os
from base64 import b64encode
from M2Crypto import RSA            

key = RSA.gen_key(1024, 65537)
print key
raw_key = key.pub()[1]
print raw_key
b64key = b64encode(raw_key)

#username = os.getlogin()
#hostname = os.uname()[1]
keystring = 'ssh-rsa {}'.format(b64key)
dir(RSA)
#RSA.importKey(keystring, passphrase="f00bar")
print keystring