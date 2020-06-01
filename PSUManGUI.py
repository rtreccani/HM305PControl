from PSUMan import *
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QTimer
import time





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

def updateLiveVoltage():
    liveVoltageReadout.setText(str(getVoltageReal()))

liveVoltageReadout = QLabel('live voltage')
voltageTimer = QTimer()
voltageTimer.timeout.connect(updateLiveVoltage)
voltageTimer.start(200)
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
vertStack.addLayout(currentBox)

def updateLiveCurrent():
    liveCurrentReadout.setText(str(getCurrentReal()))

liveCurrentReadout = QLabel('live current')
currentTimer = QTimer()
currentTimer.timeout.connect(updateLiveCurrent)
currentTimer.start(200)
currentBox.addWidget(liveCurrentReadout)
#end -----------------------------------------------------------------










window.setLayout(vertStack)
window.show()
PSUConnect()
app.exec_()



