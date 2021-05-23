import bpy

from .. import core


class Creat_Armature():
    def __init__(self, 烛龙文件=core.aurogon_type.烛龙文件()):
        if 烛龙文件.骨架.名称 != "":
            self.__烛龙文件 = 烛龙文件
            self.__creat()

    def __creat(self):
        烛龙骨架 = self.__烛龙文件.骨架
        obj = bpy.data.objects.new(烛龙骨架.名称, bpy.data.armatures.new(
            烛龙骨架.名称))  # 和烛龙骨架同一层级的姿态/pos会同时建立
        bpy.data.collections["烛龙文件"].objects.link(obj)

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        for 烛龙骨骼 in 烛龙骨架.骨骼列表:
            edit_bone = obj.data.edit_bones.new(烛龙骨骼.名称)
            edit_bone.head = 烛龙骨骼.头位置
            edit_bone.tail = 烛龙骨骼.尾位置

            ebone = obj.data.edit_bones[烛龙骨骼.名称]
            if 烛龙骨骼.父骨骼名称 == "":
                continue
            pbone = obj.data.edit_bones[烛龙骨骼.父骨骼名称]
            ebone.parent = pbone

        bpy.ops.object.mode_set(mode='OBJECT')
