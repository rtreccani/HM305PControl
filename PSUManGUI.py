from PSUMan import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
import time

UNIT=0x01

def ctrlc_handler(sig, frame):
    print('program closing')
    client.close()
    sys.exit(0)


PSUConnect()

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
PSUToggleButton = QPushButton('toggle PSU')
PSUToggleButton.clicked.connect(togglePSU)
layout.addWidget(PSUToggleButton)
window.setLayout(layout)
window.show()
app.exec_()


