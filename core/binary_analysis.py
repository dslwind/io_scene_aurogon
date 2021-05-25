import os

import numpy as np


class Analy():
    def __init__(self, variable=1, little=True):
        self.__little = little
        if type(variable) == str:
            self.uint8list = np.fromfile(variable,
                                         dtype=np.uint8)  # numpy1.17版本新增功能
        elif type(variable) == bytes:
            self.uint8list = np.fromfile(variable, dtype=np.uint8)
        elif type(variable) == np.ndarray and variable.dtype == np.uint8:
            self.uint8list = variable
        elif type(variable) == list or type(variable) == tuple:
            self.uint8list = np.asarray(variable, dtype=np.uint8)
        else:
            print(
                "Union[str , bytes , numpy.ndarray(dtype=numpy.uint8) , list[->numpy.ndarray(dtype=numpy.uint8)]."
            )
            传入的类型 = type(variable)
            # python3.8才支持字符串f增强，blender28目前是python3.7
            print("Binary Analysis Error：传入的类型({传入的类型=})未支持!")

        if little:
            self.endian = "<"
        else:
            self.endian = ">"
        self._currut = 0
        self._size = len(self.uint8list)
        self.__fmt_step = {
            "b": 1,
            "B": 1,
            "h": 2,
            "H": 2,
            "i": 4,
            "I": 4,
            "q": 8,
            "Q": 8,
            "f2": 2,
            "f4": 4,
            "f8": 8,
            "F4": 8,
            "F8": 16,
            "a": 1,
            "U": 2,
        }
        self.__equalfunc()

    def check(self, num, fmt=""):
        nums = num * self.__fmt_step[fmt]
        if nums > self._size - self._currut:
            print("Binary Analysis Error：读取{num=}个元素所需的字节超出范围!")
            return False
        else:
            return True

    def size(self):
        return self._size

    def EOF(self):
        if self._currut < self.size() - 1:
            return False
        elif self._currut == self.size() - 1:
            return True
        else:
            print("Binary Analysis Error：光标{self._currut=}的指向超出范围!")

    def tell(self):
        return self._currut

    def seek(self, offset, flag=0):
        if flag == 0:
            self._currut = offset
        elif flag == 1:
            self._currut += offset
        elif flag == 2:
            self._currut = self._size - self._currut
        else:
            print("Binary Analysis Error：设置光标，未支持的{flag=}!")

    def remain(self):
        return self._size - self._currut

    def readremain(self):
        uint8list = self.uint8list[self._currut:]
        return uint8list

    def readremainlist(self):
        uint8list = self.uint8list[self._currut:]
        return list(uint8list)

    def remainlist(self):
        uint8list = self.uint8list[self._currut:]
        return list(uint8list)

    def read(self, num):
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        return uint8list

    def readslice(self, num):
        """返回1个Analy类的类似列表切片的实例对象，请注意命名区分。"""
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        instance = Analy(uint8list, self.__little)
        return instance

    def readfmt(self, var):
        if type(var) == int:
            uint8list = self.uint8list[self._currut:self._currut + var]
            self._currut += var
            return uint8list
        elif type(var) == str:
            pass
        else:
            格式 = type(var)
            print("Binary Analysis Error：传入的变量{var=}其{格式=}读取未支持!")

    def readslice(self, num):
        """返回1个Analy类的类似列表切片的实例对象，请注意命名区分。"""
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        instance = Analy(uint8list, self.__little)
        return instance

    def readlist(self, num):
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        return list(uint8list)

    def readall(self):
        self._currut = self._size
        return self.uint8list

    def readalllist(self):
        self._currut = self._size
        return list(self.uint8list)

    def readuint8s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        return list(uint8list)

    def readuint8(self):
        uint8list = self.uint8list[self._currut:self._currut + 1]
        self._currut += 1
        return list(uint8list)[0]

    def readint8s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        return list(np.frombuffer(uint8list, dtype=self.endian + "b"))

    def readint8(self):
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += 1
        return list(np.frombuffer(uint8list, dtype=self.endian + "b"))[0]

    def readuint16s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 2 * num]
        self._currut += 2 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "H"))

    def readuint16(self):
        uint8list = self.uint8list[self._currut:self._currut + 2]
        self._currut += 2
        return list(np.frombuffer(uint8list, dtype=self.endian + "H"))[0]

    def readint16s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 2 * num]
        self._currut += 2 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "h"))

    def readint16(self):
        uint8list = self.uint8list[self._currut:self._currut + 2]
        self._currut += 2
        return list(np.frombuffer(uint8list, dtype=self.endian + "h"))[0]

    def readuint32s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 4 * num]
        self._currut += 4 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "I"))

    def readuint32(self):
        uint8list = self.uint8list[self._currut:self._currut + 4]
        self._currut += 4
        return list(np.frombuffer(uint8list, dtype=self.endian + "I"))[0]

    def readint32s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 4 * num]
        self._currut += 4 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "i"))

    def readint32(self):
        uint8list = self.uint8list[self._currut:self._currut + 4]
        self._currut += 4
        return list(np.frombuffer(uint8list, dtype=self.endian + "i"))[0]

    def readuint64s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 8 * num]
        self._currut += 8 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "Q"))

    def readuint64(self):
        uint8list = self.uint8list[self._currut:self._currut + 8]
        self._currut += 8
        return list(np.frombuffer(uint8list, dtype=self.endian + "Q"))[0]

    def readint64s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 8 * num]
        self._currut += 8 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "q"))

    def readint64(self):
        uint8list = self.uint8list[self._currut:self._currut + 8]
        self._currut += 8
        return list(np.frombuffer(uint8list, dtype=self.endian + "q"))[0]

    def readfloat16s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 2 * num]
        self._currut += 2 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "f2"))

    def readfloat16(self):
        uint8list = self.uint8list[self._currut:self._currut + 2]
        self._currut += 2
        return list(np.frombuffer(uint8list, dtype=self.endian + "f2"))[0]

    def readfloat32s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 4 * num]
        self._currut += 4 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "f4"))

    def readfloat32(self):
        uint8list = self.uint8list[self._currut:self._currut + 4]
        self._currut += 4
        return list(np.frombuffer(uint8list, dtype=self.endian + "f4"))[0]

    def readfloat64s(self, num):
        uint8list = self.uint8list[self._currut:self._currut + 8 * num]
        self._currut += 8 * num
        return list(np.frombuffer(uint8list, dtype=self.endian + "f8"))

    def readfloat64(self):
        uint8list = self.uint8list[self._currut:self._currut + 8]
        self._currut += 8
        return list(np.frombuffer(uint8list, dtype=self.endian + "f8"))[0]

    def readstr(self, num):
        if num <= 0:
            return ""
        uint8list = self.uint8list[self._currut:self._currut + num]
        self._currut += num
        chars = np.frombuffer(uint8list, dtype=self.endian + "a" + str(num))[0]
        return chars.decode()

    def __equalfunc(self):
        self.readushorts = self.readuint16s
        self.readushort = self.readuint16
        self.readUshorts = self.readuint16s
        self.readUshort = self.readuint16

        self.readshorts = self.readint16s
        self.readshort = self.readint16
        self.readShorts = self.readint16s
        self.readShort = self.readint16

        self.readuints = self.readuint32s
        self.readuint = self.readuint32
        self.readUints = self.readuint32s
        self.readUint = self.readuint32

        self.readints = self.readint32s
        self.readint = self.readint32
        self.readInts = self.readint32s
        self.readInt = self.readint32

        self.readulongs = self.readuint64s
        self.readulong = self.readuint64
        self.readUlongs = self.readuint64s
        self.readUlong = self.readuint64

        self.readlongs = self.readint64s
        self.readlong = self.readint64
        self.readLongs = self.readint64s
        self.readLong = self.readint64

        self.readfloats = self.readfloat32s
        self.readfloat = self.readfloat32
        self.readFloats = self.readfloat32s
        self.readFloat = self.readfloat32

        self.readdoubles = self.readfloat64s
        self.readdouble = self.readfloat64
        self.readDoubles = self.readfloat64s
        self.readDouble = self.readfloat64

        self.readchr = self.readstr
        self.readchar = self.readstr

    def find_textures_folder(self, file_path):
        cwd_dir = os.path.dirname(file_path)
        all_file_name_list = os.listdir(cwd_dir)
        if "Textures" in all_file_name_list:  # 古剑2,古剑3
            textures_folder = cwd_dir + "\\" + "Textures"
        elif "textures" in all_file_name_list:
            textures_folder = cwd_dir + "\\" + "textures"
        else:
            cwd_dir = os.path.dirname(cwd_dir)
            all_file_name_list = os.listdir(cwd_dir)
            if "textures" in all_file_name_list:  # 古剑3
                textures_folder = cwd_dir + "\\" + "textures"
            elif "texture" in all_file_name_list:  # 古剑1
                textures_folder = cwd_dir + "\\" + "texture"
            else:
                textures_folder = ""
        return textures_folder


# 约定，读取个数的出错判断在上层，不在本文件。后续看情况再调整。
