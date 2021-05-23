import os
import mathutils

from . import aurogon_type, binary_analysis


class 解析():

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__数据准备()  # 实例化烛龙类型，建立1套骨架等
        self.__数据读取()
        # self.__数据处理()

    def __数据准备(self):
        # 实例烛龙文件
        self.烛龙文件 = aurogon_type.烛龙文件()
        self.烛龙文件.动作文件.名称 = os.path.basename(self.__file_path)

    def __数据读取(self):
        bp = binary_analysis.Analy(self.__file_path)
        Header = bp.read(8)
        while True:
            if bp.remain() <= 4:
                break
            块标识, 块大小, 块计数 = bp.readuint32s(3)
            数据区 = bp.readslice(块大小)

            # 块标识==201: 文件信息
            # 块标识==202: 动作数据
            if 块标识 == 202:
                self.__骨骼动作(数据区)

    def __骨骼动作(self, bp):
        骨骼总数, 未知数 = bp.readuint16s(2)
        for i in range(骨骼总数):
            骨骼动作 = aurogon_type.烛龙骨骼动作()
            bp.seek(80, 1)
            位置num, 旋转num, un位置num, un旋转num = bp.readuint32s(4)
            bp.seek(4, 1)
            char_num = bp.readuint32()
            str_buf = bp.readstr(char_num)
            if "body" in str_buf:
                骨骼名称 = "body"
                骨骼动作.骨骼名称 = "body"
                self.烛龙文件.动作文件.适用body文件名称 = str_buf
            elif "face" in str_buf:
                骨骼名称 = "face"
                骨骼动作.骨骼名称 = "face"
                self.烛龙文件.动作文件.适用face文件名称 = str_buf
            else:
                骨骼名称 = str_buf
                骨骼动作.骨骼名称 = str_buf

            位置 = bp.readslice(位置num * 16)
            旋转 = bp.readslice(旋转num * 12)
            und位置 = bp.readslice(un位置num * 16)
            und旋转 = bp.readslice(un旋转num * 12)
            帧数集 = set()
            帧数集.add(0)

            for i in range(位置num):
                位置帧 = aurogon_type.烛龙位置帧()
                位置帧.location = mathutils.Vector(位置.readfloat32s(3))
                位置帧.frame = int(round(位置.readfloat32()*30))
                骨骼动作.位置帧列表.append(位置帧)
                帧数集.add(位置帧.frame)

            for i in range(旋转num):
                旋转帧 = aurogon_type.烛龙旋转帧()
                四元数 = [x*2**-15 for x in 旋转.readuint16s(4)]
                旋转帧.rotation_quaternion = mathutils.Quaternion(
                    [四元数[3], 四元数[0], 四元数[1], 四元数[2]])
                # 旋转帧.rotation_quaternion=mathutils.Quaternion(四元数)
                旋转帧.frame = int(round(旋转.readfloat32()*30))
                骨骼动作.旋转帧列表.append(旋转帧)
                帧数集.add(旋转帧.frame)

            骨骼动作.帧max数 = max(帧数集)
            self.烛龙文件.动作文件.骨骼动作列表.append(骨骼动作)
