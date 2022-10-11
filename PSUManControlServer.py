"""
Run this file to start a server to permit remote control of the PSU over ZeroConnect,
like with https://github.com/Erhannis/HM305PRemote or the simple zc_client_test.py script.
"""

import threading
import re

from zeroconnect import ZeroConnect, Ad
from PSUMan import *
import time

SERVICE_ID = "0f50032d-cc47-407c-9f1a-a3a28a680c1e"
#SERVICE_ID = "0f50032d-cc47"
#SERVICE_ID = "PSUTEST"

zc = ZeroConnect("HM305P") #TODO Name?

def rxMSock(sock, nodeId, serviceId):
    print(f"got connection from {nodeId}")
    r = re.compile(r'^([-a-zA-Z0-9_]+)=([0-9.]+)$')

    while True:
        msg = sock.recvMsg()
        try:
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
            else:
                msg = msg.decode("utf-8")
                m = r.match(msg)
                if m == None:
                    print(f"messages unhandled")
                    continue
                var = m.group(1)
                val = 0
                try:
                    val = float(m.group(2))
                except:
                    print(f"invalid double {m.group(2)}")
                    continue
                if var == "voltageSetpoint":
                    print(f"setVoltageSetpoint {val}")
                    setVoltageSetpoint(val)
                elif var == "currentSetpoint":
                    print(f"setCurrentSetpoint {val}")
                    setCurrentSetpoint(val)
                elif var == "voltageOverprotect":
                    print(f"setVoltageOverProtect {val}")
                    setVoltageOverProtect(val)
                elif var == "currentOverprotect":
                    print(f"setCurrentOverProtect {val}")
                    setCurrentOverProtect(val)
                else:
                    print(f"unhandled key: {var}")
        except Exception as e:
            print(f"error processing message: {e}")

def broadcastLoop():
    nextTime = time.time()+0.2
    while True:
        sleepLength = nextTime-time.time()
        if sleepLength > 0:
            time.sleep(sleepLength)
        nextTime = time.time()+0.2

        if getPSUConnected():
            try:
                (state, liveVoltage, liveCurrent, voltageSetpoint, currentSetpoint, voltageOverprotect, currentOverprotect) = getPSUData()

                zc.broadcast(f"connected:{getPSUConnected()}")
                zc.broadcast(f"state:{state}")
                zc.broadcast(f"liveVoltage:{liveVoltage}")
                zc.broadcast(f"liveCurrent:{liveCurrent}")
                zc.broadcast(f"voltageSetpoint:{voltageSetpoint}")
                zc.broadcast(f"currentSetpoint:{currentSetpoint}")
                zc.broadcast(f"voltageOverprotect:{voltageOverprotect}")
                zc.broadcast(f"currentOverprotect:{currentOverprotect}")
            except Exception as e:
                print(f"error broadcasting state: {e}")
        else:
            #TODO Try reconnect?
            pass

threading.Thread(target=broadcastLoop, args=(), daemon=True).start()

PSUAutoconnect()

zc.advertise(rxMSock, SERVICE_ID)

try:
    input("Press enter to exit...\n\n")
finally:
    zc.close()
    PSUDisconnect()