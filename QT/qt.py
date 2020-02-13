import sys
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import *
from mainUi import Ui_Frame
import socket
import time
import threading
from datetime import datetime
from multiprocessing import Process
'''pyuic5  init.ui > mainUi.py'''

'''Comunication'''
UDP_IP = "192.168.250.1"
UDP_PORT = 9600

class com:
    sock= None

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("UDP target IP:", UDP_IP)
            print("UDP target port:", UDP_PORT)

        except socket.error:
            print('Failed to create socket')


    testmessage = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x00\x05\x01'

    # Write message on PLC
    def writeMessage(self, memmory, message):
        try:
            # 010282006E000002AAAABBBB
            # 8000010001000020001A010282006E000002AAAABBBB
            header = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0A\x01\x02\x82\x00'
            header = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0A\x01\x02\x30\x00'
                                                                #0102300ADD0A000101

            footer = b'\x00\x00\x01'#\x80\x00\x01\x00\x01\x00\x00\x20\x00\x00\x01\x02\x82\x00\x6e\x00\x00\x01'
            print(memmory.to_bytes(2,'big'))
            sendMessage = header + memmory.to_bytes(1,'big') + footer + message.to_bytes(2,'big')
            print("Sendmessage")
            print(sendMessage)
            self.sock.sendto(sendMessage, (UDP_IP, UDP_PORT))
        except self.sock.error:
            print('Unable to send message')



    # Read message on PLC
    def readOneMemory(self,memory):
        messageHeader = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0B\x01\x01\x82\x00'
        messageFooter = b'\x00\x00'

        sendMessage = messageHeader + memory.to_bytes(1, 'big')+ messageFooter

        print ("sefC")
        self.sock.sendto(sendMessage, (UDP_IP, UDP_PORT))

    def readTwoMemory(self,memory):
        messageHeader = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0B\x01\x01\x82\x00'
        messageFooter = b'\x00\x00\x02'
        nextMemory = memory + 1
        sendMessage = messageHeader + memory.to_bytes(1, 'big') + messageFooter

        print ("sefC")
        self.sock.sendto(sendMessage, (UDP_IP, UDP_PORT))

    def decodeBytes(self,bts):
        val = b'\x00' + bts[-2:]
        # print(val)
        # print(int.from_bytes(val, byteorder='big', signed=True))
        #
        return int.from_bytes(val, byteorder='big', signed=True)

    def decodeTwoBytes(self,bts):
        val = b'\x00' + bts[-1:]
        val1 = b'\x00' + bts[-4:-2]
        print(val)
        # print(int.from_bytes(val, byteorder='big', signed=True))
        #
        return (int.from_bytes(val, byteorder='big', signed=True),int.from_bytes(val1, byteorder='big', signed=True))

    def receivedOneMemory(self):
        defi = int(0)
        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        print(data[9:10])
        if data[9:10] == b'\x0B' :  #preciso ver o codigo
            #     # response from read
            defi = self.decodeBytes(data)
            print(defi)
            return int(defi)
        elif data[9:10] == b'\x0A':  # preciso ver o codigo
            # response from write
            return -1

    def receivedTwoMemory(self):
        defi = int(0)
        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        print(data[9:10])
        if data[9:10] == b'\x0B':  # preciso ver o codigo
             #     # response from read
            defi = self.decodeTwoBytes(data)

            #print(defi)
            return defi
        elif data[9:10] == b'\x0A':  # preciso ver o codigo
            # response from write
            return -1



def test():
    global com1
    com1.readMessage(100)
    com1.received()


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        self.initState()
        self.show()
        self.showMaximized()
        self.ui.buttonInOut.clicked.connect(self.toggleInOutFrame)
        self.ui.buttonData.clicked.connect(self.toggleDataFrame)
        self.ui.buttonManual.clicked.connect(self.toggleManual)
        self.ui.buttonTeach.clicked.connect(self.teachButtonClicked)

    def initState(self):
        self.ui.frameInOut.setVisible (False)
        self.ui.frameCounter.setVisible (False)
        self.ui.slider_X.setVisible (False)
        self.ui.slider_Y.setVisible (False)
        self.ui.buttonStep.setVisible (False)
        self.ui.buttonZ.setVisible (False)
        self.ui.buttonDrill.setVisible (False)
        self.ui.buttonTeach.setVisible (False)
        self.ui.buttonNextDrill.setVisible (False)
        self.ui.buttonEndTeach.setVisible (False)
        self.ui.buttonCartesianEnable.setVisible (False)

    def toggleManual(self):
        if self.ui.buttonManual.text() == "Manual":
            self.ui.slider_X.setVisible(True)
            self.ui.slider_Y.setVisible (True)
            self.ui.buttonStep.setVisible (True)
            self.ui.buttonZ.setVisible (True)
            self.ui.buttonDrill.setVisible (True)
            self.ui.buttonTeach.setVisible(True)
            self.ui.buttonNextDrill.setVisible(True)
            self.ui.buttonEndTeach.setVisible(True)
            self.ui.buttonCartesianEnable.setVisible(True)
            self.ui.buttonManual.setText ("Auto")
        else:
            self.ui.slider_X.setVisible (False)
            self.ui.slider_Y.setVisible (False)
            self.ui.buttonStep.setVisible (False)
            self.ui.buttonZ.setVisible (False)
            self.ui.buttonDrill.setVisible (False)
            self.ui.buttonTeach.setVisible(False)
            self.ui.buttonNextDrill.setVisible(False)
            self.ui.buttonEndTeach.setVisible(False)
            self.ui.buttonCartesianEnable.setVisible (False)
            self.ui.buttonManual.setText ("Manual")

    def teachButtonClicked(self):
        self.ui.lb_X.setText("we")
        #com1.readOneMemory(100)
        #com1.receivedOneMemory()

        #self.ui.lb_X.setText (data)





    def toggleManual1(self):
        self.ui.slider_Y.setVisible (True)  
        if self.ui.slider_X.isVisible():
        #if self.ui.buttonManual.text == "Manual":
            self.ui.slider_X.setVisible (True)
            self.ui.slider_Y.setVisible (True)
            self.ui.buttonStep.setVisible (True)
            self.ui.buttonZ.setVisible (True)
            self.ui.buttonDrill.setVisible (True)
            self.ui.buttonManual.setText ("Auto")
        else:
            self.ui.buttonManual.setText ("Manual")
            self.ui.slider_X.setVisible (False)
            self.ui.slider_Y.setVisible (False)
            self.ui.buttonStep.setVisible (False)
            self.ui.buttonZ.setVisible (False)
            self.ui.buttonDrill.setVisible (False)

    def toggleInOutFrame(self):
        if self.ui.frameInOut.isVisible():
            self.ui.frameInOut.setVisible (False)
        else:
            self.ui.frameInOut.setVisible (True)

    def toggleDataFrame(self):
        if self.ui.frameCounter.isVisible():
            self.ui.frameCounter.setVisible (False)
        else:
            self.ui.frameCounter.setVisible (True)

    def updateDateTime(self):
        now = datetime.now()
        date = now.strftime("%d of %B, %Y")
        currentTime = now.strftime("%H:%M:%S")
        self.ui.lb_Date.setText(date)
        self.ui.lb_time.setText(currentTime)


    def updateState(self):
        '''Read State from PLC'''
        com1.readOneMemory(18)
        numberState = com1.receivedOneMemory()
        switcher= {
            0:'NA',
            1:'Initializing',
            2:'Waiting',
            3:'Automatic',
            4:'Manual'

        }
        self.ui.lb_state.setText (switcher.get(numberState, "Invalid"))

    def updateProgram(self):
        com1.readOneMemory()
        numberProgram = com1.receivedOneMemory()
        self.ui.lb_program.setText (str(numberProgram))

    def updatePositions(self):
        com1.readTwoMemory(14)
        position = com1.receivedTwoMemory()
        self.ui.lb_X.setText(str(position[0]))
        self.ui.lb_Y.setText(str(position[1]))

"""Thread definition"""
def updateQt(i,w):
    w.updateDateTime()
    #w.updateState()
    #w.updatePositions()
    global t
    t = threading.Timer(1.0, updateQt, args=(i,w,))
    t.start()




def testThread():
    print("hello. Timer")
    global t
    t = threading.Timer(1.0, testThread)
    t.start()

def loop_a():
    app = QApplication(sys.argv)
    global com1
    com1=com()
    w = AppWindow()
    w.show()
    updateQt(1,w)
    sys.exit(app.exec_())


"""________Code Start_________"""
com1 = None
t=None
if __name__=="__main__":

    Process(target=loop_a).start()



