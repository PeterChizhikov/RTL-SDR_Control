import json

class SDRConfiguration:
    def load_settings(json_data):
        data = json.loads(json_data)
        keys_to_check = ['sample_rate', 'center_frequency', 'frequency_correction']
        all_keys_exist = all(key in data for key in keys_to_check)
        if all_keys_exist:
            return SDRConfiguration(
                sample_rate=data.get('sample_rate',2.048e6),
                center_freq=data.get('center_freq',None),
                freq_correction=data.get('freq_correction',60),
                gain=data.get('gain', 'auto'),
                read_samples = data.get('read_samples',1024)
            )
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

    def from_json(json_message):    
        try:
            message = json.loads(json_message)
            if message['type'] == 'system':
                if message['action'] == 'start':
                    if start_receiver():
                        return json.dumps({"answer": 200})
                    else:
                        return json.dumps({"answer": 423})
                elif message['action'] == 'stop':
                    if stop_receiver():
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
