import sys
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import *
from mainUi import Ui_Frame
import cv2
import socket
import  time
from timeloop import Timeloop
from datetime import timedelta
from datetime import datetime
import signal
t2 = Timeloop()
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

        #openSocket()

    #def openSocket():


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
        except self.sock.error:
            print('Unable to send message')

    # Read message on PLC
    def readMessage(self,memory):
        messageHeader = b'\x80\x00\x01\x00\x01\x00\x00\x20\x00\x0B\x01\x01\x82\x00'
        messageFooter = b'\x00\x00\x01'
        sendMessage = messageHeader + memory.to_bytes(1, 'big') + messageFooter

        print ("sefC")
        self.sock.sendto(sendMessage, (UDP_IP, UDP_PORT))

    def decodeBytes(self,bts):
        val = b'\x00' + bts[-2:]
        # print(val)
        # print(int.from_bytes(val, byteorder='big', signed=True))
        #
        return int.from_bytes(val, byteorder='big', signed=True)

    def received(self):
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
        com1.readMessage(100)
        com1.received()
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


    def updateImg(self):
        #self.ui.Img_label.setPixmap(QPixmap("pNewProd.bmp"))
        #self.ui.pushButton_5.setVisible(False)


        '''
    def updateImgPro(self):
        self.ui.lb_img_pro.setPixmap(QPixmap("frame_pro.jpg"))

    def updateMedidas(self, m1, m2, m3):
        self.ui.lb_m1.setText(str(m1) + " mm")
        self.ui.lb_m2.setText(str(m2) + " mm")
        self.ui.lb_m3.setText(str(m3) + " mm")

    def updateMedidasPlc(self, m1_G1, m2_G1, m3_G1,
                                    m1_G2, m2_G2, m3_G2,
                                    m1_G3, m2_G3, m3_G3,
                                    m1_G4, m2_G4, m3_G4,
                                    m1_G5, m2_G5, m3_G5):
        self.ui.lb_m1_G1.setText(str(m1_G1 / 100) + " mm")
        self.ui.lb_m2_G1.setText(str(m2_G1 / 100) + " mm")
        self.ui.lb_m3_G1.setText(str(m3_G1 / 100) + " mm")
        self.ui.lb_m1_G2.setText(str(m1_G2 / 100) + " mm")
        self.ui.lb_m2_G2.setText(str(m2_G2 / 100) + " mm")
        self.ui.lb_m3_G2.setText(str(m3_G2 / 100) + " mm")
        self.ui.lb_m1_G3.setText(str(m1_G3 / 100) + " mm")
        self.ui.lb_m2_G3.setText(str(m2_G3 / 100) + " mm")
        self.ui.lb_m3_G3.setText(str(m3_G3 / 100) + " mm")
        self.ui.lb_m1_G4.setText(str(m1_G4 / 100) + " mm")
        self.ui.lb_m2_G4.setText(str(m2_G4 / 100) + " mm")
        self.ui.lb_m3_G4.setText(str(m3_G4 / 100) + " mm")
        self.ui.lb_m1_G5.setText(str(m1_G5 / 100) + " mm")
        self.ui.lb_m2_G5.setText(str(m2_G5 / 100) + " mm")
        self.ui.lb_m3_G5.setText(str(m3_G5 / 100) + " mm")

    def updateStatusPlc(self, group, status):
        self.ui.lb_plc_start.setText(status)
        self.ui.lb_plc_group.setText(group)

'''

"""Timer definition"""
@t2.job(interval=timedelta(seconds=1))
def updateQt(w):
    w.updateDateTime()
    #.updateImg()
    # Get and save frame
    #ret, frame = input.read()
    #cv2.imwrite("frame.jpg", frame)
    #cv2.imwrite("frame_pro.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    '''w.updateImg()
    w.updateImgPro()
    w.updateMedidas(1.43, 2.23, 3.11)
    w.updateStatusPlc("G1", "Stop")
    w.updateMedidasPlc(111,112,113,121,122,123,131,132,133,141,142,143,151,152,153)
    '''


def loop_a():
    app = QApplication(sys.argv)
    global com1
    com1=com()
    w = AppWindow()
    w.show()
    import sched, time
    s = sched.scheduler(time.time, time.sleep)
    #t2.start(block=True)
    updateQt(w)
    sys.exit(app.exec_())

def loop_b():
    while True:
        a =1#Image process


"""________Code Start_________"""
com1 = None
if __name__=="__main__":

    Process(target=loop_a).start()
    #Process(target=loop_b).start()



