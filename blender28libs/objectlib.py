import bpy
from bpy_extras.io_utils import unpack_list

from .. import core


class Creat_Object():
    def __init__(self, 烛龙文件=core.aurogon_type.烛龙文件(), 贴图转换=False):  # 烛龙骨架:烛龙数据.烛龙材质()

        if len(烛龙文件.网格列表) > 0:
            self.__烛龙文件 = 烛龙文件
            self.__贴图转换 = 贴图转换
            self.__creat()

    def __creat(self):
        for 烛龙网格 in self.__烛龙文件.网格列表:
            me = bpy.data.meshes.new(烛龙网格.名称)
            obj = bpy.data.objects.new(烛龙网格.名称, me)
            bpy.data.collections["烛龙文件"].objects.link(obj)

            me.vertices.add(烛龙网格.顶点个数)
            me.vertices.foreach_set("co", unpack_list(
                烛龙网格.顶点位置列表))  # 接受[x,y,z,x,y,z......]形式列表

            if 烛龙网格.Loop总数 > 0:
                me.loops.add(烛龙网格.Loop总数)
                # 接受[0,1,2,1,3,4......]形式列表
                me.loops.foreach_set("vertex_index", 烛龙网格.Loop列表)

                me.polygons.add(烛龙网格.三角面数)
                loop_start_list = []
                loop_total_list = []
                for i in range(0, 烛龙网格.Loop总数, 3):  # 若是四角面，则步长为4。
                    loop_start_list.append(i)
                    loop_total_list.append(3)
                me.polygons.foreach_set("loop_start", loop_start_list)
                me.polygons.foreach_set("loop_total", loop_total_list)

            if len(烛龙网格.顶点UV列表) > 0:
                loops_uv = []
                for i in 烛龙网格.Loop列表:
                    loops_uv.append(烛龙网格.顶点UV列表[i][0])  # UV翻转，镜像等处理在解析文件
                    loops_uv.append(烛龙网格.顶点UV列表[i][1])
                me.uv_layers.new()
                me.uv_layers[0].data.foreach_set("uv", loops_uv)

            me.validate()
            me.update()

            for 顶点组 in 烛龙网格.顶点组列表:
                vertex_group = obj.vertex_groups.new(name=顶点组.骨骼名称)

                for 顶点ID_权重值 in 顶点组.顶点ID和权重值列表:
                    顶点ID, 权重值 = 顶点ID_权重值.顶点ID, 顶点ID_权重值.权重值
                    vertex_group.add([顶点ID], 权重值, "ADD")

            # 材质
            try:
                if self.__贴图转换:
                    ma = bpy.data.materials[烛龙网格.材质.名称 + "PNG"]
                else:
                    ma = bpy.data.materials[烛龙网格.材质.名称 + "DDS"]
                me.materials.append(ma)
            except:
                pass
