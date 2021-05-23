import bpy

from .. import core


class Bind_Object_to_Armature():
    def __init__(self, 烛龙文件=core.aurogon_type.烛龙文件()):
        if 烛龙文件.骨架.名称 != "":
            self.__烛龙文件 = 烛龙文件
            self.__creat()

    def __creat(self):
        for 烛龙网格 in self.__烛龙文件.网格列表:
            obj = bpy.data.objects[烛龙网格.名称]
            obj.parent = bpy.data.objects[self.__烛龙文件.骨架.名称]
            骨架修改器 = obj.modifiers.new(self.__烛龙文件.骨架.名称, 'ARMATURE')
            骨架修改器.object = bpy.data.objects[self.__烛龙文件.骨架.名称]
