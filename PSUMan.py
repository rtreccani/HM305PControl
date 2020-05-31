from pymodbus.client.sync import ModbusSerialClient
import signal, sys, time
from PSUManDefs import *

UNIT=0x01

client = ModbusSerialClient(method = 'rtu', port='COM9', timeout=2, baudrate=9600)

def ctrlc_handler(sig, frame):
    print('program closing')
    client.close()
    sys.exit(0)


def PSUConnect():
    signal.signal(signal.SIGINT, ctrlc_handler)
    res = client.connect()
    if(res == False):
        print('connecting to port failed')
        sys.exit(0)

def PSUDisconnect(): 
    client.close()   




def setVoltage(v):
    if(v<0.0 or v > 32.0):
        print('voltage out of range')
    else:
        v = int(v*100.0)
        a = client.write_register(REG_VSET, v, unit=UNIT)
        if(a.isError()):
            print(a)

def getVoltage():
    a = client.read_holding_registers(REG_VGET, 1, unit=UNIT)
    if(a.isError()):
        print('unable to read voltage')
    else:
        return(float(a.registers[0]/100))

def getVoltageSetpoint():
    a = client.read_holding_registers(REG_VSET, 1, unit=UNIT)
    if(a.isError()):
        print('unable to read voltage')
    else:
        return(float(a.registers[0]/100))



    
def setCurrent(i):
    if(i<0.0 or i > 5.000):
        print('current out of range')
    else:
        i = int(i*1000.0)
        a = client.write_register(REG_ISET, i, unit=UNIT)
        if(a.isError()):
            print(a)

def getCurrent():
    a = client.read_holding_registers(REG_IGET, 1, unit=UNIT)
    if(a.isError()==0):
        return(float(a.registers[0]/1000))
    else:
        print('unable to read current')

def getCurrentSetpoint():
    a = client.read_holding_registers(REG_ISET, 1, unit=UNIT)
    if(a.isError()==0):
        return(float(a.registers[0]/1000))
    else:
        print('unable to read current')



def togglePSU():
    a = client.read_holding_registers(REG_ONOFF, 1, unit=UNIT)
    if(a.isError()):
        print('unable to read PSU status')
    else:
        stat = a.registers[0]
        stat = 1-stat #invert the value
        a = client.write_register(REG_ONOFF, stat, unit=UNIT)
        if(a.isError()):
            print('was able to read PSU status but not write it')

def getPSUStatus():
    a = client.read_holding_registers(REG_ONOFF, 1, unit=UNIT)
    if(a.isError()):
        print('unable to read PSU status')
    else:
        stat = a.registers[0]
        if(stat == 0):
            return(False)
        elif(stat == 1):
            return(True)
        else:
            print('PSU status returned invalid')
            print(a.registers[0])

def setPSUStatus(stat):
    a = client.write_register(REG_ONOFF, stat, unit=UNIT)
    if(a.isError()):
        print('unable to write PSU status')
