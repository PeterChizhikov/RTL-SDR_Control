from rtlsdr import RtlSdr
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

    def startReadDeviceDataSlot(self):
        print("startReadDeviceDataSlot")
        with self.mutex:
            self.read_device_data_status = True



    def run(self):
        while not self.read_device_data_status:
            time.sleep(0.5)
            

    def stopReadDeviceDataSlot(self):
        print("stopReadDeviceDataSlot")
        with self.mutex:
            self.read_device_data_status = False


    def readDeviceData(self):
        while self.read_device_data_status:
            self.samplesArr = self.sdr.read_samples(self.read_samples_num)
            self.processSamples(self.samplesArr)
        # return self.samplesArr

    def processSamples(self, IQSamples):
            # cF = 60e6
            # N = 256*1024
        Fs = self.sdr.sample_rate / 1e6
        PSD = np.abs(np.fft.fft(IQSamples))**2/(self.read_samples_num*Fs)
        PSD_log = 10.0*np.log10(PSD)
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

        data = SDRData.SDRData(f,PSD_shifted,minF,maxF, minY, maxY)

        self.saveToQueueSignal.emit(data)

    def __del__(self):
        if self.sdr:
            self.sdr.close()

 