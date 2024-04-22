from rtlsdr import RtlSdr
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from threading import Thread, Lock
import numpy as np
from Structures import SDRData


class DeviceController(Thread, QObject):
    samplesArr = []
    def __init__(self, sampleRate, centerFreq, freq_correction,
                 gain,read_samples):
        Thread.__init__(self)
        QObject.__init__(self)
        self.sdr = RtlSdr()
        self.daemon = True
        self.sdr.sample_rate = sampleRate
        self.sdr.center_freq = centerFreq
        self.sdr.freq_correction = freq_correction 
        self.sdr.gain = gain
        self.read_samples_num = read_samples
        self.read_device_data_status = False
        self.mutex = Lock()

    saveToQueueSignal = pyqtSignal(SDRData.SDRData)


    def startReadDeviceDataSlot(self):
        with self.mutex:
            self.read_device_data_status = True
            self.readDeviceData()


    def stopReadDeviceDataSlot(self):
        with self.mutex:
            self.read_device_data_status = False


    def readDeviceData(self):
        while self.read_device_data_status:
            self.samplesArr = self.sdr.read_samples(self.read_samples_num)
            self.processSamples(self.samplesArr)
            print("self.samplesArr")
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

        data = SDRData.SDRData(f,PSD_shifted,minF,maxF)

        self.saveToQueueSignal.emit(data)

    def __del__(self):
        if self.sdr:
            self.sdr.close()

 