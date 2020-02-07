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
import signal
t2 = Timeloop()
from multiprocessing import Process
'''pyuic5  init.ui > mainUi.py'''


class Timeout():
    """Timeout class using ALARM signal."""

    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)  # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        self.show()
        self.ui.pbNext.clicked.connect(self.getImageServer)

    def getImageServer(self):
        try:
            with Timeout(sec=1):
                input = cv2.VideoCapture("http://192.168.250.200:5000/video_feed")
                input.set(6, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                ret, frame = input.read()
                cv2.imwrite("frame.jpg", frame)
                cv2.imwrite("frame_pro.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
                self.ui.lb_Ping.setText("OK")
        except:
            self.ui.lb_Ping.setText("No Response")
            print("Can't connect to the server")


    def updateImg(self):
        self.ui.lb_imgCam.setPixmap(QPixmap("frame.jpg"))

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



"""Timer definition"""
@t2.job(interval=timedelta(seconds=1))
def updateQt(w):
    # Get and save frame
    #ret, frame = input.read()
    #cv2.imwrite("frame.jpg", frame)
    #cv2.imwrite("frame_pro.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    w.updateImg()
    w.updateImgPro()
    w.updateMedidas(1.43, 2.23, 3.11)
    w.updateStatusPlc("G1", "Stop")
    w.updateMedidasPlc(111,112,113,121,122,123,131,132,133,141,142,143,151,152,153)



def loop_a():
    app = QApplication(sys.argv)
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
if __name__=="__main__":
    Process(target=loop_a).start()
    Process(target=loop_b).start()


