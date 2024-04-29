from MainProcessor import MainProcessor
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt,QEventLoop,QThread
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainProc = MainProcessor()   


