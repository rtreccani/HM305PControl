from PSUMan import *
import time

UNIT=0x01

def ctrlc_handler(sig, frame):
    print('program closing')
    client.close()
    sys.exit(0)


PSUConnect()


togglePSU()


v = float(input('what voltage? : '))
setVoltage(v)
time.sleep(0.2)
print(getVoltage())


i = float(input('what current? : '))
setCurrent(i)
time.sleep(0.2)
print(getCurrent())


togglePSU()
setPSUStatus(True)
time.sleep(0.5)
if(getPSUStatus()!=True):
    print('wasnt able to change status to true')
setPSUStatus(False)
time.sleep(0.5)
if(getPSUStatus()!=False):
    print('wasnt able to change status to false')


PSUDisconnect()

