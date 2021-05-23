import os
import mathutils

from . import aurogon_type
from . import binary_analysis


class 解析():

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__数据准备()  # 实例化烛龙类型，建立1套骨架等
        self.__数据读取()
        self.__数据处理()

    def __数据准备(self):
        # 实例烛龙文件
        self.烛龙文件 = aurogon_type.烛龙文件()
        self.__file_name = os.path.basename(self.__file_path)
        self.__材质列表 = []
        self.__标识_函数_字典 = {
            # 模型
            "HSMV": self.__HSMV解析,
            "SRTM": self.__SRTM解析,
            "MBUS": self.__MBUS解析,
            "RPXE": self.__myfun,
            "LEKS": self.__LEKS解析,
            "THGW": self.__THGW解析,
            "XBBB": self.__myfun,
            "RPBC": self.__myfun,
            "SDNB": self.__myfun,

            # 动作
            # 角色
        }

    def __数据读取(self):

        bp = binary_analysis.Analy(self.__file_path)
        Header = bp.read(8)
        while True:
            if bp.remain() <= 4:
                break
            块标识, 块名称, 块大小 = bp.readuint32(), bp.readstr(4), bp.readuint32()
            数据区 = bp.readslice(块大小)
            块标识, 块名称 = bp.readuint32(), bp.readstr(4)

            if 块名称 in self.__标识_函数_字典:
                self.__标识_函数_字典[块名称](数据区)

    def __HSMV解析(self, bp):
        """网格"""
        网格 = aurogon_type.烛龙网格()
        Header = bp.read(12)
        unflag, unsed, unnum = bp.readuint32s(3)
        flag_area = bp.read(44)
        flag = flag_area[0]

        unflag, unsed, vertnum = bp.readuint32s(3)
        file_base_name, file_ext = os.path.splitext(self.__file_path)
        if file_ext == ".model":
            bp.seek(34, 1)
            网格.顶点个数 = vertnum
            vertsize = vertnum * flag
            loopsize = bp.remain() - vertsize - 28
            顶点区, Loop区 = bp.readslice(vertsize), bp.readslice(loopsize)
            if int(flag/4) % 2 == 1:
                for i in range(vertnum):
                    bc = 顶点区.readslice(flag)
                    网格.顶点位置列表.append(bc.readfloat32s(3))
                    bc.seek(4, 1)
                    网格.顶点UV列表.append(bc.readfloat32s(2))
            else:
                for i in range(vertnum):
                    bc = 顶点区.readslice(flag)
                    网格.顶点位置列表.append(bc.readfloat32s(3))
                    bc.seek(4, 1)
                    bc.seek(4, 1)
                    网格.顶点UV列表.append(bc.readfloat32s(2))

        elif file_ext == ".vmesh":
            bp.seek(28, 1)
            网格.顶点个数 = vertnum
            vertsize = vertnum * flag
            loopsize = bp.remain() - vertsize - 28
            顶点区, Loop区 = bp.readslice(vertsize), bp.readslice(loopsize)
            if int(flag/4) % 2 == 1:
                for i in range(vertnum):
                    bc = 顶点区.readslice(flag)
                    网格.顶点位置列表.append(bc.readfloat32s(3))
                    bc.readfloat32s(3)
                    网格.顶点UV列表.append(bc.readfloat32s(2))
            else:
                for i in range(vertnum):
                    bc = 顶点区.readslice(flag)
                    网格.顶点位置列表.append(bc.readfloat32s(3))
                    bc.readfloat32s(3)
                    bc.seek(4, 1)
                    网格.顶点UV列表.append(bc.readfloat32s(2))

        if vertnum <= 65535:
            网格.Loop总数 = int(loopsize/2)
            网格.Loop列表 = Loop区.readuint16s(网格.Loop总数)
        else:
            网格.Loop总数 = int(loopsize/4)
            网格.Loop列表 = Loop区.readuint32s(网格.Loop总数)

        网格.三角面数 = int(网格.Loop总数/3)
        self.__总网格 = 网格

    def __SRTM解析(self, bp):
        """材质"""
        def LRTM解析(bp):
            """材质名称与贴图字典"""
            材质 = aurogon_type.烛龙材质()
            材质标识 = bp.readuint16()
            char_num = bp.readuint32()
            材质.名称 = bp.readstr(char_num)
            file_base_name, file_ext = os.path.splitext(self.__file_path)
            if file_ext == ".model":
                bp.seek(35, 1)
            elif file_ext == ".vmesh":
                bp.seek(30, 1)
            textures_folder = bp.find_textures_folder(self.__file_path)
            while True:
                for i in range(3):
                    char_num = bp.readuint32()
                    if char_num > 0:
                        buf_str = bp.readstr(char_num)
                        buf_路径 = os.path.abspath(buf_str)
                        贴图名称 = os.path.basename(buf_路径).split(".")[0]
                        贴图路径 = textures_folder + "\\" + 贴图名称 + ".dds"
                        材质.贴图字典[贴图名称] = 贴图路径

                接下来贴图数 = bp.readuint32()
                for i in range(接下来贴图数):
                    if 接下来贴图数 == 0:
                        break
                    char_num = bp.readuint32()
                    if char_num > 0:
                        buf_str = bp.readstr(char_num)
                        buf_路径 = os.path.abspath(buf_str)
                        贴图名称 = os.path.basename(buf_路径).split(".")[0]
                        贴图路径 = textures_folder + "\\" + 贴图名称 + ".dds"
                        # print(贴图路径)
                        材质.贴图字典[贴图名称] = 贴图路径

                接下来贴图数 = bp.readuint32()
                if 接下来贴图数 == 0:
                    break
                for i in range(接下来贴图数):
                    char_num = bp.readuint32()
                    if char_num > 0:
                        buf_str = bp.readstr(char_num)
                        buf_路径 = os.path.abspath(buf_str)
                        贴图名称 = os.path.basename(buf_路径).split(".")[0]
                        贴图路径 = textures_folder + "\\" + 贴图名称 + ".dds"
                        材质.贴图字典[贴图名称] = 贴图路径

            self.__材质列表.append(材质)

        材质总数 = bp.readuint32()
        for i in range(材质总数):
            块标识, 块名称, 块大小 = bp.readuint32(), bp.readstr(4), bp.readuint32()
            数据区 = bp.readslice(块大小)
            块标识, 块名称 = bp.readuint32(), bp.readstr(4)
            LRTM解析(数据区)

    def __MBUS解析(self, bp):
        """总网格分离成各个子网格, UV不会重叠在一起"""
        def 处理(loop索引左值, loop索引个数, vert索引左值, vert索引个数, 材质索引, j):
            网格 = aurogon_type.烛龙网格()
            网格.名称 = self.__file_name + "_" + str(j)
            网格.顶点个数 = vert索引个数
            网格.顶点位置列表 = self.__总网格.顶点位置列表[vert索引左值: vert索引左值 + vert索引个数]
            网格.顶点UV列表 = self.__总网格.顶点UV列表[vert索引左值: vert索引左值 + vert索引个数]
            网格.Loop总数 = loop索引个数
            网格.三角面数 = int(loop索引个数/3)
            网格.Loop列表 = self.__总网格.Loop列表[loop索引左值: loop索引左值 + loop索引个数]

            for i in range(网格.Loop总数):
                网格.Loop列表[i] -= vert索引左值

            网格.材质 = self.__材质列表[材质索引]
            return 网格

        bp.seek(8, 1)
        材质名称块总数 = bp.readuint32()
        for i in range(材质名称块总数):
            bp.seek(36, 1)
            char_num = bp.readuint32()
            材质名称 = bp.readstr(char_num)
            bp.seek(2, 1)

        网格块总数 = bp.readuint32()
        for j in range(网格块总数):  # 64字节/块
            loop索引左值, loop索引个数 = bp.readuint32s(2)
            unsed = bp.readuint32s(2)
            vert索引左值, vert索引个数 = bp.readuint32s(2)
            unsed = bp.readuint32s(2)
            unfloat1, unfloat2 = bp.readfloat32s(3), bp.readfloat32s(3)
            材质索引 = bp.readuint32()
            字节对齐 = bp.read(4)  # FFFFFFFF

            网格 = 处理(loop索引左值, loop索引个数, vert索引左值, vert索引个数, 材质索引, j)
            self.烛龙文件.网格列表.append(网格)

    def __LEKS解析(self, bp):
        self.烛龙文件.骨架 = aurogon_type.烛龙骨架()
        self.烛龙文件.骨架.名称 = self.__file_name  # 约定骨架名称与文件名称一致
        块标识 = bp.readuint16()
        bip骨骼总数 = bp.readuint16()
        for i in range(bip骨骼总数):
            骨骼 = aurogon_type.烛龙骨骼()
            char_num = bp.readuint32()
            骨骼.ID = i
            骨骼.名称 = bp.readstr(char_num)
            骨骼.父骨骼ID = bp.readint16()

            骨骼.尾位置vec3 = mathutils.Vector(bp.readfloat32s(3))
            骨骼.中四元数 = mathutils.Quaternion(bp.readfloat32s(4))
            骨骼.中位置vec3 = mathutils.Vector(bp.readfloat32s(3))
            bp.seek(16, 1)

            self.烛龙文件.骨架.骨骼列表.append(骨骼)

    def __THGW解析(self, bp):
        """
        按照点的顺序排列的骨骼权重信息
        两字节 Ushort 项数
            两字节 Ushort 骨骼序号
            两字节 Ushort 权重值
            .
            .
            .
            重复项数次
        .
        .
        .
        重复点数次
        """
        标识, unsed0 = bp.readuint16s(2)
        for i in range(self.__总网格.顶点个数):
            顶点权重 = aurogon_type.烛龙顶点权重()
            顶点权重.顶点ID = i
            权重个数 = bp.readuint16()
            for j in range(权重个数):
                骨骼ID和权重值 = aurogon_type.烛龙骨骼ID和权重值()
                骨骼ID和权重值.骨骼ID, 骨骼ID和权重值.权重值 = bp.readuint16(), bp.readuint16() * 2**-15
                顶点权重.骨骼ID和权重值列表.append(骨骼ID和权重值)
            self.__总网格.顶点权重列表.append(顶点权重)

    def XBBB解析(self, bp):
        骨骼总数 = bp.readuint16()

    def __myfun(self, bp):
        pass

    def __数据处理(self):
        for 骨骼 in self.烛龙文件.骨架.骨骼列表:
            父骨骼 = self.烛龙文件.骨架.骨骼列表[骨骼.父骨骼ID]
            # if 骨骼.父骨骼ID == -1: # 古剑2
            #     骨骼.父骨骼名称 = ""
            #     骨骼.头位置 = 骨骼.location
            #     骨骼.四元数 = 骨骼.rotation_quaternion
            # else:
            #     骨骼.父骨骼名称 = 父骨骼.名称
            #     骨骼.头位置 = 父骨骼.四元数 @ 骨骼.location + 父骨骼.头位置
            #     骨骼.四元数 = 父骨骼.四元数 @ 骨骼.rotation_quaternion
            # bvec = mathutils.Vector([0,0,0]) - 骨骼.头位置
            # bvec.normalize()
            # 骨骼.尾位置 = 骨骼.头位置 + 0.1*bvec
            骨骼.中四元数 = mathutils.Quaternion(
                [骨骼.中四元数[3], 骨骼.中四元数[0], 骨骼.中四元数[1], 骨骼.中四元数[2]])
            骨骼.头位置vec3 = 骨骼.尾位置vec3 + 骨骼.中位置vec3

            if 骨骼.父骨骼ID == -1:
                骨骼.父骨骼名称 = ""
                骨骼.头位置 = 骨骼.头位置vec3
                骨骼.尾位置 = 骨骼.尾位置vec3
            else:
                父骨骼 = self.烛龙文件.骨架.骨骼列表[骨骼.父骨骼ID]
                骨骼.父骨骼名称 = 父骨骼.名称
                骨骼.头位置 = 骨骼.中四元数 @ 骨骼.头位置vec3
                骨骼.尾位置 = 骨骼.中四元数 @ 骨骼.尾位置vec3

            骨骼.头位置.x = -骨骼.头位置.x
            骨骼.头位置.y = -骨骼.头位置.y
            骨骼.头位置.z = -骨骼.头位置.z
            骨骼.尾位置.x = -骨骼.尾位置.x
            骨骼.尾位置.y = -骨骼.尾位置.y
            骨骼.尾位置.z = -骨骼.尾位置.z

        # 将权重分配给每个网格
        start = 0
        for 网格 in self.烛龙文件.网格列表:
            end = 网格.顶点个数 + start
            网格.顶点权重列表 = self.__总网格.顶点权重列表[start: end]

            for 骨骼 in self.烛龙文件.骨架.骨骼列表:
                顶点组 = aurogon_type.烛龙顶点组()
                顶点组.骨骼ID = 骨骼.ID
                顶点组.骨骼名称 = 骨骼.名称
                网格.顶点组列表.append(顶点组)

            for 顶点权重 in 网格.顶点权重列表:
                for 骨骼ID_权重值 in 顶点权重.骨骼ID和权重值列表:
                    骨骼ID, 权重值 = 骨骼ID_权重值.骨骼ID, 骨骼ID_权重值.权重值
                    顶点组 = 网格.顶点组列表[骨骼ID]
                    顶点ID_权重值 = aurogon_type.烛龙顶点ID和权重值()
                    顶点ID_权重值.顶点ID, 顶点ID_权重值.权重值 = int(顶点权重.顶点ID - start), 权重值
                    顶点组.顶点ID和权重值列表.append(顶点ID_权重值)

            start = end

        # UV, Y轴镜像
        for 网格 in self.烛龙文件.网格列表:
            for i, [u, v] in enumerate(网格.顶点UV列表):
                v = 1 - v
                网格.顶点UV列表[i] = [u, v]
