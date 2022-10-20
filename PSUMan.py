from pymodbus.client.sync import ModbusSerialClient
import signal, sys, time
import serial.tools.list_ports

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
REG_VPROTECT_GET = 32
REG_IPROTECT_GET = 33
REG_PPROTECT_GET = 34
REG_VPROTECT_SET = 36 # Doesn't work??  Just use _GET
REG_IPROTECT_SET = 37 # Haven't tried, but _GET works
REG_PPROTECT_SET = 38 # Haven't tried either way, but given the other two....
REG_VIRTUALBUSID = 39321 #why 

class flags:
    OVP = False
    OCP = False
    OPP = False
    OTP = False
    SCP = False



UNIT=0x01

client = ModbusSerialClient(method = 'rtu', port='COM9', timeout=2, baudrate=9600)

def PSUAutoconnect():
    PSUDisconnect()
    ports = serial.tools.list_ports.comports()
    for port in ports:
        client.port = port.device
        connStat = client.connect()
        if connStat:
            try:
                getVoltageReal() # A check to see if we're actually connected to a PSU
                print(f"connected to {port.device}")
                return
            except:
                pass
        client.close()
    assert(False == True) , 'Couldn\'t connect to PSU' 

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
    assert(v >= 0.0 and v <= 33.0), 'voltage overprotect value not in range'
    v = int(v*100.0)
    stat = client.write_register(REG_VPROTECT_GET, v, unit=UNIT)
    assert(not stat.isError()), 'unable to set voltage overprotect'

def getVoltageOverProtect():
    stat = client.read_holding_registers(REG_VPROTECT_GET, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get voltage overprotect'
    return(float(stat.registers[0]/100))



def setCurrentSetpoint(i):
    assert(i>=0.0 and i <= 10.10),'current out of range'
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

def setCurrentOverProtect(i):
    assert(i >= 0.0 and i <= 10.5), 'current overprotect value not in range'
    i = int(i*1000.0)
    stat = client.write_register(REG_IPROTECT_GET, i, unit=UNIT)
    assert(not stat.isError()), 'unable to set current overprotect'

def getCurrentOverProtect():
    stat = client.read_holding_registers(REG_IPROTECT_GET, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get current overprotect'
    return(float(stat.registers[0]/1000))



def togglePSU():
    stat = getPSUStatus()
    if(stat):
        setPSUStatus(False)
    else:
        setPSUStatus(True)

def getPSUConnected():
    return client.is_socket_open() # Doesn't distinguish from a connected, incorrect com port, but should work in MOST circumstances.

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

def getPSUData():
    stat = client.read_holding_registers(0, 50, unit=UNIT)
    assert(not stat.isError()), 'unable to get PSU status'
    stat = stat.registers
    state = stat[REG_ONOFF]
    liveVoltage = stat[REG_VGET] / 100
    liveCurrent = stat[REG_IGET] / 1000
    voltageSetpoint = stat[REG_VSET] / 100
    currentSetpoint = stat[REG_ISET] / 1000
    voltageOverprotect = stat[REG_VPROTECT_GET] / 100
    currentOverprotect = stat[REG_IPROTECT_GET] / 1000
    return (state, liveVoltage, liveCurrent, voltageSetpoint, currentSetpoint, voltageOverprotect, currentOverprotect)
    





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
    stat = client.read_holding_registers(REG_TAIL, 1, unit=UNIT)
    assert(not stat.isError()), 'unable to get tail'
    value = stat.registers[0]
    print(value)
    return(value)