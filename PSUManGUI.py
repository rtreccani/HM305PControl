from PSUMan import *
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QDoubleValidator, QPalette, QColor, QColorConstants
from PyQt5.QtCore import QTimer
import time
from pyqt_led import Led





app = QApplication([])
window = QWidget()
finish = QAction('Quit')
finish.triggered.connect(PSUDisconnect)
vertStack = QVBoxLayout()

# Create pushbutton to toggle PSU -----------------------------------
PSUToggleButton = QPushButton('toggle PSU')
PSUToggleButton.clicked.connect(togglePSU)
vertStack.addWidget(PSUToggleButton)
#end ------------------------------------------------------------



# all the voltage stuff goes here -----------------------------------
def handleNewVoltage():
    setVoltageSetpoint(float(voltageInput.text()))

voltageInput = QLineEdit()
validator = QDoubleValidator(0,32,2)
voltageInput.setValidator(validator)
voltageInput.setToolTip('input a voltage between 0 and 32v and hit enter')
voltageInput.setPlaceholderText('voltage')
voltageInput.editingFinished.connect(handleNewVoltage)

voltageBox = QHBoxLayout()
voltageBox.addWidget(QLabel('enter a new voltage'))
voltageBox.addWidget(voltageInput)
voltageBox.addWidget(QLabel('volts'))
vertStack.addLayout(voltageBox)

liveVoltageReadout = QLabel('live voltage')
voltageBox.addWidget(liveVoltageReadout)
#end -----------------------------------------------------------------


# all the current stuff goes here -----------------------------------
def handleNewCurrent():
    setCurrentSetpoint(float(currentInput.text()))

currentInput = QLineEdit()
validator = QDoubleValidator(0,5,3)
currentInput.setValidator(validator)
currentInput.setToolTip('input a current between 0 and 5A and hit enter')
currentInput.setPlaceholderText('current')
currentInput.editingFinished.connect(handleNewCurrent)

currentBox = QHBoxLayout()
currentBox.addWidget(QLabel('enter a new current limit'))
currentBox.addWidget(currentInput)
currentBox.addWidget(QLabel('amps'))
CCLed = Led(None, Led.red, Led.black, Led.circle)
CCLed.set_status(False)
currentBox.addWidget(CCLed)
vertStack.addLayout(currentBox)

liveCurrentReadout = QLabel('live current')
currentBox.addWidget(liveCurrentReadout)
#end -----------------------------------------------------------------

def updateAllReadings():
    (stat, liveVoltage, liveCurrent, voltageSetpoint, currentSetpoint) = getPSUData()

    if(not voltageInput.hasFocus()):
        voltageInput.setText(str(voltageSetpoint))

    if(not currentInput.hasFocus()):
        currentInput.setText(str(currentSetpoint))

    if(stat==True):
        PSUToggleButton.setStyleSheet("background-color:rgb(11,231, 13)")
    else:
        PSUToggleButton.setStyleSheet("")

    liveVoltageReadout.setText(str(liveVoltage))
    liveCurrentReadout.setText(str(liveCurrent))
    if(stat and abs(liveVoltage - voltageSetpoint)>0.1 or abs(liveCurrent-currentSetpoint)<0.1):
        CCLed.set_status(True)
    else:
        CCLed.set_status(False)


readingsTimer = QTimer()
readingsTimer.timeout.connect(updateAllReadings)
readingsTimer.start(200)




window.setWindowTitle('HM305P control by Timecop97')
window.setLayout(vertStack)
window.show()
PSUAutoconnect()
app.exec_()



