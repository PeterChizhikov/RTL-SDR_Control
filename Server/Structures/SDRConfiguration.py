import json

class SDRConfiguration:
    def __init__(self):
        self.sample_rate = 2.048e6
        self.center_frequency = 60e6
        self.frequency_correction = 60
        self.gain  = 'auto'
        self.read_samples = 1024
        
    def load_settings(self,data):
        # data = json.loads(json_data)
        keys_to_check = ['sample_rate', 'center_frequency', 'frequency_correction']
        all_keys_exist = all(key in data for key in keys_to_check)
        if all_keys_exist:
            self.sample_rate=data.get('sample_rate'),
            self.center_frequency=data.get('center_freq'),
            self.frequency_correction=data.get('freq_correction'),
            self.gain=data.get('gain'),
            self.read_samples = data.get('reaаd_samples')
            return [self.sample_rate, 
            self.center_frequency, 
            self.frequency_correction, 
            self.gain, 
            self.read_samples]
            # return SDRConfiguration(
            #     sample_rate=data.get('sample_rate',2.048e6),
            #     center_freq=data.get('center_freq',None),
            #     freq_correction=data.get('freq_correction',60),
            #     gain=data.get('gain', 'auto'),
            #     read_samples = data.get('reaаd_samples',1024)
            # )
        else:
            raise ValueError("Ошибка настроек")

    def settings_handler(json_data):
        keys_to_check = ['sample_rate', 'center_frequency', 'frequency_correction']
        data = json.loads(json_data)
        all_keys_exist = all(key in data for key in keys_to_check)
        if all_keys_exist:
            return json.dumps({"answer": 200})
        else:
            return json.dumps({"answer": 409, "error": "Ошибка настроек"})


    def start_receiver(json):
        return True
        #добавить значения по умолчанию

    def stop_receiver(json):
        return True

    def from_json(message):    
        try:
            # message = json.loads(json_message)
            if message['type'] == 'system':
                if message['action'] == 'start':
                    if SDRConfiguration.start_receiver(json_message):
                        return json.dumps({"answer": 200})
                    else:
                        return json.dumps({"answer": 423})
                elif message['action'] == 'stop':
                    if SDRConfiguration.stop_receiver(json_message):
                        return json.dumps({"answer": 200})
                    else:
                        return json.dumps({"answer": 423})
                else:
                    return json.dumps({"answer": 400, "error": "Неизвестное действие"})
            elif message['type'] == 'settings':
                return SDRConfiguration.settings_handler(json_message)
            else:
                return json.dumps({"answer": 400, "error": "Неизвестный тип"})
        except json.JSONDecodeError:
            return json.dumps({"answer": 400, "error": "Недействительный JSON"})
        except KeyError:
            return json.dumps({"answer": 400, "error": "KeyError"})
