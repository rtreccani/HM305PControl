import threading

from zeroconnect import ZeroConnect, Ad
from PSUMan import *
import time

SERVICE_ID = "0f50032d-cc47-407c-9f1a-a3a28a680c1e"

zc = ZeroConnect("HM305P") #TODO Name?

def rxMSock(sock, nodeId, serviceId):
    print(f"got connection from {nodeId}")

    while True:
        msg = sock.recvMsg()
        print(f"got message from {nodeId}: {msg}")
        if msg == b"power=true":
            print("power on")
            setPSUStatus(True)
        elif msg == b"power=false":
            print("power off")
            setPSUStatus(False)
        elif msg == None:
            print(f"connection closed remotely: {nodeId}")
            sock.close()
            return

def broadcastLoop():
    nextTime = time.time()+0.2
    while True:
        sleepLength = nextTime-time.time()
        if sleepLength > 0:
            time.sleep(sleepLength)
        nextTime = time.time()+0.2

        if getPSUConnected():
            try:
                #st = time.time()

                # This method is ~0.36s
                # state = getPSUStatus()
                # liveVoltage = getVoltageReal()
                # liveCurrent = getCurrentReal()
                # voltageSetpoint = getVoltageSetpoint()
                # currentSetpoint = getCurrentSetpoint()

                # This one's ~0.17s
                (state, liveVoltage, liveCurrent, voltageSetpoint, currentSetpoint) = getPSUData()
                #print(f"time {time.time() - st}")

                zc.broadcast(f"stat:{state}")
                zc.broadcast(f"liveVoltage:{liveVoltage}")
                zc.broadcast(f"liveCurrent:{liveCurrent}")
                zc.broadcast(f"voltageSetpoint:{voltageSetpoint}")
                zc.broadcast(f"currentSetpoint:{currentSetpoint}")
            except Exception as e:
                print(f"error broadcasting state: {e}")

threading.Thread(target=broadcastLoop, args=(), daemon=True).start()

PSUAutoconnect()

zc.advertise(rxMSock, SERVICE_ID)

try:
    input("Press enter to exit...\n\n")
finally:
    zc.close()
    PSUDisconnect()