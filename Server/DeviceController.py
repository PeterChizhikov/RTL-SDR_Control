from rtlsdr import RtlSdr

class DeviceController():
    samplesArr = []
    def __init__(self, sampleRate, centerFreq, freq_correction,
                 gain,read_samples):
        
        
        self.sdr = RtlSdr()
        self.sdr.sample_rate = sampleRate
        self.sdr.center_freq = centerFreq
        self.sdr.freq_correction = freq_correction 
        self.sdr.gain = gain
        self.read_samples_num = read_samples

    def readDeviceData(self):
        self.samplesArr = self.sdr.read_samples(self.read_samples_num)
        return self.samplesArr
        

    def __del__(self):
        self.sdr.close()

 