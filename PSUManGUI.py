from PSUMan import *
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QDoubleValidator
import time





app = QApplication([])
window = QWidget()
finish = QAction('Quit')
finish.triggered.connect(PSUDisconnect)
vertStack = QVBoxLayout()


PSUToggleButton = QPushButton('toggle PSU')
PSUToggleButton.clicked.connect(togglePSU)



# all the voltage stuff goes here -----------------------------------
def handleNewVoltage():
    setVoltageSetpoint(float(voltageInput.text()))

voltageInput = QLineEdit()
validator = QDoubleValidator(0,32,2)
voltageInput.setValidator(validator)
voltageInput.setToolTip('enter a new voltage and hit enter')
voltageInput.setPlaceholderText('voltage')
voltageInput.editingFinished.connect(handleNewVoltage)

voltageBox = QHBoxLayout()
voltageBox.addWidget(QLabel('enter a new voltage'))
voltageBox.addWidget(voltageInput)
voltageBox.addWidget(QLabel('volts'))
#end -----------------------------------------------------------------


# all the current stuff goes here -----------------------------------
def handleNewCurrent():
    setCurrentSetpoint(float(currentInput.text()))

currentInput = QLineEdit()
validator = QDoubleValidator(0,5,3)
currentInput.setValidator(validator)
currentInput.setToolTip('enter a new current and hit enter')
currentInput.setPlaceholderText('current')
currentInput.editingFinished.connect(handleNewCurrent)

currentBox = QHBoxLayout()
currentBox.addWidget(QLabel('enter a new current limit'))
currentBox.addWidget(currentInput)
currentBox.addWidget(QLabel('amps'))
#end -----------------------------------------------------------------


vertStack.addWidget(PSUToggleButton)
vertStack.addLayout(voltageBox)
vertStack.addLayout(currentBox)





window.setLayout(vertStack)
window.show()
PSUConnect()
app.exec_()



