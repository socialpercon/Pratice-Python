from websocket import create_connection
import time

ws = create_connection("ws://localhost:8080")
print "Sending 'Hello, World'..."
for i in range(5):
    ws.send("Hello, World")
    time.sleep(5)
    print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()
