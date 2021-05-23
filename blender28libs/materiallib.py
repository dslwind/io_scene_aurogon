import bpy
from bpy_extras import node_shader_utils

from .. import core, texconvert


class Creat_Material():
    def __init__(self, 烛龙文件=core.aurogon_type.烛龙文件(), 贴图转换=False):
        if len(烛龙文件.网格列表) > 0:
            self.__烛龙文件 = 烛龙文件
            self.__贴图转换 = 贴图转换
            self.__creat()

    def __creat(self):
        for 烛龙网格 in self.__烛龙文件.网格列表:
            烛龙材质 = 烛龙网格.材质
            if self.__贴图转换:
                材质名称 = 烛龙材质.名称 + "PNG"
            else:
                材质名称 = 烛龙材质.名称 + "DDS"

            if 材质名称 in bpy.data.materials:  # key_in_dict
                continue
            else:
                bl材质 = bpy.data.materials.new(材质名称)
                材质wrap = node_shader_utils.PrincipledBSDFWrapper(
                    bl材质, is_readonly=False)  # 新建节点wrap
                材质wrap.use_nodes = True  # 使用节点材质

                for 贴图名称, 贴图路径 in 烛龙材质.贴图字典.items():
                    if self.__贴图转换:
                        贴图路径 = texconvert.texconv.贴图格式转换(贴图路径)

                    try:
                        im = bpy.data.images.load(贴图路径, check_existing=True)
                        if 贴图名称.endswith("d") or 贴图名称.endswith("D"):
                            材质wrap.base_color_texture.image = im
                            材质wrap.base_color_texture.texcoords = 'UV'
                        elif 贴图名称.endswith("s") or 贴图名称.endswith("S"):
                            材质wrap.specular_texture.image = im
                            材质wrap.specular_texture.texcoords = 'UV'
                        elif 贴图名称.endswith("n") or 贴图名称.endswith("N"):
                            材质wrap.normalmap_texture.image = im
                            材质wrap.normalmap_texture.texcoords = 'UV'
                        elif 贴图名称.endswith("m") or 贴图名称.endswith("M"):
                            材质wrap.metallic_texture.image = im
                            材质wrap.metallic_texture.texcoords = 'UV'
                    except Exception as e:
                        print(e)
