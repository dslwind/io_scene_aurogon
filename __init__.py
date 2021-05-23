# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

# Noesisv434（Written by Rich Whitehouse）
# written in part using http://www.richwhitehouse.com/index.php?content=inc_projects.php as a reference

# Blender249[Gujian2][xac][xsm][2015-03-02]（Written by Szkaradek123）
# written in part using http://forum.xentax.com/viewtopic.php?f=16&t=12641 as a reference

# written in part using {贴吧用户：q024588} as a reference

# nif仅支持古剑1 Gamebryo nif 2.6.0.0版本，其他nif版本不支持。（注：当前版本未支持）

bl_info = {
    "name": "烛龙类型数据文件导入插件",
    "author": "AnsWdy RuiDing",
    "version": (1, 0, 9),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import nif, kf, xac, xsm, vmesh and model。Import 烛龙类型 de mesh, UV, materials, textures，and animations",
    }


import bpy

# Support 'reload' case.
if "bpy" in locals():
    import importlib
    if "Blender28UI" in locals():
        importlib.reload(Blender28UI)


from . import Blender28UI
# 类别名，也许需要注意2个py的import语句要一致
烛龙类型Impoter=Blender28UI.导入器

# 注册菜单的前置函数
def menu_func_import(self, context):
    self.layout.operator(烛龙类型Impoter.bl_idname, text="烛龙文件 (.model/.xac/.nif/.xsm......)")

# 启用插件时候执行
def register(): # 在blender插件界面，勾选插件时执行。勾选后，每次blender启动时执行
    # 注册类
    bpy.utils.register_class(烛龙类型Impoter)
    # 注册菜单
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

# 取消插件时候执行
def unregister():
    bpy.utils.unregister_class(烛龙类型Impoter)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
