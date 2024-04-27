import json

class SDRConfiguration:
    def __init__(self, sample_rate=None, center_freq=None, freq_correction=None, gain=None, read_samples = None):
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.freq_correction = freq_correction
        self.gain = gain
        self.read_samples = read_samples

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        return SDRConfiguration(
            sample_rate=data.get('sample_rate',2.048e6,),
            center_freq=data.get('center_freq',None),
            freq_correction=data.get('freq_correction',60),
            gain=data.get('gain', 'auto'),
            read_samples = data.get('read_samples',1024)
        )
