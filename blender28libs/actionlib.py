import bpy
import math
import mathutils

from .. import core


class Creat_Action():
    """Zhulong_Action_to_Blender_Actio"""
    def __init__(self, 烛龙文件=core.aurogon_type.烛龙文件()):
        if 烛龙文件.动作文件.名称 != "":
            self.__烛龙文件 = 烛龙文件
            self.__creat()

    def __creat(self):
        action = bpy.data.actions.new(self.__烛龙文件.动作文件.名称)
        name = bpy.data.objects.data.armatures[0].name
        obj = bpy.data.objects[name]

        obj.animation_data_create()
        obj.animation_data.action = action

        def quaternion_xyz_to_zxy(self, quaternion_xyz):
            沿Z轴逆时针旋转90度 = mathutils.Quaternion((0, 0, 1), -90)

            # 左乘规则，越后乘越左边
            return ""

        namelist = [骨骼动作.骨骼名称 for 骨骼动作 in self.__烛龙文件.动作文件.骨骼动作列表]
        for pbone in obj.pose.bones:
            pbone.rotation_mode = 'QUATERNION'
            for i, name in enumerate(namelist):
                if pbone.name in name:
                    骨骼动作 = self.__烛龙文件.动作文件.骨骼动作列表[i]
                    沿x轴逆时针旋转90度 = mathutils.Quaternion((1, 0, 0),
                                                       math.radians(-180))
                    for 旋转帧 in 骨骼动作.旋转帧列表:
                        if pbone.parent:
                            # pbone.rotation_quaternion = 旋转帧.rotation_quaternion.rotation_difference(pbone.parent.rotation_quaternion)
                            # pbone.rotation_quaternion = 旋转帧.rotation_quaternion.rotation_difference(pbone.parent.rotation_quaternion) @ pbone.parent.rotation_quaternion
                            # pbone.rotation_quaternion = 旋转帧.rotation_quaternion @ pbone.parent.rotation_quaternion

                            pbone.rotation_quaternion = 沿x轴逆时针旋转90度 @ 旋转帧.rotation_quaternion.rotation_difference(
                                pbone.parent.rotation_quaternion)
                        else:
                            pbone.rotation_quaternion = 沿x轴逆时针旋转90度 @ 旋转帧.rotation_quaternion
                        pbone.keyframe_insert("rotation_quaternion",
                                              frame=旋转帧.frame)

                    # for 位置帧 in 骨骼动作.位置帧列表:

                    #     # zxylocation = mathutils.Vector([位置帧.location[2], 位置帧.location[0], 位置帧.location[1]])
                    #     pbone.location = 位置帧.location
                    #     pbone.keyframe_insert("location", frame=位置帧.frame)
                    break

        # # for 骨骼动作 in self.__烛龙文件.动作文件.骨骼动作字典:
        # #     data_path = 'pose.bones["%s"].location' % 骨骼动作.骨骼名称
        # #     location = [0,0,0]
        # #     bone_translate_matrix = mathutils.Matrix.T
        # for pbone in obj.pose.bones:
        #     pbone.rotation_mode = 'QUATERNION'
        #     try:
        #         骨骼动作 = self.__烛龙文件.动作文件.骨骼动作字典[pbone.name]
        #         for 位置帧 in 骨骼动作.位置帧列表:

        #             pbone.location = [位置帧.location[2], 位置帧.location[0], 位置帧.location[1]]
        #             pbone.keyframe_insert("location", frame = 位置帧.frame)

        #         # for matrix帧 in 骨骼动作.matrix帧列表:
        #         #     if pbone.parent:
        #         #         pbone.matrix = pbone.parent.matrix @ matrix帧.matrix
        #         #     else:
        #         #         pbone.matrix = matrix

        #         #     pbone.keyframe_insert("matrix", frame = matrix帧.frame)
        #     except Exception as e:
        #         print(e)
