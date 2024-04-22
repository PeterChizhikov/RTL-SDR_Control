from rtlsdr import RtlSdr
from PySide6.QtCore import QObject, Signal, Slot
import time
from threading import Thread, Lock
import numpy as np
from queue import Queue
import struct
import zlib
import array


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

    class SDRData:
        def __init__(self,x,y,minf,maxf):
            self.coordinates = list(zip(x, y))
            self.minf = minf 
            self.maxf = maxf
        def getCoordinates(self):
            return self.coordinates
        def getMax(self):
            return self.maxf
        def getMin(self):
            return self.minf
        def pack(self):
            # Формат для структуры SDRData
            # '!': сетевой порядок байтов
            # 'I': беззнаковое целое число 4 байта
            # 'f': число с плавающей запятой 4 байта
            # 'i': целое число со знаком 4 байта
            # 'f': число с плавающей запятой 4 байта
            # 'i': целое число со знаком 4 байта
            # 'f': число с плавающей запятой 4 байта
            format_string = '!I{}f'.format(len(self.coordinates) * 2 + 2)

            # Упаковка координат в список
            coordinates_list = [item for sublist in self.coordinates for item in sublist]

            # # Проверка, что количество элементов в coordinates_list соответствует ожидаемому
            # expected_items = 1 + 2 * len(self.coordinates) + 2  # 1 для длины, 2 для minf и maxf
            # if len(coordinates_list+1) + 2 != expected_items:
            #     raise ValueError(f"Expected {expected_items} items for packing, got {len(coordinates_list) + 2}")

            # Упаковка всех значений в байтовый объект
            packed_data = struct.pack(format_string, len(self.coordinates)+ 2, *coordinates_list, self.minf, self.maxf)

            # Сжатие упакованных данныёх
            compressed_data = zlib.compress(packed_data)

            return compressed_data

        @staticmethod
        def unpack(compressed_data):
            # Распаковка сжатых данных
            unpacked_data = zlib.decompress(compressed_data)

            # Формат для распаковки
            format_string = '!I{}f'.format(int((len(unpacked_data) - 8) / 4))

            # Распаковка данных
            num_coordinates, *coordinates_list, minf, maxf = struct.unpack(format_string, unpacked_data)

            # Разделение координат
            coordinates = list(zip(coordinates_list[::2], coordinates_list[1::2]))

            # Создание нового экземпляра SDRData
            sdr_data = SDRData([], [], minf, maxf)
            sdr_data.coordinates = coordinates

            return sdr_data
            

    saveToQueueSignal = Signal(SDRData)


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
        
        # while True:
            # queue = Queue()
        data = self.SDRData(f,PSD_shifted,minF,maxF)

            # cordsToRecive = self.queue.put(data)

        self.saveToQueueSignal.emit(data)

    def __del__(self):
        if self.sdr:
            self.sdr.close()

 