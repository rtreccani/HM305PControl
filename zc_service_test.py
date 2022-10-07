from zeroconnect import ZeroConnect, Ad
from PSUMan import *

SERVICE_ID = "0f50032d-cc47-407c-9f1a-a3a28a680c1e"

zc = ZeroConnect("HM305P") #TODO Name?

def rxMSock(sock, nodeId, serviceId):
    print(f"got connection from {nodeId}")
    while True:
        msg = sock.recvMsg()
        print(f"got message from {nodeId}: {msg}")
        if msg == b"[power=true]":
            print("power on")
            setPSUStatus(True)
        elif msg == b"[power=false]":
            print("power off")
            setPSUStatus(False)
        elif msg == None:
            print(f"connection closed remotely: {nodeId}")
            sock.close()
            return

PSUAutoconnect()

zc.advertise(rxMSock, SERVICE_ID)

try:
    input("Press enter to exit...\n\n")
finally:
    zc.close()
    PSUDisconnect()