import os
import bpy

from . import core
from . import blender28libs


class 解析器(object):
    """判断文件格式,调用各自的解析函数。解析完成后，调用blender导入函数。"""

    def __init__(self, file_path):
        self.__文件列表 = [file_path]
        self.__扩展名_函数_字典 = {
            # 模型
            ".nif": self.__gamebryo_engine_file_解析,
            ".xac": self.__xac解析,
            ".vmesh": self.__vision_engine_file_解析,
            ".model": self.__vision_engine_file_解析,
            ".avatar": self.__avatar解析,
            # 动作
            ".kf": self.__gamebryo_engine_file_解析,
            ".xsm": self.__xsm解析,
            ".hka": None,
        }

    def 参数设置(self, *列表, **字典):
        if 字典["所有文件"]:
            self.__获取当前文件夹所选格式所有文件()

        self.__bool_DDS_to_PNG = 字典["贴图转换"]  # true or fales

    def 执行(self):
        file_path = self.__文件列表[0]
        file_base_name, file_ext = os.path.splitext(file_path)
        # 解析
        for file_path in self.__文件列表:
            if file_ext in self.__扩展名_函数_字典:
                self.__扩展名_函数_字典[file_ext](file_path)
            else:
                try:
                    self.__vision_engine_file_解析(file_path)
                except:
                    print("所选文件格式io_scene_烛龙数据插件未支持。")

    def __获取当前文件夹所选格式所有文件(self):
        file_path = self.__文件列表[0]
        cwd_dir = os.path.dirname(file_path)  # 当前目录
        file_base_name, file_ext = os.path.splitext(
            file_path)  # "E:\\.....", ".xac"
        all_file_name_list = os.listdir(cwd_dir)  # 当前文件夹的所选文件及所选文件的同级文件

        self.__文件列表 = []
        for file_name in all_file_name_list:
            if file_name.endswith(file_ext):
                self.__文件列表.append(cwd_dir+"\\"+file_name)

    def __xac解析(self, file_path):
        烛龙文件 = core.xac.解析(file_path).烛龙文件
        self.__烛龙文件_to_Blender28(烛龙文件)

    def __xsm解析(self, file_path):
        烛龙文件 = core.xsm.解析(file_path).烛龙文件
        self.__烛龙文件_to_Blender28(烛龙文件)

    def __vision_engine_file_解析(self, file_path):
        烛龙文件 = core.vision_engine_file.解析(file_path).烛龙文件
        self.__烛龙文件_to_Blender28(烛龙文件)

    def __avatar解析(self, file_path):
        avatar文件 = core.avatar.解析(file_path)
        for file_path in avatar文件.文件列表:
            self.__vision_engine_file_解析(file_path)

        collection = bpy.data.collections["烛龙文件"]
        collection.name = avatar文件.文件名称

    def __gamebryo_engine_file_解析(self, file_path):
        烛龙文件 = core.gamebryo_engine_file.解析(file_path).烛龙文件
        self.__烛龙文件_to_Blender28(烛龙文件)

    def __烛龙文件_to_Blender28(self, 烛龙文件):
        if "烛龙文件" not in bpy.data.collections:
            collection = bpy.data.collections.new("烛龙文件")
            bpy.context.scene.collection.children.link(collection)

        blender28libs.armaturelib.Creat_Armature(烛龙文件)
        blender28libs.materiallib.Creat_Material(
            烛龙文件, 贴图转换=self.__bool_DDS_to_PNG)
        blender28libs.objectlib.Creat_Object(烛龙文件, 贴图转换=self.__bool_DDS_to_PNG)
        blender28libs.bindlib.Bind_Object_to_Armature(烛龙文件)
        blender28libs.actionlib.Creat_Action(烛龙文件)
