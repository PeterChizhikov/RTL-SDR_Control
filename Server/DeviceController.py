from rtlsdr import RtlSdr
from PySide6.QtCore import QObject, Signal, Slot
import time
from threading import Thread, Lock

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


    @Slot()
    def startReadDeviceDataSlot(self):
        with self.mutex:
            self.read_device_data_status = True

        readDeviceDataThread = Thread(target=self.readDeviceData)
        readDeviceDataThread.daemon = True
        readDeviceDataThread.start()



    @Slot()
    def stopReadDeviceDataSlot(self):
        with self.mutex:
            self.read_device_data_status = False


    def readDeviceData(self):
        while self.read_device_data_status:
            time.sleep(0.5)
            self.samplesArr = self.sdr.read_samples(self.read_samples_num)
            print("self.samplesArr")
        # return self.samplesArr


    def __del__(self):
        if self.sdr:
            self.sdr.close()

 