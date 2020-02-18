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


''' COmunication class '''
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

            footer = b'\x00\x00\x01'#\x80\x00\x01\x00\x01\x00\x00\x20\x00\x00\x01\x02\x82\x00\x6e\x00\x00\x01'
            print(memmory.to_bytes(2,'big'))
            sendMessage = header + memmory.to_bytes(1,'big') + footer + message.to_bytes(2,'big')
            print("Sendmessage")
            print(sendMessage)
            self.sock.sendto(sendMessage, (UDP_IP, UDP_PORT))
            self.receivedOneMemory()
        except self.sock.error:
            print('Unable to send message')

    def writeBit(self,memmory, bit, state):
        self.readOneMemory(memmory)
        data = self.receivedOneMemory()
        print("fefefe")
        print (data)

        masc= 1
        masc = masc << bit
        if (state == True):
            sendData = data | masc
        else:
            sendData = data & (~masc)
        self.writeMessage(memmory,sendData)


    # Read message on PLC
    def readOneMemory(self,memory):
        messageHeader = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0B\x01\x01\x82\x00'
        messageFooter = b'\x00\x00\x01'

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

    def readCounterMemory(self,memory):
        messageHeader = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0B\x01\x01\x82\x00'
        messageFooter = b'\x00\x00\x0A'
        nextMemory = memory + 1
        sendMessage = messageHeader + memory.to_bytes(1, 'big') + messageFooter

        print ("sefC")
        self.sock.sendto(sendMessage, (UDP_IP, UDP_PORT))

    def decodeBytes(self,bts):
        val = b'\x00' + bts[-2:]
        print("decoding")
        print(val)
        # print(int.from_bytes(val, byteorder='big', signed=True))
        #
        return int.from_bytes(val, byteorder='big', signed=True)

    def decodeTwoBytes(self,bts):
        val = b'\x00' + bts[-2:]
        val1 = b'\x00' + bts[-4:-2]
        print(val)
        # print(int.from_bytes(val, byteorder='big', signed=True))
        #
        return (int.from_bytes(val1, byteorder='big', signed=True),int.from_bytes(val, byteorder='big', signed=True))

    def decodeTenBytes(self,bts):
        val = [b'\x00' + bts[-2:],
        b'\x00' + bts[-4:-2],
        b'\x00' + bts[-6:-4],
        b'\x00' + bts[-8:-6],
        b'\x00' + bts[-10:-8],
        b'\x00' + bts[-12:-10],
        b'\x00' + bts[-14:-12],
        b'\x00' + bts[-16:-14],
        b'\x00' + bts[-18:-16],
        b'\x00' + bts[-20:-18]
        ]
        #print(val)
        # print(int.from_bytes(val, byteorder='big', signed=True))
        #
        values = list()
        for i in reversed(range(10)):
            values.append(int.from_bytes(val[i], byteorder='big'))
        return values


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


    def receivedCounterMemory(self):
        defi = int(0)
        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        print(data[9:10])
        if data[9:10] == b'\x0B':  # preciso ver o codigo
             #     # response from read
            defi = self.decodeTenBytes(data)

            #print(defi)
            return defi
        elif data[9:10] == b'\x0A':  # preciso ver o codigo
            # response from write
            return -1


'''GUI class'''
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
        self.ui.buttonManual.clicked.connect(self.openLoginPage)
        self.ui.buttonTeach.clicked.connect(self.teachButtonClicked)
        self.ui.buttonNextDrill.clicked.connect(self.nextDrillButtonClicked)
        self.ui.buttonZ.clicked.connect(self.buttonZClicked)
        self.ui.buttonStep.clicked.connect(self.stepButtonClick)
        self.ui.buttonCartesianEnable.clicked.connect(self.cartEnableButtonClick)
        self.ui.slider_X.valueChanged.connect(self.sliderXChanged)
        self.ui.slider_Y.valueChanged.connect(self.sliderYChanged)
        self.ui.buttonWarningClose.clicked.connect(self.warningButtonClick)
        self.ui.buttonLogin.clicked.connect(self.checkLogin)

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
        self.ui.warningFrame.setVisible (False)
        self.ui.loginFrame.setVisible (False)

    def openLoginPage(self):
        self.ui.label_5.setText("Insert PIN:")
        if self.ui.buttonManual.isChecked():
            if self.ui.buttonManual.text() == "Manual":
                self.ui.loginFrame.setVisible(True)
            else:
                print("ENDMODE")
                com1.writeBit(20,7,True)

        else:
            self.ui.loginFrame.setVisible(False)

    def checkLogin(self):
        if self.ui.lineEdit.text() == "1111":
            com1.writeBit(20,12,True)
            self.ui.loginFrame.setVisible(False)
            self.ui.buttonManual.toggle()
        else:
            self.ui.label_5.setText ("Try again")


    def teachButtonClicked(self):

        #print("teach button CLick")
        com1.writeBit(23, 1, True)
        com1.writeBit(23, 1, False)

    def nextDrillButtonClicked(self):
        com1.readOneMemory(96)
        numberDrill = com1.receivedOneMemory()
        numberDrill+=1
        com1.writeMessage(96, numberDrill)


    def endTeachButton(self):
        # print("end teach button CLick")
        com1.writeBit(23, 2, True)
        com1.writeBit(23, 2, False)

    def buttonZClicked(self):
        if (self.ui.buttonZ.isChecked()):
            #print("Zon")
            com1.writeBit(22, 4, True)
        else:
            #print("Zoff")
            com1.writeBit(22, 4, False)

    def buttonDrillClicked(self):
        if (self.ui.buttonZ.isChecked()):
            #print("Zon")
            com1.writeBit(22, 5, True)
        else:
            #print("Zoff")
            com1.writeBit(22, 5, False)

    def sliderXChanged(self):
        com1.writeMessage(10, int(self.ui.slider_X.value()))
        #print(int(self.ui.slider_X.value()))

    def sliderYChanged(self):
        com1.writeMessage(11, int(self.ui.slider_Y.value()))
        #print(int(self.ui.slider_Y.value()))

    def toggleManual(self, value):
        if value == True:
        #if self.ui.buttonManual.text() == "Manual":
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

    def stepButtonClick(self):
        com1.writeBit(22, 7, True)
        com1.writeBit(22, 7, False)

    def cartEnableButtonClick(self):
        if (self.ui.buttonCartesianEnable.isChecked()):
            #print("Cartisian enable click")
            com1.writeBit(22, 6, True)
            self.ui.buttonCartesianEnable.setText("Cartesian Disable")
        else:
            #print("Cartiesian disable click")
             com1.writeBit(22, 6, False)
             self.ui.buttonCartesianEnable.setText("Cartesian Enable")

    def warningButtonClick(self):
        self.ui.warningFrame.setVisible(False)

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
        com1.readOneMemory(16)
        numberProgram = com1.receivedOneMemory()
        self.ui.lb_program.setText (str(numberProgram))

    def updatePositions(self):
        com1.readTwoMemory(10)
        nextPosition = com1.receivedTwoMemory()

        '''Adjust coordinates to image'''

        px=nextPosition[0]*310/100
        py=nextPosition[1]*310/100
        self.ui.main_cross.move(px+40,py+80)
        com1.readTwoMemory(14)
        actualPosition = com1.receivedTwoMemory()
        apx = actualPosition[0] * 310 / 100
        apy = actualPosition[1] * 310 / 100
        self.ui.main_circle.move(apx + 40, apy + 80)

        if self.ui.buttonManual.text() == "Manual":
            self.ui.lb_X.setText(str(actualPosition[0]))
            self.ui.lb_Y.setText(str(actualPosition[1]))
        elif self.ui.buttonManual.text() == "Auto":
            self.ui.lb_X.setText(str(nextPosition[0]))
            self.ui.lb_Y.setText(str(nextPosition[1]))



        '''update cilinder z state'''


        com1.readOneMemory(25)
        zState = com1.receivedOneMemory()

        if zState == 0 :
            pixmap = QPixmap('Images\circle_lGreen.png')
            self.ui.main_circle.setPixmap(pixmap)
        if zState == 1 :
            pixmap = QPixmap('Images\circle_Yellow.png')
            self.ui.main_circle.setPixmap(pixmap)
        if zState == 2 :
            pixmap = QPixmap('Images\circle_Red.png')
            self.ui.main_circle.setPixmap(pixmap)

    def updateCounters(self):
        com1.readCounterMemory(51)
        counters = com1.receivedCounterMemory()
        self.ui.lb_Counter1.setText(str(counters[0]))
        self.ui.lb_Counter2.setText(str(counters[1]))
        self.ui.lb_Counter3.setText(str(counters[2]))
        self.ui.lb_Counter4.setText(str(counters[3]))
        self.ui.lb_Counter5.setText(str(counters[4]))
        self.ui.lb_Counter6.setText(str(counters[5]))
        self.ui.lb_Counter7.setText(str(counters[6]))
        self.ui.lb_Counter8.setText(str(counters[7]))
        self.ui.lb_Counter9.setText(str(counters[8]))
        self.ui.lb_Counter10.setText(str(counters[9]))

    def updateInOut(self):
        com1.readTwoMemory(10)
        inOutData = com1.receivedTwoMemory()


        '''Update Inputs'''
        for i in range(9):
            aux=1

            bit =  inOutData[0] & (aux<<i)
            label = "lb_inp" + str(i)
            print(label)
            if bit > 0:
                pixmap = QPixmap('Images\circle_lGreen.png')
                getattr(self.ui,label).setPixmap(pixmap)
            else:
                pixmap = QPixmap('Images\circle_dGreen.png')
                getattr(self.ui, label).setPixmap(pixmap)

        '''Update Outputs'''
        for i in range(7):
            aux=1

            bit =  inOutData[1] & (aux<<i)
            label = "lb_out" + str(i)
            print(label)
            if bit > 0:
                pixmap = QPixmap('Images\circle_lGreen.png')
                getattr(self.ui,label).setPixmap(pixmap)
            else:
                pixmap = QPixmap('Images\circle_dGreen.png')
                getattr(self.ui, label).setPixmap(pixmap)

    def updateWarning(self):
        com1.readOneMemory(20)
        warning = com1.receivedOneMemory()
        aux=1
        bit = warning & (aux << 9)
        if bit >0:
            self.ui.warningFrame.setVisible(True)


    def updateDrillNumber(self):
        com1.readOneMemory(96)
        numberDrill = com1.receivedOneMemory()
        self.ui.lb_drillNumber.setText(str(numberDrill))


    def updateManualPage(self):
        com1.readOneMemory(20)
        auxData = com1.receivedOneMemory()
        # auxData = 32768
        # auxData = 0
        aux=1
        aux = aux << 15
        if (aux & auxData) > 0:
            self.toggleManual(1)
        else:
            self.toggleManual(0)



"""Thread definition"""
def updateQt(i,w):
    # w.updateDateTime()
    # w.updateProgram()
    # w.updateState()
    # w.updatePositions()
    # w.updateCounters()
    # w.updateInOut()
    # w.updateDrillNumber()
    #
    # w.updateWarning()

    # w.updateManualPage()

    global t
    t = threading.Timer(1.0, updateQt, args=(i,w,))
    t.start()


def loop_a():
    app = QApplication(sys.argv)
    global com1
    com1 = com()
    w = AppWindow()
    w.show()
    updateQt(1,w)
    sys.exit(app.exec_())


"""________Code Start_________"""
com1 = None
t=None
if __name__=="__main__":

    Process(target=loop_a).start()



