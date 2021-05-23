import bpy
import bpy_extras


class 导入器(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """
    烛龙类型数据文件导入器。
    支持上海烛龙信息科技有限公司研发的游戏
    古剑奇谭：琴心剑魄今何在,
    古剑奇谭二：永夜初晗凝碧天,
    古剑奇谭三：梦付千秋星垂野,
    古剑奇谭网络版：帝首熠兮风雨乱。
    """

    bl_idname = "zhulong.fileimporter"  # Blender28界面UI按钮和菜单项绑定本类的唯一标识符。有规范
    bl_label = "导入"                   # 弹出的文件浏览器的确定按钮上显示的文本

    # # filter_glob 全局变量，改名后浏览窗口的文件过滤不起作用
    # filter_glob: bpy.props.StringProperty(
    #     default="*.model;*.xac;*.xsm;*.vmesh",
    #     options={'HIDDEN'},
    #     maxlen=255,
    # )

    # blenderUI
    所有文件_RadioButton: bpy.props.BoolProperty(
        name="当前文件夹所选格式所有同级文件",
        description="用于启用功能，导入当前文件夹内所选格式的所有同级文件。"
                    "Tips,不会导入子级文件的相同扩展名文件。"
                    "Warning, 导入时间非常长，期间blender无反应，请勿操作blender。",
        default=False,
    )

    贴图转换_RadioButton: bpy.props.BoolProperty(
        name="DDS_to_PNG",
        description="开启后，贴图更换为PNG格式"
                    "Tips, Nothing。"
                    "Warning, 会在贴图原始文件夹生成PNG贴图。",
        default=False,
    )

    def execute(self, context):
        """from . import aurogon_file 必须在此处。若出现在代码的第1行，blender出现"addon not found: 'io_scene_烛龙数据'"错误。
        原理估计与插件类只注册1次有关，而execute会执行多次有关。
        self.filepath, 类继承而来的变量。
        功能代码此处区域写。"""
        self.report({'INFO'}, "%s" % self.filepath)
        from . import aurogon_file
        解析器 = aurogon_file.解析器(self.filepath)
        解析器.参数设置(所有文件=self.所有文件_RadioButton, 贴图转换=self.贴图转换_RadioButton,
                 key="value")
        解析器.执行()

        return {'FINISHED'}
