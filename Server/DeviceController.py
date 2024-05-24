from rtlsdr import RtlSdr
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal,QThread
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal,QThread
from threading import Thread, Lock
import numpy as np
from Structures import SDRData
import time
from Structures import SDRConfiguration

class DeviceController(QThread, QObject):
    samplesArr = []
    def __init__(self, sampleRate, centerFreq, freq_correction,
                 gain,read_samples):
        QThread.__init__(self)
        QObject.__init__(self)
        try:
            self.sdr = RtlSdr()
        except IOError as e:
            print(e)
        else:
            self.sdr.sample_rate = sampleRate
            self.sdr.center_freq = centerFreq
            self.sdr.freq_correction = freq_correction 
            self.sdr.gain = gain
            self.read_samples_num = read_samples
        self.read_device_data_status = False
        self.mutex = Lock()
        self.daemon = True
        self.unMutex = Lock()
        self.workerMut = Lock()

    saveToQueueSignal = pyqtSignal(SDRData.SDRData)
    setSettingsResponseSignal = pyqtSignal(int)
    startAndStopReadDataFromDeviceResponseSignal = pyqtSignal(int)
    

    def startReadDeviceDataSlot(self):
        with self.mutex:
            self.read_device_data_status = True
        self.readDeviceData()

    def run(self):
        while not self.read_device_data_status:
            time.sleep(0.5)

    def setNewSettingsSlot(self, settingsList):
        try:
            self.sdr.set_sample_rate(settingsList[0])
            self.sdr.set_center_freq(settingsList[1])
            self.sdr.set_freq_correction(settingsList[2])
            self.sdr.set_gain(settingsList[3])
            
        except Exception as exptText:
            print(type(exptText))
            print(exptText)
            
            self.setSettingsResponseSignal.emit(409)
        else:
            self.setSettingsResponseSignal.emit(200)

    def stopReadDeviceDataSlot(self):
        with self.mutex:
            self.read_device_data_status = False
        self.startAndStopReadDataFromDeviceResponseSignal.emit(200)    

    def readDeviceData(self):
        try:
            self.samplesArr = self.sdr.read_samples(self.read_samples_num)
        except Exception:
            self.startAndStopReadDataFromDeviceResponseSignal.emit(423)
        else:
            self.startAndStopReadDataFromDeviceResponseSignal.emit(200)

        threadloop = Thread(target=self.readDataloop)
        threadloop.start()
        

    def readDataloop(self):
        while self.read_device_data_status:
            self.samplesArr = self.sdr.read_samples(self.read_samples_num)   
            self.processSamples(self.samplesArr)



    def processSamples(self, IQSamples):
            # cF = 60e6
            # N = 256*1024
        Fs = self.sdr.sample_rate
        PSD = np.abs(np.fft.fft(IQSamples))**2/(self.read_samples_num*Fs)
        PSD_log = 10.0*np.log10(PSD, where=PSD>0)
            #y:
        PSD_shifted = np.fft.fftshift(PSD_log)
            #x:
        f = np.arange(Fs/-2.0, Fs/2.0, Fs/self.read_samples_num) # start, stop, step
        f += self.sdr.center_freq
            #min
        minF = min(f)
            #max
        maxF = max(f)

        minY = min(PSD_shifted)
        maxY = max(PSD_shifted)


        # i = 0
        # while i < len(PSD_shifted):
        #     if PSD_shifted[i] < -110 or PSD_shifted[i] > 110:
        #         np.delete(PSD_shifted, i)
        #         np.delete(f, i)
        #         i = i +1

        data = SDRData.SDRData(f,PSD_shifted,minF,maxF, minY, maxY)

        self.saveToQueueSignal.emit(data)

    def __del__(self):
        if self.sdr:
            self.sdr.close()

 