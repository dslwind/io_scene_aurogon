import os

import mathutils
from . import aurogon_type, binary_analysis


class 解析():

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__数据准备()
        self.__数据读取()
        self.__数据处理()

    def __数据准备(self):
        # 实例烛龙文件
        self.烛龙文件 = aurogon_type.烛龙文件()
        self.__file_name = os.path.basename(self.__file_path)
        self.__textures_folder = os.path.dirname(self.__file_path)
        self.__总网格列表 = []
        self.__材质列表 = []

    def __数据读取(self):
        bp = binary_analysis.Analy(self.__file_path)
        Header = bp.read(8)
        while True:
            if bp.remain() <= 4:
                break
            块标识, 块大小, 块计数 = bp.readuint32s(3)
            数据区 = bp.readslice(块大小)
            # 块标识== 7: 文件信息
            # 块标识==11: 骨骼区
            # 块标识==13: 材质区
            # 块标识== 1: 网格区
            if 块标识 == 7:
                pass
            elif 块标识 == 11:
                self.__骨骼(数据区)

            elif 块标识 == 13:
                材质总数 = max(数据区.readall())  # (0, 16, 16, 0) 形式
                for i in range(材质总数):
                    材质 = aurogon_type.烛龙材质()
                    块标识, 块大小, 块计数 = bp.readuint32s(3)
                    # 材质区 = bp.read(块大小) # 88 + num + str
                    bp.seek(87, 1)
                    贴图总数 = bp.read(1)[0]
                    char_num = bp.readuint32()
                    材质.名称 = bp.readstr(char_num)
                    for i in range(贴图总数):  # 28 + num + str
                        bp.seek(28, 1)
                        char_num = bp.readuint32()
                        贴图名称 = bp.readstr(char_num)
                        材质.贴图字典[贴图名称] = self.__textures_folder + \
                            "\\" + 贴图名称 + ".dds"
                    self.__材质列表.append(材质)

            elif 块标识 == 1:
                self.__网格(数据区)
            elif 块标识 == 2:
                self.__权重(数据区)

            elif 块标识 == 12:
                pass  # 未知
            else:
                pass  # unknow

    def __骨骼(self, bp):
        self.烛龙文件.骨架 = aurogon_type.烛龙骨架()
        self.烛龙文件.骨架.名称 = self.__file_name  # 约定骨架名称与文件名称一致

        骨骼总数, 块标识 = bp.readuint32s(2)
        for i in range(骨骼总数):
            骨骼 = aurogon_type.烛龙骨骼()
            骨骼.ID = i

            ba = bp.readslice(80)
            骨骼.头四元数 = mathutils.Quaternion(ba.readfloat32s(4))
            ba.seek(16, 1)
            骨骼.头位置vec3 = mathutils.Vector(ba.readfloat32s(3))
            ba.seek(32, 1)
            骨骼.父骨骼ID = ba.readint32()  # 76:80

            bc = bp.readslice(80)
            bc.seek(76, 1)
            char_num = bc.readuint32()  # 76:80

            骨骼.名称 = bp.readstr(char_num)
            self.烛龙文件.骨架.骨骼列表.append(骨骼)

    def __网格(self, bp):
        总网格ID, unsed1, skinvert总数, 顶点总数, unsed4, 子网格总数, 数据块总数, unsed7, unsed8 = bp.readuint32s(
            9)
        总网格 = aurogon_type.烛龙网格()
        总网格.ID = 总网格ID
        总网格.skinvert总数 = skinvert总数
        for i in range(数据块总数):
            标识, 步长 = bp.readuint32s(2)
            if 标识 == 4:
                总网格.skinvert索引 = bp.readuint32s(顶点总数)  # uint32
            elif 标识 == 0:
                unsed0, unsed1 = bp.readuint16s(2)
                总网格.顶点位置列表 = [bp.readfloat32s(3)
                              for x in range(顶点总数)]  # float32s(3)
            elif 标识 == 1:
                unsed0, unsed1 = bp.readuint16s(2)
                法线区 = bp.read(顶点总数 * 12)  # float32s(3)
            elif 标识 == 3:
                unsed0, unsed1 = bp.readuint16s(2)
                总网格.顶点UV列表 = [bp.readfloat32s(2)
                              for x in range(顶点总数)]  # float32s(2)
            elif 标识 == 2:
                unsed0, unsed1 = bp.readuint16s(2)
                unlist = bp.read(顶点总数 * 16)  # float32s(4)
            else:
                unsed0, unsed1 = bp.readuint16s(2)
                unlist = bp.read(顶点总数 * 步长)  # float32s()

        self.__总网格列表.append(总网格)

        def 处理(vert索引左值, vert索引个数, 材质索引, j):
            网格 = aurogon_type.烛龙网格()
            网格.总网格ID = 总网格ID
            网格.名称 = self.__file_name + "_" + str(总网格ID) + "_" + str(j)
            网格.顶点个数 = vert索引个数
            网格.顶点位置列表 = 总网格.顶点位置列表[vert索引左值: vert索引左值 + vert索引个数]
            网格.顶点UV列表 = 总网格.顶点UV列表[vert索引左值: vert索引左值 + vert索引个数]
            try:
                网格.材质 = self.__材质列表[材质索引]
            except Exception as e:
                print(e)
            return 网格

        vert索引左值 = 0
        for j in range(子网格总数):
            loop总数, vert索引个数, 材质索引, 骨骼总数 = bp.readuint32s(4)
            网格 = 处理(vert索引左值, vert索引个数, 材质索引, j)
            vert索引左值 += vert索引个数
            网格.Loop总数 = loop总数
            网格.Loop列表 = bp.readuint32s(loop总数)
            网格.三角面数 = int(loop总数/3)
            self.烛龙文件.网格列表.append(网格)
            BoneMap = bp.readuint32s(骨骼总数)

    def __权重(self, bp):
        总网格ID, unsed1, unsed2, 权重总数, unsed4 = bp.readuint32s(5)
        权重列表 = []
        for i in range(权重总数):
            骨骼ID_权重值 = aurogon_type.烛龙骨骼ID和权重值()
            骨骼ID_权重值.权重值, 骨骼ID_权重值.骨骼ID = bp.readfloat32(), bp.readuint32()
            权重列表.append(骨骼ID_权重值)

        对应总网格 = None
        for 总网格 in self.__总网格列表:
            if 总网格.ID == 总网格ID:
                对应总网格 = 总网格
                break

        权重索引左值_权重数_列表 = []
        for i in range(对应总网格.skinvert总数):
            权重索引左值_权重数_列表.append(bp.readuint32s(2))

        start = 0
        for i, ID in enumerate(对应总网格.skinvert索引):
            顶点权重 = aurogon_type.烛龙顶点权重()
            顶点权重.顶点ID = i
            权重索引左值, 权重数 = 权重索引左值_权重数_列表[ID]
            顶点权重.骨骼ID和权重值列表 = 权重列表[权重索引左值: 权重索引左值 + 权重数]
            对应总网格.顶点权重列表.append(顶点权重)

        # 将权重分配给每个网格
        start = 0
        for 网格 in self.烛龙文件.网格列表:
            if 网格.总网格ID == 总网格ID:
                end = 网格.顶点个数 + start
                网格.顶点权重列表 = 对应总网格.顶点权重列表[start: end]

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
                        顶点ID_权重值.顶点ID, 顶点ID_权重值.权重值 = int(
                            顶点权重.顶点ID - start), 权重值
                        顶点组.顶点ID和权重值列表.append(顶点ID_权重值)

                start = end

    def __数据处理(self):

        for 骨骼 in self.烛龙文件.骨架.骨骼列表:
            父骨骼 = self.烛龙文件.骨架.骨骼列表[骨骼.父骨骼ID]
            骨骼.头四元数 = mathutils.Quaternion(
                [骨骼.头四元数[3], 骨骼.头四元数[0], 骨骼.头四元数[1], 骨骼.头四元数[2]])

            if 骨骼.父骨骼ID == -1:
                骨骼.父骨骼名称 = ""
                骨骼.头位置 = 骨骼.头位置vec3
                骨骼.尾位置 = mathutils.Vector([0, 10, 0])
            else:
                父骨骼 = self.烛龙文件.骨架.骨骼列表[骨骼.父骨骼ID]
                骨骼.父骨骼名称 = 父骨骼.名称
                骨骼.头位置 = 父骨骼.头四元数 @ 骨骼.头位置vec3 + 父骨骼.头位置
                骨骼.头四元数 = 父骨骼.头四元数 @ 骨骼.头四元数

                bvec = mathutils.Vector([0, 0, 0]) - 骨骼.头位置
                bvec.normalize()
                骨骼.尾位置 = 骨骼.头位置 + 1.5*bvec

        # UV, Y轴镜像
        for 网格 in self.烛龙文件.网格列表:
            for i, [u, v] in enumerate(网格.顶点UV列表):
                if u < 0:
                    u = -u
                v = 1 - v
                网格.顶点UV列表[i] = [u, v]
