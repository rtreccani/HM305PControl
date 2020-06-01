from pymodbus.client.sync import ModbusSerialClient
import signal, sys, time

REG_ONOFF = 1
REG_FLAGS = 2
REG_SPECTYPE = 3
REG_TAIL = 4
REG_DEC_CAPACITY= 5
REG_VGET = 16
REG_IGET = 17
REG_PGETH = 18
REG_PGETL = 19
REG_VSET = 48
REG_ISET = 49
REG_VPROTECT = 36
REG_IPROTECT = 37
REG_PPROTECT = 38
REG_VIRTUALBUSID = 39321 #why 

class flags:
    OVP = False
    OCP = False
    OPP = False
    OTP = False
    SCP = False



UNIT=0x01

client = ModbusSerialClient(method = 'rtu', port='COM9', timeout=2, baudrate=9600)


def PSUConnect():
    connStat = client.connect()
    assert(connStat == True) , 'Couldn\'t connect to PSU' 


def PSUDisconnect(): 
    client.close()   #no return value :(



def setVoltageSetpoint(v):
    assert(v>=0.0 and v <= 32.0), 'voltage setpoint request out of range'
    v = int(v*100.0)
    stat = client.write_register(REG_VSET, v, unit=UNIT)
    assert(not stat.isError()), 'unable to set voltage setpoint'

def getVoltageReal():
    stat = client.read_holding_registers(REG_VGET, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get real voltage'
    return(float(stat.registers[0]/100))

def getVoltageSetpoint():
    stat = client.read_holding_registers(REG_VSET, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get voltage Setpoint'
    return(float(stat.registers[0]/100))

def setVoltageOverProtect(v):
    assert(v >= 0.0 and v <= 32.0), 'voltage overprotect value not in range'
    v = int(v*100.0)
    stat = client.write_register(REG_VPROTECT, v, unit=UNIT)
    assert(not stat.isError()), 'unable to set voltage over-protect'



def setCurrentSetpoint(i):
    assert(i>=0.0 and i <= 5.0),'current out of range'
    i = int(i*1000.0)
    stat = client.write_register(REG_ISET, i, unit=UNIT)
    assert(not stat.isError()), 'unable to set current setpoint'

def getCurrentReal():
    stat = client.read_holding_registers(REG_IGET, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get real current'
    return(float(stat.registers[0]/1000))

def getCurrentSetpoint():
    stat = client.read_holding_registers(REG_ISET, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get current setpoint'
    return(float(stat.registers[0]/1000))



def togglePSU():
    stat = getPSUStatus()
    if(stat):
        setPSUStatus(False)
    else:
        setPSUStatus(True)

def getPSUStatus():
    stat = client.read_holding_registers(REG_ONOFF, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get PSU status'
    stat = stat.registers[0]
    assert(stat == 0 or stat == 1), 'status return code invalid'
    if(stat == 0):
        return(False)
    else:
        return(True)

def setPSUStatus(stat):
    stat = client.write_register(REG_ONOFF, stat, unit=UNIT)
    assert(not stat.isError()), 'unable to set PSU status'



def getPowerReal():
    powerH = client.read_holding_registers(REG_PGETH, 1, unit=UNIT)
    powerL = client.read_holding_registers(REG_PGETL, 1, unit=UNIT)
    assert((not powerH.isError()) and (not powerL.isError())), 'unable to read power level'
    return((a.registers[0]*65535 + b.registers[0])/1000) #merge the two together




def getFlags():
    stat = client.read_holding_registers(REG_FLAGS, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get flags'
    value = stat.registers[0]
    print(value)
    retFlags = flags()
    return(retFlags)

def getTail():
    stat = client.read_holding_registers(REG_FLAGS, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get flags'
    value = stat.registers[0]
    print(value)