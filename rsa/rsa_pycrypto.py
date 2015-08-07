from Crypto.PublicKey import RSA

date = "20140720"
key = RSA.generate(2048)

private_key = key.exportKey('PEM')
public_key = key.publickey()
public_key_str = public_key.exportKey('PEM')
print "private_key : {}".format(private_key)
print "public_key : {}".format(public_key_str)
print type(RSA.importKey(public_key_str))
