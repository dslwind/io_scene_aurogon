import os
import math
import mathutils

from . import aurogon_type, binary_analysis


class NIF贴图块():
    def __init__(self, bp):
        self.NiSourceTextureID = bp.readuint32()
        flag总数 = bp.readuint16()
        max各向异性过滤 = bp.readuint16()
        has形变 = bp.readuint8()
        if has形变:
            floatlist = bp.readfloat32s(8)


class NIF数据块():
    def __init__(self, bp, 总名称列表):
        self.NiDataStreamID = bp.readuint32()
        是标准网格 = bp.readuint8()
        NiDataStream子网格区域映射项总数 = bp.readuint16()
        NiDataStream子网格区域映射项列表 = []
        for i in range(NiDataStream子网格区域映射项总数):
            NiDataStream子网格区域映射项列表.append(bp.readuint16())
        NiDataStream描述总数 = bp.readuint32()
        self.NiDataStream描述列表 = []
        for i in range(NiDataStream描述总数):
            名称索引 = bp.readuint32()
            描述名称 = 总名称列表[名称索引]
            描述索引 = bp.readuint32()
            self.NiDataStream描述列表.append([描述名称, 描述索引])


class NIF对象():
    def __init__(self, bp, 总名称列表):
        self.bp = bp
        self.ID = -1
        self.名称 = ""
        self.类型 = ""
        self.父对象ID = -1
        self.父对象名称 = ""
        self.父对象类型 = ""

        self.总名称列表 = 总名称列表  # 需要对名称列表只读

    def 读取名称(self, bp):
        名称索引 = bp.readuint32()
        if 名称索引 == 0xFFFFFFFF:
            return ""
        else:
            return self.总名称列表[名称索引]

    def 读取链接(self, bp):
        ID总数 = bp.readuint32()  # -1, 256, 8192
        if -1 < ID总数 < 8192:
            ID列表 = bp.readint32s(ID总数)
            ID列表_new = [x for x in ID列表 if -1 < x < 8192]
            return ID总数, ID列表_new
        else:
            return ID总数, []

    # ======================================================================
    # 模型
    # ======================================================================
    def NiNode解析(self):
        bp = self.bp

        # ObjectNET
        self.名称 = self.读取名称(bp)
        扩展数据ID总数, 扩展数据ID列表 = self.读取链接(bp)
        未知ID1 = bp.readuint32()  # 0xFFFFFFFF

        # AVObject矩阵信息
        self.flag = bp.readuint16()
        self.location = mathutils.Vector(bp.readfloat32s(3))
        self.rotation_matrix = mathutils.Matrix(
            [bp.readfloat32s(3),
             bp.readfloat32s(3),
             bp.readfloat32s(3)]).to_4x4()
        self.scale = bp.readfloat32()
        self.rotation_quaternion = self.rotation_matrix.to_quaternion()
        self.matrix = None
        节点属性ID总数, 节点属性ID列表 = self.读取链接(bp)
        未知ID2 = bp.readuint32()  # 0xFFFFFFFF

        # NiNode
        self.子连接ID总数, self.子连接ID列表 = self.读取链接(bp)
        灯光连接ID总数, 灯光连接ID列表 = self.读取链接(bp)

    def NiMesh解析(self):
        bp = self.bp

        # ObjectNET
        self.名称 = self.读取名称(bp)
        扩展数据ID总数, 扩展数据ID列表 = self.读取链接(bp)
        未知ID1 = bp.readuint32()  # 0xFFFFFFFF

        # AVObject矩阵信息
        self.flag = bp.readuint16()
        self.location = mathutils.Vector(bp.readfloat32s(3))
        self.rotation_matrix = mathutils.Matrix(
            [bp.readfloat32s(3),
             bp.readfloat32s(3),
             bp.readfloat32s(3)]).to_4x4()
        self.scale = bp.readfloat32()
        self.rotation_quaternion = self.rotation_matrix.to_quaternion()
        self.matrix = None
        self.节点属性ID总数, self.节点属性ID列表 = self.读取链接(bp)
        未知ID2 = bp.readuint32()  # 0xFFFFFFFF

        # Renderable
        材质总数 = bp.readuint32()
        材质扩展数据列表 = []
        材质名称列表 = []
        for i in range(材质总数):
            材质名称索引 = bp.readuint32()
            材质扩展数据 = bp.readuint32()
            材质扩展数据列表.append(材质扩展数据)
        材质索引 = bp.readuint32()
        材质是否需要更新 = bp.readuint8()

        # NiMesh
        self.meshPrimType = bp.readuint32()
        self.子网格总数 = bp.readuint16()
        self.网格是否是实例 = bp.readuint8()
        self.包围盒中心 = bp.readfloat32s(3)
        self.包围盒旋转弧度 = bp.readfloat32()

        数据块总数 = bp.readuint32()
        self.数据块列表 = []
        for i in range(数据块总数):
            数据块 = NIF数据块(bp, self.总名称列表)
            self.数据块列表.append(数据块)

        self.修改器ID总数, self.修改器ID列表 = self.读取链接(bp)

    def NiMaterialProperty解析(self):
        bp = self.bp
        # ObjectNET
        self.名称 = self.读取名称(bp)

        # 余下不再解析

    def NiTexturingProperty解析(self):
        bp = self.bp
        名称 = self.读取名称(bp)  # 一般读取后为空，该项不使用
        扩展数据ID总数, 扩展数据ID列表 = self.读取链接(bp)
        未知ID1 = bp.readuint32()

        # NiTexturingProperty
        贴图属性flag总数 = bp.readuint16()
        贴图块总数 = bp.readuint32()  # 需 < 256
        self.贴图块列表 = []
        for i in range(贴图块总数):
            has_map = bp.readuint8()
            if has_map:
                贴图 = NIF贴图块(bp)
                if i == 5:
                    bp.readfloat32s(6)
                elif i == 7:
                    bp.readfloat32()
                self.贴图块列表.append(贴图)  # 存在没有贴图块的情况
            else:
                pass

    def NiSourceTexture解析(self):
        bp = self.bp

        # ObjectNET
        名称 = self.读取名称(bp)
        扩展数据ID总数, 扩展数据ID列表 = self.读取链接(bp)
        未知ID1 = bp.readuint32()

        # NiSourceTexture
        是外部贴图 = bp.readuint8()
        self.贴图名称 = self.读取名称(bp)

        # ......剩余部分不再读取

    def NiDataStream解析(self):
        bp = self.bp

        块大小 = bp.readuint32()
        克隆数 = bp.readuint32()
        区域总数 = bp.readuint32()
        self.区域列表 = []
        for i in range(区域总数):
            self.区域列表.append(bp.readuint32s(2))

        块标识总数 = bp.readuint32()
        self.块标识列表 = []
        for i in range(块标识总数):
            self.块标识列表.append(bp.readuint8s(4))

        self.块数据 = bp.readslice(块大小)
        块存在 = bp.readuint8()

    def NiSkinningMeshModifier解析(self):
        bp = self.bp

        # base mesh modifier
        sync计数 = bp.readuint32()
        for i in range(sync计数):
            bp.readuint16()
        sync计数 = bp.readuint32()
        for i in range(sync计数):
            bp.readuint16()

            # skinned mesh modifier
        skinflags = bp.readuint16()
        self.根骨骼ID = bp.readuint32()
        self.父骨骼location = mathutils.Vector(bp.readfloat32s(3))
        self.父骨骼rotation_quaternion = mathutils.Matrix(
            [bp.readfloat32s(3),
             bp.readfloat32s(3),
             bp.readfloat32s(3)]).to_quaternion()
        self.父骨骼scale = bp.readfloat32()
        self.骨骼总数, self.骨骼ID列表 = self.读取链接(bp)

        self.骨骼_loca_quat_scal_列表 = []
        for i in range(self.骨骼总数):
            location = mathutils.Vector(bp.readfloat32s(3))
            rotation_quaternion = mathutils.Matrix(
                [bp.readfloat32s(3),
                 bp.readfloat32s(3),
                 bp.readfloat32s(3)]).to_quaternion()
            scale = bp.readfloat32()
            self.骨骼_loca_quat_scal_列表.append(
                [location, rotation_quaternion, scale])

        if skinflags & 2:
            # bounds are unused
            for i in range(0, self.骨骼总数):
                包围盒中心 = bp.readfloat32s(3)
                包围盒旋转弧度 = bp.readfloat32()

    def NiMorphMeshModifier解析(self):
        pass

    # ======================================================================
    # 动作
    # ======================================================================
    def NiSequenceData解析(self):
        bp = self.bp

        self.名称 = self.读取名称(bp)
        self.EvalID总数, self.EvalID列表 = self.读取链接(bp)

    def NiTransformEvaluator解析(self):
        bp = self.bp

        # Evaluator
        self.名称 = self.读取名称(bp)  # name of the target node
        PropType = self.读取名称(bp)
        CtrlType = self.读取名称(bp)
        CtrlID = self.读取名称(bp)
        EvalID = self.读取名称(bp)
        ChanTypes = bp.readuint8s(4)

        # NiTransformEvaluator
        self.location = bp.readfloat32s(3)
        self.quaternion = bp.readfloat32s(4)
        self.scale = bp.readfloat32()
        self.NiTransformDataID = bp.readint32()

    def NiBSplineCompTransformEvaluator解析(self):
        bp = self.bp

        # Evaluator
        self.名称 = self.读取名称(bp)
        PropType = self.读取名称(bp)
        CtrlType = self.读取名称(bp)
        CtrlID = self.读取名称(bp)
        EvalID = self.读取名称(bp)
        ChanTypes = bp.readuint8s(4)

        # NiConstTransformEvaluator
        self.location = bp.readfloat32s(3)
        self.quaternion = bp.readfloat32s(4)
        self.scale = bp.readfloat32()
        self.unsedfloats = bp.readfloat32s(4)
        self.父对象ID = bp.readint32()

    def NiTransformData解析(self):
        bp = self.bp

        self.frame_quaternion_列表 = []
        self.frame_location_列表 = []
        self.frame_scale_列表 = []

        self.quaternion总数 = bp.readuint32()
        if self.quaternion总数 > 0:
            rotKeyType = bp.readuint32()
        for i in range(self.quaternion总数):
            if rotKeyType == 0 or rotKeyType == 1:
                frame = int(round(bp.readfloat32()))
                quaternion = bp.readfloat32s(4)  # [w, x, y, z]
                self.frame_quaternion_列表.append([frame, quaternion])
            elif rotKeyType == 4:
                xyz = [[], [], []]
                帧数集 = set()
                for i in range(3):
                    子帧数 = bp.readuint32()
                    if 子帧数 > 0:
                        radianKeyType = bp.readuint32()
                    for j in range(子帧数):
                        frame = int(round(bp.readfloat32()))
                        帧数集.add(frame)
                        if radianKeyType == 0 or radianKeyType == 1:
                            xyz[i].append([frame, bp.readfloat32()])
                        elif radianKeyType == 2:
                            xyz[i].append([frame, bp.readfloat32()])
                            bezierIn = bp.readfloat32()
                            bezierOut = bp.readfloat32()
                        else:
                            return

                xrlist, yrlist, zrlist = xyz
                max帧数 = max(帧数集)
                for m in range(max帧数 + 1):
                    quat_a, quat_b, quat_c = None, None, None
                    for frame, xr in xrlist:
                        if frame == m:
                            quat_a = mathutils.Quaternion((1.0, 0.0, 0.0), xr)
                            break
                    for frame, yr in yrlist:
                        if frame == m:
                            quat_b = mathutils.Quaternion((1.0, 0.0, 0.0), yr)
                            break
                    for frame, zr in zrlist:
                        if frame == m:
                            quat_c = mathutils.Quaternion((1.0, 0.0, 0.0), zr)
                            break
                    quaternion = mathutils.Quaternion([1, 0, 0, 0])
                    if quat_a is not None:
                        quaternion = quat_a @ quaternion
                    if quat_b is not None:
                        quaternion = quat_b @ quaternion
                    if quat_c is not None:
                        quaternion = quat_c @ quaternion

                    if quat_a is not None or quat_b is not None or quat_c is not None:
                        self.frame_quaternion_列表.append([m, quaternion])

        self.location总数 = bp.readuint32()
        if self.location总数 > 0:
            locKeyType = bp.readuint32()
        for i in range(self.location总数):
            frame = int(round(bp.readfloat32()))
            if locKeyType == 0 or locKeyType == 1:
                location = bp.readfloat32s(3)
            elif locKeyType == 2:
                location = bp.readfloat32s(3)
                bezierIn = bp.readfloat32s(3)
                bezierOut = bp.readfloat32s(3)
            else:
                return
            self.frame_location_列表.append([frame, location])

        self.scale总数 = bp.readuint32()
        if self.scale总数 > 0:
            sclKeyType = bp.readuint32()
        for i in range(self.scale总数):
            frame = bp.readfloat32()
            if sclKeyType == 0 or sclKeyType == 1:
                scale = bp.readfloat32()
            elif sclKeyType == 2:
                scale = bp.readfloat32()
                bezierIn = bp.readfloat32()
                bezierOut = bp.readfloat32()
            else:
                return
            self.frame_scale_列表.append([frame, scale])

    def 解析(self):
        # ======================================================================
        # 模型
        # ======================================================================
        if self.类型 == "NiNode":
            self.NiNode解析()
        elif self.类型 == "NiMesh":
            self.NiMesh解析()
        elif self.类型 == "NiMaterialProperty":
            self.NiMaterialProperty解析()
        elif self.类型 == "NiTexturingProperty":
            self.NiTexturingProperty解析()
        elif self.类型 == "NiSourceTexture":
            self.NiSourceTexture解析()
        elif "NiDataStream" in self.类型:
            self.NiDataStream解析()
        elif self.类型 == "NiSkinningMeshModifier":
            self.NiSkinningMeshModifier解析()
        # ======================================================================
        # 动作
        # ======================================================================
        elif self.类型 == "NiSequenceData":
            self.NiSequenceData解析()
        elif self.类型 == "NiTransformEvaluator":
            self.NiTransformEvaluator解析()
        elif self.类型 == "NiTransformData":
            self.NiTransformData解析()


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

    def __数据读取(self):
        bp = binary_analysis.Analy(self.__file_path)
        self.__textures_folder = bp.find_textures_folder(self.__file_path)

        Header = bp.read(39)
        文件版本 = bp.readlist(4)[::-1]
        is_little = bp.readuint8()
        用户版本 = bp.readlist(4)[::-1]

        nif对象总数 = bp.readuint32()
        nif类型总数 = bp.readuint16()
        类型名称列表 = []
        for i in range(nif类型总数):
            char_num = bp.readuint32()
            类型名称 = bp.readstr(char_num)
            类型名称列表.append(类型名称)

        类型名称索引列表 = []
        for i in range(nif对象总数):
            类型名称索引列表.append(bp.readuint16())

        nif对象数据块size列表 = []
        for i in range(nif对象总数):
            nif对象数据块size列表.append(bp.readuint32())

        nif名称总数 = bp.readuint32()
        nif名称列表 = []
        nif名称max字符数 = bp.readuint32()
        for i in range(nif名称总数):
            char_num = bp.readuint32()
            名称 = bp.readstr(char_num)
            nif名称列表.append(名称)

        nif对象Group总数 = bp.readuint32()

        # 读取对象
        self.__nif对象列表 = []
        for i in range(nif对象总数):
            类型名称 = 类型名称列表[类型名称索引列表[i]]
            size = nif对象数据块size列表[i]
            数据区 = bp.readslice(size)

            nif对象 = NIF对象(数据区, nif名称列表)
            nif对象.ID = i
            nif对象.类型 = 类型名称
            nif对象.解析()
            self.__nif对象列表.append(nif对象)

        for nif对象 in self.__nif对象列表:
            if nif对象.类型 == "NiNode":
                self.烛龙文件.骨架.名称 = self.__file_name
                break

        # 节点遍历, 骨骼也在遍历过程中建立
        self.__Ni节点遍历()

    def __Ni节点遍历(self):
        def 链表遍历(nif对象):
            if nif对象.类型 == "NiNode":
                self.__NiNode处理(nif对象)
                骨骼 = aurogon_type.烛龙骨骼()
                骨骼.名称 = nif对象.名称
                骨骼.ID = nif对象.ID
                骨骼.父骨骼ID = nif对象.父对象ID
                骨骼.父骨骼名称 = nif对象.父对象名称
                骨骼.头位置 = nif对象.matrix @ mathutils.Vector([0, 0, 0])
                bvec = mathutils.Vector([0, 0, 0]) - 骨骼.头位置
                bvec.normalize()
                骨骼.尾位置 = 骨骼.头位置 + 1.5 * bvec
                self.烛龙文件.骨架.骨骼列表.append(骨骼)

                for i in nif对象.子连接ID列表:
                    znif对象 = self.__nif对象列表[i]
                    znif对象.父对象ID = nif对象.ID
                    znif对象.父对象名称 = nif对象.名称
                    链表遍历(znif对象)

            elif nif对象.类型 == "NiMesh":
                self.__NiMesh处理(nif对象)

            elif nif对象.类型 == "NiSequenceData":
                self.__NiSequenceData处理(nif对象)

            else:
                pass

        根节点 = self.__nif对象列表[0]
        链表遍历(根节点)

        # ======================================================================
        # NiNode methods
        # ======================================================================
    def __NiNode处理(self, NiNode):
        mat_loc = mathutils.Matrix.Translation(NiNode.location)
        mat_rot = NiNode.rotation_matrix
        mat_out = mat_loc @ mat_rot
        if NiNode.父对象名称 == "":
            NiNode.matrix = mat_out
        else:
            fnif对象 = self.__nif对象列表[NiNode.父对象ID]
            NiNode.matrix = fnif对象.matrix @ mat_out

    # ======================================================================
    # NiMesh methods
    # ======================================================================
    def __NiMesh处理(self, NiMesh):
        材质 = aurogon_type.烛龙材质()
        for ID in NiMesh.节点属性ID列表:
            nif对象 = self.__nif对象列表[ID]
            if nif对象.类型 == "NiMaterialProperty":
                材质.名称 = nif对象.名称
            elif nif对象.类型 == "NiTexturingProperty":
                for 贴图块 in nif对象.贴图块列表:
                    znif对象 = self.__nif对象列表[贴图块.NiSourceTextureID]
                    贴图名称 = znif对象.贴图名称.split(".")[0]
                    材质.贴图字典[贴图名称] = ""

        mat_loc = mathutils.Matrix.Translation(NiMesh.location)
        mat_rot = NiMesh.rotation_matrix
        mat_out = mat_loc @ mat_rot

        fnif对象 = self.__nif对象列表[NiMesh.父对象ID]
        NiMesh.matrix = fnif对象.matrix @ mat_out

        描述_数据_字典 = {}
        for 数据块 in NiMesh.数据块列表:
            dnif对象 = self.__nif对象列表[数据块.NiDataStreamID]
            NiDataStream描述列表 = 数据块.NiDataStream描述列表
            区域列表 = dnif对象.区域列表
            块标识列表 = dnif对象.块标识列表
            块数据 = dnif对象.块数据

            for index in range(NiMesh.子网格总数):
                elems列表 = []
                左值, 总数 = 区域列表[index]
                for i in range(总数):
                    elems = []
                    for dataType, size, count, unsed in 块标识列表:
                        # print(dataType, size , count, unsed)
                        if dataType == 21:  # 21, 2, 1, 0
                            # print(dataType, size , count, unsed)
                            elems.append(块数据.readuint16())
                        elif dataType == 54:  # 54, 4, 2, 0
                            elems.append(块数据.readfloat32s(2))
                        elif dataType == 55:  # 55, 4, 3, 0
                            elems.append(块数据.readfloat32s(3))
                        elif dataType == 8:  # 8, 1, 4, 0
                            elems.append(块数据.readuint8s(4))
                        elif dataType == 53:  # 53, 4, 1, 0
                            # float32() or uint32()
                            elems.append(块数据.readfloat32())
                        else:
                            elems.append(块数据.read(size * count))
                    elems列表.append(elems)

                buf列表 = []
                for i, 块标识 in enumerate(块标识列表):
                    列表 = []
                    for j in range(总数):
                        列表.append(elems列表[j][i])
                    buf列表.append(列表)

                for m, [描述, 索引] in enumerate(NiDataStream描述列表):
                    列表 = buf列表[m]
                    描述_数据_字典[描述 + str(索引) + str(index)] = 列表

        for i in range(NiMesh.子网格总数):
            网格 = aurogon_type.烛龙网格()
            网格.名称 = NiMesh.名称 + "_" + str(i)
            网格.材质 = 材质
            网格.父对象名称 = NiMesh.父对象名称
            if "TEXCOORD0" + str(i) in 描述_数据_字典:
                网格.Loop总数 = len(描述_数据_字典["INDEX0" + str(i)])
                网格.三角面数 = int(网格.Loop总数 / 3)
                网格.Loop列表 = 描述_数据_字典["INDEX0" + str(i)]

                网格.顶点个数 = len(描述_数据_字典["TEXCOORD0" + str(i)])
                网格.顶点UV列表 = 描述_数据_字典["TEXCOORD0" + str(i)]
                try:
                    网格.顶点位置列表 = 描述_数据_字典["POSITION0" + str(i)]
                except:
                    网格.顶点位置列表 = 描述_数据_字典["POSITION_BP0" + str(i)]

                try:
                    网格.权重值索引列表 = 描述_数据_字典["BLENDINDICES0" + str(i)]
                    网格.权重值列表 = 描述_数据_字典["BLENDWEIGHT0" + str(i)]
                except:
                    pass
                    # 脸部及模型自带的武器网格没有权重
                try:
                    bone索引列表 = 描述_数据_字典["BONE_PALETTE0" + str(i)]
                    for 修改器ID in NiMesh.修改器ID列表:
                        xnif对象 = self.__nif对象列表[修改器ID]
                        if xnif对象.类型 == "NiSkinningMeshModifier":
                            buf骨骼ID列表 = xnif对象.骨骼ID列表
                    for index in bone索引列表:
                        网格.骨骼ID列表.append(buf骨骼ID列表[index])
                except:
                    pass

                for j, 位置vec3 in enumerate(网格.顶点位置列表):
                    位置vec3 = NiMesh.matrix @ mathutils.Vector(位置vec3)
                    网格.顶点位置列表[j] = 位置vec3

                self.烛龙文件.网格列表.append(网格)

    def __NiSequenceData处理(self, NiSequenceData):
        self.烛龙文件.动作文件.名称 = self.__file_name
        for ID in NiSequenceData.EvalID列表:
            nif对象 = self.__nif对象列表[ID]
            if nif对象.类型 == "NiTransformEvaluator":
                骨骼动作 = aurogon_type.烛龙骨骼动作()
                骨骼动作.骨骼名称 = nif对象.名称
                if nif对象.NiTransformDataID != -1:
                    NiTransformData = self.__nif对象列表[nif对象.NiTransformDataID]
                    for frame, quaternion in NiTransformData.frame_quaternion_列表:
                        旋转帧 = aurogon_type.烛龙旋转帧()
                        旋转帧.frame = frame
                        旋转帧.rotation_quaternion = mathutils.Quaternion(
                            quaternion
                        )  # @ mathutils.Quaternion(nif对象.quaternion)
                        骨骼动作.旋转帧列表.append(旋转帧)

                    for frame, location in NiTransformData.frame_location_列表:
                        位置帧 = aurogon_type.烛龙位置帧()
                        位置帧.frame = frame
                        # + mathutils.Vector(nif对象.location)
                        位置帧.location = mathutils.Vector(location)
                        骨骼动作.位置帧列表.append(位置帧)

                self.烛龙文件.动作文件.骨骼动作字典[骨骼动作.骨骼名称] = 骨骼动作

    def __数据处理(self):
        for 网格 in self.烛龙文件.网格列表:
            for 贴图名称 in 网格.材质.贴图字典.keys():
                网格.材质.贴图字典[贴图名称] = self.__textures_folder + \
                    "\\" + 贴图名称.lower() + ".dds"

            for i, [u, v] in enumerate(网格.顶点UV列表):
                小数, 浮点整数 = math.modf(v)
                v = 1 - 小数
                网格.顶点UV列表[i] = [u, v]

            for i in range(len(网格.权重值列表)):
                顶点权重 = aurogon_type.烛龙顶点权重()
                顶点权重.顶点ID = i

                for j in range(len(网格.权重值列表[i])):
                    骨骼ID_权重值 = aurogon_type.烛龙骨骼ID和权重值()
                    索引 = 网格.权重值索引列表[i][j]
                    骨骼ID_权重值.骨骼ID = 网格.骨骼ID列表[索引]
                    骨骼ID_权重值.权重值 = 网格.权重值列表[i][j]
                    顶点权重.骨骼ID和权重值列表.append(骨骼ID_权重值)

                网格.顶点权重列表.append(顶点权重)

        for 网格 in self.烛龙文件.网格列表:
            for 骨骼ID in 网格.骨骼ID列表:
                顶点组 = aurogon_type.烛龙顶点组()
                顶点组.骨骼ID = 骨骼ID
                nif对象 = self.__nif对象列表[骨骼ID]
                顶点组.骨骼名称 = nif对象.名称
                网格.顶点组列表.append(顶点组)

            for 顶点权重 in 网格.顶点权重列表:
                for 骨骼ID_权重值 in 顶点权重.骨骼ID和权重值列表:
                    骨骼ID, 权重值 = 骨骼ID_权重值.骨骼ID, 骨骼ID_权重值.权重值
                    nif对象 = self.__nif对象列表[骨骼ID]
                    骨骼名称 = nif对象.名称
                    for 顶点组 in 网格.顶点组列表:
                        if 顶点组.骨骼名称 == 骨骼名称:
                            顶点ID_权重值 = aurogon_type.烛龙顶点ID和权重值()
                            顶点ID_权重值.顶点ID, 顶点ID_权重值.权重值 = int(顶点权重.顶点ID), 权重值
                            顶点组.顶点ID和权重值列表.append(顶点ID_权重值)

            if len(网格.顶点权重列表) == 0:
                顶点组 = aurogon_type.烛龙顶点组()
                顶点组.骨骼名称 = 网格.父对象名称
                for i in range(网格.顶点个数):
                    顶点ID_权重值 = aurogon_type.烛龙顶点ID和权重值()
                    顶点ID_权重值.顶点ID, 顶点ID_权重值.权重值 = i, 1.0
                    顶点组.顶点ID和权重值列表.append(顶点ID_权重值)
                网格.顶点组列表.append(顶点组)


# ['INDEX', 0]
# ['TEXCOORD', 0]
# ['POSITION_BP', 0]
# ['NORMAL_BP', 0]
# ['BINORMAL_BP', 0]
# ['TANGENT_BP', 0]
# ['BLENDINDICES', 0]
# ['BLENDWEIGHT', 0]
# ['BONE_PALETTE', 0]

# Skin_Face:2
# ['INDEX', 0]
# ['POSITION', 0]
# ['NORMAL', 0]
# ['TEXCOORD', 0]
# ['MORPH_POSITION', 0]
# ['MORPH_POSITION', 1]
# ['MORPH_POSITION', 2]
# ['MORPH_POSITION', 3]
# ['MORPH_POSITION', 4]
# ['MORPH_POSITION', 5]
# ['MORPH_POSITION', 6]
# ['MORPH_POSITION', 7]
# ['MORPH_POSITION', 8]
# ['MORPH_POSITION', 9]
# ['MORPH_POSITION', 10]
# ['MORPH_POSITION', 11]
# ['MORPH_POSITION', 12]
# ['MORPH_POSITION', 13]
# ['MORPH_POSITION', 14]
# ['MORPH_POSITION', 15]
# ['MORPH_POSITION', 16]
# ['MORPH_POSITION', 17]
# ['MORPH_POSITION', 18]
# ['MORPH_POSITION', 19]
# ['MORPH_POSITION', 20]
# ['MORPH_POSITION', 21]
# ['MORPH_POSITION', 22]
# ['MORPH_POSITION', 23]
# ['MORPH_POSITION', 24]
# ['MORPHWEIGHTS', 0]

# NiNode
# NiZBufferProperty
# NiVertexColorProperty
# NiFloatExtraData
# NiStringExtraData
# NiTransformController
# NiIntegerExtraData
# NiMesh
# NiMaterialProperty
# NiDataStream╔0╔18
# NiDataStream╔1╔18
# NiMorphWeightsController
# NiTexturingProperty
# NiSourceTexture
# NiAlphaProperty
# NiSpecularProperty
# NiDataStream╔1╔24
# NiDataStream╔1╔3
# NiDataStream╔3╔5
# NiMorphMeshModifier
# NiCamera
# NiPointLight
# NiDataStream╔3╔3
# NiSkinningMeshModifier
# NiAmbientLight

# NiSequenceData
# NiConstFloatEvaluator
# NiBSplineCompTransformEvaluator
# NiBSplineData
# NiBSplineBasisData
# NiTransformEvaluator
# NiTransformData
# NiTextKeyExtraData
