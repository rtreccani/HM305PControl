from zeroconnect import ZeroConnect, Ad
from time import sleep
import threading

SERVICE_ID = "0f50032d-cc47-407c-9f1a-a3a28a680c1e"

zc = ZeroConnect()

sock = zc.connectToFirst(SERVICE_ID)

def printMsgs():
    while True:
        msg = sock.recvMsg()
        if msg == None:
            return
        print(msg)

threading.Thread(target=printMsgs, args=(), daemon=True).start()

sleep(0.1)
sock.sendMsg("power=true")
sleep(1)
sock.sendMsg("power=false")

sleep(10000)

zc.close()