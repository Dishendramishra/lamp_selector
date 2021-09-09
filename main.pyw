from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
from qt_material import apply_stylesheet
import traceback, sys
import serial
import serial.tools.list_ports

if sys.platform == "linux" or sys.platform == "linux2":
    pass

elif sys.platform == "win32":
    import ctypes
    myappid = u'prl.microk'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

elif sys.platform == "darwin":
    pass

class WorkerSignals(QObject):
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)
    result = pyqtSignal(object)
    finished = pyqtSignal()
    
class Worker(QRunnable):

    def __init__(self, fn, signals_flag, *args, **kwargs):
        # signals_flag = [progress, result, finished]

        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs    
        self.signals = WorkerSignals()
        self.signals_flag = signals_flag

        if self.signals_flag[0]:
            kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if self.signals_flag[1]:
                self.signals.result.emit(result) # Return the result of the processing
        finally:
            if self.signals_flag[2]:
                self.signals.finished.emit() # Done

class Ui(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(Ui, self).__init__(*args, **kwargs)

        uic.loadUi('gui.ui', self)
        self.setWindowTitle("Lamp Controller")

        # self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.ser = None
        self.img_uar = "resources/icons/off.png"
        self.img_tung = "resources/icons/off.png"
        self.img_fabry  = "resources/icons/off.png"
        self.connect_ser()
        self.ui_settings()
        self.show()

    def ui_settings(self):
        
        self.btn_uar.clicked.connect(self.go_home)
        self.btn_tung.clicked.connect(self.place_tung)
        self.btn_fabry.clicked.connect(self.place_fabry)

        self.lbl_uar.setPixmap(QPixmap(self.img_uar).scaled(32,32))
        self.lbl_tung.setPixmap(QPixmap(self.img_tung).scaled(32,32))
        self.lbl_fabry.setPixmap(QPixmap(self.img_uar).scaled(32,32))
        

    def connect_ser(self):
        ports = serial.tools.list_ports.comports()
        target_port = None
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            if "PID=2341:0043" in hwid:
                # print(port)
                target_port = port

        self.ser = serial.Serial(target_port, 9600)


    def go_home(self):
        self.ser.write("home".encode())
        output = self.ser.readline().strip().decode()

        if output == "done":
            if self.img_uar == "resources/icons/off.png":
                self.img_uar = "resources/icons/on.png"
                self.lbl_uar.setPixmap(QPixmap(self.img_uar).scaled(32,32))
                
            else:
                self.img_uar = "resources/icons/off.png"
                self.lbl_uar.setPixmap(QPixmap(self.img_uar).scaled(32,32))
        else:
            print("error")

    def place_tung(self):
        self.ser.write("ma19000".encode())
        output = self.ser.readline().strip().decode()

        if output == "done":
            if self.img_tung == "resources/icons/off.png":
                self.img_tung = "resources/icons/on.png"
                self.lbl_tung.setPixmap(QPixmap(self.img_tung).scaled(32,32))
                
            else:
                self.img_tung = "resources/icons/off.png"
                self.lbl_tung.setPixmap(QPixmap(self.img_tung).scaled(32,32))
                
        else:
            print("error")

    def place_fabry(self):
        self.ser.write("ma38000".encode())
        output = self.ser.readline().strip().decode()

        if output == "done":
            if self.img_fabry == "resources/icons/off.png":
                self.img_fabry = "resources/icons/on.png"
                self.lbl_fabry.setPixmap(QPixmap(self.img_fabry).scaled(32,32))
                
            else:
                self.img_fabry = "resources/icons/off.png"
                self.lbl_fabry.setPixmap(QPixmap(self.img_fabry).scaled(32,32))
                
        else:
            print("error")



app = QApplication(sys.argv)
app.setWindowIcon(QIcon("resources/icons/prl.png"))
apply_stylesheet(app, theme='dark_blue.xml')
window = Ui()
app.exec_()