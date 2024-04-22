import struct
import zlib
import array

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